# Boundary

`#Boundary` is a platform-independent ThinkingOS Skill. Define what is inside, outside, and crossing a system boundary for a validated problem.

## Purpose

Make scope choices and boundary assumptions explicit before reasoning about a system. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `validatedProblem` — ValidatedProblem input.
- `constraintSet` — ConstraintSet input.
- `stakeholders` — Stakeholders input.

## Outputs

- `SystemBoundary`
- `InScopeElements`
- `OutOfScopeElements`
- `BoundaryAssumptions`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates ScopeClarity, InterfaceCoverage, StakeholderFit, AssumptionTransparency, Usefulness on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (right-problem, constraints) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
