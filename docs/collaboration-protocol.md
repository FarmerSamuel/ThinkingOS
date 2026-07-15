# Multi-AI Collaboration Protocol

> **Lifecycle:** Draft · **Stability:** Experimental · **Protocol version:** `0.1.0-draft.1`

ThinkingOS defines a platform-independent, versioned contract for multi-AI collaboration and may provide stateless reference implementations. The project does not operate a central execution platform or retain user credentials or private conversation state.

This document is normative for the draft collaboration contract. Draft fields may change before release and are not covered by the stable v1 compatibility guarantee.

## Responsibilities

ThinkingOS owns:

- role, execution-envelope, arbitration, lineage, and conformance semantics;
- schema-valid interchange formats;
- evidence-based divergence classification;
- synthetic fixtures and deterministic contract tests.

The calling application owns:

- provider and model selection;
- network I/O, credentials, retry, rate-limit, privacy, and retention policy;
- scheduling candidate runs;
- storing or transmitting envelopes and records;
- obtaining required human approval.

Provider-specific transport remains in `adapters/`. Thinking logic remains in `core/` and `skills/`.

## Role and platform separation

A role describes cognitive responsibility, not a preferred provider. Standard roles are `analyst`, `critic`, `evidence-reviewer`, and `arbiter`; applications may declare additional roles without assigning them permanently to a platform.

Role rotation is optional at L1, useful as a diagnostic at L2, and required at least once during controlled L3 conformance. A conclusion that changes after a platform takes the same role must be examined for instruction, input, state, adapter, model, or contract differences before being treated as evidence.

## Execution envelope

Every candidate run produces a `collaboration-envelope` containing:

- session, run, level, actor, role, provider, and model identifiers;
- framework release, source commit, Skill identifier, and Skill version;
- base state version and digest;
- digests for compiled instructions, inputs, state, and the complete request identity;
- one schema-valid universal ThinkingOS output;
- creation time and draft lifecycle metadata.

The `instructionsDigest` covers the final compiled `AdapterRequest.instructions` value immediately before provider mapping. It does not cover only a source template or role label.

The collaboration envelope wraps the universal output. It never adds collaboration fields to `schemas/output.schema.json`.

## Digest profile

Draft collaboration digests use:

- algorithm: SHA-256;
- canonicalization: RFC 8785 JSON Canonicalization Scheme (JCS);
- representation: `sha256:` followed by 64 lowercase hexadecimal characters;
- string encoding: UTF-8 after canonicalization.

`instructionsDigest`, `inputsDigest`, and `stateDigest` are calculated independently so divergence diagnosis can isolate the changed component. `caseDigest` covers framework identity, Skill identity, input digest, and state digest so different roles can be grouped against one case. `requestDigest` additionally covers role and instruction digest, identifying the complete execution request.

Digests establish equality and continuity. They are not signatures, identity proofs, confidentiality controls, or evidence that the source content is true. Low-entropy sensitive values can remain guessable even when hashed; hosts must minimize sensitive inputs rather than relying on digests for privacy.

## Single writer and state lineage

AI actors never directly mutate committed conversation state. They return candidate envelopes based on one declared base state. The arbiter is the only writer and applies accepted findings sequentially.

Each `sessionId` has one committed state lineage. Multiple candidate runs may share a session, `baseStateVersion`, and `baseStateDigest`. They are parallel proposals, not state forks.

If arbitration must preserve more than one incompatible committed successor, create a child session with `parentSessionId` and `forkedFromStateVersion`. Never create two committed successors in one session.

An envelope based on an older state version or different base digest is stale and must be rejected or rerun before merging.

## Arbitration record

An arbitration record cites candidate `runId` values and assigns each one:

- `accepted`, `rejected`, or `partial` disposition;
- a concise evidence-based reason;
- JSON Pointer `acceptedPaths` when disposition is `partial`.

Partial paths are evaluated against the immutable candidate output and must exist, be non-overlapping, and identify the exact accepted values.

The record also captures divergence classification, evidence references, Never Rule violations, rubric findings, arbiter identity and type, human approval, and the resulting state version and digest. L3 arbitration requires explicit human approval.

## State and record chains

Each arbitration transition must satisfy:

```text
resultStateVersion = baseStateVersion + 1
next.baseStateDigest = previous.resultStateDigest
next.previousRecordDigest = previous.recordDigest
```

For the first record in a session, `previousRecordDigest` is `null`. To calculate `recordDigest`:

1. Copy the complete arbitration record.
2. Remove the `recordDigest` property entirely.
3. Canonicalize the remaining object with RFC 8785.
4. Hash the canonical UTF-8 bytes with SHA-256.
5. Store the lowercase result with the `sha256:` prefix.

The digest chain provides continuity and tamper evidence relative to a trusted anchor; it does not provide identity, authenticity, or non-repudiation by itself. A protected Git branch and verified signed release tag may anchor committed records, subject to repository and signing-key governance. Runtime records are unanchored until committed or otherwise secured by the host.

## Divergence diagnosis

Before changing a Skill contract, diagnose a repeatable disagreement in this order:

1. Compare framework, Skill, and source-commit identity.
2. Compare instruction, input, state, and request digests.
3. Reject stale base state and schema-invalid output.
4. Check adapter mapping and fail-closed parsing.
5. Repeat controlled runs to estimate stochastic variance.
6. Classify the remaining divergence.

Supported classifications include input, state, instruction, or version mismatch; adapter or schema nonconformance; stochastic variance; model nonconformance; contract ambiguity; and unresolved divergence.

Each classification has a different improvement path:

- adapter nonconformance becomes an adapter contract test;
- schema nonconformance becomes a parser or validation test;
- model variance informs role and provider configuration;
- confirmed contract ambiguity becomes a Skill or collaboration regression case.

Disagreement is not automatically evidence that the Skill contract is ambiguous.

## Synthetic fixtures

Repository fixtures must be fully synthetic and declare:

```json
{
  "synthetic": true,
  "containsRealUserData": false
}
```

No fixture content or digest may be derived from a real user conversation, private state, credential, or sensitive source. Schema validation confirms the declaration, while contribution review remains responsible for confirming provenance.

## Draft schema lifecycle

Draft schemas use a versioned canonical `$id`, `x-thinkingos-lifecycle: draft`, and `x-thinkingos-stability: experimental`. Draft identifiers may change before release and must not be treated as stable dependencies.

After controlled conformance and review, released schemas receive a stable semantic versioned `$id`. A separate unversioned URL may resolve to the latest compatible released version, but durable records must retain the exact versioned identifier used for validation.

## Conformance

Contract conformance uses synthetic positive and negative fixtures plus cross-field tests. Before release, mapping must be exercised through at least one provider-API adapter with structured-output capability and the MCP adapter. Controlled live interoperability is a release gate; production experience informs later improvements without placing private conversations in the repository.

Reference coordinators remain non-normative, stateless, and subordinate to this contract.
