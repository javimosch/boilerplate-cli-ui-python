# Smoke Test Guide for Boilerplate Python CLI

This skill provides comprehensive smoke testing procedures for the boilerplate-cli-ui-python template. Use this to validate that your implementation works correctly after making changes.

## Quick Agent Installation

Before running smoke tests, install the CLI using agent scripts:

```bash
# Quick install (test immediately)
curl -sSL https://raw.githubusercontent.com/javimosch/boilerplate-cli-ui-python/main/scripts/quick-install.sh | bash

# Permanent installation (for agents)
curl -sSL https://raw.githubusercontent.com/javimosch/boilerplate-cli-ui-python/main/scripts/install-for-agents.sh | bash
```

## Template Location

**Full Path**: `/home/jarancibia/ai/supercli-clis/boilerplate-cli-ui-python`

**GitHub Repository**: https://github.com/javimosch/boilerplate-cli-ui-python

## Quick Smoke Test

```bash
# Navigate to project directory
cd boilerplate-cli-ui-python

# Test basic CLI command
python3 -m src.main greet --name SmokeTest
```

Expected output:
```json
{"version":"1.0","data":{"greeting":"Hello, SmokeTest","name":"SmokeTest","timestamp":"..."},"timestamp":"..."}
```

## Comprehensive Smoke Tests

### 1. CLI Command Tests

#### Test JSON Output (Default)
```bash
python3 -m src.main greet --name TestUser
```
**Expected:** JSON output with greeting data

#### Test Human Mode
```bash
python3 -m src.main greet --name TestUser --human
```
**Expected:** Human-readable text output

#### Test Version Command
```bash
python3 -m src.main version
```
**Expected:** JSON with version information

#### Test Machine-Readable Help
```bash
python3 -m src.main --help-json
```
**Expected:** JSON with command documentation

#### Test Schema Discovery
```bash
python3 -m src.main greet --schema
```
**Expected:** JSON schema for greet command output

### 2. Daemon/Server Tests

#### Test Server Start (Foreground)
```bash
# Start server in foreground (Ctrl+C to stop)
python3 -m src.main start --port 9999
```
**Expected:** Server starts and shows "Server starting on http://127.0.0.1:9999"

#### Test Server Start (Background)
```bash
# Start server as daemon
python3 -m src.main start --port 9999 --daemon
```
**Expected:** JSON response with daemon PID and log file location

#### Test Daemon Status
```bash
python3 -m src.main status
```
**Expected:** JSON with daemon status (running/not_running)

#### Test Daemon Stop
```bash
python3 -m src.main stop
```
**Expected:** JSON confirming daemon stopped

### 3. HTTP API Tests

#### Test Root Endpoint
```bash
# Start server first: python3 -m src.main start --port 9999
curl -s http://localhost:9999/
```
**Expected:** JSON with API information

#### Test Status Endpoint
```bash
curl -s http://localhost:9999/api/status
```
**Expected:** JSON with server status, uptime, port

#### Test Health Endpoint
```bash
curl -s http://localhost:9999/api/health
```
**Expected:** JSON with health status

### 4. Error Handling Tests

#### Test Invalid Port
```bash
python3 -m src.main start --port invalid
```
**Expected:** JSON error with code 85 (invalid_argument)

#### Test Resource Not Found
```bash
python3 -m src.main status --schema
```
**Expected:** JSON error with code 92 (resource_not_found) for schema

### 5. Docker Tests

#### Test Docker Build
```bash
docker build -t boilerplate-cli-ui-python .
```
**Expected:** Successful build with image ID

#### Test Docker Container CLI
```bash
docker run --rm boilerplate-cli-ui-python python -m src.main greet --name DockerTest
```
**Expected:** JSON greeting from container

#### Test Docker Compose
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```
**Expected:** Services start successfully, logs visible, clean shutdown

### 6. Configuration Tests

#### Test Environment Variables
```bash
export BOILERPLATE_PORT=3000
python3 -m src.main start --daemon
python3 -m src.main status
```
**Expected:** Daemon uses custom port from environment

#### Test NO_COLOR
```bash
export NO_COLOR=1
python3 -m src.main greet --human
```
**Expected:** Output without ANSI color codes

## Binary Compilation Tests

### Local Binary Compilation

#### Test PyInstaller Build
```bash
# Install PyInstaller
pip install pyinstaller

# Build binary
pyinstaller --onefile --name boilerplate-cli-ui-python --add-data "schemas:schemas" --hidden-import=src src/main.py

# Test binary
./dist/boilerplate-cli-ui-python greet --name BinaryTest
```
**Expected:** Binary executes and produces JSON output

### GitHub Release Binary Tests

#### Download and Test Binary
```bash
# Download latest release (when available)
wget https://github.com/javimosch/boilerplate-cli-ui-python/releases/latest/download/boilerplate-cli-ui-python-linux-amd64

# Make executable
chmod +x boilerplate-cli-ui-python-linux-amd64

# Test binary
./boilerplate-cli-ui-python-linux-amd64 greet --name ReleaseTest
```
**Expected:** Binary executes and produces JSON output

#### Test Installation Script
```bash
curl -sSL https://raw.githubusercontent.com/javimosch/boilerplate-cli-ui-python/main/install.sh | bash
boilerplate-cli-ui-python greet --name InstallTest
```
**Expected:** Binary installs to /usr/local/bin and executes correctly

## Automated Smoke Test Script

Create `scripts/smoke-test.sh`:

```bash
#!/bin/bash
set -e

echo "=== Boilerplate CLI UI Python Smoke Tests ==="

# Test 1: Basic CLI
echo "Test 1: Basic CLI command"
python3 -m src.main greet --name SmokeTest | jq -e '.data.greeting == "Hello, SmokeTest"'

# Test 2: Human mode
echo "Test 2: Human mode"
python3 -m src.main greet --name HumanTest --human | grep -q "Hello, HumanTest"

# Test 3: Version command
echo "Test 3: Version command"
python3 -m src.main version | jq -e '.data.version == "1.0.0"'

# Test 4: Help JSON
echo "Test 4: Help JSON"
python3 -m src.main --help-json | jq -e '.data.commands.greet'

# Test 5: Schema discovery
echo "Test 5: Schema discovery"
python3 -m src.main greet --schema | jq -e '.data.properties'

# Test 6: Docker build
echo "Test 6: Docker build"
docker build -t boilerplate-cli-ui-python . > /dev/null
echo "Docker build successful"

# Test 7: Docker container
echo "Test 7: Docker container"
docker run --rm boilerplate-cli-ui-python python -m src.main greet --name DockerSmokeTest | jq -e '.data.greeting == "Hello, DockerSmokeTest"'

echo "=== All smoke tests passed ==="
```

Run with:
```bash
chmod +x scripts/smoke-test.sh
./scripts/smoke-test.sh
```

## Validation Checklist

After making changes, ensure:

- [ ] All CLI commands return valid JSON
- [ ] Human mode (--human) produces readable output
- [ ] Semantic exit codes are correct (0, 80-119)
- [ ] Error messages include recovery suggestions
- [ ] Daemon start/stop/status work correctly
- [ ] HTTP API endpoints return valid JSON
- [ ] Docker build succeeds
- [ ] Docker container executes CLI correctly
- [ ] Environment variables are respected
- [ ] Schema discovery works for all commands
- [ ] Help JSON is complete and accurate

## Common Issues and Fixes

### Issue: "Address already in use"
**Fix:** Use different port or kill existing process: `lsof -ti:PORT | xargs kill -9`

### Issue: PyInstaller build fails
**Fix:** Ensure Python 3.10+ is used, check for missing dependencies in hidden-imports

### Issue: Docker container can't find schemas
**Fix:** Ensure schemas directory is copied in Dockerfile with correct permissions

### Issue: Daemon PID file persists after crash
**Fix:** Manually remove PID file: `rm /tmp/boilerplate-cli-ui-python.pid`

### Issue: JSON output has RuntimeWarning
**Fix:** This is a Python module import warning, can be ignored or fixed by using `python -m` correctly

## Integration with CI/CD

Add to GitHub Actions workflow:

```yaml
- name: Smoke Tests
  run: |
    python3 -m src.main greet --name CITest | jq -e '.data.greeting == "Hello, CITest"'
    python3 -m src.main --help-json | jq -e '.data.commands'
    docker build -t boilerplate-cli-ui-python .
    docker run --rm boilerplate-cli-ui-python python -m src.main version
```

## Performance Benchmarks

Track binary size and startup time:

```bash
# Binary size
ls -lh dist/boilerplate-cli-ui-python

# Startup time
time ./dist/boilerplate-cli-ui-python version
```

Expected results:
- Binary size: ~10-15MB (PyInstaller)
- Startup time: <1 second

## Notes for Extending This Template

When using this boilerplate as a template:

1. **Update smoke tests** to match your new commands
2. **Add schema validation** for new command outputs
3. **Test error paths** for custom error types
4. **Validate exit codes** match your error definitions
5. **Test daemon functionality** with your specific use case
6. **Update Docker tests** if you add dependencies
7. **Document any custom smoke tests** in your project's AGENTS.md

This smoke test guide ensures your agent-first CLI implementation maintains quality and reliability across different deployment scenarios.