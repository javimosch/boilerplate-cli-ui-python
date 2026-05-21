# Boilerplate Python CLI Usage Guide

This skill teaches agents how to use the agent-first Python CLI boilerplate for crafting CLI applications.

## Quick Start

### Basic Commands

```bash
# Greet command (JSON output by default)
python -m src.main greet
# Output: {"version":"1.0","data":{"greeting":"Hello, World","timestamp":"2026-05-21T23:21:00Z"},"timestamp":"2026-05-21T23:21:00Z"}

# Greet with custom name
python -m src.main greet --name Alice
# Output: {"version":"1.0","data":{"greeting":"Hello, Alice","timestamp":"..."},"timestamp":"..."}

# Human-readable output
python -m src.main greet --name Alice --human
# Output: greeting: Hello, Alice
#         name: Alice
#         timestamp: 2026-05-21T23:21:00Z

# Version command
python -m src.main version
# Output: {"version":"1.0","data":{"name":"boilerplate-cli-ui-python","version":"1.0.0","timestamp":"..."},"timestamp":"..."}
```

### Daemon/Server Commands

```bash
# Start server in foreground (for development)
python -m src.main start --port 8080
# Output: {"version":"1.0","data":{"mode":"foreground","port":8080,"timestamp":"..."},"timestamp":"..."}

# Start server as daemon (background)
python -m src.main start --port 8080 --daemon
# Output: {"version":"1.0","data":{"mode":"daemon","port":8080,"pid":12345,"log_file":"/tmp/...","timestamp":"..."},"timestamp":"..."}

# Check daemon status
python -m src.main status
# Output: {"version":"1.0","data":{"status":"running","pid":12345,"log_file":"/tmp/...","timestamp":"..."},"timestamp":"..."}

# Stop daemon
python -m src.main stop
# Output: {"version":"1.0","data":{"status":"stopped","pid":12345,"timestamp":"..."},"timestamp":"..."}
```

### Machine-Readable Help

```bash
# Get machine-readable help
python -m src.main --help-json
# Output: {"version":"1.0.0","commands":{"greet":{...},"version":{...},...},"output_formats":["json","human"],"exit_codes":{...}}

# Get schema for specific command
python -m src.main greet --schema
# Output: {"$schema":"http://json-schema.org/draft-07/schema#","type":"object","properties":{...}}
```

## Environment Variables

Configure behavior using environment variables:

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

## HTTP API Usage

When the server is running, interact via HTTP API:

```bash
# API information
curl http://localhost:8080/
# Output: {"name":"boilerplate-cli-ui-python","version":"1.0.0","description":"...","endpoints":{...}}

# Server status
curl http://localhost:8080/api/status
# Output: {"status":"running","port":8080,"uptime_seconds":123.45,"start_time":"...","timestamp":"..."}

# Health check
curl http://localhost:8080/api/health
# Output: {"status":"healthy","timestamp":"..."}
```

## Error Handling

All errors follow structured format:

```bash
# Invalid argument
python -m src.main start --port invalid
# Output: {"error":{"code":85,"type":"invalid_argument","message":"Invalid port number","details":{...},"recoverable":false,"retry_after":null,"suggestions":[...]}}

# Check exit code
echo $?
# Output: 85
```

## Exit Code Reference

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

## Agent Usage Patterns

### Parse JSON Output

```bash
# Extract specific field
python -m src.main greet --name Alice | jq -r '.data.greeting'
# Output: Hello, Alice

# Extract timestamp
python -m src.main greet | jq -r '.data.timestamp'
# Output: 2026-05-21T23:21:00Z
```

### Compose Commands

```bash
# Get status, check if running, then stop
if python -m src.main status | jq -r '.data.status' | grep -q running; then
    python -m src.main stop
fi
```

### Error Recovery

```bash
# Retry on connection timeout
python -m src.main start || exit_code=$?
if [ $exit_code -eq 105 ]; then
    sleep 2
    python -m src.main start
fi
```

## Binary Usage

After building with `./build.sh`:

```bash
# Use binary directly
./boilerplate-cli-ui-python greet --name Alice

# Move to PATH
sudo cp boilerplate-cli-ui-python /usr/local/bin/boilerplate-cli-ui-python
boilerplate-cli-ui-python greet
```

## Docker Usage

```bash
# Build image
docker build -t boilerplate-cli-ui-python .

# Run commands
docker run --rm boilerplate-cli-ui-python greet --name Alice

# Start server
docker run -p 8080:8080 boilerplate-cli-ui-python start --port 8080
```

## Common Workflows

### Development Workflow

```bash
# 1. Start server in foreground
python -m src.main start --port 8080

# 2. In another terminal, test API
curl http://localhost:8080/api/status

# 3. Stop with Ctrl+C
```

### Production Workflow

```bash
# 1. Start as daemon
python -m src.main start --port 8080 --daemon

# 2. Check status
python -m src.main status

# 3. View logs
tail -f /tmp/boilerplate-cli-ui-python.log

# 4. Stop when done
python -m src.main stop
```

### Agent Integration Workflow

```bash
# 1. Discover capabilities
python -m src.main --help-json > capabilities.json

# 2. Get schema for validation
python -m src.main greet --schema > greet.schema.json

# 3. Execute command
python -m src.main greet --name Alice > output.json

# 4. Validate output
jq -f greet.schema.json output.json

# 5. Parse result
jq -r '.data.greeting' output.json
```

## Troubleshooting

### Port Already in Use

```bash
# Error: resource_conflict (code 94)
# Solution: Use different port or stop existing process
python -m src.main start --port 8081
```

### Permission Denied

```bash
# Error: permission_denied (code 86)
# Solution: Check file permissions or run with appropriate privileges
```

### Daemon Not Running

```bash
# Check status first
python -m src.main status

# If not_running, start it
python -m src.main start --daemon
```

## Best Practices

1. **Always parse JSON output** - Don't rely on text parsing
2. **Check exit codes** - Use semantic codes for decision-making
3. **Use --help-json** - Discover capabilities programmatically
4. **Validate schemas** - Use --schema to validate output
5. **Handle errors** - Check error.recoverable field
6. **Log to stderr** - Keep stdout clean for data
7. **Use environment variables** - Configure without flags