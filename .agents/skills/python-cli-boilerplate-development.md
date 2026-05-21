# Python CLI Boilerplate Development

Use this skill when developing agent-first Python CLI tools with HTTP API and daemon capabilities.

## Core Principles

### Agent-First Design
- **JSON-by-default**: All commands output JSON even on TTY unless `--human` flag
- **Semantic exit codes**: 0 (success), 80-89 (user errors), 90-99 (resource errors), 100-109 (integration errors), 110-119 (software errors)
- **Structured errors**: Error objects with code, type, recoverable field, and suggestions
- **Output separation**: stdout for data, stderr for logs/progress
- **No interactivity**: No prompts by default, `--no-interactive` is default behavior
- **Schema discovery**: `--schema` flag for JSON schema of each command output

### File Organization
- **Max 500 LOC per module file** - Split files that exceed this limit
- **Clear module responsibilities**: Each module has single, well-defined purpose
- **Naming conventions**: `snake_case.py` for files, `snake_case` for functions, `PascalCase` for classes

## Common Pitfalls & Solutions

### Daemon Process Management
**Pitfall**: Stop command removes PID file immediately without waiting for process termination
**Solution**: Add wait loop (5 seconds max) to ensure process terminates before cleanup
```python
# Wait for process to terminate (max 5 seconds)
for _ in range(50):  # 50 * 0.1s = 5 seconds
    try:
        os.kill(pid, 0)  # Check if process exists
        time.sleep(0.1)
    except ProcessLookupError:
        break  # Process has terminated
else:
    os.kill(pid, signal.SIGKILL)  # Force kill if needed
```

### Relative Import Issues in Daemons
**Pitfall**: Subprocess execution fails with `ImportError: attempted relative import with no known parent package`
**Solution**: Create entry point script (`run.py`) that sets up Python path and uses absolute imports
```python
#!/usr/bin/env python3
import sys
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)
from src.main import main
if __name__ == '__main__':
    main()
```

### HTTP Server Encoding
**Pitfall**: Python 3 HTTP server expects bytes but `json.dump()` writes strings
**Solution**: Encode JSON to bytes before writing to response stream
```python
json_bytes = json.dumps(data).encode('utf-8')
self.wfile.write(json_bytes)  # Instead of json.dump(data, self.wfile)
```

### Port Conflicts
**Pitfall**: Default ports often conflict with other services
**Solution**: Use dynamic port allocation or provide clear error messages with alternatives
```python
import socket
def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port
```

## Backend Guidelines

### Configuration Management
- Prefix all environment variables with project name (e.g., `BOILERPLATE_PORT`)
- Support CLI override of environment variables
- Provide sensible defaults for all configuration
- Document all environment variables in `.env.example`

### Error Handling Pattern
```python
try:
    result = perform_operation()
    formatter.output(result, EXIT_SUCCESS)
except CLIError as e:
    formatter.output_error(e.to_dict(), e.code)
except Exception as e:
    error = InternalError(f"Unexpected error: {str(e)}")
    formatter.output_error(error.to_dict(), error.code)
```

### Module Structure
- `main.py`: Entry point, argument parsing, command routing
- `cli.py`: Command handlers, business logic
- `output.py`: Output formatting, JSON schema validation
- `server.py`: HTTP server, API endpoints
- `daemon.py`: Process management, PID files
- `config.py`: Configuration loading, environment variables
- `errors.py`: Error definitions, semantic exit codes
- `utils.py`: Shared utilities, validation functions

## Frontend Guidelines (React CDN)

### Modular Architecture
- **Max 200 LOC per component file** - Split larger components
- **Max 500 LOC per module file** - For services, composables, views
- **Clear separation**: Services (API calls), Composables (state), Components (UI), Views (pages)

### Layout Best Practices
- Use flexbox for proper sidebar/content alignment
- `flex flex-col` for vertical stacking with proper overflow
- `flex-1 overflow-auto` for scrollable content areas
- `flex-shrink-0` for fixed-width elements like sidebars
- Avoid fixed positioning for layout structure (use for overlays only)

### React CDN Patterns
```javascript
// Proper component structure with hooks
const { useState, useEffect } = React;

function MyComponent() {
    const [state, setState] = useState(null);
    
    useEffect(() => {
        // Component lifecycle
        lucide.createIcons();
    }, [dependencies]);
    
    return <div>JSX here</div>;
}
```

### Routing with Hashbang
- Use React Router with HashRouter for CDN deployment
- Each route should have unique URL: `#/`, `#/api-test`, `#/settings`
- Support full page reload (no client-only state)
- Use `<Navigate>` for redirects

### Performance Optimization
- Use `useCallback` for event handlers to prevent unnecessary re-renders
- Implement proper cleanup in useEffect
- Use loading states and error boundaries
- Debounce rapid API calls (status refresh, search, etc.)

## Testing & Verification

### Smoke Testing Checklist
- [ ] CLI commands output valid JSON by default
- [ ] `--human` flag provides human-readable output
- [ ] Semantic exit codes for all error paths
- [ ] Daemon start/stop/status functionality
- [ ] HTTP API endpoints respond correctly
- [ ] UI loads and functions in browser
- [ ] Mobile responsive navigation
- [ ] Error handling and user feedback

### Common Failure Points
1. **Import errors**: Check Python path in daemon subprocess
2. **Port conflicts**: Verify port availability before starting
3. **Zombie processes**: Ensure proper cleanup in stop command
4. **Memory leaks**: Monitor long-running daemon processes
5. **UI routing**: Test hashbang routing with page reloads

## Deployment Considerations

### Binary Compilation
- Use PyInstaller for standalone binary creation
- Include all dependencies in spec file
- Test binary on target deployment environment
- Consider UPX compression for smaller binary size

### Docker Deployment
- Use minimal base images (python:3.11-slim)
- Multi-stage builds for smaller final image
- Expose only necessary ports
- Run as non-root user when possible

### CI/CD Integration
- Test on multiple Python versions
- Run smoke tests in CI pipeline
- Build and test Docker images
- Automate GitHub releases with binary attachments

## Documentation Requirements

### AGENTS.md
- Project structure and module responsibilities
- Coding rules and conventions
- Agent-first design principles
- Common patterns and examples
- Troubleshooting guide

### SKILL.md Files
- Usage guidance for agents
- Development patterns and pitfalls
- Environment setup instructions
- Testing and verification procedures

### README.md
- Installation instructions
- Quick start guide
- API documentation
- Configuration options
- Troubleshooting common issues