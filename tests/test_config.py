"""
Test configuration management for agent-first CLI.
"""

import os
import pytest
from src.config import Config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    
    assert config.port == 8080
    assert config.host == "127.0.0.1"
    assert config.log_level == "INFO"
    assert config.no_color == True
    assert config.no_interactive == False


def test_config_env_override():
    """Test environment variable override."""
    os.environ['BOILERPLATE_PORT'] = "3000"
    os.environ['BOILERPLATE_HOST'] = "0.0.0.0"
    os.environ['BOILERPLATE_LOG_LEVEL'] = "DEBUG"
    os.environ['BOILERPLATE_NO_INTERACTIVE'] = "1"
    
    try:
        config = Config()
        
        assert config.port == 3000
        assert config.host == "0.0.0.0"
        assert config.log_level == "DEBUG"
        assert config.no_interactive == True
    finally:
        # Clean up
        del os.environ['BOILERPLATE_PORT']
        del os.environ['BOILERPLATE_HOST']
        del os.environ['BOILERPLATE_LOG_LEVEL']
        del os.environ['BOILERPLATE_NO_INTERACTIVE']


def test_config_no_color_env():
    """Test NO_COLOR environment variable."""
    os.environ['NO_COLOR'] = '1'
    
    try:
        config = Config()
        assert config.no_color == True
    finally:
        del os.environ['NO_COLOR']


def test_config_invalid_port():
    """Test invalid port handling."""
    os.environ['BOILERPLATE_PORT'] = "invalid"
    
    try:
        config = Config()
        # Should fall back to default on invalid value
        assert config.port == 8080
    finally:
        del os.environ['BOILERPLATE_PORT']


def test_config_override():
    """Test CLI override."""
    config = Config()
    
    # Override with CLI arguments
    config.override(port=9000, host="localhost")
    
    assert config.port == 9000
    assert config.host == "localhost"


def test_config_to_dict():
    """Test config to_dict conversion."""
    config = Config()
    
    result = config.to_dict()
    
    assert isinstance(result, dict)
    assert "port" in result
    assert "host" in result
    assert "log_level" in result
    assert "no_color" in result
    assert "no_interactive" in result