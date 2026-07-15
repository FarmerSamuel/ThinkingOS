"""Claude Messages API payload mapping."""

from typing import Any, Mapping

from adapters.base import AdapterError, AdapterRequest, AdapterResponse, BaseAdapter, ProviderRequest


class ClaudeAdapter(BaseAdapter):
    provider = "claude"

    @property
    def capabilities(self) -> frozenset[str]:
        return frozenset({"conversation-state", "system-instructions"})

    def build_request(self, request: AdapterRequest, **options: Any) -> ProviderRequest:
        request.validate()
        max_tokens = options.get("max_tokens", 4096)
        if not isinstance(max_tokens, int) or max_tokens < 1:
            raise AdapterError("max_tokens must be a positive integer")
        system = request.instructions
        if request.output_schema is not None:
            system += "\nReturn only a JSON object conforming to the supplied output schema."
        context: dict[str, Any] = request.context()
        if request.output_schema is not None:
            context["outputSchema"] = dict(request.output_schema)
        payload = {
            "model": self.require_model(options),
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": self.decode_for_message(context)}],
        }
        return ProviderRequest(self.provider, "messages.create", payload)

    @staticmethod
    def decode_for_message(context: Mapping[str, Any]) -> str:
        import json

        return json.dumps(context, ensure_ascii=False, separators=(",", ":"))

    def parse_response(self, payload: Mapping[str, Any]) -> AdapterResponse:
        parts = payload.get("content", [])
        text = "".join(
            str(part.get("text", ""))
            for part in parts
            if isinstance(part, Mapping) and part.get("type") == "text"
        )
        if not text:
            raise AdapterError("Claude response contains no text content")
        metadata = {key: payload[key] for key in ("id", "model", "usage", "stop_reason") if key in payload}
        return AdapterResponse(self.decode_json(text), self.provider, metadata)
