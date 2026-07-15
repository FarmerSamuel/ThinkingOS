"""Gemini GenerateContent API payload mapping."""

from typing import Any, Mapping

from adapters.base import AdapterError, AdapterRequest, AdapterResponse, BaseAdapter, ProviderRequest


class GeminiAdapter(BaseAdapter):
    provider = "gemini"

    @property
    def capabilities(self) -> frozenset[str]:
        return frozenset({"structured-output", "conversation-state", "system-instructions"})

    def build_request(self, request: AdapterRequest, **options: Any) -> ProviderRequest:
        request.validate()
        model = self.require_model(options)
        payload: dict[str, Any] = {
            "systemInstruction": {"parts": [{"text": request.instructions}]},
            "contents": [{"role": "user", "parts": [{"text": self.encoded_context(request)}]}],
        }
        if request.output_schema is not None:
            payload["generationConfig"] = {
                "responseMimeType": "application/json",
                "responseJsonSchema": dict(request.output_schema),
            }
        return ProviderRequest(self.provider, f"models/{model}:generateContent", payload)

    def parse_response(self, payload: Mapping[str, Any]) -> AdapterResponse:
        candidates = payload.get("candidates", [])
        if not candidates:
            reason = payload.get("promptFeedback", {}).get("blockReason", "unknown")
            raise AdapterError(f"Gemini response contains no candidates (reason: {reason})")
        first = candidates[0]
        parts = first.get("content", {}).get("parts", []) if isinstance(first, Mapping) else []
        text = "".join(str(part.get("text", "")) for part in parts if isinstance(part, Mapping))
        if not text:
            raise AdapterError("Gemini candidate contains no text")
        metadata = {key: payload[key] for key in ("responseId", "modelVersion", "usageMetadata") if key in payload}
        return AdapterResponse(self.decode_json(text), self.provider, metadata)
