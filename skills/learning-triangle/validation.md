# Learning Triangle Validation

## Entry gates

- `elaboratedConcepts` must be present when required, relevant, and semantically compatible.
- `understandingGaps` must be present when required, relevant, and semantically compatible.
- `learningGoal` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: deep-processing.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (LearningGoal, Explanation, Practice, Feedback, UnderstandingGap) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
