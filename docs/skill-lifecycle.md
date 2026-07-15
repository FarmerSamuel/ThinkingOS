# ThinkingOS Skill Lifecycle

## Lifecycle

```text
Draft
  ↓
Review
  ↓
Testing
  ↓
Release
  ↓
Improvement
  ↓
Deprecation
```

### Draft

Define the single thinking habit, purpose, boundaries, inputs, rules, evaluation criteria, outputs, examples, and tests using the Skill Specification. Draft skills are unstable and must not be presented as released capabilities.

**Exit criteria:** The definition is complete enough for schema validation and independent review.

### Review

Evaluate conceptual clarity, responsibility boundaries, overlap with existing skills, platform independence, evidence quality, and consistency with Core principles.

**Exit criteria:** Review findings are resolved or explicitly accepted, and the skill is approved for conformance testing.

### Testing

Run schema validation, positive cases, invalid-input cases, ambiguity cases, boundary conditions, Never Rule tests, logic tests, output checks, and cross-platform conformance tests where applicable.

**Exit criteria:** Required tests pass and known limitations are documented.

### Release

Assign a Semantic Version, publish the skill definition and tests, record changes, and declare compatibility. A release must be immutable; corrections require a new version.

**Exit criteria:** The released artifact is discoverable, versioned, documented, and reproducible.

### Improvement

Collect evidence from usage, defects, evaluation quality, and compatibility feedback. Proposed changes return through Draft, Review, and Testing before another release.

**Exit criteria:** An improvement is rejected with rationale, retained for future work, or released as a new version.

### Deprecation

Mark a skill or version as discouraged when it is unsafe, redundant, superseded, or no longer maintainable. Provide the reason, replacement or migration path, support window, and removal plan.

**Exit criteria:** Consumers have clear migration guidance; removal occurs only under the declared versioning policy.

## Semantic Versioning

ThinkingOS Skills use `MAJOR.MINOR.PATCH` according to Semantic Versioning.

- **MAJOR:** Incompatible changes to inputs, validation behavior, logic semantics, evaluation meaning, output contract, state transitions, or public identifiers.
- **MINOR:** Backward-compatible capabilities, optional inputs, evaluation criteria, examples, or additive output extensions.
- **PATCH:** Backward-compatible corrections, clarifications, reference updates, or test improvements that do not change intended semantics.

Pre-release versions may use identifiers such as `1.0.0-alpha.1`. Version `0.y.z` indicates initial development and does not remove the obligation to document breaking changes.

## Compatibility and change control

- Every release must include a changelog entry.
- Tests and examples are versioned with the skill.
- Consumers should pin a compatible version range rather than assume latest behavior.
- Deprecation does not alter an existing release; it adds lifecycle metadata and migration guidance.
- A renamed or split skill is a breaking change unless an explicit backward-compatible alias preserves the original contract.
