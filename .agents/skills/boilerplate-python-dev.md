# Boilerplate Python CLI Development Guide

This skill teaches agents how to develop and extend the agent-first Python CLI boilerplate.

## Development Setup

### Local Development

```bash
# Navigate to project directory
cd boilerplate-cli-ui-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run CLI
python -m src.main greet --name Alice
```

### Development Commands

```bash
# Run with human output for debugging
python -m src.main greet --name Alice --human

# Start server in foreground (development mode)
python -m src.main start --port 8080

# Test API in another terminal
curl http://localhost:8080/api/status
```

## Project Structure Understanding

### Core Modules

- **main.py**: Entry point, argument parsing, command routing
- **cli.py**: Command handlers, business logic
- **output.py**: Output formatting (JSON/human), error display
- **server.py**: HTTP server, API endpoints
- **daemon.py**: Process management, PID files
- **config.py**: Configuration management
- **errors.py**: Error definitions, exit codes
- **utils.py**: Shared utilities

### Adding New Commands

#### Step 1: Add Command Handler

Edit `src/cli.py`:

```python
def handle_mycommand(self, args: argparse.Namespace) -> None:
    """Handle mycommand."""
    param = args.param or "default"
    
    data = {
        "result": "success",
        "param": param,
        "timestamp": get_timestamp()
    }
    
    self.formatter.output(data, EXIT_SUCCESS)
```

#### Step 2: Add Argument Parser

Edit `src/main.py` in `parse_args()`:

```python
# Add to subparsers
mycommand_parser = subparsers.add_parser('mycommand', add_help=False)
mycommand_parser.add_argument('--param', type=str, help='Parameter description')
```

#### Step 3: Add Command Routing

Edit `src/main.py` in `main()`:

```python
elif args.command == 'mycommand':
    handler.handle_mycommand(args)
```

#### Step 4: Create JSON Schema

Create `schemas/mycommand.schema.json`:

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

#### Step 5: Update Help JSON

Edit `src/cli.py` in `handle_help_json()`:

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

## Error Handling Patterns

### Using Semantic Exit Codes

```python
from .errors import InvalidArgumentError, ResourceNotFoundError

# Validate input
if not validate_port(port):
    raise InvalidArgumentError(
        f"Invalid port: {port}",
        details={"port": port, "valid_range": "1-65535"}
    )

# Check resource exists
if not file_exists(path):
    raise ResourceNotFoundError("config file", path)
```

### Structured Error Output

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

### Custom Error Types

Add to `src/errors.py`:

```python
class MyCustomError(CLIError):
    """Custom error for specific use case."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=95,  # Use appropriate code range
            error_type="my_custom_error",
            message=message,
            details=details,
            recoverable=True,
            retry_after=5,
            suggestions=["Retry operation", "Check configuration"]
        )
```

## Configuration Management

### Adding New Configuration

Edit `src/config.py`:

```python
# Add default
DEFAULT_MY_SETTING = "default_value"

# Add getter method
def _get_my_setting(self) -> str:
    return os.environ.get('BOILERPLATE_MY_SETTING', self.DEFAULT_MY_SETTING)

# Initialize in __init__
def __init__(self):
    # ... existing config
    self.my_setting = self._get_my_setting()
```

### Using Configuration

```python
from .config import Config

config = Config()
setting = config.my_setting

# Override with CLI arguments
config.override(my_setting="custom_value")
```

## Output Formatting

### JSON Output (Default)

```python
from .output import OutputFormatter

formatter = OutputFormatter(human_mode=False)
data = {"result": "success", "timestamp": get_timestamp()}
formatter.output(data, EXIT_SUCCESS)
```

### Human Output

```python
formatter = OutputFormatter(human_mode=True)
formatter.output(data, EXIT_SUCCESS)
```

### Error Output

```python
error_dict = {
    "error": {
        "code": 85,
        "type": "invalid_argument",
        "message": "Invalid input",
        "details": {},
        "recoverable": False,
        "retry_after": None,
        "suggestions": ["Check input"]
    }
}
formatter.output_error(error_dict, 85)
```

### Logging

```python
# Info log
formatter.log("Processing...", level="info")

# Progress log
formatter.log_progress("Step 1/3 complete")

# Warning log
formatter.log("Deprecated feature", level="warning")
```

## HTTP Server Extensions

### Adding New API Endpoints

Edit `src/server.py` in `APIHandler`:

```python
def do_GET(self) -> None:
    """Handle GET requests."""
    if self.path == '/api/myendpoint':
        self._handle_myendpoint()
    # ... existing endpoints

def _handle_myendpoint(self) -> None:
    """Handle custom endpoint."""
    data = {
        "result": "success",
        "timestamp": get_timestamp()
    }
    self._send_json_response(data)
```

### Adding POST/PUT/DELETE

```python
def do_POST(self) -> None:
    """Handle POST requests."""
    if self.path == '/api/myresource':
        self._handle_create_resource()

def _handle_create_resource(self) -> None:
    """Handle resource creation."""
    try:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # Process data
        result = process_resource(data)
        
        self._send_json_response(result, 201)
    except Exception as e:
        self._send_error_response(str(e), 400)
```

## Testing

### Test Structure

Create `tests/test_mycommand.py`:

```python
import pytest
from src.cli import CLIHandler
from src.config import Config
from src.output import OutputFormatter
from io import StringIO
import sys

def test_mycommand_json_output():
    """Test mycommand outputs valid JSON."""
    config = Config()
    formatter = OutputFormatter(human_mode=False)
    handler = CLIHandler(config, formatter)
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        handler.handle_mycommand(type('Args', (), {'param': 'test'})())
        output = sys.stdout.getvalue()
        
        # Validate JSON
        import json
        data = json.loads(output)
        assert data['data']['param'] == 'test'
    finally:
        sys.stdout = old_stdout

def test_mycommand_human_output():
    """Test mycommand human output."""
    config = Config()
    formatter = OutputFormatter(human_mode=True)
    handler = CLIHandler(config, formatter)
    
    # Test human output
    # ...
```

### Running Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run specific test file
pytest tests/test_mycommand.py

# Run with coverage
pytest --cov=src tests/
```

## Building Binary

### PyInstaller Setup

Edit `build.sh`:

```bash
#!/bin/bash
# Build Python CLI with PyInstaller

# Install PyInstaller if not installed
pip install pyinstaller

# Build single-file binary
pyinstaller \
  --onefile \
  --name boilerplate-cli-ui-python \
  --add-data "schemas:schemas" \
  --hidden-import=src \
  src/main.py

# Move to project root
mv dist/boilerplate-cli-ui-python .

# Cleanup
rm -rf build/ dist/ boilerplate-cli-ui-python.spec

# Show size
ls -lh boilerplate-cli-ui-python
```

### Build Commands

```bash
# Make executable
chmod +x build.sh

# Build binary
./build.sh

# Test binary
./boilerplate-cli-ui-python greet --name Alice
```

## Docker Development

### Building Image

```bash
# Build image
docker build -t boilerplate-cli-ui-python .

# Test image
docker run --rm boilerplate-cli-ui-python greet --name Alice
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Code Quality

### File Size Limits

- **Max 500 LOC per module file** - Use `wc -l src/module.py` to check
- **Max 300 LOC per SKILL.md file** - Keep documentation concise

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and small

### Module Organization

Each module should have a single responsibility:
- Split files that exceed 500 LOC
- Use clear module boundaries
- Minimize inter-module dependencies

## Common Development Tasks

### Adding Dependencies

Edit `requirements.txt`:

```
requests>=2.31.0
pydantic>=2.0.0
```

Install:

```bash
pip install -r requirements.txt
```

### Updating Version

Edit `src/__init__.py`:

```python
__version__ = "1.1.0"
```

### Adding Environment Variables

1. Add to `.env.example`:

```
BOILERPLATE_MY_SETTING=default_value
```

2. Add getter in `config.py`:

```python
def _get_my_setting(self) -> str:
    return os.environ.get('BOILERPLATE_MY_SETTING', self.DEFAULT_MY_SETTING)
```

### Debugging

```bash
# Enable debug logging
export BOILERPLATE_LOG_LEVEL=DEBUG

# Run with human output
python -m src.main greet --human

# Check logs
tail -f /tmp/boilerplate-cli-ui-python.log
```

## CI/CD Integration

### GitHub Actions

Add to `.github/workflows/python.yml`:

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest
      - run: python -m src.main greet
```

## Troubleshooting

### Import Errors

```bash
# Ensure running from project root
cd boilerplate-cli-ui-python
python -m src.main greet

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/main.py greet
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port
python -m src.main start --port 8081
```

### Daemon Issues

```bash
# Check if running
python -m src.main status

# Stop if running
python -m src.main stop

# Clean up PID file manually
rm /tmp/boilerplate-cli-ui-python.pid
```

## Best Practices

1. **Keep modules under 500 LOC** - Split when necessary
2. **Use semantic exit codes** - Follow error code ranges
3. **Output JSON by default** - Use `--human` for readable output
4. **Separate stdout/stderr** - Data on stdout, logs on stderr
5. **Add JSON schemas** - For all command outputs
6. **Write tests** - Test JSON output and exit codes
7. **Document changes** - Update AGENTS.md and SKILL.md files
8. **Version your output** - Use version field in JSON output

## Next Steps

After extending this boilerplate:

1. **Update AGENTS.md** - Document new commands and patterns
2. **Create SKILL.md files** - For specific guidance
3. **Update README.md** - User-facing documentation
4. **Add tests** - Ensure agent-friendly behavior
5. **Build binary** - Test distribution
6. **Update CI/CD** - Add build and test steps