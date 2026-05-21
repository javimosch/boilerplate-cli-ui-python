"""
HTTP server with JSON API for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- JSON API responses only
- No visual fluff by default
- API-first design
- Progress on stderr
"""

import json
import sys
import signal
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict
from datetime import datetime
from threading import Event

from .config import Config
from .errors import InternalError
from .utils import validate_port, get_timestamp


class ServerStatus:
    """Server status tracking."""
    
    def __init__(self, port: int):
        self.status = "running"
        self.port = port
        self.start_time = datetime.utcnow()
        self.uptime_seconds = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert status to dictionary."""
        self.uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()
        return {
            "status": self.status,
            "port": self.port,
            "uptime_seconds": self.uptime_seconds,
            "start_time": self.start_time.isoformat() + "Z",
            "timestamp": get_timestamp()
        }


class APIHandler(BaseHTTPRequestHandler):
    """HTTP API request handler."""
    
    server_status: ServerStatus = None
    shutdown_event: Event = None
    
    def log_message(self, format: str, *args: Any) -> None:
        """Log to stderr instead of stdout."""
        logging.info(format, *args)
    
    def _send_json_response(self, data: Dict[str, Any], status_code: int = 200) -> None:
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json.dump(data, self.wfile)
    
    def _send_error_response(self, message: str, status_code: int = 500) -> None:
        """Send error response."""
        error_data = {
            "error": {
                "code": status_code,
                "type": "http_error",
                "message": message,
                "recoverable": status_code < 500,
                "timestamp": get_timestamp()
            }
        }
        self._send_json_response(error_data, status_code)
    
    def do_GET(self) -> None:
        """Handle GET requests."""
        try:
            if self.path == '/':
                self._handle_root()
            elif self.path == '/api/status':
                self._handle_status()
            elif self.path == '/api/health':
                self._handle_health()
            else:
                self._send_error_response("Not found", 404)
        except Exception as e:
            self._send_error_response(f"Internal error: {str(e)}", 500)
    
    def _handle_root(self) -> None:
        """Handle root endpoint - API info."""
        data = {
            "name": "boilerplate-cli-ui-python",
            "version": "1.0.0",
            "description": "Agent-first CLI with HTTP API",
            "endpoints": {
                "/": "API information",
                "/api/status": "Server status",
                "/api/health": "Health check"
            },
            "timestamp": get_timestamp()
        }
        self._send_json_response(data)
    
    def _handle_status(self) -> None:
        """Handle status endpoint."""
        if self.server_status:
            self._send_json_response(self.server_status.to_dict())
        else:
            self._send_error_response("Server not initialized", 500)
    
    def _handle_health(self) -> None:
        """Handle health check endpoint."""
        self._send_json_response({"status": "healthy", "timestamp": get_timestamp()})


class HTTPServerManager:
    """Manages HTTP server lifecycle."""
    
    def __init__(self, config: Config):
        self.config = config
        self.server: HTTPServer = None
        self.server_status: ServerStatus = None
        self.shutdown_event = Event()
    
    def start(self, port: int) -> None:
        """Start HTTP server."""
        if not validate_port(port):
            raise InternalError(f"Invalid port: {port}")
        
        # Setup logging to stderr
        logging.basicConfig(
            stream=sys.stderr,
            level=getattr(logging, self.config.log_level),
            format='%(message)s'
        )
        
        # Initialize server status
        self.server_status = ServerStatus(port)
        
        # Setup handler with server status
        APIHandler.server_status = self.server_status
        APIHandler.shutdown_event = self.shutdown_event
        
        # Create server
        try:
            self.server = HTTPServer((self.config.host, port), APIHandler)
            logging.info(f"Server starting on http://{self.config.host}:{port}")
            logging.info(f"Press Ctrl+C to stop")
            
            # Setup signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # Serve until shutdown
            self.server.serve_forever()
            
        except OSError as e:
            raise InternalError(f"Failed to start server: {str(e)}")
        except KeyboardInterrupt:
            logging.info("Server stopped by user")
            self._cleanup()
        except Exception as e:
            raise InternalError(f"Server error: {str(e)}")
    
    def _signal_handler(self, signum: int, frame) -> None:
        """Handle shutdown signals."""
        logging.info(f"Received signal {signum}, shutting down...")
        self.shutdown_event.set()
        self._cleanup()
        sys.exit(0)
    
    def _cleanup(self) -> None:
        """Cleanup resources."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.server_status:
            self.server_status.status = "stopped"