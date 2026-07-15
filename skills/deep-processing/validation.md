# Deep Processing Validation

## Entry gates

- `validatedProblem` must be present when required, relevant, and semantically compatible.
- `problemComponents` must be present when required, relevant, and semantically compatible.
- `sourceMaterial` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: right-problem, break-it-down.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (Concept, Explanation, Evidence, Connection, UnderstandingGap) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
