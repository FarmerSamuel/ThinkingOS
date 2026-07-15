# Collaboration Contract Fixtures

All files in this directory are fully synthetic and must declare:

```json
{
  "synthetic": true,
  "containsRealUserData": false
}
```

`valid/` contains schema-valid scenarios whose digests, candidate references, JSON Pointer paths, state transitions, and arbitration chains must pass cross-field validation.

`invalid/` contains one intentional contract failure per fixture. Failures may be expressible through JSON Schema or through semantic invariants tested by `tests/test_collaboration_contracts.py`.

Never copy a real conversation into this directory, even after redaction. Never calculate fixture digests from private or sensitive source values.
