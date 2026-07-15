# Break It Down Validation

## Entry gates

- `validatedProblem` and `goal` must be present and mutually consistent.
- Scope and system boundary must be sufficiently clear for the chosen decomposition basis.
- A preselected solution must not be treated as the problem structure.

## Decomposition checks

- **Basis:** Sibling components use the same organizing principle.
- **Coverage:** No material in-scope concern is omitted.
- **Distinctness:** Overlap is absent or explicitly explained.
- **Tractability:** Leaf units can be evaluated independently enough to support a next step.
- **Integrity:** Dependencies and shared resources are not erased by decomposition.
- **Goal alignment:** Every retained component can be related to the validated goal.

Return `needs clarification` when missing scope, boundary, or success criteria could materially change the tree. Never invent components solely to make the structure appear complete.
