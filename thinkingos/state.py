"""Serializable, reusable ThinkingOS conversation state."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping

from .errors import ContractError


@dataclass
class ConversationState:
    current_skill: str | None = None
    current_goal: str | None = None
    collected_inputs: dict[str, Any] = field(default_factory=dict)
    pending_questions: list[str] = field(default_factory=list)
    next_skill: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "currentSkill": self.current_skill,
            "currentGoal": self.current_goal,
            "collectedInputs": dict(self.collected_inputs),
            "pendingQuestions": list(self.pending_questions),
            "nextSkill": self.next_skill,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ConversationState":
        inputs = data.get("collectedInputs", {})
        questions = data.get("pendingQuestions", [])
        if not isinstance(inputs, Mapping) or not isinstance(questions, list) or not all(isinstance(q, str) for q in questions):
            raise ContractError("invalid conversation state collections")
        for key in ("currentSkill", "currentGoal", "nextSkill"):
            if data.get(key) is not None and not isinstance(data[key], str):
                raise ContractError(f"{key} must be a string or null")
        return cls(data.get("currentSkill"), data.get("currentGoal"), dict(inputs), list(questions), data.get("nextSkill"))

    @classmethod
    def from_json(cls, value: str) -> "ConversationState":
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ContractError("conversation state is not valid JSON") from exc
        if not isinstance(data, Mapping):
            raise ContractError("conversation state must be a JSON object")
        return cls.from_mapping(data)

    def merge_inputs(self, values: Mapping[str, Any]) -> None:
        self.collected_inputs.update(values)
