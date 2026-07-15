"""Provider-neutral integration contracts for ThinkingOS."""

from .base import (
    AdapterError,
    AdapterRequest,
    AdapterResponse,
    BaseAdapter,
    ProviderRequest,
)

__all__ = [
    "AdapterError",
    "AdapterRequest",
    "AdapterResponse",
    "BaseAdapter",
    "ProviderRequest",
]
