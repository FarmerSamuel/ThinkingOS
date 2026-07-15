# Make Association Validation

## Entry gates

- `elaboratedConcepts` must be present when required, relevant, and semantically compatible.
- `structuralMapping` must be present when required, relevant, and semantically compatible.
- `priorKnowledge` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: analogy, deep-processing.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (Concept, Association, PriorKnowledge, Relationship, NovelConnection) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
