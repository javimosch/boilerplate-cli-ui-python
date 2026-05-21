"""
boilerplate-cli-ui-python - Agent-first CLI with HTTP API

A boilerplate template for crafting CLI applications with:
- JSON output by default (agent-first)
- HTTP server for web UI
- Daemon process management
- Semantic exit codes
- Docker support
"""

__version__ = "1.0.0"
__author__ = "Javier Leandro Arancibia"

from .main import main