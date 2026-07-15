# Make Association

`#MakeAssociation` is a platform-independent ThinkingOS Skill. Create and evaluate meaningful connections between elaborated concepts and prior knowledge.

## Purpose

Generate connections, then test their relevance and strength. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `elaboratedConcepts` — ElaboratedConcepts input.
- `structuralMapping` — StructuralMapping input.
- `priorKnowledge` — PriorKnowledge input.

## Outputs

- `Associations`
- `AssociationStrengths`
- `NovelConnections`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates Relevance, Strength, Novelty, Evidence, Usefulness on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (analogy, deep-processing) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
