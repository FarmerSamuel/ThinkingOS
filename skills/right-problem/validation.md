# Right Problem Validation

## Validation outcome

Validation returns exactly one state:

- **Ready:** Required inputs are sufficient and materially unambiguous.
- **Ready with disclosed assumptions:** Non-blocking gaps can be handled through explicit, low-risk assumptions.
- **Needs clarification:** A missing or ambiguous input could materially change the evaluation.

## Input rules

### Problem statement

- Must describe an undesirable condition, gap, risk, or decision difficulty.
- Must not be only a preferred solution, such as “we need a new app.”
- Must be specific enough to distinguish the affected outcome or stakeholder.

### Goal

- Must describe a desired outcome rather than an activity.
- Must be distinguishable from the problem statement.
- Should include success evidence or a decision criterion when available.

### Success criteria

- Must describe observable evidence of improvement, not merely completion of an activity.
- Should identify the affected outcome, relevant scope, and threshold or decision rule when those details can change the evaluation.
- May use Given/When/Then for operational scenarios, but no documentation syntax is universally required.

### Context

- May be omitted when the frame can be evaluated without it.
- Becomes blocking when environment, stakeholder, timeframe, or evidence changes the meaning of the problem.

### Known constraints

- Must be separated from obstacles: a constraint governs feasible action; an obstacle explains the current goal gap.
- Claimed constraints should be labeled as fixed, negotiable, assumed, or unknown when evidence permits.

## Material ambiguity checks

Flag vague degree, time, scope, quality, frequency, capability, or quantity terms only when more than one reasonable interpretation could change the evaluation. Clarify unclear ownership, mixed timeframes, proxy goals, or bundled problems. Do not reject useful natural language merely because it contains a word from a checklist.

## Obstacle and constraint diagnostic

Ask whether additional resources, authority, time, or evidence would remove the condition. A removable condition is more likely an obstacle; a boundary that still governs the feasible space is more likely a constraint. This is a diagnostic heuristic, not proof. Classify each condition using context and evidence, and allow `unknown` when the distinction is not yet supported.

## Consistency checks

- The goal must not contradict a fixed constraint.
- The obstacle must plausibly relate to the goal gap.
- Material causal claims must be tested against a plausible alternative explanation or disconfirming observation.
- Evidence must not directly invalidate a required premise without that conflict being addressed.
- The problem must not define success as merely implementing a preselected solution.

## Missing-information priority

Ask first about the unknown with the greatest expected impact on problem validity. Do not ask for information that would not change the result.

## Prohibited fallback

Never invent stakeholders, causes, evidence, constraints, or success criteria to make an incomplete frame appear valid.
