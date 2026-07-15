"""Stable, dependency-free contracts shared by all ThinkingOS adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
from typing import Any, Mapping


JSON = dict[str, Any]


class AdapterError(ValueError):
    """Raised when an adapter cannot safely map or parse a payload."""


@dataclass(frozen=True)
class AdapterRequest:
    """Provider-neutral request to execute one ThinkingOS skill."""

    skill_id: str
    instructions: str
    inputs: Mapping[str, Any]
    state: Mapping[str, Any] = field(default_factory=dict)
    output_schema: Mapping[str, Any] | None = None

    def validate(self) -> None:
        if not self.skill_id.strip():
            raise AdapterError("skill_id must not be empty")
        if not self.instructions.strip():
            raise AdapterError("instructions must not be empty")
        if not isinstance(self.inputs, Mapping):
            raise AdapterError("inputs must be an object")
        if not isinstance(self.state, Mapping):
            raise AdapterError("state must be an object")
        if self.output_schema is not None and not isinstance(self.output_schema, Mapping):
            raise AdapterError("output_schema must be an object")

    def context(self) -> JSON:
        return {
            "skillId": self.skill_id,
            "inputs": dict(self.inputs),
            "conversationState": dict(self.state),
        }


@dataclass(frozen=True)
class ProviderRequest:
    """Serializable payload plus non-secret routing metadata."""

    provider: str
    operation: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class AdapterResponse:
    """Normalized result returned to the ThinkingOS engine."""

    output: Mapping[str, Any]
    provider: str
    provider_metadata: Mapping[str, Any] = field(default_factory=dict)


class BaseAdapter(ABC):
    """Interface implemented by model and host adapters."""

    provider: str

    @property
    @abstractmethod
    def capabilities(self) -> frozenset[str]:
        """Return stable capability labels supported by the mapping."""

    @abstractmethod
    def build_request(self, request: AdapterRequest, **options: Any) -> ProviderRequest:
        """Map a neutral request into a provider payload without sending it."""

    @abstractmethod
    def parse_response(self, payload: Mapping[str, Any]) -> AdapterResponse:
        """Normalize a provider response or raise AdapterError."""

    @staticmethod
    def require_model(options: Mapping[str, Any]) -> str:
        model = options.get("model")
        if not isinstance(model, str) or not model.strip():
            raise AdapterError("model is required and must be a non-empty string")
        return model

    @staticmethod
    def decode_json(value: Any) -> JSON:
        if isinstance(value, Mapping):
            return dict(value)
        if not isinstance(value, str) or not value.strip():
            raise AdapterError("provider returned no structured output")
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            raise AdapterError("provider output is not valid JSON") from exc
        if not isinstance(decoded, dict):
            raise AdapterError("provider output must be a JSON object")
        return decoded

    @staticmethod
    def encoded_context(request: AdapterRequest) -> str:
        return json.dumps(request.context(), ensure_ascii=False, separators=(",", ":"))
