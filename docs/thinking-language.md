# ThinkingOS Language Specification

## Purpose

ThinkingOS Language (TOL) is a small, platform-independent domain-specific language for expressing reusable thinking structures. It identifies skills, thinking elements, context, state, evaluation results, and logical relationships without depending on an LLM, prompt format, API, or runtime.

The language describes thinking. It does not implement the named skills or prescribe how an application renders them.

## Lexical form

A reference consists of a sigil followed immediately by a PascalCase identifier:

```text
Reference := Sigil Identifier
Sigil    := "#" | "$" | "@" | "%" | "!"
Identifier := PascalCaseName
```

Canonical references contain no whitespace between the sigil and identifier. Each statement is written on its own line. Blank lines may be used for readability, and a line beginning with `//` is a comment.

## Core concepts

### Skill: `#Skill`

Represents a ThinkingOS Skill—the reusable thinking habit currently applied or referenced.

```text
#RightProblem
#BreakItDown
#GapAnalysis
```

These names are examples of references, not skill implementations.

### Element: `$Element`

Represents a unit of thought examined or transformed by a skill.

```text
$Goal
$Obstacle
$Constraint
$InitialState
$TargetState
```

### Constraint or context: `@Context`

Represents an environmental condition, boundary, or contextual factor that governs the analysis.

```text
@Budget
@Time
@Organization
```

`$Constraint` refers to a constraint as an analyzed thinking element; `@Constraint` would refer to that constraint acting as governing context.

### State: `%State`

Represents the current conversation or reasoning lifecycle state.

```text
%CollectingInputs
%Validating
%LogicTesting
```

State is descriptive and reusable across implementations. It must not encode provider-specific session behavior.

### Evaluation: `!Evaluation`

Represents a structured evaluation outcome or status.

```text
!Valid
!Invalid
!Incomplete
```

An evaluation token is a result label, not a substitute for the evidence and reasoning required by the ThinkingOS output schema.

### Logic

Logic expressions connect references or declared propositions.

#### Leads to: `->`

Means **leads to**, **produces**, or **supports the transition to**. It does not by itself prove causation; the applicable skill must define and test the relationship.

```text
$ObstacleRemoved -> $GoalAchievable
```

#### Decomposes or transforms to: `↓`

Means **is decomposed into**, **is refined into**, or **moves to the next analytical representation**.

```text
$InitialProblem ↓ $MinimumTractableUnit
```

Operators are evaluated from left to right. Parentheses, precedence rules, negation, and boolean operators are not part of version 1 of the language; complex logic should be expressed as multiple explicit statements.

## Document structure

A language document should declare one primary skill, followed by its elements, context, optional state, logic expressions, and evaluation result:

```text
#Skill
$Element
@Context
%State
$Element -> $Element
!Evaluation
```

References may repeat when their position in a sequence is meaningful. Implementations should preserve statement order.

## Examples

### Example 1: problem validation vocabulary

```text
#RightProblem
$Goal
$Obstacle
@Constraint
%Validating
!Valid
```

This declares the vocabulary and state of an evaluation. It does not define how `#RightProblem` performs validation.

### Example 2: decomposition vocabulary

```text
#BreakItDown
$InitialProblem
$InitialProblem ↓ $MinimumTractableUnit
$MinimumTractableUnit
```

### Example 3: gap analysis relationship

```text
#GapAnalysis
$InitialState
$TargetState
@Time
$InitialState -> $TargetState
!Incomplete
```

## Serialization

Text notation is the canonical human-readable form. Systems that need validation or interchange should serialize the same concepts as a JSON abstract syntax tree conforming to `schemas/thinking-language.schema.json`. A serializer must preserve concept type, identifier, statement order, operator, and operands.

## Conformance

A conforming document:

1. Uses only the defined sigils and operators.
2. Uses PascalCase identifiers after sigils.
3. Declares at least one skill reference.
4. Keeps platform and model configuration outside the language.
5. Uses evaluation tokens only with the reasoning and output requirements defined by the active skill.
