# Break It Down Tests

| ID | Case | Expected result |
| --- | --- | --- |
| BID-001 | Valid process decomposition | Complete ordered components and score at least 3. |
| BID-002 | Missing validated problem | Stop and request prerequisite input. |
| BID-003 | Missing goal | Return incomplete; do not generate a tree. |
| BID-004 | Mixed decomposition bases | Detect inconsistency and request one basis. |
| BID-005 | Material component omitted | Coverage score no higher than 2. |
| BID-006 | Overlapping siblings | Identify overlap and refine boundaries. |
| BID-007 | Leaves remain broad | Continue decomposition or disclose stopping limitation. |
| BID-008 | Excessive fragmentation | Merge trivial units that lost independent meaning. |
| BID-009 | Hidden dependency | Record dependency issue and cap overall score. |
| BID-010 | Cross-cutting concern | Preserve it explicitly rather than duplicating silently. |
| BID-011 | Alternative valid basis | Explain trade-off and use the basis aligned to the goal. |
| BID-012 | Output conformance | Validate universal output fields and score mapping. |

All cases must preserve facts, assumptions, ordering, and conversation state; none may generate solutions to the decomposed units.
