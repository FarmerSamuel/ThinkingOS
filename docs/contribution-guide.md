# Contribution Guide

This guide supplements the repository-level `CONTRIBUTING.md` with the framework-specific review process.

## Choose the correct layer

| Change | Location |
| --- | --- |
| Universal behavior or principles | `core/` |
| Execution ordering | `core/engine.md` |
| Public contracts and schemas | `schemas/` and specification docs |
| One thinking habit | `skills/<id>/` |
| Reusable evidence or terminology | `knowledge/` |
| Provider or interface translation | `adapters/` |

Avoid duplicating shared behavior in multiple skills or leaking provider assumptions upward.

## Contribution workflow

1. Search existing issues, Registry entries, and skills for overlap.
2. Discuss material architecture or public contract changes before implementation.
3. Create a focused branch and make small semantic commits.
4. Add or update validation, examples, tests, references, and changelogs.
5. Run `python tools/validate_repository.py` and `mkdocs build --strict`.
6. Open a pull request using the project template and explain compatibility impact.

## Review criteria

Reviewers evaluate scope, layer ownership, evidence, AI independence, Schema conformance, dependency correctness, testing, documentation, versioning, and migration impact.

## Breaking changes

Changes to public identifiers, required inputs, logic semantics, evaluation meaning, output fields, or dependencies may require a major version. Provide migration guidance and do not rewrite released artifacts in place.

## Community standards

All participation is governed by the [Code of Conduct](https://github.com/FarmerSamuel/ThinkingOS/blob/main/CODE_OF_CONDUCT.md). Report suspected security issues privately rather than in public issues.
