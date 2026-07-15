# ThinkingOS

ThinkingOS is an open-source, AI-agnostic framework for improving human reasoning through reusable Thinking Skills. It is not a prompt collection and does not depend on a particular model, provider, user interface, or tool protocol.

## What the framework provides

- A universal reasoning persona and set of core principles.
- A validation-first execution Engine shared by every skill.
- Machine-verifiable Skill, Evaluation, Output, and Language schemas.
- A directed Thinking Graph with explicit dependencies and transitions.
- Thirteen reusable Thinking Skills with versioned contracts and tests.
- A reusable knowledge layer separated from skill logic.
- Platform adapters that translate host formats without changing semantics.

## How ThinkingOS works

```mermaid
flowchart LR
    I["Input"] --> V["Validate"]
    V --> E["Evaluate Elements"]
    E --> L["Run Logic"]
    L --> Q["Evaluate Reasoning"]
    Q --> O["Structured Output"]
    O --> N["Next Skill"]
```

The Engine stops or loops when a blocking ambiguity, contradiction, or missing dependency appears. It never treats fluent output as evidence that reasoning is valid.

## Start here

- Read the [Architecture](architecture.md) for layer responsibilities.
- Review the [Skill Specification](skill-specification.md) before authoring a skill.
- Use the [Developer Guide](developer-guide.md) to validate and test the repository.
- Follow the [Skill Author Guide](skill-author-guide.md) to create a conforming package.
- See the [Thinking Graph](thinking-graph.md) for skill relationships.

## Project status

ThinkingOS is progressing toward v1.0. Registry status and per-skill changelogs are authoritative; roadmap inclusion alone does not imply a stable release.
