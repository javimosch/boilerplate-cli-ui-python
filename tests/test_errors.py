"""
Test error handling for agent-first CLI.
"""

import pytest
from src.errors import (
    CLIError,
    InvalidArgumentError,
    PermissionError,
    ResourceNotFoundError,
    ResourceConflictError,
    ConnectionTimeoutError,
    InternalError,
    EXIT_INVALID_ARGUMENT,
    EXIT_BAD_PERMISSIONS,
    EXIT_RESOURCE_NOT_FOUND,
    EXIT_RESOURCE_CONFLICT,
    EXIT_CONNECTION_TIMEOUT,
    EXIT_INTERNAL_ERROR
)


def test_cli_error_structure():
    """Test CLIError structure."""
    error = CLIError(
        code=85,
        error_type="test_error",
        message="Test error message",
        details={"key": "value"},
        recoverable=False,
        retry_after=None,
        suggestions=["Suggestion 1"]
    )
    
    assert error.code == 85
    assert error.error_type == "test_error"
    assert error.message == "Test error message"
    assert error.details == {"key": "value"}
    assert error.recoverable == False
    assert error.retry_after is None
    assert error.suggestions == ["Suggestion 1"]


def test_cli_error_to_dict():
    """Test CLIError to_dict conversion."""
    error = CLIError(
        code=85,
        error_type="test_error",
        message="Test error message",
        details={"key": "value"},
        recoverable=True,
        retry_after=5,
        suggestions=["Retry"]
    )
    
    result = error.to_dict()
    
    assert result["error"]["code"] == 85
    assert result["error"]["type"] == "test_error"
    assert result["error"]["message"] == "Test error message"
    assert result["error"]["details"] == {"key": "value"}
    assert result["error"]["recoverable"] == True
    assert result["error"]["retry_after"] == 5
    assert result["error"]["suggestions"] == ["Retry"]


def test_invalid_argument_error():
    """Test InvalidArgumentError."""
    error = InvalidArgumentError("Invalid port", details={"port": "invalid"})
    
    assert error.code == EXIT_INVALID_ARGUMENT
    assert error.error_type == "invalid_argument"
    assert error.message == "Invalid port"
    assert error.details == {"port": "invalid"}
    assert error.recoverable == False
    assert len(error.suggestions) > 0


def test_permission_error():
    """Test PermissionError."""
    error = PermissionError("Access denied", details={"file": "/etc/passwd"})
    
    assert error.code == EXIT_BAD_PERMISSIONS
    assert error.error_type == "permission_denied"
    assert error.message == "Access denied"
    assert error.recoverable == False


def test_resource_not_found_error():
    """Test ResourceNotFoundError."""
    error = ResourceNotFoundError("config file", "/path/to/config")
    
    assert error.code == EXIT_RESOURCE_NOT_FOUND
    assert error.error_type == "resource_not_found"
    assert "config file" in error.message
    assert "/path/to/config" in error.message
    assert error.details == {
        "resource_type": "config file",
        "resource_id": "/path/to/config"
    }
    assert error.recoverable == False


def test_resource_conflict_error():
    """Test ResourceConflictError."""
    error = ResourceConflictError("Resource already exists", details={"id": 123})
    
    assert error.code == EXIT_RESOURCE_CONFLICT
    assert error.error_type == "resource_conflict"
    assert error.recoverable == False


def test_connection_timeout_error():
    """Test ConnectionTimeoutError."""
    error = ConnectionTimeoutError("Connection timed out", retry_after=5)
    
    assert error.code == EXIT_CONNECTION_TIMEOUT
    assert error.error_type == "connection_timeout"
    assert error.recoverable == True
    assert error.retry_after == 5
    assert len(error.suggestions) > 0


def test_internal_error():
    """Test InternalError."""
    error = InternalError("Internal bug occurred", details={"trace": "..."})
    
    assert error.code == EXIT_INTERNAL_ERROR
    assert error.error_type == "internal_error"
    assert error.recoverable == False
    assert len(error.suggestions) > 0


def test_semantic_exit_codes():
    """Test semantic exit code ranges."""
    # User errors (80-89)
    assert 80 <= EXIT_INVALID_ARGUMENT <= 89
    assert 80 <= EXIT_BAD_PERMISSIONS <= 89
    
    # Resource errors (90-99)
    assert 90 <= EXIT_RESOURCE_NOT_FOUND <= 99
    assert 90 <= EXIT_RESOURCE_CONFLICT <= 99
    
    # Integration errors (100-109)
    assert 100 <= EXIT_CONNECTION_TIMEOUT <= 109
    
    # Software errors (110-119)
    assert 110 <= EXIT_INTERNAL_ERROR <= 119