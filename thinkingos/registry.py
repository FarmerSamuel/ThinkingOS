"""Skill registry discovery and directed-graph traversal."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml

from .errors import DependencyError, RegistryError


@dataclass(frozen=True)
class SkillRecord:
    id: str
    display_name: str
    category: str
    version: str
    status: str
    dependencies: tuple[str, ...]
    produces: tuple[str, ...]
    consumes: tuple[str, ...]

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "SkillRecord":
        required = {"id", "displayName", "category", "version", "status", "dependencies", "produces", "consumes"}
        missing = required - set(data)
        if missing:
            raise RegistryError(f"skill record missing fields: {sorted(missing)}")
        try:
            return cls(
                id=str(data["id"]),
                display_name=str(data["displayName"]),
                category=str(data["category"]),
                version=str(data["version"]),
                status=str(data["status"]),
                dependencies=tuple(data["dependencies"] or ()),
                produces=tuple(data["produces"] or ()),
                consumes=tuple(data["consumes"] or ()),
            )
        except TypeError as exc:
            raise RegistryError("registry list fields must be arrays") from exc


class SkillRegistry:
    """Immutable view over registered skills and their dependency graph."""

    def __init__(self, records: Iterable[SkillRecord]) -> None:
        items = tuple(records)
        self._records = {record.id: record for record in items}
        if len(self._records) != len(items):
            raise RegistryError("registry contains duplicate skill ids")
        self._validate_graph()

    @classmethod
    def from_file(cls, path: str | Path) -> "SkillRegistry":
        source = Path(path)
        try:
            data = yaml.safe_load(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise RegistryError(f"cannot load registry {source}: {exc}") from exc
        if not isinstance(data, Mapping) or not isinstance(data.get("skills"), list):
            raise RegistryError("registry root must contain a skills array")
        return cls(SkillRecord.from_mapping(item) for item in data["skills"])

    def __len__(self) -> int:
        return len(self._records)

    def __iter__(self):
        return iter(self._records.values())

    def get(self, skill_id: str) -> SkillRecord:
        try:
            return self._records[skill_id]
        except KeyError as exc:
            raise RegistryError(f"unknown skill: {skill_id}") from exc

    def prerequisites(self, skill_id: str, *, transitive: bool = False) -> tuple[SkillRecord, ...]:
        record = self.get(skill_id)
        ids = set(record.dependencies)
        if transitive:
            queue = list(record.dependencies)
            while queue:
                current = queue.pop()
                for dependency in self.get(current).dependencies:
                    if dependency not in ids:
                        ids.add(dependency)
                        queue.append(dependency)
        order = self.topological_order()
        return tuple(self.get(item) for item in order if item in ids)

    def successors(self, skill_id: str) -> tuple[SkillRecord, ...]:
        self.get(skill_id)
        return tuple(record for record in self if skill_id in record.dependencies)

    def available(self, completed: Iterable[str]) -> tuple[SkillRecord, ...]:
        completed_ids = set(completed)
        unknown = completed_ids - set(self._records)
        if unknown:
            raise RegistryError(f"completed set contains unknown skills: {sorted(unknown)}")
        return tuple(
            self.get(skill_id)
            for skill_id in self.topological_order()
            if skill_id not in completed_ids and set(self.get(skill_id).dependencies) <= completed_ids
        )

    def topological_order(self) -> tuple[str, ...]:
        incoming = {skill_id: set(record.dependencies) for skill_id, record in self._records.items()}
        ready = sorted(skill_id for skill_id, deps in incoming.items() if not deps)
        order: list[str] = []
        while ready:
            current = ready.pop(0)
            order.append(current)
            for skill_id in sorted(incoming):
                if current in incoming[skill_id]:
                    incoming[skill_id].remove(current)
                    if not incoming[skill_id] and skill_id not in order and skill_id not in ready:
                        ready.append(skill_id)
                        ready.sort()
        if len(order) != len(self._records):
            raise DependencyError("registry dependency graph contains a cycle")
        return tuple(order)

    def _validate_graph(self) -> None:
        known = set(self._records)
        for record in self:
            unknown = set(record.dependencies) - known
            if unknown:
                raise DependencyError(f"{record.id} has unknown dependencies: {sorted(unknown)}")
            if record.id in record.dependencies:
                raise DependencyError(f"{record.id} depends on itself")
        self.topological_order()
