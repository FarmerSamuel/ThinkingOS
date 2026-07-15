# Skill Author Guide

## Design the thinking habit

Before creating files, write one sentence each for:

- The single thinking problem.
- The reusable thinking habit.
- The outcome the skill produces.
- What is explicitly out of scope.

If two independent habits appear, design two composable skills.

## Select inputs and outputs

Reuse Registry semantics where meanings match. Required inputs must be necessary for valid logic; optional inputs become blocking only when their absence could materially change the result.

Outputs should be useful downstream without depending on prose interpretation. Declare dependencies and transition conditions explicitly.

## Create the package

Every project skill contains:

```text
README.md
metadata.yaml
skill.json
workflow.md
validation.md
evaluation.md
rubric.md
examples.md
tests.md
references.md
CHANGELOG.md
```

Use `skills/right-problem/` as the Golden Skill reference. A curated catalog entry may be scaffolded with `tools/generate_skill_packages.py`.

## Write the contract

1. Define purpose, scope, and thinking elements.
2. Declare typed required and optional inputs.
3. Write validation gates before logic rules.
4. Make logic ordered, observable, and reproducible.
5. Define dimension criteria and a calibrated rubric.
6. Map overall score to `evaluation.score` and dimension findings to `reasoning` without violating the strict universal output schema.
7. Add neutral conversation rules and explicit Never Rules.
8. Declare dependency-safe next-skill transitions.

## Test the skill

Include at least ten documented cases covering valid input, missing input, ambiguity, contradiction, unsupported assumptions, missing dependencies, alternatives, boundaries, low evidence, output conformance, state preservation, and transition gating.

Tests verify contract outcomes, not exact model wording.

## Release the skill

- Start at `0.1.0` and `draft`.
- Progress through review and testing before release.
- Keep Registry, metadata, `skill.json`, tests, and changelog versions aligned.
- Follow [Skill Lifecycle](skill-lifecycle.md) and Semantic Versioning.

## Validate

```bash
python tools/validate_repository.py
mkdocs build --strict
```

Do not release a skill that passes structural validation but still has generic, unsupported, overlapping, or provider-dependent logic.
