"""Loading and validation for versioned ThinkingOS skill packages."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .errors import ContractError


@dataclass(frozen=True)
class SkillDefinition:
    id: str
    version: str
    data: Mapping[str, Any]
    package_path: Path

    @property
    def next_skills(self) -> tuple[str, ...]:
        return tuple(item["skill"] for item in self.data.get("nextSkill", []) if isinstance(item, Mapping) and "skill" in item)


class SkillLoader:
    """Loads skill.json packages and validates the official JSON Schema."""

    def __init__(self, skills_path: str | Path, schema_path: str | Path) -> None:
        self.skills_path = Path(skills_path)
        self.schema_path = Path(schema_path)
        try:
            self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(self.schema)
        except (OSError, UnicodeError, json.JSONDecodeError, SchemaError) as exc:
            raise ContractError(f"cannot load skill schema: {exc}") from exc
        self.validator = Draft202012Validator(self.schema)

    def load(self, skill_id: str) -> SkillDefinition:
        if not skill_id or "/" in skill_id or "\\" in skill_id or skill_id in {".", ".."}:
            raise ContractError("invalid skill id")
        package_path = self.skills_path / skill_id
        source = package_path / "skill.json"
        try:
            data = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ContractError(f"cannot load {skill_id}: {exc}") from exc
        violations = sorted(self.validator.iter_errors(data), key=lambda error: tuple(str(p) for p in error.path))
        if violations:
            first = violations[0]
            location = ".".join(str(part) for part in first.path) or "<root>"
            raise ContractError(f"{skill_id} violates skill schema at {location}: {first.message}")
        if data.get("name") != skill_id:
            raise ContractError(f"{skill_id} package name does not match directory")
        return SkillDefinition(skill_id, data["version"], data, package_path)

    def discover(self) -> tuple[str, ...]:
        if not self.skills_path.is_dir():
            raise ContractError(f"skills path does not exist: {self.skills_path}")
        return tuple(sorted(path.name for path in self.skills_path.iterdir() if (path / "skill.json").is_file()))
