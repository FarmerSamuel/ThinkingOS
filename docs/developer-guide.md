# Developer Guide

## Prerequisites

- Git
- Python 3.10 or newer
- Optional: a virtual environment for documentation dependencies

The core repository validator uses only the Python standard library. Building documentation requires the packages in `requirements-docs.txt`.

## Set up the repository

```bash
git clone https://github.com/FarmerSamuel/ThinkingOS.git
cd ThinkingOS
python -m venv .venv
```

Activate the environment using the command appropriate for your shell, then install documentation dependencies:

```bash
python -m pip install -r requirements-docs.txt
```

## Validate the repository

```bash
python tools/validate_repository.py
```

The validator checks Registry references and cycles, required package files, JSON syntax, Skill Schema top-level contracts, metadata consistency, test counts, and registered lifecycle state.

## Build documentation

```bash
mkdocs build --strict
```

For local preview:

```bash
mkdocs serve
```

Strict mode treats invalid navigation and documentation warnings as build failures.

## Generate a skill package

The curated generator is intended for project-maintained catalog entries:

```bash
python tools/generate_skill_packages.py constraints
```

Generated output is a starting contract, not an automatic approval. Review all domain language, examples, logic rules, transitions, and references before committing.

## Development rules

- Keep Core, Engine, Specification, Skill, Knowledge, and Adapter responsibilities separate.
- Preserve AI and platform independence outside `adapters/`.
- Use Semantic Versioning for public contracts and Conventional Commit-style messages.
- Update tests, Registry metadata, documentation, and changelogs with behavior changes.
- Run repository and documentation validation before opening a pull request.

## Troubleshooting

- A dependency cycle is a Registry design error; do not suppress it in the validator.
- A missing prerequisite should produce clarification or a transition recommendation, not an invented input.
- If an adapter requires platform-specific fields, map them at the boundary rather than extending skill semantics silently.
