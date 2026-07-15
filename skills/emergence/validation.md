# Emergence Validation

## Entry gates

- `complexityProfile` must be present when required, relevant, and semantically compatible.
- `interactionMap` must be present when required, relevant, and semantically compatible.
- `associations` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: complexity, make-association.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (Interaction, Pattern, SystemBehavior, EmergenceCondition, AlternativeExplanation) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
