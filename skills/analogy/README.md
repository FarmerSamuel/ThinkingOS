# Analogy

`#Analogy` is a platform-independent ThinkingOS Skill. Transfer insight through explicit structural mappings while exposing where an analogy fails.

## Purpose

Compare relationships, not surface resemblance. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `validatedProblem` — ValidatedProblem input.
- `targetStructure` — TargetStructure input.
- `candidateAnalogues` — CandidateAnalogues input.

## Outputs

- `SourceAnalogue`
- `StructuralMapping`
- `AnalogyLimitations`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates StructuralFit, Relevance, DifferenceAwareness, Evidence, TransferValidity on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (right-problem) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
