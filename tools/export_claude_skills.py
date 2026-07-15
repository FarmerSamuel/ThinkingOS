#!/usr/bin/env python3
"""Generate Claude Agent Skill packages from canonical ThinkingOS contracts.

The canonical source of every Thinking Skill is its package under ``skills/``.
This exporter renders each released skill, plus one framework-level routing
skill, into the Claude Agent Skill layout under ``.claude/skills/<id>/SKILL.md``
so the skills load directly in Claude Code and can be uploaded to other Claude
surfaces. Generated files must never be edited by hand; rerun this tool after
changing a skill package.

Usage:
    python tools/export_claude_skills.py            # regenerate .claude/skills
    python tools/export_claude_skills.py --check    # fail if output is stale
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / ".claude" / "skills"
CORE_SKILL_ID = "thinkingos"
MAX_DESCRIPTION_LENGTH = 1024

ENGINE_PIPELINE = """```text
Collect Inputs -> Validate -> Detect Missing Information -> Evaluate Elements
-> Run Logic Rules -> Evaluate Reasoning -> Generate Evaluation
-> Generate Output -> Recommend Next Skill
```"""

UNIVERSAL_OUTPUT = """Return one fenced JSON object that conforms to the ThinkingOS universal
output contract (`schemas/output.schema.json`), then a short plain-language
recap of the recommendation and next step.

Required fields:

- `summary` — one-paragraph result including the frame status.
- `evaluation` — object with `score`, `strengths`, `weaknesses`,
  `missingInformation`, `logicalIssues`, `recommendation`, `confidence`.
- `reasoning` — array of strings; report each rubric dimension as a structured
  entry (for example `Goal Score: 3/4 — supported by stated evidence`).
- `assumptions` — every assumption the analysis relied on.
- `missingInformation` — unknowns that could materially change the result.
- `questions` — outstanding clarification questions (at most one prioritized
  question when a blocking gap exists).
- `nextStep` — the single most useful next action.
- `confidence` — `low`, `medium`, or `high` (or a number from 0 to 1).

Preserve material uncertainty. Never hide a blocking weakness behind a strong
overall score, and never treat fluent prose as evidence of valid reasoning."""


@dataclass
class RegistryEntry:
    """A parsed ``skills/registry.yaml`` skill block."""

    id: str
    display_name: str
    category: str
    version: str
    status: str
    dependencies: list[str] = field(default_factory=list)
    produces: list[str] = field(default_factory=list)
    consumes: list[str] = field(default_factory=list)


def parse_registry() -> list[RegistryEntry]:
    """Parse the registry with the same shape assumptions as the validator."""
    text = (ROOT / "skills" / "registry.yaml").read_text(encoding="utf-8")
    entries: list[RegistryEntry] = []
    for block in re.split(r"(?m)(?=^  - id: )", text):
        match = re.match(r"  - id: ([a-z0-9-]+)\n", block)
        if not match:
            continue

        def scalar(key: str) -> str:
            found = re.search(rf"(?m)^    {key}: (.+)$", block)
            return found.group(1).strip() if found else ""

        def sequence(key: str) -> list[str]:
            section = re.search(
                rf"(?m)^    {key}:\n((?:      - .+\n)*)", block
            )
            if not section:
                return []
            return re.findall(r"(?m)^      - (.+)$", section.group(1))

        entries.append(
            RegistryEntry(
                id=match.group(1),
                display_name=scalar("displayName"),
                category=scalar("category"),
                version=scalar("version"),
                status=scalar("status"),
                dependencies=sequence("dependencies"),
                produces=sequence("produces"),
                consumes=sequence("consumes"),
            )
        )
    return entries


def yaml_quote(value: str) -> str:
    """Return a double-quoted YAML scalar."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def table_cell(value: str) -> str:
    """Escape a value for use inside a Markdown table cell."""
    return value.replace("|", "\\|").replace("\n", " ").strip()


def sentence(value: str) -> str:
    """Normalize whitespace and guarantee terminal punctuation."""
    text = " ".join(value.split())
    if text and text[-1] not in ".!?":
        text += "."
    return text


def frontmatter_description(data: dict, entry: RegistryEntry) -> str:
    """Compose the trigger-oriented frontmatter description."""
    description = sentence(data["description"])
    problem = sentence(data["purpose"]["problem"])
    parts = [description]
    if problem and problem != description:
        parts.append(f"Prevents this failure mode: {problem}")
    parts.append(f"ThinkingOS {entry.category} skill.")
    text = " ".join(parts)
    if len(text) > MAX_DESCRIPTION_LENGTH:
        text = text[: MAX_DESCRIPTION_LENGTH - 1].rstrip() + "."
    return text


def render_rule_list(rules: list[dict], ordered: bool) -> list[str]:
    """Render validation or logic rules as a Markdown list."""
    lines: list[str] = []
    for index, rule in enumerate(rules, start=1):
        marker = f"{index}." if ordered else "-"
        text = sentence(rule["description"])
        failure = sentence(rule["onFailure"])
        lines.append(f"{marker} **{rule['id']}** — {text} If it fails: {failure}")
    return lines


def render_skill(data: dict, entry: RegistryEntry) -> str:
    """Render one canonical skill package as a Claude Agent Skill."""
    purpose = data["purpose"]
    description = sentence(data["description"])
    problem = sentence(purpose["problem"])
    lines: list[str] = [
        "---",
        f"name: {entry.id}",
        f"description: {yaml_quote(frontmatter_description(data, entry))}",
        "---",
        "",
        f"# {entry.display_name} (ThinkingOS)",
        "",
        description,
        "",
        f"**Thinking habit:** {sentence(data['thinkingHabit'])}",
        "",
        f"Generated from the canonical package `skills/{entry.id}/` "
        f"(version {data['version']}). Do not edit this file; update the "
        "package and run `python tools/export_claude_skills.py`.",
        "",
        "## Purpose",
        "",
    ]
    if problem and problem != description:
        lines.extend([problem, ""])
    lines.extend([f"Target outcome: {sentence(purpose['outcome'])}", ""])

    lines.extend(["### In scope", ""])
    lines.extend(f"- {sentence(item)}" for item in purpose["inScope"])
    lines.extend(["", "### Out of scope", ""])
    lines.extend(f"- {sentence(item)}" for item in purpose["outOfScope"])

    lines.extend(["", "## Position in the thinking graph", ""])
    if entry.dependencies:
        lines.append(
            "Run after: "
            + ", ".join(f"`{dependency}`" for dependency in entry.dependencies)
            + "."
        )
        lines.append(
            "If a prerequisite artifact is missing from the conversation, run "
            "the prerequisite skill first or ask the user for an equivalent "
            "input. Never invent it."
        )
    else:
        lines.append(
            "This is an entry-point skill with no prerequisite skills."
        )
    lines.append("")
    if entry.consumes:
        lines.append(
            "- Consumes: "
            + ", ".join(f"`{item}`" for item in entry.consumes)
            + "."
        )
    if entry.produces:
        lines.append(
            "- Produces: "
            + ", ".join(f"`{item}`" for item in entry.produces)
            + "."
        )

    lines.extend(["", "## Required inputs", ""])
    lines.append("| Input | Required | Description |")
    lines.append("| --- | --- | --- |")
    for spec in data["requiredInputs"]:
        required = "Yes" if spec["required"] else "No"
        lines.append(
            f"| `{spec['name']}` | {required} | "
            f"{table_cell(sentence(spec['description']))} |"
        )
    lines.extend(
        [
            "",
            "Collect required inputs before analysis. When a required input is "
            "missing or materially ambiguous, ask the single highest-impact "
            "clarification question and wait for the answer.",
        ]
    )

    lines.extend(["", "## Execution pipeline", ""])
    lines.append("Follow the shared ThinkingOS Engine order:")
    lines.extend(["", ENGINE_PIPELINE, ""])
    lines.append(
        "A later stage must not bypass an unresolved blocking result from an "
        "earlier stage."
    )

    lines.extend(["", "## Validation gates", ""])
    lines.extend(render_rule_list(data["validation"], ordered=False))

    lines.extend(["", "## Logic rules", "", "Apply in order:", ""])
    lines.extend(render_rule_list(data["logic"], ordered=True))

    lines.extend(["", "## Conversation rules", ""])
    lines.extend(f"- {sentence(rule)}" for rule in data["conversationRules"])

    evaluation = data["evaluation"]
    scale = evaluation["scoringScale"]
    lines.extend(["", "## Evaluation", ""])
    lines.append(
        f"Score each criterion from {scale['minimum']} to {scale['maximum']}:"
    )
    lines.append("")
    lines.append("| Criterion | Weight | Description |")
    lines.append("| --- | --- | --- |")
    for criterion in evaluation["criteria"]:
        weight = criterion.get("weight")
        weight_text = f"{weight}" if weight is not None else "—"
        lines.append(
            f"| {table_cell(criterion['name'])} | {weight_text} | "
            f"{table_cell(sentence(criterion['description']))} |"
        )
    lines.append("")
    labels = ", ".join(
        f"{score} = {label}"
        for score, label in sorted(
            scale["labels"].items(), key=lambda item: int(item[0])
        )
    )
    lines.append(f"Scale: {labels}.")

    lines.extend(["", "## Output format", "", UNIVERSAL_OUTPUT])

    lines.extend(["", "## Never rules", ""])
    lines.extend(f"- {sentence(rule)}" for rule in data["neverRules"])

    lines.extend(["", "## Next skill transitions", ""])
    transitions = data.get("nextSkill", [])
    if transitions:
        lines.append("Recommend at most one downstream skill:")
        lines.append("")
        for transition in transitions:
            lines.append(
                f"- `{transition['skill']}` — Condition: "
                f"{sentence(transition['condition'])} Reason: "
                f"{sentence(transition['reason'])}"
            )
        lines.append("")
        lines.append(
            "Never recommend a downstream skill whose prerequisites are "
            "unsatisfied. When no transition condition holds, recommend a "
            "direct action or clarification instead."
        )
    else:
        lines.append(
            "This skill declares no downstream transitions. Recommend a direct "
            "action or clarification."
        )

    return "\n".join(lines) + "\n"


def render_core_skill(entries: list[RegistryEntry]) -> str:
    """Render the framework-level routing skill from Core contracts."""
    project_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    description = (
        "Validation-first reasoning framework that routes structured thinking "
        "through composable Thinking Skills. Use when a problem, decision, "
        "plan, or analysis should be validated before solutions are generated, "
        "or when unsure which ThinkingOS skill applies. Covers problem "
        "framing, decomposition, constraints, gap analysis, analogy, "
        "heuristics, learning, synthesis, and systems thinking."
    )
    lines: list[str] = [
        "---",
        f"name: {CORE_SKILL_ID}",
        f"description: {yaml_quote(description)}",
        "---",
        "",
        "# ThinkingOS Core",
        "",
        "ThinkingOS improves the quality of human reasoning without replacing "
        "human judgment. It validates the problem frame before any solution "
        "work and treats uncertainty, questions, and revision as productive "
        "parts of reasoning.",
        "",
        f"Generated from the canonical Core contracts in `core/` and "
        f"`skills/registry.yaml` (project version {project_version}). Do not "
        "edit this file; update the canonical sources and run "
        "`python tools/export_claude_skills.py`.",
        "",
        "## Persona",
        "",
        "Act simultaneously as:",
        "",
        "- **Senior strategy consultant** — structure complex situations and "
        "identify decision-relevant evidence.",
        "- **Critical thinker** — test claims, assumptions, causality, "
        "trade-offs, and internal consistency.",
        "- **Socratic facilitator** — help the user clarify what they know, "
        "what they believe, and what must be learned next.",
        "",
        "Never become a life coach, a motivational speaker, or a solution "
        "generator that acts before the problem, evidence, constraints, and "
        "success criteria are validated. Be direct, respectful, "
        "evidence-aware, and explicit about uncertainty.",
        "",
        "## Core principles",
        "",
        "1. Do not fabricate facts, sources, user intent, certainty, or "
        "completed actions.",
        "2. Ask when information is insufficient; request the smallest amount "
        "needed to proceed responsibly.",
        "3. Challenge assumptions, including assumptions embedded in the "
        "user's framing.",
        "4. Prefer clarification over guessing; disclose any bounded "
        "assumption you adopt.",
        "5. Separate observations, interpretations, assumptions, "
        "recommendations, and value judgments.",
        "6. Support conclusions with evidence and logic, not authority or "
        "rhetorical confidence.",
        "7. Calibrate confidence to evidence quality and acknowledge "
        "meaningful unknowns.",
        "8. Preserve human agency: make trade-offs visible and leave "
        "consequential judgment with the user.",
        "9. Stay goal-aligned; avoid analysis that does not advance the "
        "validated goal.",
        "",
        "## Execution pipeline",
        "",
        "Every Thinking Skill runs the shared Engine order:",
        "",
        ENGINE_PIPELINE,
        "",
        "The Engine stops or loops when material information is missing. "
        "Fluent output is never proof of valid reasoning.",
        "",
        "## Questioning style",
        "",
        "- Ask the most decision-relevant question first, one question at a "
        "time.",
        "- Probe assumptions neutrally: \"What evidence supports this?\" "
        "\"What would change this conclusion?\"",
        "- Test alternatives: \"What other explanation could fit the same "
        "facts?\"",
        "- Avoid questionnaires, rhetorical traps, and questions that will "
        "not affect the analysis.",
        "",
        "## Skill graph",
        "",
        "Route work through the registered skills. Each skill in this project "
        "is available as its own Claude skill with the same identifier.",
        "",
        "| Skill | Category | Depends on | Produces |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        depends = ", ".join(f"`{d}`" for d in entry.dependencies) or "—"
        produces = ", ".join(f"`{p}`" for p in entry.produces) or "—"
        lines.append(
            f"| `{entry.id}` | {entry.category} | {depends} | {produces} |"
        )
    lines.extend(
        [
            "",
            "## Routing guidance",
            "",
            "- Start with `right-problem` whenever a new problem, request, or "
            "decision arrives; it is the entry point of the graph.",
            "- Move to `constraints`, `break-it-down`, or `gap-analysis` once "
            "the frame is valid, following each skill's transition conditions.",
            "- Use `analogy`, `heuristic`, `deep-processing`, and "
            "`make-association` for reasoning, decision, and learning work.",
            "- Use `boundary`, `complexity`, and `emergence` for "
            "systems-thinking work; use `mind-map` and `learning-triangle` "
            "for synthesis and learning plans.",
            "- Recommend at most one next skill at a time, and only when its "
            "prerequisites are satisfied.",
            "",
            "## Thinking language",
            "",
            "ThinkingOS Language references thinking structures with sigils:",
            "",
            "```text",
            "#Skill      a Thinking Skill, e.g. #RightProblem",
            "$Element    a unit of thought, e.g. $Goal, $Obstacle",
            "@Context    a governing constraint or context, e.g. @Budget",
            "%State      a conversation state, e.g. %Validating",
            "!Result     an evaluation result, e.g. !Valid, !Incomplete",
            "```",
            "",
            "## Output contract",
            "",
            UNIVERSAL_OUTPUT,
            "",
            "## Canonical sources",
            "",
            "The authoritative contracts live in this repository: `core/` for "
            "persona, philosophy, principles, workflow, validation, and "
            "Engine; `skills/<id>/` for each skill package; `schemas/` for "
            "machine-verifiable payloads; `knowledge/` for reusable thinking "
            "knowledge. When reasoning about ThinkingOS itself, read those "
            "files instead of relying on this summary.",
        ]
    )
    return "\n".join(lines) + "\n"


def generate() -> dict[str, str]:
    """Return the full generated tree as ``{relative path: content}``."""
    entries = parse_registry()
    outputs: dict[str, str] = {
        f"{CORE_SKILL_ID}/SKILL.md": render_core_skill(entries)
    }
    for entry in entries:
        data = json.loads(
            (ROOT / "skills" / entry.id / "skill.json").read_text(encoding="utf-8")
        )
        outputs[f"{entry.id}/SKILL.md"] = render_skill(data, entry)
    return outputs


def existing_files() -> dict[str, str]:
    """Return the checked-in generated tree."""
    if not OUTPUT_ROOT.exists():
        return {}
    return {
        str(path.relative_to(OUTPUT_ROOT)): path.read_text(encoding="utf-8")
        for path in sorted(OUTPUT_ROOT.rglob("SKILL.md"))
    }


def write(outputs: dict[str, str]) -> None:
    """Write the generated tree and prune stale generated files."""
    for relative, content in sorted(outputs.items()):
        target = OUTPUT_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    for relative in existing_files():
        if relative not in outputs:
            stale = OUTPUT_ROOT / relative
            stale.unlink()
            if not any(stale.parent.iterdir()):
                stale.parent.rmdir()


def check(outputs: dict[str, str]) -> list[str]:
    """Return drift messages between generated and checked-in trees."""
    current = existing_files()
    problems: list[str] = []
    for relative in sorted(set(outputs) | set(current)):
        if relative not in current:
            problems.append(f"missing generated file .claude/skills/{relative}")
        elif relative not in outputs:
            problems.append(f"stale generated file .claude/skills/{relative}")
        elif current[relative] != outputs[relative]:
            diff = difflib.unified_diff(
                current[relative].splitlines(),
                outputs[relative].splitlines(),
                fromfile=f".claude/skills/{relative}",
                tofile="regenerated",
                lineterm="",
                n=1,
            )
            excerpt = "\n".join(list(diff)[:12])
            problems.append(
                f"out-of-date file .claude/skills/{relative}\n{excerpt}"
            )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify .claude/skills matches the canonical packages",
    )
    arguments = parser.parse_args()
    outputs = generate()
    if arguments.check:
        problems = check(outputs)
        if problems:
            print("Claude skill export is out of date:", file=sys.stderr)
            for problem in problems:
                print(f"- {problem}", file=sys.stderr)
            print(
                "Run `python tools/export_claude_skills.py` and commit the "
                "result.",
                file=sys.stderr,
            )
            return 1
        print(f"Claude skill export is in sync: {len(outputs)} packages.")
        return 0
    write(outputs)
    print(f"Generated {len(outputs)} Claude skill packages in .claude/skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
