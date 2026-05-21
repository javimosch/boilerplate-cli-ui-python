"""
Output formatting for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- JSON output by default (even on TTY)
- --human flag for human-readable output
- Output separation (stdout data, stderr logs)
- Versioned output format
- No colors by default
"""

import sys
import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime


OUTPUT_VERSION = "1.0"


class OutputFormatter:
    """Handles output formatting for agent-first CLI."""
    
    def __init__(self, human_mode: bool = False, no_color: bool = True):
        self.human_mode = human_mode
        self.no_color = no_color or self._env_no_color()
        self.logger = self._setup_logging()
    
    def _env_no_color(self) -> bool:
        """Check NO_COLOR environment variable."""
        import os
        return os.environ.get('NO_COLOR', '').lower() in ('1', 'true', 'yes')
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging to stderr only."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        return logger
    
    def output(self, data: Any, exit_code: int = 0) -> None:
        """
        Output data in appropriate format.
        
        Args:
            data: Data to output
            exit_code: Exit code for process
        """
        if self.human_mode:
            self._output_human(data)
        else:
            self._output_json(data)
        
        sys.exit(exit_code)
    
    def _output_json(self, data: Any) -> None:
        """Output data as JSON to stdout."""
        output = {
            "version": OUTPUT_VERSION,
            "data": data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        json.dump(output, sys.stdout, indent=None)
        sys.stdout.write('\n')
    
    def _output_human(self, data: Any) -> None:
        """Output data in human-readable format to stdout."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for subkey, subvalue in value.items():
                        print(f"  {subkey}: {subvalue}")
                else:
                    print(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                print(item)
        else:
            print(data)
    
    def output_error(self, error_dict: Dict[str, Any], exit_code: int) -> None:
        """
        Output error in appropriate format.
        
        Args:
            error_dict: Error dictionary from CLIError
            exit_code: Exit code for process
        """
        if self.human_mode:
            self._output_error_human(error_dict)
        else:
            self._output_error_json(error_dict)
        
        sys.exit(exit_code)
    
    def _output_error_json(self, error_dict: Dict[str, Any]) -> None:
        """Output error as JSON to stderr."""
        json.dump(error_dict, sys.stderr, indent=None)
        sys.stderr.write('\n')
    
    def _output_error_human(self, error_dict: Dict[str, Any]) -> None:
        """Output error in human-readable format to stderr."""
        error = error_dict.get('error', {})
        print(f"Error: {error.get('message', 'Unknown error')}", file=sys.stderr)
        if error.get('suggestions'):
            print("Suggestions:", file=sys.stderr)
            for suggestion in error['suggestions']:
                print(f"  - {suggestion}", file=sys.stderr)
    
    def log(self, message: str, level: str = "info") -> None:
        """Log message to stderr."""
        if level == "debug":
            self.logger.debug(message)
        elif level == "warning":
            self.logger.warning(message)
        else:
            self.logger.info(message)
    
    def log_progress(self, message: str) -> None:
        """Log progress message to stderr."""
        self.logger.info(message)


def format_help_json(
    version: str,
    commands: Dict[str, Any],
    output_formats: list[str],
    exit_codes: Dict[str, str]
) -> Dict[str, Any]:
    """Format help as JSON for machine consumption."""
    return {
        "version": version,
        "commands": commands,
        "output_formats": output_formats,
        "exit_codes": exit_codes
    }