# Boilerplate CLI UI Python

**Agent-First Python CLI Boilerplate with Modular React UI for 2026 Agentic Standards**

Part of [SuperCLI](https://github.com/javimosch/supercli) - build CLI/UI plugins fast for 2026.

| Stack | Repo | Binary |
|-------|------|--------|
| Go + inline HTML | [boilerplate-cli-ui-go](https://github.com/javimosch/boilerplate-cli-ui-go) | ~5MB |
| Go + Vue 3 CDN | [boilerplate-cli-ui-go-v2-vue](https://github.com/javimosch/boilerplate-cli-ui-go-v2-vue) | ~5MB |
| Go + React 18 CDN | [boilerplate-cli-ui-go-v2-react](https://github.com/javimosch/boilerplate-cli-ui-go-v2-react) | ~5MB |
| Deno + vanilla JS | [boilerplate-cli-ui-deno](https://github.com/javimosch/boilerplate-cli-ui-deno) | ~76MB |
| Node.js + vanilla JS | [boilerplate-cli-ui-node](https://github.com/javimosch/boilerplate-cli-ui-node) | ~123MB |
| **Python + React CDN** | **boilerplate-cli-ui-python** | **~10MB** |
| Rust + vanilla JS | [boilerplate-cli-ui-rust](https://github.com/javimosch/boilerplate-cli-ui-rust) | ~1.1MB |
| .NET 8 + Vue 3 | [boilerplate-cli-ui-dotnet](https://github.com/javimosch/boilerplate-cli-ui-dotnet) | ~21MB |

**Author:** Javier Leandro Arancibia, Senior Engineer

A comprehensive reference implementation for crafting modular, agent-first CLI applications with modern React UIs. This boilerplate embodies 2026 agentic development standards, providing production-ready patterns for backend services, frontend interfaces, and the integration patterns that AI agents need to work reliably with software systems.

## 🎯 Executive Summary for Agents

This codebase serves as a **complete reference** for building modular applications following 2026 agentic standards. It demonstrates:

- **Agent-first backend design**: JSON-by-default CLI with semantic error handling
- **Modular React UI**: CDN-based architecture with proper separation of concerns
- **Daemon process management**: Production-ready background process lifecycle
- **HTTP API integration**: RESTful JSON API with web interface
- **2026 architectural patterns**: LOC limits, modular boundaries, clear responsibilities

**Core Philosophy**: Design for programmatic consumption first, human interaction second. Every architectural decision prioritizes agent reliability and predictability.

## ⚠️ Important Notice

**This is an opinionated boilerplate** designed specifically for building agentic-ready applications in 2026. The architectural decisions, patterns, and conventions reflect specific choices about how AI agents should interact with software systems.

**No contributions are accepted.** This boilerplate is maintained as a reference implementation and will not accept pull requests, feature requests, or external modifications. It is provided as-is for educational and reference purposes.

## 🏗️ 2026 Agentic Standards Implementation

### Modular Architecture Principles

**File Size Constraints** (Strict):
- **Python modules**: Max 500 LOC per file
- **React components**: Max 200 LOC per file  
- **React modules**: Max 500 LOC per file (app.js, routing)
- **SKILL.md files**: Max 300 LOC per file

**Separation of Concerns**:
```
Backend Layer (Python):
├── Entry/Orchestration (main.py)
├── Business Logic (cli.py) 
├── Data Layer (server.py, daemon.py)
├── Cross-cutting (config.py, errors.py, utils.py)
└── Presentation (output.py)

Frontend Layer (React):
├── Services (API calls, data fetching)
├── Composables (state management, side effects)
├── Components (presentational UI)
└── Views (page-level composition)
```

### Agent-First Design Contract

**JSON-By-Default Guarantee**:
```bash
# All commands output JSON on TTY
python -m src.main greet --name Test
# {"version":"1.0","data":{"greeting":"Hello, Test",...},"timestamp":"..."}

# Human mode is opt-in only
python -m src.main greet --name Test --human
# greeting: Hello, Test
```

**Semantic Exit Codes** (Agent Decision Matrix):
- `0`: Success
- `80-89`: User errors (invalid args, permissions, validation)
- `90-99`: Resource errors (not found, conflicts, allocation)
- `100-109`: Integration errors (timeouts, API failures, auth)
- `110-119`: Software errors (internal, panics, unexpected)

**Structured Error Format**:
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

## 🚀 Quick Start for Agents

### Installation (Multiple Methods)

**Agent Quick Test** (temporary, no cleanup):
```bash
curl -sSL https://raw.githubusercontent.com/javimosch/boilerplate-cli-ui-python/master/scripts/quick-install.sh | bash
```

**Permanent Installation** (for agent workflows):
```bash
curl -sSL https://raw.githubusercontent.com/javimosch/boilerplate-cli-ui-python/master/scripts/install-for-agents.sh | bash
export PATH="$HOME/.local/share/boilerplate-cli-ui-python:$PATH"
```

**Development Setup**:
```bash
git clone https://github.com/javimosch/boilerplate-cli-ui-python.git
cd boilerplate-cli-ui-python
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m src.main greet --name AgentTest
```

### Immediate Verification

```bash
# Test JSON output (agent-first)
python -m src.main greet --name Test | jq '.data.greeting'
# Output: "Hello, Test"

# Test semantic exit codes
python -m src.main greet --name Test; echo "Exit: $?"
# Output: Exit: 0

# Test HTTP API
python -m src.main start --port 8080 --daemon
curl http://localhost:8080/api/health
python -m src.main stop
```

## 📐 Architecture Reference

### Backend Structure (Python)

**Module Responsibilities** (Max 500 LOC each):
```python
src/
├── main.py          # Entry point, argument parsing, command routing
├── cli.py           # Command handlers, business logic per command  
├── output.py        # Output formatting, JSON validation, error display
├── server.py        # HTTP server, API endpoints, request handling
├── daemon.py        # Process management, PID files, background processes
├── config.py        # Configuration loading, env vars, CLI override
├── errors.py        # Error definitions, semantic exit codes
└── utils.py         # Shared utilities, validation, file operations
```

**Critical Patterns**:

1. **Daemon Process Management** (Prevents Zombie Processes):
```python
def stop(self) -> dict:
    pid = self._read_pid()
    try:
        os.kill(pid, signal.SIGTERM)
        
        # Wait for process termination (max 5 seconds)
        for _ in range(50):  # 50 * 0.1s = 5 seconds
            try:
                os.kill(pid, 0)  # Check if process exists
                time.sleep(0.1)
            except ProcessLookupError:
                break
        else:
            os.kill(pid, signal.SIGKILL)  # Force kill
            time.sleep(0.1)
        
        os.remove(self.pid_file)
        return {"status": "stopped", "pid": pid}
```

2. **Relative Import Solution** (Subprocess Execution):
```python
# run.py - Entry point script
#!/usr/bin/env python3
import sys, os
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)
from src.main import main
if __name__ == '__main__':
    main()
```

3. **HTTP Response Encoding** (Python 3 Compatibility):
```python
def _send_json_response(self, data, status_code=200):
    self.send_response(status_code)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    json_bytes = json.dumps(data).encode('utf-8')  # Critical: encode to bytes
    self.wfile.write(json_bytes)
```

### Frontend Structure (React CDN)

**Component Architecture** (Max 200 LOC each):
```javascript
templates/
├── index.html              # Main HTML with CDN dependencies
└── js/
    ├── app.js              # Root app with routing (max 500 LOC)
    ├── services/           # API call layer (max 200 LOC each)
    │   └── apiService.js
    ├── composables/        # State management (max 200 LOC each)
    │   └── useDaemonStatus.js
    ├── components/         # Reusable UI components (max 200 LOC each)
    │   ├── Sidebar.js
    │   ├── StatusCard.js
    │   ├── ResponseViewer.js
    │   ├── APITester.js
    │   └── MobileHeader.js
    └── views/              # Page components (max 200 LOC each)
        ├── Dashboard.js
        ├── APITestView.js
        └── SettingsView.js
```

**Critical Layout Pattern** (Prevents Alignment Issues):
```javascript
// Correct flex layout structure
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

**Service Layer Pattern**:
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

**Composable Pattern**:
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
        return () => clearInterval(interval); // Critical cleanup
    }, [fetchStatus, refreshInterval]);
    
    return { status, loading, refresh: fetchStatus };
}
```

## ⚠️ Common Pitfalls & Solutions

### Backend Critical Issues

**1. Zombie Daemon Processes**
- **Problem**: Stop command removes PID file before process terminates
- **Solution**: Implement 5-second wait loop with force kill fallback
- **Reference**: `python-cli-boilerplate-development.md` → Daemon Process Management

**2. Subprocess Import Errors**
- **Problem**: `ImportError: attempted relative import with no known parent package`
- **Solution**: Create `run.py` entry point script with proper Python path
- **Reference**: `python-cli-boilerplate-development.md` → Relative Import Issues

**3. HTTP Encoding Issues**
- **Problem**: Python 3 expects bytes but `json.dump()` writes strings
- **Solution**: Encode JSON to bytes: `json.dumps(data).encode('utf-8')`
- **Reference**: `python-cli-boilerplate-development.md` → HTTP Server Response Encoding

**4. Port Conflicts**
- **Problem**: Default ports conflict with other services
- **Solution**: Dynamic port allocation or clear error messaging
- **Reference**: `python-cli-boilerplate-development.md` → Port Conflicts

### Frontend Critical Issues

**1. Layout Misalignment**
- **Problem**: Sidebar and main content not vertically aligned
- **Solution**: Use flexbox layout with `flex flex-1 overflow-hidden`
- **Reference**: `react-cdn-modular-ui.md` → Layout Architecture

**2. Missing Vertical Scroll**
- **Problem**: Content extends beyond viewport without scroll
- **Solution**: Add `overflow-auto` to main content area
- **Reference**: `react-cdn-modular-ui.md` → Common Layout Pitfalls

**3. Memory Leaks**
- **Problem**: Intervals not cleaned up cause memory leaks
- **Solution**: Always return cleanup function in useEffect
- **Reference**: `react-cdn-modular-ui.md` → Performance Optimization

**4. Icon Rendering Issues**
- **Problem**: Icons don't appear after dynamic content updates
- **Solution**: Call `lucide.createIcons()` after content updates
- **Reference**: `react-cdn-modular-ui.md` → Icon Management

## 🧪 Development Workflow

### Backend Development

1. **Create module** following max 500 LOC constraint
2. **Implement semantic error handling** with proper exit codes
3. **Add JSON schema** for command outputs
4. **Test with JSON and --human modes**
5. **Verify daemon lifecycle** (start/stop/status)
6. **Update AGENTS.md** with new patterns

### Frontend Development

1. **Create component** following max 200 LOC constraint
2. **Implement proper state management** with composables
3. **Add loading and error states** for better UX
4. **Test responsive design** at all breakpoints
5. **Verify hashbang routing** with page reloads
6. **Test mobile drawer navigation**

### Testing Checklist

**Backend Verification**:
- [ ] CLI commands output valid JSON by default
- [ ] `--human` flag provides human-readable output
- [ ] Semantic exit codes for all error paths
- [ ] Daemon start/stop/status functionality
- [ ] HTTP API endpoints respond correctly
- [ ] No zombie processes after stop command

**Frontend Verification**:
- [ ] UI loads and functions in browser
- [ ] Mobile responsive navigation works
- [ ] Hashbang routing supports full page reload
- [ ] Sidebar and content properly aligned
- [ ] Independent scrolling in content areas
- [ ] No memory leaks in long-running sessions

## 📚 Comprehensive Documentation

This codebase includes extensive documentation for agents:

### Core Documentation
- **[AGENTS.md](AGENTS.md)** - Complete development guide with backend/frontend guidelines
- **[docs/AGENTS_FRIENDLY_TOOLS.md](docs/AGENTS_FRIENDLY_TOOLS.md)** - Agent-first CLI design principles and patterns
- **[python-cli-boilerplate-development.md](.agents/skills/python-cli-boilerplate-development.md)** - Backend development patterns and pitfalls
- **[react-cdn-modular-ui.md](.agents/skills/react-cdn-modular-ui.md)** - Frontend development patterns and pitfalls

### Agent Guidance
- **[boilerplate-python-usage.md](.agents/skills/boilerplate-python-usage.md)** - Usage patterns for agents
- **[boilerplate-python-dev.md](.agents/skills/boilerplate-python-dev.md)** - Development workflow for agents
- **[boilerplate-python-smoke-tests.md](.agents/skills/boilerplate-python-smoke-tests.md)** - Comprehensive smoke testing

### Configuration Reference
- **[.env.example](.env.example)** - Environment variable template
- **[pyproject.toml](pyproject.toml)** - Modern Python project configuration
- **[requirements.txt](requirements.txt)** - Python dependencies

## 🔧 HTTP API Reference

### Endpoints

```bash
# API information
GET / → {"name":"boilerplate-cli-ui-python","endpoints":{...}}

# Server status  
GET /api/status → {"status":"running","port":8080,"uptime_seconds":123,...}

# Health check
GET /api/health → {"status":"healthy","timestamp":"..."}

# Web UI
GET /ui → HTML interface with React application
```

### Response Format

All endpoints return JSON with consistent structure:
```json
{
  "version": "1.0",
  "data": { /* response data */ },
  "timestamp": "2026-05-21T22:00:00.000Z"
}
```

## 🎨 Frontend Technology Stack

**React CDN Architecture**:
- React 18 via CDN with Babel JSX transformation
- React Router with HashRouter for hashbang routing
- Tailwind CSS + DaisyUI for utility-first styling
- Lucide Icons for consistent iconography
- Geist font family for premium typography

**Routing Pattern**:
- Hash-based routing (`#/`, `#/api-test`, `#/settings`)
- Full page reload support (no client-only state)
- Browser back/forward navigation
- Direct URL access to all routes

## 🐳 Deployment Options

### Binary Distribution
```bash
# Build standalone binary
./build.sh

# Binary includes Python runtime (~10-15MB)
# No dependencies required on target system
```

### Docker Deployment
```bash
# Build image
docker build -t boilerplate-cli-ui-python .

# Run container
docker run -p 8080:8080 boilerplate-cli-ui-python start --daemon
```

### Development Mode
```bash
# Run with Python for development
python -m src.main start --port 8080 --daemon

# Access UI at http://localhost:8080/ui
```

## 🤖 Agent Integration Patterns

### Command Composition
```bash
# Chain commands using exit codes
python -m src.main start --daemon && \
python -m src.main status | jq '.data.status' | grep -q running && \
echo "Daemon started successfully"
```

### JSON Processing
```bash
# Extract specific fields for decision making
STATUS=$(python -m src.main status | jq -r '.data.status')
if [ "$STATUS" = "running" ]; then
    python -m src.main stop
fi
```

### Error Recovery
```bash
# Retry on transient errors
python -m src.main start --daemon || EXIT_CODE=$?
if [ $EXIT_CODE -eq 105 ]; then  # Connection timeout
    sleep 2
    python -m src.main start --daemon
fi
```

### Schema Validation
```bash
# Validate output against schema
python -m src.main greet --schema > greet.schema.json
python -m src.main greet --name Test | jq --argfile greet.schema
```

## 📋 Exit Code Reference

**Semantic Exit Codes** (Agent Decision Matrix):

| Range | Type | Codes | Purpose |
|-------|------|-------|---------|
| 0 | Success | 0 | Operation completed successfully |
| 80-89 | User Errors | 85-87 | Invalid arguments, permissions, validation |
| 90-99 | Resource Errors | 92-94 | Not found, conflicts, allocation issues |
| 100-109 | Integration Errors | 105-107 | Timeouts, API failures, authentication |
| 110-119 | Software Errors | 110-111 | Internal errors, panics, unexpected failures |

## 🔄 CI/CD Integration

### GitHub Actions

This boilerplate includes CI/CD workflows for:
- **Automated testing** on Python 3.10, 3.11, 3.12
- **Binary compilation** for multiple platforms
- **Docker image builds** with multi-stage optimization
- **Automated releases** with binary attachments

### Release Process

```bash
# Tag release
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will:
# 1. Run tests on all Python versions
# 2. Build binaries for linux-amd64, linux-arm64
# 3. Create GitHub release with binaries
# 4. Build and push Docker image
```

## 🎯 Use Cases for Agents

This boilerplate is ideal for:

- **SuperCLI Plugins**: Add web interfaces to CLI tools
- **Microservices**: Small HTTP services with CLI management
- **Admin Panels**: Simple admin interfaces for system tools
- **Agent Tools**: CLI tools that agents can control programmatically
- **Development Prototyping**: Quick CLI + web application scaffolding
- **Background Services**: Long-running processes with web monitoring

## 📊 Performance Considerations

### Backend Performance
- **Daemon startup**: < 2 seconds with proper process management
- **HTTP response time**: < 100ms for API endpoints
- **Memory footprint**: ~20MB for daemon process
- **Binary size**: ~10-15MB (includes Python runtime)

### Frontend Performance
- **Initial load**: < 2 seconds with CDN dependencies
- **Route transitions**: < 100ms with hashbang routing
- **Memory usage**: ~50MB for React application
- **Bundle size**: ~200KB total (CDN dependencies cached)

## 🔐 Security Considerations

### Backend Security
- **Input validation**: All CLI arguments validated before processing
- **Process isolation**: Daemon runs with minimal privileges
- **PID file protection**: Proper permissions on PID files
- **Error message sanitization**: No sensitive data in errors

### Frontend Security
- **XSS prevention**: React's built-in escaping
- **CORS handling**: Same-origin policy by default
- **No sensitive data in URLs**: Hashbang routing doesn't expose data
- **Input sanitization**: All user inputs validated

## 📖 Additional References

### Design Philosophy
- **[minimalist-ui skill](.claude/skills/minimalist-ui/)** - Premium minimalist design guidelines
- **[redesign-existing-projects skill](.claude/skills/redesign-existing-projects/)** - Design upgrade principles

### Technical References
- **[Semantic Exit Codes](https://squareup.com/)** - Based on Square Engineering practices
- **[JSON Schema](http://json-schema.org/)** - Schema validation standard
- **[PyInstaller](https://pyinstaller.org/)** - Python binary compilation
- **[React CDN](https://react.dev/)** - React development patterns

### Project Integration
- **[SuperCLI](https://github.com/javimosch/supercli)** - Universal CLI framework

## 📄 License

MIT License - Feel free to use this boilerplate as a reference for your projects. This is provided as-is with no contributions accepted.

## 🙏 Acknowledgments

Designed by **Javier Leandro Arancibia** as a comprehensive reference for 2026 agentic development standards. This boilerplate embodies years of experience in building agent-first systems, modular architectures, and production-ready CLI tools with modern web interfaces.

**Core Philosophy**: Every design decision prioritizes agent reliability, predictability, and efficiency. The goal is to create software that AI agents can use as effectively as human operators, with clear patterns, comprehensive error handling, and predictable behavior.

---

**For agents**: Use the comprehensive documentation in AGENTS.md and the skills directory as your primary reference. This codebase is intentionally well-documented to serve as a learning resource and pattern library for crafting awesome modular applications following 2026 agentic standards.