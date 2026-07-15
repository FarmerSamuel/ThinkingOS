# Pull Request

## Summary

Describe the validated problem and the change made.

## Layer and scope

- Layer:
- In scope:
- Out of scope:

## Contract and compatibility impact

List affected schemas, identifiers, inputs, logic semantics, outputs, dependencies, versions, or migrations. Write `None` when not applicable.

## Verification

- [ ] `python tools/validate_repository.py`
- [ ] `mkdocs build --strict`
- [ ] New or changed behavior has tests.
- [ ] Registry, metadata, versions, references, and changelogs are aligned.
- [ ] No provider-specific behavior leaked outside `adapters/`.
- [ ] Collaboration fixtures are fully synthetic and contain no real user data.
- [ ] Fixture digests were computed only from synthetic source values.
- [ ] Draft schemas declare lifecycle, stability, versioned `$id`, and migration expectations.
- [ ] Cross-field collaboration invariants have positive and negative tests.

## Evidence

Include concise test output, screenshots, examples, or reasoning supporting the change.

## Checklist

- [ ] The change has one clear responsibility.
- [ ] Documentation and migration guidance are updated.
- [ ] The commit history uses semantic messages.
- [ ] I have reviewed the Code of Conduct and contribution guide.
