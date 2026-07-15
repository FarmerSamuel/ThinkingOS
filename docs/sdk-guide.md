# ThinkingOS SDK Guide

The Python SDK provides deterministic access to framework contracts. It does
not execute a language model or replace a Thinking Skill's reasoning rules.

## Install for development

```console
python -m pip install -e .
```

Python 3.11 or newer is required. Runtime dependencies are limited to PyYAML
for the Registry and `jsonschema` for Skill contract validation.

## Discover and traverse skills

```python
from thinkingos import SkillRegistry

registry = SkillRegistry.from_file("skills/registry.yaml")

for skill_id in registry.topological_order():
    skill = registry.get(skill_id)
    print(skill.id, skill.dependencies)

available = registry.available(completed={"right-problem"})
```

The registry rejects duplicate identifiers, unknown dependencies, self
dependencies, and cycles. `available` returns skills whose direct prerequisites
are satisfied.

## Load a Skill package

```python
from thinkingos import SkillLoader

loader = SkillLoader("skills", "schemas/skill.schema.json")
skill = loader.load("gap-analysis")
print(skill.version, skill.next_skills)
```

`SkillLoader` validates `skill.json` against the official Draft 2020-12 JSON
Schema and ensures the package directory matches its identifier. Skill IDs are
also checked against path traversal.

## Preserve conversation state

```python
from thinkingos import ConversationState

state = ConversationState(
    current_skill="right-problem",
    current_goal="Reduce avoidable delivery delays",
)
state.merge_inputs({"timeframe": "Q3"})

serialized = state.to_json()
restored = ConversationState.from_json(serialized)
```

State serialization uses the universal fields defined in
[`core/conversation-state.md`](../core/conversation-state.md). Applications
should persist only goal-relevant data and apply their own privacy and retention
controls.

## Connect an AI or host

Use an adapter after loading and validating a Skill. Adapters produce payloads;
the application owns transport, authentication, retries, and output validation.
See the repository's [`adapters/README.md`](../adapters/README.md).

## Compatibility

The public names exported from `thinkingos` follow Semantic Versioning. Skill
contracts, Registry entries, schemas, and adapters remain separately versioned
artifacts. A major SDK release may remove or change public Python APIs; a Skill
major release may change that Skill's inputs or output semantics.
