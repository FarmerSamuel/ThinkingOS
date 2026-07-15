# Deep Processing

`#DeepProcessing` is a platform-independent ThinkingOS Skill. Develop durable understanding by elaborating concepts, explanations, evidence, and relationships.

## Purpose

Explain, connect, and test knowledge instead of merely repeating it. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `validatedProblem` — ValidatedProblem input.
- `problemComponents` — ProblemComponents input.
- `sourceMaterial` — SourceMaterial input.

## Outputs

- `ElaboratedConcepts`
- `ExplanatoryLinks`
- `UnderstandingGaps`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates ExplanationDepth, EvidenceUse, ConnectionQuality, Retrievability, GapAwareness on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (right-problem, break-it-down) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
