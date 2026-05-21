"""
Utility functions for agent-first CLI.

Common helpers for logging, validation, etc.
"""

import sys
import os
from typing import Optional
from datetime import datetime


def check_python_version(min_version: tuple = (3, 10)) -> None:
    """Check Python version meets minimum requirement."""
    current = sys.version_info[:2]
    if current < min_version:
        print(f"Python {'.'.join(map(str, min_version))}+ required", file=sys.stderr)
        sys.exit(1)


def validate_port(port: int) -> bool:
    """Validate port number is in valid range."""
    return 1 <= port <= 65535


def validate_positive_int(value: int, name: str = "value") -> bool:
    """Validate value is positive integer."""
    return value > 0


def get_timestamp() -> str:
    """Get current UTC timestamp."""
    return datetime.utcnow().isoformat() + "Z"


def ensure_dir_exists(path: str) -> None:
    """Ensure directory exists, create if not."""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def file_exists(path: str) -> bool:
    """Check if file exists."""
    return os.path.exists(path)


def read_file(path: str) -> Optional[str]:
    """Read file content, return None if not exists."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading file {path}: {e}", file=sys.stderr)
        return None


def write_file(path: str, content: str) -> bool:
    """Write content to file."""
    try:
        ensure_dir_exists(path)
        with open(path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {path}: {e}", file=sys.stderr)
        return False


def get_executable_path() -> Optional[str]:
    """Get current executable path."""
    try:
        return sys.executable
    except Exception:
        return None