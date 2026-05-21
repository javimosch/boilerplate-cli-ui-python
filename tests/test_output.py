"""
Test output formatting for agent-first CLI.
"""

import json
import sys
from io import StringIO
import pytest

from src.output import OutputFormatter, format_help_json, OUTPUT_VERSION


def test_output_formatter_json_mode():
    """Test JSON output format."""
    formatter = OutputFormatter(human_mode=False, no_color=True)
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        data = {"result": "success", "value": 42}
        formatter.output(data, 0)
        output = sys.stdout.getvalue()
        
        # Parse JSON
        result = json.loads(output)
        
        assert result["version"] == OUTPUT_VERSION
        assert result["data"] == data
        assert "timestamp" in result
    finally:
        sys.stdout = old_stdout


def test_output_formatter_human_mode():
    """Test human output format."""
    formatter = OutputFormatter(human_mode=True, no_color=True)
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        data = {"result": "success", "value": 42}
        formatter.output(data, 0)
        output = sys.stdout.getvalue()
        
        # Should not be JSON
        assert "result: success" in output
        assert "value: 42" in output
    finally:
        sys.stdout = old_stdout


def test_output_error_json():
    """Test error output in JSON format."""
    formatter = OutputFormatter(human_mode=False, no_color=True)
    
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = StringIO()
    
    try:
        error_dict = {
            "error": {
                "code": 85,
                "type": "invalid_argument",
                "message": "Invalid input",
                "details": {},
                "recoverable": False,
                "retry_after": None,
                "suggestions": ["Check input"]
            }
        }
        formatter.output_error(error_dict, 85)
        output = sys.stderr.getvalue()
        
        # Parse JSON
        result = json.loads(output)
        
        assert result["error"]["code"] == 85
        assert result["error"]["type"] == "invalid_argument"
    finally:
        sys.stderr = old_stderr


def test_format_help_json():
    """Test help JSON formatting."""
    commands = {
        "test": {
            "description": "Test command",
            "flags": {"--flag": "Test flag"}
        }
    }
    
    result = format_help_json(
        version="1.0.0",
        commands=commands,
        output_formats=["json", "human"],
        exit_codes={"0": "success", "85": "invalid_argument"}
    )
    
    assert result["version"] == "1.0.0"
    assert result["commands"]["test"]["description"] == "Test command"
    assert "json" in result["output_formats"]
    assert result["exit_codes"]["0"] == "success"


def test_no_color_env_var():
    """Test NO_COLOR environment variable."""
    import os
    
    # Set NO_COLOR
    os.environ['NO_COLOR'] = '1'
    formatter = OutputFormatter(human_mode=False)
    assert formatter.no_color == True
    
    # Unset NO_COLOR
    del os.environ['NO_COLOR']
    formatter = OutputFormatter(human_mode=False)
    assert formatter.no_color == True  # Default is True