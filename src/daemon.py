"""
Daemon process management for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- PID file management
- JSON status output by default
- Semantic exit codes
- No interactive prompts
"""

import os
import sys
import signal
import subprocess
from typing import Optional
from datetime import datetime

from .config import Config
from .errors import (
    ResourceNotFoundError,
    ResourceConflictError,
    InternalError,
    EXIT_RESOURCE_NOT_FOUND,
    EXIT_RESOURCE_CONFLICT
)
from .utils import file_exists, read_file, write_file, get_timestamp


class DaemonManager:
    """Manages daemon process lifecycle."""
    
    def __init__(self, config: Config):
        self.config = config
        self.pid_file = config.pid_file
        self.log_file = config.log_file
    
    def start(self, port: int, daemon_mode: bool = False) -> dict:
        """
        Start daemon process.
        
        Args:
            port: HTTP server port
            daemon_mode: Run as background process
            
        Returns:
            Status dictionary
        """
        if self.is_running():
            raise ResourceConflictError(
                "Daemon is already running",
                details={"pid": self._read_pid()}
            )
        
        if daemon_mode:
            return self._start_daemon(port)
        else:
            # Run in foreground - caller manages the server
            return {
                "mode": "foreground",
                "port": port,
                "pid": os.getpid(),
                "timestamp": get_timestamp()
            }
    
    def _start_daemon(self, port: int) -> dict:
        """Start daemon in background."""
        try:
            # Get current executable path
            exec_path = sys.executable
            
            # Get project directory (parent of src directory)
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Path to run.py script
            run_script = os.path.join(project_dir, "run.py")
            
            # Create command to run server in foreground using run.py
            cmd = [exec_path, run_script, "start", f"--port={port}"]
            
            # Set up logging
            log_file_handle = open(self.log_file, 'a')
            
            # Start the process
            process = subprocess.Popen(
                cmd,
                stdout=log_file_handle,
                stderr=log_file_handle,
                stdin=subprocess.DEVNULL,
                cwd=project_dir
            )
            
            # Write PID file
            pid = process.pid
            if not write_file(self.pid_file, str(pid)):
                process.kill()
                raise InternalError("Failed to write PID file")
            
            return {
                "mode": "daemon",
                "port": port,
                "pid": pid,
                "log_file": self.log_file,
                "timestamp": get_timestamp()
            }
            
        except Exception as e:
            raise InternalError(f"Failed to start daemon: {str(e)}")
    
    def stop(self) -> dict:
        """Stop daemon process."""
        if not self.is_running():
            raise ResourceNotFoundError("daemon", "process")
        
        pid = self._read_pid()
        try:
            os.kill(pid, signal.SIGTERM)
            os.remove(self.pid_file)
            return {
                "status": "stopped",
                "pid": pid,
                "timestamp": get_timestamp()
            }
        except ProcessLookupError:
            # Process not running, clean up PID file
            os.remove(self.pid_file)
            raise ResourceNotFoundError("daemon", f"PID {pid}")
        except Exception as e:
            raise InternalError(f"Failed to stop daemon: {str(e)}")
    
    def status(self) -> dict:
        """Get daemon status."""
        if not self.is_running():
            return {
                "status": "not_running",
                "timestamp": get_timestamp()
            }
        
        pid = self._read_pid()
        return {
            "status": "running",
            "pid": pid,
            "log_file": self.log_file,
            "timestamp": get_timestamp()
        }
    
    def is_running(self) -> bool:
        """Check if daemon is running."""
        if not file_exists(self.pid_file):
            return False
        
        try:
            pid = self._read_pid()
            os.kill(pid, 0)  # Check if process exists
            return True
        except (ValueError, ProcessLookupError):
            # Process not running, clean up PID file
            try:
                os.remove(self.pid_file)
            except FileNotFoundError:
                pass
            return False
        except Exception:
            return False
    
    def _read_pid(self) -> int:
        """Read PID from file."""
        content = read_file(self.pid_file)
        if not content:
            raise InternalError("Failed to read PID file")
        return int(content.strip())