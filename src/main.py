"""
Main entry point for agent-first CLI.

Following AGENTS_FRIENDLY_TOOLS.md principles:
- JSON output by default (even on TTY)
- --human flag for human-readable output
- Semantic exit codes
- No interactive prompts by default
"""

import sys
import json
import argparse

from .config import Config
from .output import OutputFormatter
from .cli import CLIHandler
from .daemon import DaemonManager
from .server import HTTPServerManager
from .errors import CLIError, InternalError, EXIT_SUCCESS, EXIT_INVALID_ARGUMENT
from .utils import check_python_version
from . import guide as guide_mod
from . import lifecycle


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="boilerplate-cli-ui-python - Agent-first CLI with HTTP API",
        add_help=False  # Custom help handling
    )
    
    # Global flags
    parser.add_argument('--human', action='store_true', help='Human-readable output')
    parser.add_argument('--json', action='store_true',
                        help='JSON output (the default; accepted for consistency)')
    parser.add_argument('--help-json', action='store_true', help='Machine-readable help')
    parser.add_argument('--schema', action='store_true', help='JSON schema discovery')
    
    # Commands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Greet command
    greet_parser = subparsers.add_parser('greet', add_help=False)
    greet_parser.add_argument('--name', type=str, help='Name to greet')
    greet_parser.add_argument('--human', action='store_true', help='Human-readable output')
    greet_parser.add_argument('--schema', action='store_true', help='JSON schema discovery')
    greet_parser.add_argument('--json', action='store_true', help='JSON output (the default)')
    
    # Version command
    version_parser = subparsers.add_parser('version', add_help=False)
    version_parser.add_argument('--human', action='store_true', help='Human-readable output')
    version_parser.add_argument('--schema', action='store_true', help='JSON schema discovery')
    version_parser.add_argument('--json', action='store_true', help='JSON output (the default)')
    
    # Start command
    start_parser = subparsers.add_parser('start', add_help=False)
    start_parser.add_argument('--port', type=int, help='HTTP port')
    start_parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    start_parser.add_argument('--human', action='store_true', help='Human-readable output')
    start_parser.add_argument('--schema', action='store_true', help='JSON schema discovery')
    start_parser.add_argument('--json', action='store_true', help='JSON output (the default)')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', add_help=False)
    stop_parser.add_argument('--human', action='store_true', help='Human-readable output')
    stop_parser.add_argument('--schema', action='store_true', help='JSON schema discovery')
    stop_parser.add_argument('--json', action='store_true', help='JSON output (the default)')
    
    # Status command
    status_parser = subparsers.add_parser('status', add_help=False)
    status_parser.add_argument('--human', action='store_true', help='Human-readable output')
    status_parser.add_argument('--schema', action='store_true', help='JSON schema discovery')
    status_parser.add_argument('--json', action='store_true', help='JSON output (the default)')
    
    return parser.parse_args()


def _flag_value(argv, name, default=None):
    """Reads --name value or --name=value out of a raw argv slice."""
    prefix = name + "="
    for i, a in enumerate(argv):
        if a == name and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith(prefix):
            return a[len(prefix):]
    return default


def _serve_flags(argv):
    """Resolves --host/--port.

    The host default MUST be loopback (cli-daemon-spec §1): serving the whole
    network is a deliberate act, never something that happens because nobody
    passed a flag.
    """
    config = Config()
    host = _flag_value(argv, "--host") or _flag_value(argv, "-host") or config.host
    port_str = _flag_value(argv, "--port") or _flag_value(argv, "-port") or str(config.port)
    try:
        port = int(port_str)
    except ValueError:
        _die(EXIT_INVALID_ARGUMENT, "bad_flag_value",
             f"--port must be a number, got {port_str!r}",
             "boilerplate-cli-ui-python serve --port 8080")
    return host, port


def _die(code, etype, message, suggestion):
    """Typed error on stdout, exit code equal to .error.code (§2, §3)."""
    print(json.dumps({
        "ok": False,
        "error": {
            "code": code,
            "type": etype,
            "message": message,
            "recoverable": 100 <= code <= 109,
            "suggestions": [suggestion],
        },
    }))
    sys.exit(code)


def _dispatch_spec_commands(argv) -> bool:
    """Handles the agent-first spec command surface before argparse sees it.

    argparse exits 2 on anything it does not recognise, which is outside the
    semantic ranges cli-output-spec §2 defines — so the spec commands, and the
    unknown-command case, are resolved here instead.
    """
    if not argv:
        return False

    cmd = argv[0]
    rest = argv[1:]

    if cmd == "guide":
        if "--human" in rest:
            print(guide_mod.guide_markdown())
        else:
            print(guide_mod.guide_json())
        return True

    if cmd == "help-json":
        print(guide_mod.help_json())
        return True

    if cmd == "serve":
        host, port = _serve_flags(rest)
        config = Config()
        config.override(host=host, port=port)
        HTTPServerManager(config).start(port)
        return True

    if cmd == "daemon":
        if not rest:
            _die(EXIT_INVALID_ARGUMENT, "missing_argument",
                 "daemon needs a subcommand: start, stop or status",
                 "boilerplate-cli-ui-python daemon status")
        sub, tail = rest[0], rest[1:]
        host, port = _serve_flags(tail)
        try:
            if sub == "start":
                lifecycle.start(host, port)
            elif sub == "stop":
                lifecycle.stop(port)
            elif sub == "status":
                lifecycle.status(port)
            else:
                _die(EXIT_INVALID_ARGUMENT, "unknown_command",
                     f"unknown daemon subcommand {sub!r}",
                     "boilerplate-cli-ui-python daemon status")
        except CLIError as e:
            body = e.to_dict()
            print(json.dumps(body))
            sys.exit(e.code)
        return True

    known = {"greet", "version", "start", "stop", "status", "help",
             "--help", "-h", "--help-json", "--schema", "--human"}
    if cmd not in known and not cmd.startswith("-"):
        _die(EXIT_INVALID_ARGUMENT, "unknown_command",
             f"unknown command {cmd!r}",
             "boilerplate-cli-ui-python help-json")

    return False


def main() -> None:
    """Main entry point."""
    # Check Python version
    check_python_version((3, 10))

    # The spec command surface is resolved before argparse (see the docstring).
    if _dispatch_spec_commands(sys.argv[1:]):
        return
    
    # Parse arguments
    args = parse_args()
    
    # Initialize config
    config = Config()
    
    # Check for human mode (from global or subcommand flags)
    human_mode = getattr(args, 'human', False)
    
    # Initialize output formatter (JSON by default)
    formatter = OutputFormatter(
        human_mode=human_mode,
        no_color=config.no_color
    )
    
    # Handle help-json
    if args.help_json:
        handler = CLIHandler(config, formatter)
        handler.handle_help_json(args)
        return
    
    # Handle schema discovery
    schema_mode = getattr(args, 'schema', False)
    if schema_mode:
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
                sys.exit(error.code)
        else:
            from .errors import InvalidArgumentError
            error = InvalidArgumentError("Schema requires a command")
            formatter.output_error(error.to_dict(), error.code)
            sys.exit(error.code)
        return
    
    # Handle no command
    if not args.command:
        from .errors import InvalidArgumentError
        error = InvalidArgumentError(
            "No command specified",
            details={"available_commands": ["greet", "version", "start", "stop", "status"]}
        )
        formatter.output_error(error.to_dict(), error.code)
        sys.exit(error.code)
    
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
            sys.exit(error.code)

    except CLIError as e:
        formatter.output_error(e.to_dict(), e.code)
        sys.exit(e.code)
    except KeyboardInterrupt:
        formatter.log("Interrupted by user")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        error = InternalError(f"Unexpected error: {str(e)}")
        formatter.output_error(error.to_dict(), error.code)
        sys.exit(error.code)


if __name__ == '__main__':
    main()