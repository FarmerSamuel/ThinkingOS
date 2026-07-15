#!/usr/bin/env python3
"""Generate specification-conformant ThinkingOS skill packages from curated manifests.

The generator is deterministic and uses only the Python standard library. It is an
authoring tool: generated artifacts are reviewed, validated, and committed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATALOG = {
    "constraints": {
        "name": "Constraints", "category": "problem-framing",
        "purpose": "Identify, classify, and test the boundaries that define the feasible problem space.",
        "habit": "Make governing boundaries explicit before evaluating options.",
        "elements": ["ValidatedProblem", "Constraint", "Assumption", "FeasibleSpace", "TradeOff"],
        "inputs": ["validatedProblem", "context", "candidateConstraints"],
        "outputs": ["ConstraintSet", "ConstraintClassification", "FeasibleSpace"],
        "dependencies": ["right-problem"],
        "criteria": ["Completeness", "Classification", "Evidence", "Feasibility", "Consistency"],
        "next": ["gap-analysis", "heuristic", "boundary"],
    },
    "gap-analysis": {
        "name": "Gap Analysis", "category": "analysis",
        "purpose": "Compare validated current and target states and prioritize the gaps that prevent transition.",
        "habit": "Define the difference between current and desired states before selecting interventions.",
        "elements": ["InitialState", "TargetState", "Gap", "Constraint", "TransitionNeed"],
        "inputs": ["initialState", "targetState", "constraintSet"],
        "outputs": ["GapSet", "PrioritizedGaps", "TransitionNeeds"],
        "dependencies": ["right-problem", "constraints"],
        "criteria": ["StateClarity", "GapValidity", "Prioritization", "ConstraintFit", "Actionability"],
        "next": ["break-it-down", "heuristic"],
    },
    "analogy": {
        "name": "Analogy", "category": "reasoning",
        "purpose": "Transfer insight through explicit structural mappings while exposing where an analogy fails.",
        "habit": "Compare relationships, not surface resemblance.",
        "elements": ["TargetStructure", "SourceAnalogue", "StructuralMapping", "Difference", "Limitation"],
        "inputs": ["validatedProblem", "targetStructure", "candidateAnalogues"],
        "outputs": ["SourceAnalogue", "StructuralMapping", "AnalogyLimitations"],
        "dependencies": ["right-problem"],
        "criteria": ["StructuralFit", "Relevance", "DifferenceAwareness", "Evidence", "TransferValidity"],
        "next": ["make-association", "deep-processing"],
    },
    "heuristic": {
        "name": "Heuristic", "category": "decision-making",
        "purpose": "Construct a bounded decision shortcut with explicit applicability and failure conditions.",
        "habit": "Use shortcuts only when their boundaries and costs are visible.",
        "elements": ["DecisionContext", "Heuristic", "ApplicabilityCondition", "FailureCondition", "TradeOff"],
        "inputs": ["validatedProblem", "constraintSet", "decisionContext"],
        "outputs": ["DecisionHeuristic", "ApplicabilityConditions", "FailureConditions"],
        "dependencies": ["right-problem", "constraints"],
        "criteria": ["Simplicity", "BoundaryClarity", "Reliability", "CostOfError", "Testability"],
        "next": ["gap-analysis", "complexity"],
    },
    "deep-processing": {
        "name": "Deep Processing", "category": "learning",
        "purpose": "Develop durable understanding by elaborating concepts, explanations, evidence, and relationships.",
        "habit": "Explain, connect, and test knowledge instead of merely repeating it.",
        "elements": ["Concept", "Explanation", "Evidence", "Connection", "UnderstandingGap"],
        "inputs": ["validatedProblem", "problemComponents", "sourceMaterial"],
        "outputs": ["ElaboratedConcepts", "ExplanatoryLinks", "UnderstandingGaps"],
        "dependencies": ["right-problem", "break-it-down"],
        "criteria": ["ExplanationDepth", "EvidenceUse", "ConnectionQuality", "Retrievability", "GapAwareness"],
        "next": ["make-association", "learning-triangle", "mind-map"],
    },
    "make-association": {
        "name": "Make Association", "category": "synthesis",
        "purpose": "Create and evaluate meaningful connections between elaborated concepts and prior knowledge.",
        "habit": "Generate connections, then test their relevance and strength.",
        "elements": ["Concept", "Association", "PriorKnowledge", "Relationship", "NovelConnection"],
        "inputs": ["elaboratedConcepts", "structuralMapping", "priorKnowledge"],
        "outputs": ["Associations", "AssociationStrengths", "NovelConnections"],
        "dependencies": ["analogy", "deep-processing"],
        "criteria": ["Relevance", "Strength", "Novelty", "Evidence", "Usefulness"],
        "next": ["mind-map", "emergence"],
    },
    "learning-triangle": {
        "name": "Learning Triangle", "category": "learning",
        "purpose": "Balance explanation, practice, and feedback into a testable learning loop.",
        "habit": "Convert understanding gaps into cycles of explanation, application, and correction.",
        "elements": ["LearningGoal", "Explanation", "Practice", "Feedback", "UnderstandingGap"],
        "inputs": ["elaboratedConcepts", "understandingGaps", "learningGoal"],
        "outputs": ["LearningPlan", "PracticeLoop", "FeedbackCriteria"],
        "dependencies": ["deep-processing"],
        "criteria": ["GoalAlignment", "Balance", "PracticeQuality", "FeedbackQuality", "Adaptability"],
        "next": ["mind-map", "deep-processing"],
    },
    "mind-map": {
        "name": "Mind Map", "category": "synthesis",
        "purpose": "Represent concept hierarchy and cross-links without confusing visual proximity with logical evidence.",
        "habit": "Externalize structure so hierarchy, relationships, and gaps can be inspected.",
        "elements": ["CentralTopic", "Concept", "Hierarchy", "CrossLink", "ConceptGraph"],
        "inputs": ["problemComponents", "associations", "centralTopic"],
        "outputs": ["ConceptGraph", "ConceptHierarchy", "CrossLinks"],
        "dependencies": ["break-it-down", "make-association"],
        "criteria": ["Coverage", "Hierarchy", "LinkValidity", "Readability", "GoalAlignment"],
        "next": ["complexity", "learning-triangle"],
    },
    "boundary": {
        "name": "Boundary", "category": "systems-thinking",
        "purpose": "Define what is inside, outside, and crossing a system boundary for a validated problem.",
        "habit": "Make scope choices and boundary assumptions explicit before reasoning about a system.",
        "elements": ["SystemBoundary", "InScopeElement", "OutOfScopeElement", "Interface", "Stakeholder"],
        "inputs": ["validatedProblem", "constraintSet", "stakeholders"],
        "outputs": ["SystemBoundary", "InScopeElements", "OutOfScopeElements", "BoundaryAssumptions"],
        "dependencies": ["right-problem", "constraints"],
        "criteria": ["ScopeClarity", "InterfaceCoverage", "StakeholderFit", "AssumptionTransparency", "Usefulness"],
        "next": ["complexity", "gap-analysis"],
    },
    "complexity": {
        "name": "Complexity", "category": "systems-thinking",
        "purpose": "Evaluate interaction, dependency, uncertainty, and adaptation within a bounded system.",
        "habit": "Examine relationships and behavior rather than counting parts alone.",
        "elements": ["Component", "Interaction", "Dependency", "UncertaintyDriver", "FeedbackLoop"],
        "inputs": ["problemComponents", "systemBoundary", "dependencyStructure"],
        "outputs": ["ComplexityProfile", "InteractionMap", "UncertaintyDrivers"],
        "dependencies": ["break-it-down", "boundary"],
        "criteria": ["InteractionCoverage", "DependencyQuality", "Uncertainty", "Adaptation", "ExplanatoryPower"],
        "next": ["emergence", "heuristic"],
    },
    "emergence": {
        "name": "Emergence", "category": "systems-thinking",
        "purpose": "Identify system-level patterns that arise from interactions and cannot be explained by isolated parts alone.",
        "habit": "Test whether observed patterns arise from interactions before labeling them emergent.",
        "elements": ["Interaction", "Pattern", "SystemBehavior", "EmergenceCondition", "AlternativeExplanation"],
        "inputs": ["complexityProfile", "interactionMap", "associations"],
        "outputs": ["EmergentPatterns", "SystemBehaviors", "EmergenceConditions"],
        "dependencies": ["complexity", "make-association"],
        "criteria": ["PatternEvidence", "InteractionBasis", "LevelDistinction", "AlternativeTesting", "PredictiveUse"],
        "next": ["boundary", "complexity"],
    },
}


def title(identifier: str) -> str:
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", identifier.replace("_", "-").replace("-", " "))
    return "".join(part[:1].upper() + part[1:] for part in words.split())


def metadata(skill_id: str, c: dict) -> str:
    lines = [
        f"id: {skill_id}", f"name: {c['name']}", "version: 0.1.0", "status: draft",
        f"category: {c['category']}", "author: FarmerSamuel", "requires:",
    ]
    lines += [f"  - {title(x)}" for x in c["inputs"] if x not in {"context", "candidateConstraints", "knownStructure"}]
    lines += ["produces:"] + [f"  - {x}" for x in c["outputs"]]
    lines += ["dependencies:"] + ([f"  - {x}" for x in c["dependencies"]] or ["  []"])
    lines += ["nextSkill:"] + [f"  - id: {x}\n    condition: The current output satisfies the registered transition and dependency contracts." for x in c["next"]]
    return "\n".join(lines) + "\n"


def skill_json(skill_id: str, c: dict) -> str:
    inputs = [
        {"name": item, "description": f"The {title(item).lower()} required by {c['name']}.", "required": i < 2,
         "schema": {"type": ["string", "object", "array"]}}
        for i, item in enumerate(c["inputs"])
    ]
    validation = [
        {"id": f"{skill_id.upper().replace('-', '')}-V01", "description": "Required inputs must be present, relevant, and mutually consistent.", "condition": "required inputs pass the shared validation framework", "onFailure": "Return needs clarification with one prioritized question."},
        {"id": f"{skill_id.upper().replace('-', '')}-V02", "description": "Material ambiguity and missing information must be surfaced.", "condition": "no blocking unknown is hidden", "onFailure": "Record the gap and stop dependent logic."},
        {"id": f"{skill_id.upper().replace('-', '')}-V03", "description": "Inputs must satisfy registered dependency semantics.", "condition": "dependency outputs or validated equivalents are available", "onFailure": "Recommend the missing prerequisite."},
    ]
    logic = [
        {"id": f"{skill_id.upper().replace('-', '')}-L01", "description": f"Identify and normalize the skill's thinking elements: {', '.join(c['elements'])}.", "condition": "each required element has evidence or explicit unknown status", "onFailure": "Request or record the missing element."},
        {"id": f"{skill_id.upper().replace('-', '')}-L02", "description": f"Apply the {c['name']} relationship rules without introducing platform assumptions.", "condition": "relationships are explicit and testable", "onFailure": "Record the unsupported relationship."},
        {"id": f"{skill_id.upper().replace('-', '')}-L03", "description": "Test contradictions, alternatives, and failure conditions.", "condition": "material alternatives are considered", "onFailure": "Reduce confidence and disclose the limitation."},
        {"id": f"{skill_id.upper().replace('-', '')}-L04", "description": "Generate a schema-compatible evaluation and next-step recommendation.", "condition": "scores, reasoning, and transition are consistent", "onFailure": "Return incomplete rather than guessing."},
    ]
    criteria = [{"name": f"{x} Score", "description": f"Quality of {title(x).lower()} in the current reasoning.", "weight": round(1 / len(c["criteria"]), 2)} for x in c["criteria"]]
    examples = [
        {"name": "Valid case", "input": {c["inputs"][0]: "Validated input", c["inputs"][1]: "Relevant context"}, "expectedOutput": {"status": "sufficient"}},
        {"name": "Incomplete case", "input": {c["inputs"][0]: "Ambiguous input"}, "expectedOutput": {"status": "incomplete", "questionRequired": True}},
    ]
    tests = [
        {"name": f"{skill_id}-T{i:02d}", "input": {c["inputs"][0]: label}, "expected": {"check": expected}}
        for i, (label, expected) in enumerate([
            ("valid input", "successful evaluation"), ("missing required input", "clarification"),
            ("ambiguous input", "ambiguity detected"), ("contradictory input", "contradiction recorded"),
            ("unsupported assumption", "assumption disclosed"), ("dependency missing", "prerequisite recommended"),
            ("alternative explanation", "alternative tested"), ("boundary condition", "boundary handled"),
            ("low evidence", "confidence reduced"), ("complete input", "output schema conformance"),
        ], 1)
    ]
    data = {
        "name": skill_id, "version": "0.1.0", "description": c["purpose"],
        "purpose": {"problem": c["purpose"], "outcome": f"Produce validated {', '.join(c['outputs'])}.", "inScope": c["elements"], "outOfScope": ["Provider-specific execution", "Unvalidated solution generation"]},
        "thinkingHabit": c["habit"], "thinkingElements": c["elements"], "requiredInputs": inputs,
        "validation": validation, "logic": logic,
        "evaluation": {"criteria": criteria, "scoringScale": {"minimum": 0, "maximum": 4, "labels": {"0": "unusable", "1": "weak", "2": "partial", "3": "sufficient", "4": "robust"}}},
        "conversationRules": ["Ask one material question at a time.", "Separate facts, assumptions, and interpretations.", "Explain why a clarification affects the evaluation.", "Stop when inputs are sufficient."],
        "output": {"schema": "../../schemas/output.schema.json", "extensions": {"scoreReporting": {"overall": "evaluation.score", "dimensions": "reasoning"}}},
        "neverRules": ["Never fabricate missing information.", "Never bypass a blocking validation failure.", "Never hide uncertainty behind a score.", "Never invoke an unsatisfied downstream skill."],
        "nextSkill": [{"skill": x, "condition": "The current output satisfies the registered transition contract.", "reason": f"Continue reasoning with {title(x)}."} for x in c["next"]],
        "examples": examples,
        "references": [{"title": "ThinkingOS Skill Specification", "citation": "../../docs/skill-specification.md"}, {"title": "ThinkingOS Reasoning Engine", "citation": "../../core/engine.md"}],
        "tests": tests,
        "extensions": {"goldenSkillCompatible": True, "documentation": {name: f"{name}.md" for name in ["workflow", "validation", "evaluation", "rubric", "examples", "tests", "references"]}},
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def readme(skill_id: str, c: dict) -> str:
    return f"""# {c['name']}

`#{c['name'].replace(' ', '')}` is a platform-independent ThinkingOS Skill. {c['purpose']}

## Purpose

{c['habit']} This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

{chr(10).join(f'- `{x}` — {title(x)} input.' for x in c['inputs'])}

## Outputs

{chr(10).join(f'- `{x}`' for x in c['outputs'])}

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates {', '.join(c['criteria'])} on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies ({', '.join(c['dependencies']) or 'none'}) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
"""


def workflow(c: dict) -> str:
    return f"""# {c['name']} Workflow

1. Validate required inputs and registered dependencies.
2. Normalize {', '.join(c['elements'])} without adding unsupported facts.
3. Apply the skill-specific relationship and classification rules.
4. Test ambiguity, contradiction, alternatives, and failure conditions.
5. Evaluate {', '.join(c['criteria'])} using the shared 0–4 rubric.
6. Generate universal output, update conversation state, and recommend a dependency-safe transition.

Execution loops to clarification when a blocking gap appears. It exits only with schema-compatible output or an explicit needs-clarification result.
"""


def validation(c: dict) -> str:
    return f"""# {c['name']} Validation

## Entry gates

{chr(10).join(f'- `{x}` must be present when required, relevant, and semantically compatible.' for x in c['inputs'])}

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: {', '.join(c['dependencies']) or 'none'}.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element ({', '.join(c['elements'])}) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
"""


def evaluation(c: dict) -> str:
    dims = "\n".join(f"- **{x} Score:** Evaluates {title(x).lower()}." for x in c["criteria"])
    return f"""# {c['name']} Evaluation

Score each dimension from 0 to 4:

{dims}

The overall score is the rounded mean, capped at 2 when a blocking input, dependency, contradiction, or core logic failure remains. Map it to `evaluation.score`; include observations supporting every dimension in `reasoning`.

Confidence reflects evidence quality, input completeness, and alternative testing—not fluency or agreement.
"""


def rubric(c: dict) -> str:
    return f"""# {c['name']} Rubric

| Score | Meaning |
| ---: | --- |
| 0 | Missing, contradicted, or unusable. |
| 1 | Materially weak or unsupported. |
| 2 | Partially usable with important gaps. |
| 3 | Sufficient for the current reasoning goal. |
| 4 | Evidence-backed, complete, and robust to alternatives. |

Apply this scale independently to {', '.join(c['criteria'])}. Select the lower score when evidence falls between levels. A high overall score cannot override a blocking validation or dependency failure.
"""


def examples(c: dict) -> str:
    return f"""# {c['name']} Examples

## Simple case

Use clear, bounded inputs to produce {', '.join(c['outputs'])}; disclose the reasoning and confidence.

## Business case

Apply the skill to a validated organizational decision while separating evidence, stakeholder claims, and constraints.

## Learning case

Apply the same thinking habit to a learner's concept or practice gap without changing the skill contract.

## Failure case

When a required input or dependency is missing, return incomplete, ask one high-impact question, and do not fabricate an evaluation.
"""


def tests(skill_id: str, c: dict) -> str:
    cases = ["valid input", "missing input", "ambiguous input", "contradiction", "unsupported assumption", "missing dependency", "alternative explanation", "boundary condition", "low evidence", "output conformance", "next-skill gating", "state preservation"]
    rows = "\n".join(f"| {skill_id.upper().replace('-', '')}-{i:03d} | {case.title()} | Apply the declared validation, logic, evaluation, and output contract. |" for i, case in enumerate(cases, 1))
    return f"""# {c['name']} Tests

| ID | Case | Expected result |
| --- | --- | --- |
{rows}

Provider wording may vary; rule outcomes, scores, missing-information behavior, state changes, and output structure must remain equivalent.
"""


def references(c: dict) -> str:
    deps = "\n".join(f"- [{title(x)}](../{x}/README.md)" for x in c["dependencies"])
    return f"""# {c['name']} References

## Normative

- [Skill Specification](../../docs/skill-specification.md)
- [Reasoning Engine](../../core/engine.md)
- [Evaluation Model](../../docs/evaluation-model.md)
{deps}

## Informative

Domain references must be versioned, attributable, relevant to the skill's thinking habit, and subordinate to normative ThinkingOS contracts.
"""


def changelog(c: dict) -> str:
    return f"""# Changelog

All notable changes to {c['name']} are documented using Semantic Versioning.

## [Unreleased]

## [0.1.0] — 2026-07-15

### Added

- Initial draft skill contract, documentation, examples, and conformance tests.
"""


def update_registry(skill_id: str) -> None:
    path = ROOT / "skills" / "registry.yaml"
    text = path.read_text(encoding="utf-8")
    marker = f"  - id: {skill_id}\n"
    start = text.index(marker)
    next_start = text.find("\n  - id: ", start + len(marker))
    end = len(text) if next_start < 0 else next_start
    block = text[start:end].replace("    status: planned", "    status: draft", 1)
    path.write_text(text[:start] + block + text[end:], encoding="utf-8", newline="\n")


def generate(skill_id: str) -> None:
    c = CATALOG[skill_id]
    directory = ROOT / "skills" / skill_id
    directory.mkdir(parents=True, exist_ok=True)
    files = {
        "README.md": readme(skill_id, c), "metadata.yaml": metadata(skill_id, c),
        "skill.json": skill_json(skill_id, c), "workflow.md": workflow(c),
        "validation.md": validation(c), "evaluation.md": evaluation(c),
        "rubric.md": rubric(c), "examples.md": examples(c), "tests.md": tests(skill_id, c),
        "references.md": references(c), "CHANGELOG.md": changelog(c),
    }
    for name, content in files.items():
        (directory / name).write_text(content, encoding="utf-8", newline="\n")
    update_registry(skill_id)
    print(f"generated {skill_id}: {len(files)} files")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills", nargs="+", choices=sorted(CATALOG))
    args = parser.parse_args()
    for skill_id in args.skills:
        generate(skill_id)


if __name__ == "__main__":
    main()
