"""Contract and cross-field tests for the draft collaboration protocol."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "collaboration"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_fixture_domain(value: Any) -> None:
    """Limit fixture digest sources to the JCS-equivalent stdlib JSON subset."""
    if isinstance(value, float):
        raise AssertionError("collaboration fixtures must not use floating-point digest sources")
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise AssertionError("JSON object keys must be strings")
            assert_fixture_domain(item)
    elif isinstance(value, list):
        for item in value:
            assert_fixture_domain(item)


def canonical_bytes(value: Any) -> bytes:
    # The synthetic fixtures use only strings, integers, booleans, null, arrays,
    # and objects. For this restricted domain, these settings produce RFC 8785
    # bytes. Runtime implementations must use a complete RFC 8785 implementation.
    assert_fixture_domain(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def record_digest(record: dict[str, Any]) -> str:
    source = copy.deepcopy(record)
    source.pop("recordDigest", None)
    return digest(source)


def resolve_pointer(document: Any, pointer: str) -> Any:
    current = document
    for token in pointer.split("/")[1:]:
        key = token.replace("~1", "/").replace("~0", "~")
        current = current[int(key)] if isinstance(current, list) else current[key]
    return current


class CollaborationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schemas = [load_json(path) for path in sorted((ROOT / "schemas").glob("*.json"))]
        registry = Registry()
        for schema in schemas:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        cls.envelope_validator = Draft202012Validator(
            next(schema for schema in schemas if schema["title"] == "ThinkingOS Collaboration Envelope"),
            registry=registry,
            format_checker=FormatChecker(),
        )
        cls.arbitration_validator = Draft202012Validator(
            next(schema for schema in schemas if schema["title"] == "ThinkingOS Arbitration Record"),
            registry=registry,
            format_checker=FormatChecker(),
        )
        cls.valid_fixture = load_json(FIXTURES / "valid" / "l2-synthetic-session.json")

    def assert_synthetic(self, fixture: dict[str, Any]) -> None:
        metadata = fixture.get("fixtureMetadata", {})
        self.assertIs(metadata.get("synthetic"), True)
        self.assertIs(metadata.get("containsRealUserData"), False)
        self.assertTrue(metadata.get("purpose"))

    def test_valid_fixture_provenance(self) -> None:
        self.assert_synthetic(self.valid_fixture)

    def test_valid_documents_conform_to_schemas(self) -> None:
        documents = self.valid_fixture["documents"]
        for envelope in documents["envelopes"]:
            self.assertEqual(list(self.envelope_validator.iter_errors(envelope)), [])
        for record in documents["arbitrationRecords"]:
            self.assertEqual(list(self.arbitration_validator.iter_errors(record)), [])

    def test_component_case_and_request_digests(self) -> None:
        fixture = self.valid_fixture
        sources = fixture["digestSources"]
        for envelope in fixture["documents"]["envelopes"]:
            run_id = envelope["runId"]
            role = envelope["actor"]["role"]
            state = sources["states"][str(envelope["baseState"]["version"])]
            digests = envelope["digests"]
            instructions_digest = digest(sources["instructions"][run_id])
            inputs_digest = digest(sources["inputs"])
            state_digest = digest(state)
            case_digest = digest({
                "framework": sources["framework"],
                "skill": sources["skill"],
                "inputsDigest": inputs_digest,
                "stateDigest": state_digest,
            })
            request_digest = digest({
                "framework": sources["framework"],
                "skill": sources["skill"],
                "role": role,
                "instructionsDigest": instructions_digest,
                "inputsDigest": inputs_digest,
                "stateDigest": state_digest,
            })
            self.assertEqual(digests["instructionsDigest"], instructions_digest)
            self.assertEqual(digests["inputsDigest"], inputs_digest)
            self.assertEqual(digests["stateDigest"], state_digest)
            self.assertEqual(digests["caseDigest"], case_digest)
            self.assertEqual(digests["requestDigest"], request_digest)
            self.assertEqual(envelope["baseState"]["digest"], state_digest)

    def test_arbitration_state_and_record_chains(self) -> None:
        fixture = self.valid_fixture
        records = fixture["documents"]["arbitrationRecords"]
        state_sources = fixture["digestSources"]["states"]
        previous = None
        committed_successors: set[tuple[str, int]] = set()
        for record in records:
            base = record["baseState"]
            result = record["resultState"]
            self.assertEqual(result["version"], base["version"] + 1)
            self.assertEqual(base["digest"], digest(state_sources[str(base["version"])]))
            self.assertEqual(result["digest"], digest(state_sources[str(result["version"])]))
            self.assertEqual(record["recordDigest"], record_digest(record))
            key = (record["sessionId"], base["version"])
            self.assertNotIn(key, committed_successors)
            committed_successors.add(key)
            if previous is None:
                self.assertIsNone(record["previousRecordDigest"])
            else:
                self.assertEqual(record["previousRecordDigest"], previous["recordDigest"])
                self.assertEqual(base, previous["resultState"])
            previous = record

    def test_candidate_references_and_partial_paths(self) -> None:
        envelopes = {item["runId"]: item for item in self.valid_fixture["documents"]["envelopes"]}
        for record in self.valid_fixture["documents"]["arbitrationRecords"]:
            for decision in record["candidateDecisions"]:
                self.assertIn(decision["runId"], envelopes)
                self.assertEqual(envelopes[decision["runId"]]["session"]["sessionId"], record["sessionId"])
                self.assertEqual(envelopes[decision["runId"]]["baseState"], record["baseState"])
                paths = decision.get("acceptedPaths", [])
                for path in paths:
                    self.assertIsNotNone(resolve_pointer(envelopes[decision["runId"]]["output"], path))
                for index, path in enumerate(paths):
                    for other in paths[index + 1:]:
                        self.assertFalse(path.startswith(other + "/") or other.startswith(path + "/"))

    def test_parallel_roles_share_case_not_request_identity(self) -> None:
        first, second = self.valid_fixture["documents"]["envelopes"][:2]
        self.assertEqual(first["digests"]["caseDigest"], second["digests"]["caseDigest"])
        self.assertNotEqual(first["digests"]["requestDigest"], second["digests"]["requestDigest"])

    def test_invalid_fixtures_fail_for_declared_reason(self) -> None:
        for path in sorted((FIXTURES / "invalid").glob("*.json")):
            with self.subTest(path=path.name):
                fixture = load_json(path)
                reason = fixture["expectedFailure"]
                if reason == "fixture-provenance":
                    with self.assertRaises(AssertionError):
                        self.assert_synthetic(fixture)
                    continue
                document = fixture["document"]
                validator = self.envelope_validator if fixture["documentType"] == "collaboration-envelope" else self.arbitration_validator
                errors = list(validator.iter_errors(document))
                if reason == "schema":
                    self.assertTrue(errors)
                elif reason == "state-digest-mismatch":
                    self.assertFalse(errors)
                    self.assertNotEqual(document["baseState"]["digest"], document["digests"]["stateDigest"])
                elif reason == "record-digest-mismatch":
                    self.assertFalse(errors)
                    self.assertNotEqual(document["recordDigest"], record_digest(document))
                elif reason == "state-version-transition":
                    self.assertFalse(errors)
                    self.assertNotEqual(document["resultState"]["version"], document["baseState"]["version"] + 1)
                    self.assertEqual(document["recordDigest"], record_digest(document))
                elif reason == "unknown-run-reference":
                    self.assertFalse(errors)
                    known = set(fixture["knownRunIds"])
                    cited = {item["runId"] for item in document["candidateDecisions"]}
                    self.assertFalse(cited <= known)
                    self.assertEqual(document["recordDigest"], record_digest(document))
                else:
                    self.fail(f"unknown expected failure: {reason}")


if __name__ == "__main__":
    unittest.main()
