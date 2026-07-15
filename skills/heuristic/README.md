# Heuristic

`#Heuristic` is a platform-independent ThinkingOS Skill. Construct a bounded decision shortcut with explicit applicability and failure conditions.

## Purpose

Use shortcuts only when their boundaries and costs are visible. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `validatedProblem` — ValidatedProblem input.
- `constraintSet` — ConstraintSet input.
- `decisionContext` — DecisionContext input.

## Outputs

- `DecisionHeuristic`
- `ApplicabilityConditions`
- `FailureConditions`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates Simplicity, BoundaryClarity, Reliability, CostOfError, Testability on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (right-problem, constraints) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
