"""SDK-specific error hierarchy."""


class ThinkingOSError(Exception):
    """Base class for actionable ThinkingOS SDK failures."""


class RegistryError(ThinkingOSError):
    """Raised when registry data is malformed or inconsistent."""


class DependencyError(RegistryError):
    """Raised when skill dependency relationships are invalid."""


class ContractError(ThinkingOSError):
    """Raised when a skill or state violates its published contract."""
