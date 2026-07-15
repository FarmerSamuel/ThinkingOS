# Gap Analysis

`#GapAnalysis` is a platform-independent ThinkingOS Skill. Compare validated current and target states and prioritize the gaps that prevent transition.

## Purpose

Define the difference between current and desired states before selecting interventions. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `initialState` — InitialState input.
- `targetState` — TargetState input.
- `constraintSet` — ConstraintSet input.

## Outputs

- `GapSet`
- `PrioritizedGaps`
- `TransitionNeeds`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates StateClarity, GapValidity, Prioritization, ConstraintFit, Actionability on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (right-problem, constraints) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
