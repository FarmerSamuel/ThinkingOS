# ThinkingOS Naming Conventions

Consistent naming makes skills portable, searchable, and machine-verifiable.

## DSL identifiers

Use **PascalCase** after every ThinkingOS Language sigil.

| Concept | Pattern | Examples |
| --- | --- | --- |
| Skill | `#PascalCase` | `#RightProblem`, `#GapAnalysis` |
| Element | `$PascalCase` | `$Goal`, `$InitialState` |
| Context | `@PascalCase` | `@Budget`, `@Organization` |
| State | `%PascalCase` | `%Validating`, `%LogicTesting` |
| Evaluation | `!PascalCase` | `!Valid`, `!Incomplete` |

Names should be concise, specific, and semantic. Prefer nouns for elements and context, state-oriented terms for conversation state, and outcome-oriented terms for evaluations. Avoid provider names, implementation technologies, unexplained abbreviations, and version numbers inside identifiers.

## JSON

Use **camelCase** for JSON property names:

```json
{
  "thinkingElements": [],
  "conversationState": "%Validating",
  "nextSkill": "#GapAnalysis"
}
```

Enum values defined as DSL references retain their sigil and PascalCase identifier. Schema filenames use lowercase kebab-case with the `.schema.json` suffix.

## Markdown documentation

Use Markdown for specifications, explanations, examples, and project documentation.

- Use one level-one heading per document.
- Use sentence case for headings.
- Use fenced code blocks for DSL and JSON examples.
- Use relative links for repository-local references.
- Use lowercase kebab-case filenames, such as `thinking-language.md`.

## Skill names and directories

The human-readable skill identity uses PascalCase in the DSL. When a filesystem-safe or package identifier is needed, derive a lowercase kebab-case name without changing its meaning—for example, `#GapAnalysis` becomes `gap-analysis`.

## Stability

Names are part of the public contract. Renaming a published concept requires migration guidance and an appropriate specification version change; aliases must be explicit and temporary.
