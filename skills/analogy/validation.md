# Analogy Validation

## Entry gates

- `validatedProblem` must be present when required, relevant, and semantically compatible.
- `targetStructure` must be present when required, relevant, and semantically compatible.
- `candidateAnalogues` must be present when required, relevant, and semantically compatible.

## Required checks

- Detect missing, ambiguous, contradictory, stale, or unsupported inputs.
- Verify dependencies: right-problem.
- Distinguish facts, assumptions, interpretations, and constraints.
- Confirm that every material element (TargetStructure, SourceAnalogue, StructuralMapping, Difference, Limitation) has evidence or explicit unknown status.

Return `ready`, `ready with disclosed assumptions`, or `needs clarification`. Never fabricate data to pass a gate.
