"""
Main entry point for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- JSON output by default (even on TTY)
- --human flag for human-readable output
- Semantic exit codes
- No interactive prompts by default
"""

import sys
import argparse

from .config import Config
from .output import OutputFormatter
from .cli import CLIHandler
from .daemon import DaemonManager
from .server import HTTPServerManager
from .errors import CLIError, InternalError, EXIT_SUCCESS
from .utils import check_python_version


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="boilerplate-cli-ui-python - Agent-first CLI with HTTP API",
        add_help=False  # Custom help handling
    )
    
    # Global flags
    parser.add_argument('--human', action='store_true', help='Human-readable output')
    parser.add_argument('--help-json', action='store_true', help='Machine-readable help')
    parser.add_argument('--schema', action='store_true', help='JSON schema discovery')
    
    # Commands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Greet command
    greet_parser = subparsers.add_parser('greet', add_help=False)
    greet_parser.add_argument('--name', type=str, help='Name to greet')
    
    # Version command
    version_parser = subparsers.add_parser('version', add_help=False)
    
    # Start command
    start_parser = subparsers.add_parser('start', add_help=False)
    start_parser.add_argument('--port', type=int, help='HTTP port')
    start_parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', add_help=False)
    
    # Status command
    status_parser = subparsers.add_parser('status', add_help=False)
    
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    # Check Python version
    check_python_version((3, 10))
    
    # Parse arguments
    args = parse_args()
    
    # Initialize config
    config = Config()
    
    # Initialize output formatter (JSON by default)
    formatter = OutputFormatter(
        human_mode=args.human,
        no_color=config.no_color
    )
    
    # Handle help-json
    if args.help_json:
        handler = CLIHandler(config, formatter)
        handler.handle_help_json(args)
        return
    
    # Handle schema discovery
    if args.schema:
        if args.command:
            schema_path = f"schemas/{args.command}.schema.json"
            try:
                import json
                with open(schema_path, 'r') as f:
                    schema = json.load(f)
                formatter.output(schema, EXIT_SUCCESS)
            except FileNotFoundError:
                from .errors import ResourceNotFoundError
                error = ResourceNotFoundError("schema", args.command)
                formatter.output_error(error.to_dict(), error.code)
        else:
            from .errors import InvalidArgumentError
            error = InvalidArgumentError("Schema requires a command")
            formatter.output_error(error.to_dict(), error.code)
        return
    
    # Handle no command
    if not args.command:
        from .errors import InvalidArgumentError
        error = InvalidArgumentError(
            "No command specified",
            details={"available_commands": ["greet", "version", "start", "stop", "status"]}
        )
        formatter.output_error(error.to_dict(), error.code)
        return
    
    # Initialize daemon manager
    daemon_manager = DaemonManager(config)
    
    # Initialize CLI handler
    handler = CLIHandler(config, formatter)
    
    try:
        # Handle commands
        if args.command == 'greet':
            handler.handle_greet(args)
        elif args.command == 'version':
            handler.handle_version(args)
        elif args.command == 'start':
            # Check if running in foreground mode
            port = args.port or config.port
            daemon_mode = args.daemon or False
            
            if not daemon_mode:
                # Run server in foreground
                server_manager = HTTPServerManager(config)
                server_manager.start(port)
            else:
                handler.handle_start(args, daemon_manager)
        elif args.command == 'stop':
            handler.handle_stop(args, daemon_manager)
        elif args.command == 'status':
            handler.handle_status(args, daemon_manager)
        else:
            from .errors import InvalidArgumentError
            error = InvalidArgumentError(
                f"Unknown command: {args.command}",
                details={"available_commands": ["greet", "version", "start", "stop", "status"]}
            )
            formatter.output_error(error.to_dict(), error.code)
    
    except CLIError as e:
        formatter.output_error(e.to_dict(), e.code)
    except KeyboardInterrupt:
        formatter.log("Interrupted by user")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        error = InternalError(f"Unexpected error: {str(e)}")
        formatter.output_error(error.to_dict(), error.code)


if __name__ == '__main__':
    main()