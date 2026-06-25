"""
Configuration management for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- Environment variable support
- Command-line override
- Tool-specific env vars
- NO_COLOR support
"""

import os
from typing import Optional


class Config:
    """Configuration management with environment and CLI override."""
    
    # Default values
    DEFAULT_PORT = 8080
    DEFAULT_LOG_LEVEL = "INFO"
    DEFAULT_PID_FILE = "/tmp/boilerplate-cli-ui-python.pid"
    DEFAULT_LOG_FILE = "/tmp/boilerplate-cli-ui-python.log"
    DEFAULT_HOST = "127.0.0.1"
    
    def __init__(self):
        self.port = self._get_port()
        self.host = self._get_host()
        self.log_level = self._get_log_level()
        self.pid_file = self._get_pid_file()
        self.log_file = self._get_log_file()
        self.no_color = self._get_no_color()
        self.no_interactive = self._get_no_interactive()
    
    def _get_port(self) -> int:
        """Get port from env or default."""
        port = os.environ.get('BOILERPLATE_PORT')
        if port:
            try:
                return int(port)
            except ValueError:
                return self.DEFAULT_PORT
        return self.DEFAULT_PORT
    
    def _get_host(self) -> str:
        """Get host from env or default."""
        return os.environ.get('BOILERPLATE_HOST', self.DEFAULT_HOST)
    
    def _get_log_level(self) -> str:
        """Get log level from env or default."""
        return os.environ.get('BOILERPLATE_LOG_LEVEL', self.DEFAULT_LOG_LEVEL)
    
    def _get_pid_file(self) -> str:
        """Get PID file path from env or default."""
        return os.environ.get('BOILERPLATE_PID_FILE', self.DEFAULT_PID_FILE)
    
    def _get_log_file(self) -> str:
        """Get log file path from env or default."""
        return os.environ.get('BOILERPLATE_LOG_FILE', self.DEFAULT_LOG_FILE)
    
    def _get_no_color(self) -> bool:
        """Check NO_COLOR environment variable. Defaults to True (no color)."""
        env_val = os.environ.get('NO_COLOR')
        if env_val is None:
            return True
        return env_val.lower() not in ('0', 'false', 'no')
    
    def _get_no_interactive(self) -> bool:
        """Check non-interactive mode."""
        return os.environ.get('BOILERPLATE_NO_INTERACTIVE', '').lower() in ('1', 'true', 'yes')
    
    def override(self, **kwargs) -> None:
        """Override config with CLI arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "port": self.port,
            "host": self.host,
            "log_level": self.log_level,
            "pid_file": self.pid_file,
            "log_file": self.log_file,
            "no_color": self.no_color,
            "no_interactive": self.no_interactive
        }