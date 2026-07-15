# Right Problem

`#RightProblem` is the ThinkingOS Golden Skill: the reference implementation for authoring, reviewing, and testing future Thinking Skills. It validates whether the stated problem is the problem that should be solved before solution generation begins.

- **Version:** 1.0.0
- **Status:** Released Golden Skill

## Purpose

Right Problem turns an initial problem statement into a validated problem frame. It clarifies the desired goal, identifies the obstacle preventing that goal, surfaces governing constraints, tests the logical relationship between them, and records material unknowns.

The skill does not brainstorm solutions, create action plans, diagnose people, or guarantee that a problem is objectively correct.

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| `problemStatement` | Yes | The problem as currently understood. |
| `goal` | Yes | The outcome that would make the problem worth solving. |
| `context` | No | Relevant environment, stakeholders, evidence, history, or boundaries. |
| `knownConstraints` | No | Time, budget, policy, capacity, authority, or other restrictions. |

## Outputs

- A normalized problem statement and clarified goal.
- Identified obstacles, constraints, and assumptions.
- Goal, obstacle, constraint, logic, and overall thinking scores.
- Missing information and one prioritized clarification question when needed.
- An evaluation status: `Valid`, `Invalid`, or `Incomplete`.
- A recommended next step and, when appropriate, the next Thinking Skill.

Outputs conform to `schemas/output.schema.json`. Overall Thinking Score maps to `evaluation.score`; the four dimension scores are reported as structured entries in `reasoning`, preserving the strict universal payload.

## Workflow

```text
Collect the stated problem and goal
  ↓
Validate input sufficiency and ambiguity
  ↓
Separate goal, obstacle, constraints, and assumptions
  ↓
Test whether the obstacle explains the goal gap
  ↓
Evaluate the quality of the problem frame
  ↓
Clarify, validate, or reject the frame
  ↓
Recommend the next step or skill
```

See [workflow.md](workflow.md) for the execution contract.

## Evaluation

The skill scores five dimensions from 0 to 4:

- Goal Score
- Obstacle Score
- Constraint Score
- Logic Score
- Overall Thinking Score

The overall score is evidence-based and does not average away a blocking failure. See [evaluation.md](evaluation.md) and [rubric.md](rubric.md).

## Usage

Invoke Right Problem when a request assumes a solution, contains an ambiguous problem statement, or would benefit from validating the goal and obstacle first.

```text
#RightProblem
$Goal
$Obstacle
@Constraint
%Validating
!Incomplete
```

A host implementation supplies inputs using its own interface, maps them into `skill.json`, runs the ThinkingOS Engine, and returns the universal output structure. No specific LLM or platform is required.

## Package contents

- `metadata.yaml` — discovery and dependency metadata
- `skill.json` — machine-valid skill contract
- `workflow.md` — ordered reasoning flow
- `validation.md` — input gates and failure behavior
- `conversation.md` — Socratic interaction rules
- `evaluation.md` and `rubric.md` — scoring model
- `examples.md` — representative cases
- `tests.md` — conformance cases
- `references.md` — normative and informative sources
- `CHANGELOG.md` — version history
