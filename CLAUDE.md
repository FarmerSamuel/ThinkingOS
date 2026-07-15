# CLAUDE.md

Guidance for Claude Code sessions working in this repository.

## What this repository is

ThinkingOS is an AI-agnostic framework of versioned Thinking Skills — reasoning
contracts with explicit inputs, validation gates, logic rules, evaluation
rubrics, and structured outputs. It improves human reasoning without replacing
it. It is not a prompt collection, and nothing outside `adapters/` may depend
on a specific provider, model, or prompt format.

## Layer map

| Path | Responsibility | Editable? |
| --- | --- | --- |
| `core/` | Universal persona, philosophy, principles, workflow, validation, Engine | Canonical source |
| `skills/<id>/` | One versioned Thinking Skill package per directory | Canonical source |
| `skills/registry.yaml` | Directed acyclic skill graph (dependencies, produces, consumes) | Canonical source |
| `schemas/` | Machine-verifiable JSON Schemas for skills, evaluation, output, language, adapters | Canonical source |
| `knowledge/` | Reusable thinking knowledge, independent of skill logic | Canonical source |
| `thinkingos/` | Python SDK (registry traversal, skill loading, state) | Source code |
| `adapters/` | Provider payload mappings (OpenAI, Claude, Gemini, Cursor, Copilot, MCP) | Source code |
| `docs/` | Bilingual MkDocs site (`*.md` English, `*.zh.md` Traditional Chinese) | Docs |
| `tools/` | Dependency-light maintenance scripts | Source code |
| `tests/` | Executable SDK, adapter, and export contracts | Tests |
| `.claude/skills/` | Generated Claude Agent Skill packages | **Generated — never edit by hand** |

## Generated Claude skills

`.claude/skills/` is generated from `skills/*/skill.json`, `skills/registry.yaml`,
and `core/` by `tools/export_claude_skills.py`. After changing any skill package
or the registry, regenerate and commit the result:

```bash
python tools/export_claude_skills.py          # regenerate
python tools/export_claude_skills.py --check  # verify sync (CI enforces this)
```

`tests/test_claude_export.py` fails when the export drifts. Keep personal,
non-project skills in `~/.claude/skills`, not here.

## Validation commands

Run all of these before committing; CI runs the same checks:

```bash
python tools/validate_repository.py   # registry, skill contracts, docs parity, links
python -m unittest discover -s tests  # SDK, adapter, and export contracts
python tools/export_claude_skills.py --check
mkdocs build --strict                 # needs: pip install -r requirements-docs.txt
npx markdownlint-cli2 "**/*.md"       # lint per .markdownlint-cli2.yaml
```

`python -m pip install -r requirements-dev.txt` provides `jsonschema` and
`PyYAML` for the full validator and test suite.

## Editing rules

- **Skill changes are versioned contract changes.** When a skill's behavior
  changes, update in lockstep: `skills/<id>/skill.json` (`version`),
  `skills/<id>/metadata.yaml` (`version`), `skills/registry.yaml` (`version`),
  the skill's `CHANGELOG.md`, and the root `CHANGELOG.md` under `[Unreleased]`.
  The validator rejects mismatches.
- **Every skill package needs all required files:** README.md, metadata.yaml,
  skill.json, workflow.md, validation.md, evaluation.md, rubric.md,
  examples.md, tests.md (at least ten `| XX-NNN |` table rows), references.md,
  CHANGELOG.md. `skill.json` needs at least five contract tests.
- **Docs are bilingual.** Every `docs/*.md` must have a `docs/*.zh.md`
  counterpart, and new pages must be added to `mkdocs.yml` nav (with a
  `nav_translations` entry). The validator and strict MkDocs build enforce
  this.
- **Do not link from `docs/` to files outside `docs/`** — the strict MkDocs
  build fails on such links. Reference repository paths in backticks instead.
- **Registry must stay acyclic.** A dependency cycle is a design error; never
  suppress it in the validator.
- **Provider neutrality.** Only `adapters/` may mention providers. Skills,
  Core, schemas, and knowledge stay platform-independent.
- **Never fabricate skill content.** Examples, tests, and references in skill
  packages must be reviewed domain content, not filler.

## Conventions

- Conventional Commit-style messages (`feat(skills): ...`, `docs(i18n): ...`).
- Semantic Versioning for all public contracts; `VERSION`, `pyproject.toml`,
  and `thinkingos/__init__.py` must agree (validator-enforced).
- Python: standard library only in `tools/`; type hints; unittest (not pytest).
- Markdown: first line is a top-level heading; fenced code blocks declare a
  language; MD013 (line length) is disabled.

## Iterating on skill quality

The intended improvement loop when using these skills in Claude:

1. Use a skill in a real conversation (they load from `.claude/skills/`).
2. When it misfires — wrong question, missed ambiguity, premature solution —
   capture the conversation as a new case in `skills/<id>/examples.md` and a
   conformance row in `skills/<id>/tests.md`.
3. Encode the fix as a validation gate, logic rule, or never-rule in
   `skill.json`, not as loose prose.
4. Bump versions, update changelogs, regenerate the Claude export, run all
   validation commands, then commit.
