# Complexity

`#Complexity` is a platform-independent ThinkingOS Skill. Evaluate interaction, dependency, uncertainty, and adaptation within a bounded system.

## Purpose

Examine relationships and behavior rather than counting parts alone. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `problemComponents` — ProblemComponents input.
- `systemBoundary` — SystemBoundary input.
- `dependencyStructure` — DependencyStructure input.

## Outputs

- `ComplexityProfile`
- `InteractionMap`
- `UncertaintyDrivers`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates InteractionCoverage, DependencyQuality, Uncertainty, Adaptation, ExplanatoryPower on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (break-it-down, boundary) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
