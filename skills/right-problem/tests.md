# Right Problem Tests

## Conformance cases

| ID | Scenario | Input condition | Expected result |
| --- | --- | --- | --- |
| RP-001 | Complete valid frame | Clear outcome, supported obstacle, classified constraints | `Valid`; Goal and Logic scores at least 3. |
| RP-002 | Missing goal | Problem statement present, goal absent | `Incomplete`; ask one goal clarification question; no solution. |
| RP-003 | Solution disguised as problem | “We need a new tool” with no validated outcome | `Incomplete` or `Invalid`; identify solution-led framing. |
| RP-004 | Ambiguous goal | “Improve performance” without metric, stakeholder, or scope | `Incomplete`; prioritize success-definition question. |
| RP-005 | Symptom mistaken for obstacle | Symptom is restated as its own cause | Logic issue recorded; Logic Score no higher than 2. |
| RP-006 | Unsupported causal claim | Obstacle asserted without relevant evidence | Missing evidence recorded; confidence low or medium. |
| RP-007 | Contradictory fixed constraint | Goal requires an action prohibited by a fixed constraint | `Invalid` or `Incomplete`; Overall Score no higher than 2. |
| RP-008 | Constraint misclassified as obstacle | Governing boundary is presented as the cause of a gap | Separate constraint from obstacle before evaluation. |
| RP-009 | Multiple bundled problems | One statement contains unrelated outcomes and obstacles | `Incomplete`; ask which problem has priority. |
| RP-010 | Alternative explanation | Evidence supports two plausible obstacles | Record both; request discriminating evidence; do not overclaim. |
| RP-011 | High-quality business frame | Goal, stage-level evidence, causal obstacle, and constraints align | `Valid`; structured output and medium/high confidence. |
| RP-012 | Harmful people judgment | Problem attributes motive or character without evidence | Reject unsupported judgment; request observable behavior and outcome. |
| RP-013 | Non-blocking context gap | Optional context missing but cannot change current classification | Ready with disclosed assumption; record limitation. |
| RP-014 | Output conformance | Valid inputs complete execution | Output validates against `schemas/output.schema.json` plus declared extension. |
| RP-015 | Next-skill gating | Problem remains incomplete | No downstream skill recommendation that assumes a valid frame. |

## Test protocol

For every case, verify:

1. Required inputs and validation state.
2. The first question is the highest-impact missing item.
3. Facts, assumptions, and interpretations remain distinguishable.
4. Dimension scores cite observations from the case.
5. Safeguards cap Overall Thinking Score when required.
6. No solution is generated before a valid problem frame exists.
7. Output and conversation state conform to shared contracts.

Provider-specific wording may vary, but classification, rule outcomes, required fields, and Never Rule behavior must remain equivalent.
