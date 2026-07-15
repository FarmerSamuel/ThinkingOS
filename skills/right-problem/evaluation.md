# Right Problem Evaluation

## Scoring model

Each dimension is scored from **0 to 4** using `rubric.md`. Scores describe the quality of the current problem frame, not the user's ability.

### Goal Score

Measures whether the desired outcome is clear, relevant, distinguishable from an activity, and supported by observable success criteria.

### Obstacle Score

Measures whether the condition preventing the goal is specific, evidence-aware, and plausibly causal rather than merely a symptom or restatement.

### Constraint Score

Measures whether material boundaries are identified, classified, and separated from obstacles and unsupported assumptions.

### Logic Score

Measures whether the goal, obstacle, constraints, evidence, and conclusion form a consistent and adequately supported problem frame.

### Overall Thinking Score

Summarizes the readiness of the complete frame. Begin with the rounded mean of the four dimension scores, then apply these safeguards:

- If Goal Score or Logic Score is `0`, Overall Thinking Score cannot exceed `1`.
- If any required input is missing, Overall Thinking Score cannot exceed `2`.
- If a contradiction remains unresolved, Overall Thinking Score cannot exceed `2`.
- A higher score requires evidence quality consistent with that level.

## Evaluation status

| Status | Typical condition |
| --- | --- |
| `Valid` | Overall score is 3–4, no blocking gap remains, and Goal and Logic scores are at least 3. |
| `Incomplete` | A material ambiguity or missing input prevents a reliable judgment. |
| `Invalid` | The frame is contradicted by evidence, logically incoherent, solution-led, or unrelated to the stated goal. |

Status is determined by evidence and blocking conditions, not by score alone.

## Confidence

- **High:** Relevant evidence is credible, inputs are complete, and alternative explanations have been considered.
- **Medium:** The frame is usable but some evidence, context, or alternatives remain uncertain.
- **Low:** Material information is missing, disputed, ambiguous, or based mainly on assumption.

## Required evaluation output

Include strengths, weaknesses, missing information, logical issues, recommendation, and confidence in the universal evaluation structure. Map Overall Thinking Score to `evaluation.score`, and report Goal, Obstacle, Constraint, and Logic scores as clearly labeled entries in `reasoning`. This preserves strict conformance with `schemas/output.schema.json`.
