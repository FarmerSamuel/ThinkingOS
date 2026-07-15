import json
from pathlib import Path
import tempfile
import unittest

from thinkingos import ContractError, ConversationState, DependencyError, RegistryError, SkillLoader, SkillRecord, SkillRegistry


ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SkillRegistry.from_file(ROOT / "skills" / "registry.yaml")

    def test_loads_all_registered_skills(self) -> None:
        self.assertEqual(len(self.registry), 13)

    def test_topological_order_places_dependencies_first(self) -> None:
        order = self.registry.topological_order()
        positions = {skill_id: index for index, skill_id in enumerate(order)}
        for record in self.registry:
            for dependency in record.dependencies:
                self.assertLess(positions[dependency], positions[record.id])

    def test_transitive_prerequisites(self) -> None:
        prerequisites = {record.id for record in self.registry.prerequisites("emergence", transitive=True)}
        self.assertTrue({"complexity", "boundary", "right-problem", "make-association"} <= prerequisites)

    def test_available_skills(self) -> None:
        available = {record.id for record in self.registry.available([])}
        self.assertEqual(available, {"right-problem"})

    def test_rejects_unknown_completed_skill(self) -> None:
        with self.assertRaises(RegistryError):
            self.registry.available(["missing-skill"])

    def test_rejects_cycle(self) -> None:
        one = SkillRecord("one", "One", "test", "1.0.0", "released", ("two",), (), ())
        two = SkillRecord("two", "Two", "test", "1.0.0", "released", ("one",), (), ())
        with self.assertRaises(DependencyError):
            SkillRegistry([one, two])


class SkillLoaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.loader = SkillLoader(ROOT / "skills", ROOT / "schemas" / "skill.schema.json")

    def test_discovers_every_package(self) -> None:
        self.assertEqual(len(self.loader.discover()), 13)

    def test_loads_schema_conforming_skill(self) -> None:
        skill = self.loader.load("right-problem")
        self.assertEqual(skill.id, "right-problem")
        self.assertIn("constraints", skill.next_skills)

    def test_rejects_path_traversal(self) -> None:
        with self.assertRaises(ContractError):
            self.loader.load("../schemas")


class ConversationStateTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        state = ConversationState("right-problem", "Ship", {"goal": "Ship"}, ["By when?"], "constraints")
        self.assertEqual(ConversationState.from_json(state.to_json()).to_dict(), state.to_dict())

    def test_merge_inputs_preserves_existing_context(self) -> None:
        state = ConversationState(collected_inputs={"goal": "Ship"})
        state.merge_inputs({"budget": 100})
        self.assertEqual(state.collected_inputs, {"goal": "Ship", "budget": 100})

    def test_rejects_invalid_state_shape(self) -> None:
        with self.assertRaises(ContractError):
            ConversationState.from_mapping({"pendingQuestions": "not-a-list"})


if __name__ == "__main__":
    unittest.main()
