# Constraints

`#Constraints` is a platform-independent ThinkingOS Skill. Identify, classify, and test the boundaries that define the feasible problem space.

## Purpose

Make governing boundaries explicit before evaluating options. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `validatedProblem` — ValidatedProblem input.
- `context` — Context input.
- `candidateConstraints` — CandidateConstraints input.

## Outputs

- `ConstraintSet`
- `ConstraintClassification`
- `FeasibleSpace`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates Completeness, Classification, Evidence, Feasibility, Consistency on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (right-problem) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
