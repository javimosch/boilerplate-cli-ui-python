"""
Error definitions and handling for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- Semantic exit codes (80-119 for specific error types)
- Structured error output with recovery hints
- Error types for agent decision-making
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass


# Semantic exit codes following AGENTS_FRIENDLY_TOOLS.md
EXIT_SUCCESS = 0
EXIT_GENERIC_FAILURE = 1  # Backward compatibility

# User errors (80-89)
EXIT_INVALID_ARGUMENT = 85
EXIT_BAD_PERMISSIONS = 86
EXIT_VALIDATION_ERROR = 87

# Resource errors (90-99)
EXIT_RESOURCE_NOT_FOUND = 92
EXIT_RESOURCE_ALREADY_EXISTS = 93
EXIT_RESOURCE_CONFLICT = 94

# Integration errors (100-109)
EXIT_CONNECTION_TIMEOUT = 105
EXIT_API_UNAVAILABLE = 106
EXIT_AUTH_FAILED = 107

# Software errors (110-119)
EXIT_INTERNAL_ERROR = 110
EXIT_PANIC = 111


@dataclass
class ErrorDetails:
    """Structured error details for agent consumption."""
    code: int
    type: str
    message: str
    details: Dict[str, Any]
    recoverable: bool
    retry_after: Optional[int] = None
    suggestions: Optional[list[str]] = None


class CLIError(Exception):
    """Base exception for CLI errors with semantic exit codes."""
    
    def __init__(
        self,
        code: int,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        recoverable: bool = False,
        retry_after: Optional[int] = None,
        suggestions: Optional[list[str]] = None
    ):
        self.code = code
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        self.recoverable = recoverable
        self.retry_after = retry_after
        self.suggestions = suggestions or []
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to structured dictionary for JSON output."""
        return {
            "error": {
                "code": self.code,
                "type": self.error_type,
                "message": self.message,
                "details": self.details,
                "recoverable": self.recoverable,
                "retry_after": self.retry_after,
                "suggestions": self.suggestions
            }
        }


class InvalidArgumentError(CLIError):
    """Invalid argument or flag provided by user."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=EXIT_INVALID_ARGUMENT,
            error_type="invalid_argument",
            message=message,
            details=details,
            recoverable=False,
            suggestions=["Check command syntax", "Use --help-json for usage"]
        )


class PermissionError(CLIError):
    """Insufficient permissions for operation."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=EXIT_BAD_PERMISSIONS,
            error_type="permission_denied",
            message=message,
            details=details,
            recoverable=False,
            suggestions=["Check file permissions", "Run with appropriate privileges"]
        )


class ResourceNotFoundError(CLIError):
    """Requested resource not found."""
    
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            code=EXIT_RESOURCE_NOT_FOUND,
            error_type="resource_not_found",
            message=f"{resource_type} '{resource_id}' not found",
            details={"resource_type": resource_type, "resource_id": resource_id},
            recoverable=False,
            suggestions=[f"Verify {resource_type} exists", f"Check {resource_type} ID"]
        )


class ResourceConflictError(CLIError):
    """Resource conflict (already exists, in use, etc.)."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=EXIT_RESOURCE_CONFLICT,
            error_type="resource_conflict",
            message=message,
            details=details,
            recoverable=False,
            suggestions=["Check resource state", "Use different identifier"]
        )


class ConnectionTimeoutError(CLIError):
    """Connection or timeout error."""
    
    def __init__(self, message: str, retry_after: int = 2):
        super().__init__(
            code=EXIT_CONNECTION_TIMEOUT,
            error_type="connection_timeout",
            message=message,
            recoverable=True,
            retry_after=retry_after,
            suggestions=["Check network connectivity", "Retry with backoff"]
        )


class InternalError(CLIError):
    """Internal software error or bug."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=EXIT_INTERNAL_ERROR,
            error_type="internal_error",
            message=message,
            details=details,
            recoverable=False,
            suggestions=["Report bug", "Check logs for details"]
        )