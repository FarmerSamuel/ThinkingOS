# Emergence

`#Emergence` is a platform-independent ThinkingOS Skill. Identify system-level patterns that arise from interactions and cannot be explained by isolated parts alone.

## Purpose

Test whether observed patterns arise from interactions before labeling them emergent. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `complexityProfile` — ComplexityProfile input.
- `interactionMap` — InteractionMap input.
- `associations` — Associations input.

## Outputs

- `EmergentPatterns`
- `SystemBehaviors`
- `EmergenceConditions`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates PatternEvidence, InteractionBasis, LevelDistinction, AlternativeTesting, PredictiveUse on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (complexity, make-association) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
