"""
CLI command handlers for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- JSON output by default
- Semantic exit codes
- No interactive prompts by default
- Structured error output
"""

import argparse
from typing import Optional

from .config import Config
from .output import OutputFormatter, format_help_json
from .errors import (
    InvalidArgumentError,
    InternalError,
    EXIT_SUCCESS,
    EXIT_INVALID_ARGUMENT
)
from .utils import validate_port, get_timestamp


class CLIHandler:
    """Handles CLI commands."""
    
    def __init__(self, config: Config, formatter: OutputFormatter):
        self.config = config
        self.formatter = formatter
    
    def handle_greet(self, args: argparse.Namespace) -> None:
        """Handle greet command."""
        name = args.name or "World"
        greeting = f"Hello, {name}"
        
        data = {
            "greeting": greeting,
            "name": name,
            "timestamp": get_timestamp()
        }
        
        self.formatter.output(data, EXIT_SUCCESS)
    
    def handle_version(self, args: argparse.Namespace) -> None:
        """Handle version command."""
        data = {
            "name": "boilerplate-cli-ui-python",
            "version": "1.0.0",
            "timestamp": get_timestamp()
        }
        
        self.formatter.output(data, EXIT_SUCCESS)
    
    def handle_help_json(self, args: argparse.Namespace) -> None:
        """Handle help-json command."""
        commands = {
            "greet": {
                "description": "Greet someone by name",
                "flags": {
                    "--name": "Name to greet (default: World)",
                    "--human": "Human-readable output"
                }
            },
            "version": {
                "description": "Show version information",
                "flags": {
                    "--human": "Human-readable output"
                }
            },
            "start": {
                "description": "Start HTTP server",
                "flags": {
                    "--port": "HTTP port (default: 8080)",
                    "--daemon": "Run as background process",
                    "--human": "Human-readable output"
                }
            },
            "stop": {
                "description": "Stop daemon server",
                "flags": {
                    "--human": "Human-readable output"
                }
            },
            "status": {
                "description": "Check daemon status",
                "flags": {
                    "--human": "Human-readable output"
                }
            }
        }
        
        exit_codes = {
            "0": "success",
            "85": "invalid_argument",
            "92": "resource_not_found",
            "93": "resource_already_exists",
            "105": "connection_timeout",
            "110": "internal_error"
        }
        
        data = format_help_json(
            version="1.0.0",
            commands=commands,
            output_formats=["json", "human"],
            exit_codes=exit_codes
        )
        
        self.formatter.output(data, EXIT_SUCCESS)
    
    def handle_start(self, args: argparse.Namespace, daemon_manager) -> None:
        """Handle start command."""
        port = args.port or self.config.port
        daemon_mode = args.daemon or False
        
        if not validate_port(port):
            raise InvalidArgumentError(
                f"Invalid port: {port}",
                details={"port": port, "valid_range": "1-65535"}
            )
        
        if daemon_mode:
            try:
                result = daemon_manager.start(port, daemon_mode=True)
                self.formatter.output(result, EXIT_SUCCESS)
            except Exception as e:
                from .errors import CLIError
                if isinstance(e, CLIError):
                    self.formatter.output_error(e.to_dict(), e.code)
                else:
                    error = InternalError(str(e))
                    self.formatter.output_error(error.to_dict(), error.code)
        else:
            # Run in foreground - will be handled by main
            result = {
                "mode": "foreground",
                "port": port,
                "timestamp": get_timestamp()
            }
            self.formatter.output(result, EXIT_SUCCESS)
    
    def handle_stop(self, args: argparse.Namespace, daemon_manager) -> None:
        """Handle stop command."""
        try:
            result = daemon_manager.stop()
            self.formatter.output(result, EXIT_SUCCESS)
        except Exception as e:
            from .errors import CLIError
            if isinstance(e, CLIError):
                self.formatter.output_error(e.to_dict(), e.code)
            else:
                error = InternalError(str(e))
                self.formatter.output_error(error.to_dict(), error.code)
    
    def handle_status(self, args: argparse.Namespace, daemon_manager) -> None:
        """Handle status command."""
        try:
            result = daemon_manager.status()
            self.formatter.output(result, EXIT_SUCCESS)
        except Exception as e:
            from .errors import CLIError
            if isinstance(e, CLIError):
                self.formatter.output_error(e.to_dict(), e.code)
            else:
                error = InternalError(str(e))
                self.formatter.output_error(error.to_dict(), error.code)