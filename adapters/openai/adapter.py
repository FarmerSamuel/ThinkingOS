"""OpenAI Responses API payload mapping."""

from typing import Any, Mapping

from adapters.base import AdapterError, AdapterRequest, AdapterResponse, BaseAdapter, ProviderRequest


class OpenAIAdapter(BaseAdapter):
    provider = "openai"

    @property
    def capabilities(self) -> frozenset[str]:
        return frozenset({"structured-output", "conversation-state", "system-instructions"})

    def build_request(self, request: AdapterRequest, **options: Any) -> ProviderRequest:
        request.validate()
        payload: dict[str, Any] = {
            "model": self.require_model(options),
            "instructions": request.instructions,
            "input": self.encoded_context(request),
        }
        if request.output_schema is not None:
            payload["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "thinkingos_output",
                    "schema": dict(request.output_schema),
                    "strict": True,
                }
            }
        return ProviderRequest(self.provider, "responses.create", payload)

    def parse_response(self, payload: Mapping[str, Any]) -> AdapterResponse:
        text = payload.get("output_text")
        if text is None:
            for item in payload.get("output", []):
                if not isinstance(item, Mapping):
                    continue
                for content in item.get("content", []):
                    if isinstance(content, Mapping) and content.get("type") == "output_text":
                        text = content.get("text")
                        break
        if text is None:
            raise AdapterError("OpenAI response contains no output_text")
        metadata = {key: payload[key] for key in ("id", "model", "usage") if key in payload}
        return AdapterResponse(self.decode_json(text), self.provider, metadata)
