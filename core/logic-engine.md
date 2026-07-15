# Generic Logic Engine

The logic engine defines a common reasoning contract for every ThinkingOS skill. It is domain-neutral and contains no skill-specific logic.

```text
Input
  ↓
Validation
  ↓
Logic Rules
  ↓
Evaluation
  ↓
Output
```

## Contract

1. **Input:** Declare accepted data, the intended goal, and relevant context.
2. **Validation:** Apply the shared validation framework and stop or qualify processing when inputs are inadequate.
3. **Logic Rules:** Declare the principles, tests, conditions, priorities, and decision criteria used by the skill.
4. **Evaluation:** Apply those rules consistently, compare alternatives where relevant, and record evidence, exceptions, and uncertainty.
5. **Output:** Return the result through the universal output schema, including missing information and confidence.

Skills may extend this contract, but must not bypass validation, hide material assumptions, or present unsupported conclusions as facts.
