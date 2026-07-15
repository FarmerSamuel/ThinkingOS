# Skill Dependencies

## Purpose

A dependency means a skill requires a reasoning capability or validated semantic output normally produced by another skill. Dependencies protect analysis quality; they are not package-installation dependencies and do not force a particular user interface or AI provider.

The authoritative dependency list is `skills/registry.yaml`.

## Prerequisite relationships

| Skill | Prerequisites | Why they should precede it |
| --- | --- | --- |
| `right-problem` | None | Establishes the validated problem and goal used by downstream reasoning. |
| `break-it-down` | `right-problem` | Decomposition is only useful after confirming what should be decomposed. |
| `constraints` | `right-problem` | Constraints require a validated problem boundary and intended outcome. |
| `gap-analysis` | `right-problem`, `constraints` | A meaningful gap needs a valid goal, current and target states, and a feasible space. |
| `analogy` | `right-problem` | Structural comparison should begin from a clear target problem rather than superficial similarity. |
| `heuristic` | `right-problem`, `constraints` | A heuristic is safe only when its decision context and failure boundaries are understood. |
| `deep-processing` | `right-problem`, `break-it-down` | Deep understanding depends on valid scope and identifiable components. |
| `make-association` | `analogy`, `deep-processing` | Useful connections require both structural comparison and adequately elaborated concepts. |
| `learning-triangle` | `deep-processing` | A learning plan should respond to demonstrated understanding gaps and elaborated concepts. |
| `mind-map` | `break-it-down`, `make-association` | A concept graph needs both a component structure and meaningful cross-links. |
| `boundary` | `right-problem`, `constraints` | System scope depends on the problem, stakeholders, and governing constraints. |
| `complexity` | `break-it-down`, `boundary` | Complexity cannot be assessed reliably without components, dependencies, and an explicit system boundary. |
| `emergence` | `complexity`, `make-association` | Emergent behavior requires interaction structure and cross-element relationships. |

## Dependency satisfaction

A prerequisite is satisfied when either:

1. The prerequisite skill produced a compatible, validated result in the current state; or
2. Equivalent inputs are supplied from another trustworthy source and pass the consumer's validation rules.

Matching names alone is insufficient. Implementations must verify semantic compatibility, provenance, version compatibility, completeness, and confidence.

## Execution behavior

- The Engine detects unresolved prerequisites before running skill logic.
- Missing blocking outputs produce a clarification request or prerequisite recommendation.
- Multiple satisfied prerequisites may converge on one skill.
- A skill may produce outputs useful to several downstream skills without selecting all of them.
- Dependencies must remain acyclic in the initial graph. Iterative reasoning is represented through conversation state and repeated executions, not circular registry edges.

## Changing dependencies

Adding a required prerequisite can be a breaking change because previously valid executions may no longer run. Dependency changes must follow the Skill Lifecycle, Semantic Versioning, conformance testing, and registry review.
