# Boundary Validation

## Entry gates

- `validatedProblem` must be present when required, relevant, and semantically compatible.
- `constraintSet` must be present when required, relevant, and semantically compatible.
- `stakeholders` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: right-problem, constraints.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (SystemBoundary, InScopeElement, OutOfScopeElement, Interface, Stakeholder) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
