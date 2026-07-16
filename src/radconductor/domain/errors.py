class RadConductorError(Exception):
    """Base exception for RadConductor."""


class ToolExecutionError(RadConductorError):
    """Raised when a tool cannot complete its operation."""


class ToolRegistrationError(RadConductorError):
    """Raised when a tool cannot be registered."""


class ToolNotFoundError(RadConductorError):
    """Raised when a requested tool is not registered."""


class InvalidStudyError(RadConductorError):
    """Raised when an imaging study is missing or invalid."""


class PermissionDeniedError(RadConductorError):
    """Raised when a requested operation is not authorized."""