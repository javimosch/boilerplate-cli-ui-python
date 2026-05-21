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
├── templates/               # React UI frontend
│   ├── index.html          # Main HTML with CDN dependencies
│   └── js/
│       ├── app.js          # Main app with routing (max 500 LOC)
│       ├── services/       # API call layer (max 200 LOC each)
│       │   └── apiService.js
│       ├── composables/    # State management (max 200 LOC each)
│       │   └── useDaemonStatus.js
│       ├── components/     # Reusable UI components (max 200 LOC each)
│       │   ├── Sidebar.js
│       │   ├── StatusCard.js
│       │   ├── ResponseViewer.js
│       │   ├── APITester.js
│       │   └── MobileHeader.js
│       └── views/          # Page components (max 200 LOC each)
│           ├── Dashboard.js
│           ├── APITestView.js
│           └── SettingsView.js
├── schemas/                 # JSON schemas for command outputs
│   ├── greet.schema.json
│   ├── version.schema.json
│   ├── start.schema.json
│   ├── stop.schema.json
│   └── status.schema.json
├── tests/                   # Test suite (agent-friendly patterns)
├── .agents/
│   └── skills/              # Agent guidance (max 300 LOC per SKILL.md)
│       ├── boilerplate-python-usage.md       # Usage guide for agents
│       ├── boilerplate-python-dev.md         # Development guide for agents
│       ├── python-cli-boilerplate-development.md  # Comprehensive development learnings
│       └── react-cdn-modular-ui.md          # React UI development guidelines
├── AGENTS.md                # This file - project guide for agents
├── README.md                # User documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Modern Python project configuration
├── Dockerfile              # Docker image build
├── docker-compose.yml      # Docker compose setup
├── build.sh                # Binary compilation script (PyInstaller)
├── run.py                  # Entry point script for daemon execution
├── .env.example            # Environment variables template
└── .gitignore
```

## Coding Rules

### File Size Limits

- **Max 500 LOC per Python module file** - Split files that exceed this limit
- **Max 300 LOC per SKILL.md file** - Keep skill documentation concise
- **Max 500 LOC per React module** (app.js, main routing files)
- **Max 200 LOC per React component** (services, composables, components, views)

### Module Organization

Each module has a single, well-defined responsibility:

- **Python Backend**:
  - `main.py`: Entry point, argument parsing, command routing
  - `cli.py`: Command handlers, business logic for each command
  - `output.py`: Output formatting, JSON schema validation, error display
  - `server.py`: HTTP server, API endpoints, request handling
  - `daemon.py`: Process management, PID files, background processes
  - `config.py`: Configuration loading, environment variables, CLI override
  - `errors.py`: Error definitions, semantic exit codes, error formatting
  - `utils.py`: Shared utilities, validation functions, file operations

- **React Frontend**:
  - `app.js`: Root component with router setup and layout structure
  - `services/`: HTTP request handling and API interactions
  - `composables/`: Reusable state management and side effects
  - `components/`: Presentational UI components with minimal logic
  - `views/`: Page-level components with routing integration

### Naming Conventions

- **Python**: `snake_case.py` for files, `snake_case` for functions, `PascalCase` for classes
- **React**: `PascalCase` for components, `camelCase` for functions/variables
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

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

## Backend Development Guidelines

### Daemon Process Management

**Critical Pattern**: Always wait for process termination before cleanup
```python
def stop(self) -> dict:
    pid = self._read_pid()
    try:
        os.kill(pid, signal.SIGTERM)
        
        # Wait for process to terminate (max 5 seconds)
        for _ in range(50):  # 50 * 0.1s = 5 seconds
            try:
                os.kill(pid, 0)  # Check if process exists
                time.sleep(0.1)
            except ProcessLookupError:
                break  # Process has terminated
        else:
            # Force kill if needed
            os.kill(pid, signal.SIGKILL)
            time.sleep(0.1)
        
        os.remove(self.pid_file)
        return {"status": "stopped", "pid": pid}
    except ProcessLookupError:
        os.remove(self.pid_file)
        raise ResourceNotFoundError("daemon", f"PID {pid}")
```

### Relative Import Issues in Subprocess

**Problem**: Subprocess execution fails with relative import errors
**Solution**: Create entry point script with proper Python path

```python
# run.py
#!/usr/bin/env python3
import sys
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)
from src.main import main
if __name__ == '__main__':
    main()
```

### HTTP Server Response Encoding

**Problem**: Python 3 expects bytes but `json.dump()` writes strings
**Solution**: Encode JSON to bytes before writing

```python
def _send_json_response(self, data: Dict[str, Any], status_code: int = 200) -> None:
    self.send_response(status_code)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    json_bytes = json.dumps(data).encode('utf-8')
    self.wfile.write(json_bytes)  # Critical: encode to bytes
```

### Configuration Management

**Pattern**: Environment variables with CLI override support
```python
class Config:
    DEFAULT_PORT = 8080
    
    def _get_port(self) -> int:
        port = os.environ.get('BOILERPLATE_PORT')
        if port:
            try:
                return int(port)
            except ValueError:
                return self.DEFAULT_PORT
        return self.DEFAULT_PORT
    
    def override(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
```

### Error Handling Strategy

**Structured Error Pattern**:
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

## Frontend Development Guidelines

### React CDN Architecture

**Technical Stack**:
- React 18 via CDN with Babel JSX transformation
- React Router with HashRouter for hashbang routing
- Tailwind CSS + DaisyUI for styling
- Lucide Icons for iconography

### Layout Architecture

**Critical Pattern**: Use flexbox for proper alignment and scrolling
```javascript
// Correct layout structure
<div className="min-h-screen bg-[#F7F6F3] flex flex-col">
    <div className="lg:hidden">
        <MobileHeader />
    </div>
    
    <div className="flex flex-1 overflow-hidden">
        <Sidebar className="lg:relative w-64 flex-shrink-0" />
        <main className="flex-1 overflow-auto pt-16 lg:pt-0">
            <Routes>
                <Route path="/" element={<Dashboard />} />
            </Routes>
        </main>
    </div>
</div>
```

**Common Layout Pitfalls**:
- ❌ Using fixed positioning for layout structure
- ❌ Missing overflow handling on main content
- ❌ Not using flex-shrink-0 for fixed-width elements
- ✅ Use flex layout with proper overflow-auto
- ✅ Use relative positioning for desktop, fixed for mobile
- ✅ Ensure independent scrolling areas

### Component Architecture

**Service Layer** (API calls, max 200 LOC):
```javascript
const apiService = {
    baseUrl: window.location.origin,
    
    async request(endpoint, options = {}) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        return await response.json();
    },
    
    getStatus() { return this.request('/api/status'); }
};
```

**Composable Layer** (state management, max 200 LOC):
```javascript
function useDaemonStatus(refreshInterval = 5000) {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    
    const fetchStatus = useCallback(async () => {
        setLoading(true);
        try {
            const data = await apiService.getStatus();
            setStatus(data);
        } finally {
            setLoading(false);
        }
    }, []);
    
    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, refreshInterval);
        return () => clearInterval(interval);
    }, [fetchStatus, refreshInterval]);
    
    return { status, loading, refresh: fetchStatus };
}
```

**Component Layer** (presentational, max 200 LOC):
```javascript
function StatusCard({ status, loading, onRefresh }) {
    const [mounted, setMounted] = useState(false);
    
    useEffect(() => {
        setMounted(true);
        lucide.createIcons();
    }, []);
    
    return (
        <div className={`bg-white border rounded-xl p-6 scroll-entry ${mounted ? '' : ''}`}>
            {/* Presentational content */}
        </div>
    );
}
```

### Hashbang Routing

**Router Setup**:
```javascript
const { HashRouter, Routes, Route, Navigate } = ReactRouterDOM;

function App() {
    return (
        <HashRouter>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/api-test" element={<APITestView />} />
                <Route path="/settings" element={<SettingsView />} />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </HashRouter>
    );
}
```

**Routing Requirements**:
- Each route must be accessible via direct URL
- Support full page reload (no client-only state)
- Use URL parameters for view state when needed
- Test browser back/forward navigation

### Mobile Responsiveness

**Mobile Navigation Pattern**:
```javascript
function App() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    
    return (
        <div className="flex flex-col">
            <div className="lg:hidden">
                <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
            </div>
            
            <div className="flex flex-1 overflow-hidden">
                <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
                <main className="flex-1 overflow-auto pt-16 lg:pt-0">
                    {/* Content */}
                </main>
            </div>
        </div>
    );
}
```

**Responsive Sidebar**:
```javascript
<aside className={`
    fixed lg:relative inset-y-0 left-0 z-50 lg:z-auto
    w-64 h-full bg-white border-r
    transform transition-transform
    ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
`}>
```

### Performance Optimization

**React Performance Patterns**:
```javascript
// Use useCallback for event handlers
const handleClick = useCallback(() => {
    doSomething();
}, [dependencies]);

// Cleanup in useEffect (critical for intervals)
useEffect(() => {
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
}, []);

// Icon management
useEffect(() => {
    lucide.createIcons();
}, [dependencies]);
```

### Error Handling

**API Error Pattern**:
```javascript
const [error, setError] = useState(null);

const fetchData = async () => {
    try {
        const data = await apiService.getData();
        setData(data);
        setError(null);
    } catch (err) {
        setError(err.message);
        setData(null);
    }
};
```

**Error Display**:
```javascript
{error ? (
    <div className="bg-[#FDEBEC] text-[#9F2F2D] p-4 rounded-lg">
        <div className="flex items-center gap-2">
            <i data-lucide="alert-circle" className="w-5 h-5"></i>
            <span className="font-medium">Error</span>
        </div>
        <p className="text-sm mt-1">{error}</p>
    </div>
) : null}
```

## Common Pitfalls & Solutions

### Backend Pitfalls

1. **Daemon Zombie Processes**: Stop command must wait for process termination before removing PID file
2. **Import Errors in Subprocess**: Use entry point script with proper Python path setup
3. **HTTP Encoding Issues**: Encode JSON to bytes in Python 3 HTTP responses
4. **Port Conflicts**: Implement dynamic port allocation or clear error messaging
5. **Memory Leaks**: Monitor long-running processes, ensure proper cleanup

### Frontend Pitfalls

1. **Layout Misalignment**: Use flexbox instead of fixed positioning for structure
2. **Missing Scroll**: Add overflow-auto to content areas for independent scrolling
3. **Memory Leaks**: Always cleanup intervals and event listeners in useEffect
4. **Icon Rendering**: Call lucide.createIcons() after dynamic content updates
5. **CDN Loading Order**: Load dependencies in correct order (React → Router → Babel → App)

## Development Workflow

### Backend Workflow
1. Write module following max 500 LOC constraint
2. Implement semantic error handling
3. Add JSON schema for outputs
4. Test with JSON and --human modes
5. Verify semantic exit codes
6. Test daemon start/stop/status

### Frontend Workflow
1. Create component following max 200 LOC constraint
2. Implement proper state management with composables
3. Add loading and error states
4. Test responsive design at all breakpoints
5. Verify hashbang routing with page reloads
6. Test mobile drawer navigation

### Testing Checklist
- [ ] CLI commands output valid JSON by default
- [ ] Daemon lifecycle (start/stop/status) works correctly
- [ ] HTTP API endpoints respond with proper JSON
- [ ] UI loads and functions in browser
- [ ] Mobile responsive navigation works
- [ ] Hashbang routing supports full page reload
- [ ] Error handling and user feedback
- [ ] No memory leaks in long-running processes

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