# Claude Guide

This guide explains how to use ThinkingOS to improve thinking quality inside
Claude, and how to turn real Claude conversations into skill improvements. The
framework itself remains provider-neutral; everything Claude-specific lives in
the generated distribution and in `adapters/claude/`.

## Choose an integration path

| Path | Best for | What you use |
| --- | --- | --- |
| Claude Code | Daily thinking work and iterating on this repository | Generated Agent Skills in `.claude/skills/` |
| claude.ai | Chat-first use without a local checkout | Project instructions built from `core/`, plus uploaded skill packages where Agent Skills are supported |
| Claude API | Applications embedding ThinkingOS | `ClaudeAdapter` in `adapters/claude/` |
| MCP hosts | Tool-based integration with human-in-the-loop control | The MCP adapter in `adapters/mcp/` |

## Claude Code

Claude Code discovers project-level Agent Skills automatically. Clone the
repository and start Claude Code inside it:

```bash
git clone https://github.com/FarmerSamuel/ThinkingOS.git
cd ThinkingOS
claude
```

Fourteen skills load from `.claude/skills/`: one package per Thinking Skill
(`right-problem`, `break-it-down`, `constraints`, and the rest of the
registry) plus a `thinkingos` routing skill that carries the universal
persona, core principles, Engine pipeline, and skill graph.

Ways to work:

- Describe a problem or decision. The skill descriptions are trigger-oriented,
  so Claude selects the matching discipline — for example, a request that
  already assumes a solution triggers `right-problem`.
- Name a skill explicitly: "Use right-problem on this" or "Run constraints,
  then gap-analysis."
- Ask for routing: "Which ThinkingOS skill fits this situation?" The
  `thinkingos` skill answers from the registry graph.

Each generated skill enforces its contract: required inputs are collected
before analysis, validation gates run before logic rules, one clarification
question is asked at a time, and the result is returned as the universal
output payload with rubric scores, assumptions, missing information, and a
next-step recommendation.

The packages in `.claude/skills/` are generated from the canonical contracts.
Never edit them directly; change the skill package and regenerate:

```bash
python tools/export_claude_skills.py
```

## claude.ai

For chat-first use without a repository checkout:

1. Create a Project and build its instructions from the Core contracts:
   `core/persona.md`, `core/principles.md`, `core/workflow.md`, and
   `core/questioning-style.md`. This gives every conversation the
   validation-first behavior without binding it to one skill.
2. Add reference material from `knowledge/` (for example
   `knowledge/problem-framing.md`) to the Project so critiques cite reusable
   thinking knowledge instead of improvisation.
3. Where your plan supports Agent Skills, upload generated packages from
   `.claude/skills/` — each directory is a self-contained skill with its
   `SKILL.md` contract.
4. In conversation, ask Claude to run the discipline: "Apply Right Problem
   before proposing anything" or paste a ThinkingOS Language block such as:

```text
#RightProblem
$Goal
$Obstacle
@Constraint
%Validating
```

## Claude API

Applications call the Messages API through the provider adapter, which maps a
validated skill context into a `system` instruction and a single user message.
Your application owns transport, credentials, model choice, retries, and final
output validation:

```python
from adapters.base import AdapterRequest
from adapters.claude import ClaudeAdapter

adapter = ClaudeAdapter()
request = AdapterRequest(
    skill="right-problem",
    instructions=open("core/persona.md", encoding="utf-8").read(),
    inputs={
        "problemStatement": "We need a new CRM because sales are declining.",
        "goal": "Restore qualified-pipeline conversion from 14% to 20%.",
    },
)
provider_request = adapter.build_request(request, model="claude-sonnet-5", max_tokens=2048)
```

See the SDK Guide for loading skills and traversing the registry, and
`adapters/claude/` for payload details.

## MCP hosts

The MCP adapter in `adapters/mcp/` maps skill requests for Model Context
Protocol hosts. Keep a human in the loop for consequential decisions, as
required by the adapter's documentation and the project security policy.

## The iteration loop

ThinkingOS treats a misfiring skill as a contract bug, not a prompt tweak.
Use Claude conversations as the test bed and feed failures back into the
canonical packages:

```text
Use a skill in a real conversation
  -> Notice a failure (missed ambiguity, premature solution, wrong question)
  -> Capture the case in skills/<id>/examples.md and tests.md
  -> Encode the fix in skill.json (validation gate, logic rule, never rule)
  -> Bump versions and changelogs
  -> Regenerate the Claude export
  -> Validate and commit
```

Concretely:

1. **Capture.** Record the failing exchange as a case in
   `skills/<id>/examples.md` and add a conformance row to
   `skills/<id>/tests.md`.
2. **Encode.** Express the fix as a machine-checkable rule in
   `skills/<id>/skill.json` — a new validation gate, logic rule, or never
   rule — rather than loose prose.
3. **Version.** Update `version` in `skill.json`, `metadata.yaml`, and
   `skills/registry.yaml` together, and record the change in the skill's
   `CHANGELOG.md` and the root `CHANGELOG.md`.
4. **Regenerate.** Run `python tools/export_claude_skills.py` so the Claude
   distribution reflects the new contract.
5. **Validate.** Run the repository checks before committing:

```bash
python tools/validate_repository.py
python -m unittest discover -s tests
python tools/export_claude_skills.py --check
mkdocs build --strict
```

Continuous integration enforces the same checks, including the export sync
test, so the Claude distribution can never silently drift from the canonical
contracts.

When working inside Claude Code, the repository's `CLAUDE.md` teaches this
loop to the session itself: ask Claude to apply the fix, and it will follow
the same capture, encode, version, regenerate, and validate sequence.

## Related pages

- [Developer Guide](developer-guide.md) for repository validation.
- [Skill Author Guide](skill-author-guide.md) for authoring new skills.
- [SDK Guide](sdk-guide.md) for programmatic access.
- [Right Problem Guide](right-problem-guide.md) for the Golden Skill.
