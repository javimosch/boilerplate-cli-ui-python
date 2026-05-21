# Boilerplate CLI UI Python

**Agent-first Python CLI boilerplate with HTTP API and daemon support.**

**Author:** Javier Leandro Arancibia

A modern Python CLI template following agent-first design principles from [AGENTS_FRIENDLY_TOOLS.md](https://github.com/javimosch/supercli-cli-boilerplates). Designed for crafting CLI applications that are optimized for AI agent consumption while remaining human-friendly.

## Philosophy

**Agent-First, Human-Compatible**

This boilerplate embodies the principle that modern CLIs should be designed for programmatic consumption first, with human readability as an enhancement rather than a requirement.

- **JSON-by-default**: All commands output structured JSON, even on TTY
- **Semantic exit codes**: Precise error signaling (80-119 range)
- **Structured errors**: Error objects with recovery hints
- **No interactivity**: No prompts by default
- **Composable**: Designed for piping and automation

## Features

- **CLI-first design**: Primary interface is command-line
- **HTTP server**: Built-in JSON API for web interfaces
- **Daemon mode**: Background process management
- **Single binary**: Compilable to standalone executable
- **Agent-friendly**: JSON output, semantic errors, schema discovery
- **Docker support**: Container-ready with compose files
- **Zero dependencies**: Uses only Python standard library

## Quick Start

### Local Development

```bash
# Navigate to project directory
cd boilerplate-cli-ui-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run CLI (JSON output by default)
python -m src.main greet --name Alice
# Output: {"version":"1.0","data":{"greeting":"Hello, Alice","timestamp":"..."},"timestamp":"..."}

# Human-readable output
python -m src.main greet --name Alice --human
# Output: greeting: Hello, Alice
#         name: Alice
#         timestamp: ...
```

### Docker Usage

```bash
# Build image
docker build -t boilerplate-cli-ui-python .

# Run commands
docker run --rm boilerplate-cli-ui-python greet --name Alice

# Start server
docker run -p 8080:8080 boilerplate-cli-ui-python start --port 8080
```

## Commands

### CLI Commands

```bash
# Greet command
python -m src.main greet [--name NAME] [--human]

# Version command
python -m src.main version [--human]

# Machine-readable help
python -m src.main --help-json

# Schema discovery
python -m src.main greet --schema
```

### Daemon/Server Commands

```bash
# Start server in foreground (development)
python -m src.main start [--port PORT]

# Start server as daemon (background)
python -m src.main start --port 8080 --daemon

# Check daemon status
python -m src.main status [--human]

# Stop daemon
python -m src.main stop [--human]
```

## HTTP API

When the server is running, interact via JSON API:

```bash
# API information
curl http://localhost:8080/

# Server status
curl http://localhost:8080/api/status

# Health check
curl http://localhost:8080/api/health
```

## Configuration

### Environment Variables

```bash
# Server configuration
export BOILERPLATE_PORT=8080
export BOILERPLATE_HOST=127.0.0.1

# Logging configuration
export BOILERPLATE_LOG_LEVEL=INFO
export BOILERPLATE_LOG_FILE=/tmp/boilerplate-cli-ui-python.log

# Daemon configuration
export BOILERPLATE_PID_FILE=/tmp/boilerplate-cli-ui-python.pid

# Behavior configuration
export BOILERPLATE_NO_INTERACTIVE=1
export NO_COLOR=1
```

### Configuration File

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
# Edit .env with your settings
```

## Building Binary

### Prerequisites

```bash
# Install PyInstaller
pip install pyinstaller
```

### Build

```bash
# Make build script executable
chmod +x build.sh

# Build binary
./build.sh

# Use binary
./boilerplate-cli-ui-python greet --name Alice
```

The binary will be approximately 10-15MB (includes Python runtime).

## Agent Usage Patterns

### Parse JSON Output

```bash
# Extract specific field
python -m src.main greet --name Alice | jq -r '.data.greeting'
# Output: Hello, Alice

# Extract timestamp
python -m src.main greet | jq -r '.data.timestamp'
```

### Compose Commands

```bash
# Check status and act accordingly
if python -m src.main status | jq -r '.data.status' | grep -q running; then
    python -m src.main stop
fi
```

### Error Handling

```bash
# Retry on connection timeout
python -m src.main start || exit_code=$?
if [ $exit_code -eq 105 ]; then
    sleep 2
    python -m src.main start
fi
```

## Exit Codes

Semantic exit codes for agent decision-making:

- `0`: Success
- `85`: Invalid argument
- `86`: Bad permissions
- `87`: Validation error
- `92`: Resource not found
- `93`: Resource already exists
- `94`: Resource conflict
- `105`: Connection timeout
- `106`: API unavailable
- `107`: Auth failed
- `110`: Internal error
- `111`: Panic

## Error Format

All errors follow structured format:

```json
{
  "error": {
    "code": 85,
    "type": "invalid_argument",
    "message": "Invalid port number",
    "details": {"port": "invalid", "valid_range": "1-65535"},
    "recoverable": false,
    "retry_after": null,
    "suggestions": ["Use --port 8080", "Check port is in range 1-65535"]
  }
}
```

## Project Structure

```
boilerplate-cli-ui-python/
├── src/                      # Source code (max 500 LOC per file)
│   ├── main.py              # Entry point and argument parsing
│   ├── cli.py               # Command handlers
│   ├── output.py            # Output formatting
│   ├── server.py            # HTTP server
│   ├── daemon.py            # Process management
│   ├── config.py            # Configuration
│   ├── errors.py            # Error definitions
│   └── utils.py             # Utilities
├── schemas/                 # JSON schemas for command outputs
├── tests/                   # Test suite
├── .agents/
│   └── skills/              # Agent guidance
├── AGENTS.md                # Agent development guide
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker compose
├── build.sh                # Build script
└── .env.example            # Environment template
```

## Development

### Adding New Commands

See [AGENTS.md](AGENTS.md) for detailed development guide.

### Running Tests

```bash
# Install pytest
pip install pytest

# Run tests
pytest

# Run with coverage
pytest --cov=src tests/
```

### Code Style

- Max 500 LOC per module file
- Max 300 LOC per SKILL.md file
- Follow PEP 8 guidelines
- Use type hints where appropriate

## Agent-First Principles

This boilerplate follows these core principles:

1. **JSON-by-default**: All commands output JSON by default
2. **`--human` opt-in**: Human-readable output only when requested
3. **Semantic exit codes**: Precise error signaling (80-119 range)
4. **Structured errors**: Error objects with recovery hints
5. **Output separation**: stdout for data, stderr for logs
6. **No interactivity**: No prompts by default
7. **Schema discovery**: `--schema` flag for JSON schemas
8. **Machine-readable help**: `--help-json` for programmatic discovery

## Documentation

- **[AGENTS.md](AGENTS.md)**: Development guide for AI agents
- **[.agents/skills/boilerplate-python-usage.md](.agents/skills/boilerplate-python-usage.md)**: Usage guide for agents
- **[.agents/skills/boilerplate-python-dev.md](.agents/skills/boilerplate-python-dev.md)**: Development guide for agents

## Use Cases

- **SuperCLI plugins**: UI-enabled plugins for SuperCLI
- **CLI tools**: Add web interface to existing CLI tools
- **Microservices**: Small HTTP services with CLI management
- **Admin panels**: Simple admin interfaces for system tools
- **Development**: Quick prototyping of CLI + web applications

## Requirements

- Python 3.10+
- No external dependencies for basic functionality
- PyInstaller (for binary compilation)
- Docker (for containerization)

## License

MIT License - Feel free to use this boilerplate for your projects.

## Contributing

When extending this boilerplate:

1. **Keep modules under 500 LOC** - Split when necessary
2. **Maintain agent-first principles** - JSON-by-default, semantic errors
3. **Add JSON schemas** - For all new command outputs
4. **Update AGENTS.md** - Document new patterns
5. **Add tests** - Ensure agent-friendly behavior
6. **Update SKILL.md files** - Guide other agents

## References

- [AGENTS_FRIENDLY_TOOLS.md](https://github.com/javimosch/supercli-cli-boilerplates) - Agent-first CLI design principles
- [SuperCLI](https://github.com/javimosch/supercli) - Universal CLI framework
- [PyInstaller](https://pyinstaller.org/) - Python binary compilation

## Acknowledgments

Inspired by agent-first design principles and modern CLI best practices. Designed to serve as a recipe for crafting CLI applications that AI agents can use reliably, predictably, and efficiently.