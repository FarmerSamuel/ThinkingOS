# Complexity Validation

## Entry gates

- `problemComponents` must be present when required, relevant, and semantically compatible.
- `systemBoundary` must be present when required, relevant, and semantically compatible.
- `dependencyStructure` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: break-it-down, boundary.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (Component, Interaction, Dependency, UncertaintyDriver, FeedbackLoop) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
