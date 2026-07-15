# ThinkingOS

[![CI](https://github.com/FarmerSamuel/ThinkingOS/actions/workflows/ci.yml/badge.svg)](https://github.com/FarmerSamuel/ThinkingOS/actions/workflows/ci.yml)
[![Documentation](https://github.com/FarmerSamuel/ThinkingOS/actions/workflows/pages.yml/badge.svg)](https://farmersamuel.github.io/ThinkingOS/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](CHANGELOG.md)

ThinkingOS is a production-ready, open-source framework for reusable,
validation-first thinking. It improves human reasoning without replacing it and
remains independent of any language model, provider, prompt format, or user
interface.

It is not a prompt collection. Thinking Skills are versioned reasoning contracts
with explicit inputs, validation, logic, evaluation, conversation behavior,
structured outputs, examples, references, and tests.

## What v1.0 includes

- A universal Core persona, philosophy, workflow, validation model, and Engine.
- Thirteen composable Thinking Skills, each conforming to the official Skill
  Specification.
- JSON Schemas for skills, evaluation, output, language, and adapter requests.
- A directed, acyclic Skill Registry and Thinking Graph.
- A curated knowledge base for critical, systems, decision, and problem thinking.
- A Python SDK for Registry traversal, Skill validation, and reusable state.
- OpenAI, Claude, Gemini, Cursor, GitHub Copilot, and MCP adapters.
- Strict documentation, schema, test, lint, Pages, and release automation.

## Execution model

```text
Collect Inputs -> Validate -> Detect Missing Information -> Evaluate Elements
-> Run Logic Rules -> Evaluate Reasoning -> Generate Evaluation
-> Generate Output -> Recommend Next Skill
```

The Engine stops or loops when material information is missing. Fluent model
output is never treated as proof of valid reasoning.

## Install the SDK

Clone the repository and install it in an isolated Python 3.11+ environment:

```console
python -m pip install -e .
```

```python
from thinkingos import SkillLoader, SkillRegistry

registry = SkillRegistry.from_file("skills/registry.yaml")
loader = SkillLoader("skills", "schemas/skill.schema.json")

for skill_id in registry.topological_order():
    skill = loader.load(skill_id)
    print(skill.id, skill.version)
```

Adapters only map payloads. Your application owns transport, credentials,
model choice, retries, privacy controls, and final output validation.

## Repository structure

| Path | Responsibility |
| --- | --- |
| `core/` | Universal reasoning behavior and Engine |
| `skills/` | Versioned Thinking Skill packages and Registry |
| `knowledge/` | Reusable knowledge independent of Skill logic |
| `schemas/` | Machine-verifiable public contracts |
| `thinkingos/` | Python SDK |
| `adapters/` | Provider and host protocol mappings |
| `docs/` | Architecture, specifications, and guides |
| `tests/` | Executable SDK and adapter contracts |
| `.github/` | Community templates and automation |

## Documentation

- [English documentation](https://farmersamuel.github.io/ThinkingOS/)
- [繁體中文文件](https://farmersamuel.github.io/ThinkingOS/zh/)
- [Architecture](docs/architecture.md)
- [Skill Specification](docs/skill-specification.md)
- [SDK Guide](docs/sdk-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [Skill Author Guide](docs/skill-author-guide.md)
- [Thinking Graph](docs/thinking-graph.md)

## Contributing and security

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), follow the
[Code of Conduct](CODE_OF_CONDUCT.md), and report vulnerabilities according to
[SECURITY.md](SECURITY.md).

ThinkingOS is released under the [MIT License](LICENSE).
