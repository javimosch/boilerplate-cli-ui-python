# AGENTS.md - Agent-First Python CLI Boilerplate

This document guides AI agents in understanding, extending, and maintaining this agent-first Python CLI boilerplate.

## Project Philosophy

This boilerplate implements **agent-first CLI design** following `AGENTS_FRIENDLY_TOOLS.md` principles:

- **JSON-by-default**: All commands output JSON by default, even on TTY
- **`--human` opt-in**: Human-readable output only when explicitly requested
- **Semantic exit codes**: 0 (success), 80-89 (user errors), 90-99 (resource errors), 100-109 (integration errors), 110-119 (software errors)
- **Structured errors**: Error objects with code, type, recoverable field, and suggestions
- **Output separation**: stdout for data, stderr for logs/progress
- **No interactivity**: No prompts by default, `--no-interactive` is default behavior
- **Schema discovery**: `--schema` flag for JSON schema of each command output

## Project Structure

```
boilerplate-cli-ui-python/
├── src/                      # Source code (max 500 LOC per file)
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI entry point and argument parsing
│   ├── cli.py               # Command handlers (greet, version, start, stop, status)
│   ├── output.py            # Output formatting (JSON/human, error formatting)
│   ├── server.py            # HTTP server with JSON API
│   ├── daemon.py            # Process management (PID files, background processes)
│   ├── config.py            # Configuration management (env vars, CLI override)
│   ├── errors.py            # Error definitions and semantic exit codes
│   └── utils.py             # Utility functions (validation, file operations)
├── schemas/                 # JSON schemas for command outputs
│   ├── greet.schema.json
│   ├── version.schema.json
│   ├── start.schema.json
│   ├── stop.schema.json
│   └── status.schema.json
├── tests/                   # Test suite (agent-friendly patterns)
├── .agents/
│   └── skills/              # Agent guidance (max 300 LOC per SKILL.md)
│       ├── boilerplate-python-usage.md    # Usage guide for agents
│       └── boilerplate-python-dev.md      # Development guide for agents
├── AGENTS.md                # This file - project guide for agents
├── README.md                # User documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Modern Python project configuration
├── Dockerfile              # Docker image build
├── docker-compose.yml      # Docker compose setup
├── build.sh                # Binary compilation script (PyInstaller)
├── .env.example            # Environment variables template
└── .gitignore
```

## Coding Rules

### File Size Limits

- **Max 500 LOC per module file** - Split files that exceed this limit
- **Max 300 LOC per SKILL.md file** - Keep skill documentation concise

### Module Organization

Each module has a single, well-defined responsibility:

- **main.py**: Entry point, argument parsing, command routing
- **cli.py**: Command handlers, business logic for each command
- **output.py**: Output formatting, JSON schema validation, error display
- **server.py**: HTTP server, API endpoints, request handling
- **daemon.py**: Process management, PID files, background processes
- **config.py**: Configuration loading, environment variables, CLI override
- **errors.py**: Error definitions, semantic exit codes, error formatting
- **utils.py**: Shared utilities, validation functions, file operations

### Naming Conventions

- **Files**: `snake_case.py` (e.g., `error_handler.py`)
- **Functions**: `snake_case` (e.g., `get_user_data()`)
- **Classes**: `PascalCase` (e.g., `DataManager`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private**: `_leading_underscore` (e.g., `_internal_func()`)

### Agent-First Output Patterns

**Default JSON Output:**
```python
# Always output JSON by default
data = {"result": "success", "timestamp": "2026-05-21T23:21:00Z"}
formatter.output(data, EXIT_SUCCESS)
```

**Structured Errors:**
```python
# Use semantic exit codes and structured errors
raise InvalidArgumentError(
    "Invalid port number",
    details={"port": port, "valid_range": "1-65535"}
)
```

**Output Separation:**
```python
# Data goes to stdout, logs to stderr
formatter.output(data, exit_code)  # stdout
formatter.log("Processing...", level="info")  # stderr
```

### Semantic Exit Codes

Always use semantic exit codes from `errors.py`:

```python
from .errors import (
    EXIT_SUCCESS,           # 0
    EXIT_INVALID_ARGUMENT,  # 85
    EXIT_BAD_PERMISSIONS,   # 86
    EXIT_RESOURCE_NOT_FOUND, # 92
    EXIT_CONNECTION_TIMEOUT, # 105
    EXIT_INTERNAL_ERROR      # 110
)
```

### Error Handling Pattern

```python
try:
    result = perform_operation()
    formatter.output(result, EXIT_SUCCESS)
except CLIError as e:
    # Structured error with semantic code
    formatter.output_error(e.to_dict(), e.code)
except Exception as e:
    # Unexpected errors become internal errors
    error = InternalError(f"Unexpected error: {str(e)}")
    formatter.output_error(error.to_dict(), error.code)
```

## Adding New Commands

### 1. Add Command Handler in `cli.py`

```python
def handle_mycommand(self, args: argparse.Namespace) -> None:
    """Handle mycommand."""
    # Business logic here
    data = {
        "result": "success",
        "param": args.param,
        "timestamp": get_timestamp()
    }
    self.formatter.output(data, EXIT_SUCCESS)
```

### 2. Add Argument Parser in `main.py`

```python
# In parse_args() function
mycommand_parser = subparsers.add_parser('mycommand', add_help=False)
mycommand_parser.add_argument('--param', type=str, help='Parameter description')
```

### 3. Add Command Routing in `main.py`

```python
# In main() function
elif args.command == 'mycommand':
    handler.handle_mycommand(args)
```

### 4. Create JSON Schema in `schemas/`

Create `mycommand.schema.json` following the pattern:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "version": {"type": "string"},
    "data": {
      "type": "object",
      "properties": {
        "result": {"type": "string"},
        "param": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"}
      }
    },
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

### 5. Update Help JSON in `cli.py`

Add command info to `handle_help_json()`:
```python
commands = {
    # ... existing commands
    "mycommand": {
        "description": "My command description",
        "flags": {
            "--param": "Parameter description",
            "--human": "Human-readable output"
        }
    }
}
```

## Configuration Management

### Environment Variables

Prefix all environment variables with `BOILERPLATE_`:

```bash
BOILERPLATE_PORT=8080
BOILERPLATE_HOST=127.0.0.1
BOILERPLATE_LOG_LEVEL=INFO
BOILERPLATE_PID_FILE=/tmp/boilerplate-cli-ui-python.pid
BOILERPLATE_LOG_FILE=/tmp/boilerplate-cli-ui-python.log
BOILERPLATE_NO_INTERACTIVE=1
```

### Adding New Configuration

1. Add default in `config.py`:
```python
DEFAULT_MY_SETTING = "default_value"
```

2. Add getter method:
```python
def _get_my_setting(self) -> str:
    return os.environ.get('BOILERPLATE_MY_SETTING', self.DEFAULT_MY_SETTING)
```

3. Initialize in `__init__`:
```python
self.my_setting = self._get_my_setting()
```

## Testing Guidelines

### Test Structure

```python
# tests/test_mycommand.py
import pytest
from src.cli import CLIHandler
from src.config import Config
from src.output import OutputFormatter

def test_mycommand_json_output():
    """Test mycommand outputs valid JSON."""
    config = Config()
    formatter = OutputFormatter(human_mode=False)
    handler = CLIHandler(config, formatter)
    
    # Test implementation
    # ...
```

### Agent-Friendly Test Patterns

- Test JSON schema validation
- Test semantic exit codes
- Test error format structure
- Test `--human` mode output
- Test stderr/stdout separation
- Test environment variable handling

## Development Workflow

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run CLI
python -m src.main greet --name Alice

# Run with human output
python -m src.main greet --name Alice --human

# Start server (foreground)
python -m src.main start --port 8080

# Start server (daemon)
python -m src.main start --port 8080 --daemon
```

### Building Binary

```bash
# Make executable
chmod +x build.sh

# Build optimized binary
./build.sh
```

### Docker Development

```bash
# Build image
docker build -t boilerplate-cli-ui-python .

# Run container
docker run --rm boilerplate-cli-ui-python greet --name Alice

# Run with volume mount
docker run --rm -v $(pwd)/data:/app/data boilerplate-cli-ui-python start
```

## Agent-Friendly Design Checklist

When extending this boilerplate, ensure:

- [ ] All commands default to JSON output
- [ ] `--human` flag provides human-readable output
- [ ] Semantic exit codes for all error paths
- [ ] Structured error output with recovery hints
- [ ] Output separation (stdout data, stderr logs)
- [ ] No interactive prompts by default
- [ ] JSON schemas for all command outputs
- [ ] `--help-json` provides machine-readable help
- [ ] `--schema` provides schema discovery
- [ ] Environment variables for configuration
- [ ] Max 500 LOC per module file
- [ ] Clear module responsibilities
- [ ] Comprehensive error handling

## Common Patterns

### Reading Configuration

```python
from .config import Config

config = Config()
port = config.port  # From env or default
config.override(port=3000)  # CLI override
```

### Formatting Output

```python
from .output import OutputFormatter

formatter = OutputFormatter(human_mode=False)
formatter.output({"result": "success"}, EXIT_SUCCESS)
```

### Handling Errors

```python
from .errors import InvalidArgumentError, CLIError

try:
    # Operation
    pass
except CLIError as e:
    formatter.output_error(e.to_dict(), e.code)
```

### Logging

```python
# Logs always go to stderr
formatter.log("Processing...", level="info")
formatter.log_progress("Step 1/3 complete")
```

## References

- **AGENTS_FRIENDLY_TOOLS.md**: Complete agent-first CLI design principles
- **JSON Schema**: http://json-schema.org/
- **Semantic Exit Codes**: Based on Square Engineering blog post
- **PyInstaller**: https://pyinstaller.org/

## Notes for Agents Extending This Boilerplate

This boilerplate serves as a **recipe** for crafting agent-first CLI applications. When using this as a template:

1. **Copy this structure** to your new project
2. **Rename appropriately** (update package names, commands, etc.)
3. **Add your AGENTS.md** to teach other agents about your project
4. **Add SKILL.md files** under `.agents/skills/` for specific guidance
5. **Follow the patterns** - JSON-by-default, semantic errors, output separation
6. **Keep modules under 500 LOC** - split when necessary
7. **Maintain agent-first principles** - design for programmatic consumption

The goal is to create CLI tools that AI agents can use reliably, predictably, and efficiently. Every design decision should ask: "Does this help an agent make decisions?"