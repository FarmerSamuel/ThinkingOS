# Mind Map

`#MindMap` is a platform-independent ThinkingOS Skill. Represent concept hierarchy and cross-links without confusing visual proximity with logical evidence.

## Purpose

Externalize structure so hierarchy, relationships, and gaps can be inspected. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `problemComponents` — ProblemComponents input.
- `associations` — Associations input.
- `centralTopic` — CentralTopic input.

## Outputs

- `ConceptGraph`
- `ConceptHierarchy`
- `CrossLinks`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates Coverage, Hierarchy, LinkValidity, Readability, GoalAlignment on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (break-it-down, make-association) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
