# Mind Map Validation

## Entry gates

- `problemComponents` must be present when required, relevant, and semantically compatible.
- `associations` must be present when required, relevant, and semantically compatible.
- `centralTopic` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: break-it-down, make-association.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (CentralTopic, Concept, Hierarchy, CrossLink, ConceptGraph) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
