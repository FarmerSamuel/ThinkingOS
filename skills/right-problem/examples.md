# Right Problem Examples

These examples demonstrate the skill contract; they are not domain advice.

## Simple case

### Input

- Problem: “I keep missing my morning train.”
- Goal: “Arrive at work by 09:00 on weekdays.”
- Context: The user reaches the platform after the 08:20 train departs.

### Evaluation

The goal is clear, but “missing the train” may be a symptom. The key question is: “What most often causes you to reach the platform after 08:20?” Until that obstacle is supported, the frame is `Incomplete`.

## Business case

### Input

- Problem: “We need a new CRM because sales are declining.”
- Goal: “Restore qualified-pipeline conversion from 14% to 20%.”
- Context: Lead volume is stable; stage-level loss data is unavailable.
- Constraint: Changes must comply with existing data-retention policy.

### Evaluation

“Need a new CRM” is a proposed solution, not a validated problem. The missing stage-level evidence prevents identifying the obstacle. Ask which pipeline stage accounts for the decline before evaluating technology. Status: `Incomplete`.

## Learning case

### Input

- Problem: “I am bad at statistics.”
- Goal: “Correctly choose and explain the statistical test in course assignments.”
- Context: Calculation accuracy is high, but test-selection questions are frequently wrong.

### Evaluation

The broad self-assessment is reframed as a specific decision-skill gap. The evidence supports test selection as the likely obstacle, while explanation quality remains to be checked. Status: provisionally `Valid`, with medium confidence.

## Failure case

### Input

- Problem: “Employees lack commitment.”
- Goal: “Improve performance.”
- Context: No performance definition, evidence, timeframe, or affected group is provided.

### Evaluation

The goal is ambiguous, the obstacle is an unsupported judgment about people, and no evidence connects the claim to performance. The frame is `Invalid` as stated. Ask: “What observable performance outcome has changed, for which group, and over what period?”

## Presentation example

After evaluation, a host may map the universal output into the presentation-only [Right Problem report example](../../examples/right-problem-report/README.md). The report must preserve status, evidence basis, assumptions, missing information, and transition gating. It must not add solution recommendations or implementation plans to an incomplete frame.
