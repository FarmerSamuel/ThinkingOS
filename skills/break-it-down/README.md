# Break It Down

`#BreakItDown` decomposes a validated problem into coherent, non-overlapping, minimum tractable units while preserving dependencies and the original goal.

## Purpose

Use this skill when a valid problem is too broad, coupled, or abstract for reliable analysis. It creates a decomposition map; it does not solve the components.

## Inputs

- `validatedProblem` — a problem frame produced by `#RightProblem` or equivalent validated input.
- `goal` — the outcome the decomposition must preserve.
- `knownStructure` — optional components, dependencies, and boundaries already known.
- `stoppingCriteria` — optional conditions defining when a unit is tractable.

## Outputs

- Problem components and minimum tractable units.
- Parent-child and dependency relationships.
- Coverage, overlap, tractability, and logic evaluation.
- Missing structure and the next recommended skill or action.

## Workflow

```text
Validate problem and goal
  ↓
Choose a decomposition basis
  ↓
Generate candidate components
  ↓
Test coverage and overlap
  ↓
Refine to tractable units
  ↓
Map dependencies
  ↓
Evaluate and output
```

## Evaluation

The skill evaluates coverage, distinctness, tractability, dependency integrity, and goal alignment on a 0–4 scale. See [evaluation.md](evaluation.md) and [rubric.md](rubric.md).

## Usage

```text
#BreakItDown
$InitialProblem ↓ $MinimumTractableUnit
%LogicTesting
!Incomplete
```

Run only after the problem is validated. Use outputs as structured inputs to downstream analysis; do not treat decomposition as a solution.
