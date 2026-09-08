"""
The embedded guide and command catalog (cli-guide-spec, cli-output-spec §4).

Compiled into the distribution: an agent that lands on a machine with this tool
and no network can still learn it. Never fetch this at runtime.
"""

import json

TOOL = "boilerplate-cli-ui-python"
VERSION = "1.0.0"


def guide_dict() -> dict:
    return {
        TOOL: "An agent-first Python CLI with an embedded web UI and a JSON HTTP API.",
        "version": VERSION,
        "one_liner": (
            "Starts an HTTP server that serves a React dashboard at / and a JSON API at "
            "/api/*, from a PyInstaller single-file binary — JSON on stdout by default, "
            "with --human as the opt-in for people."
        ),
        "model": {
            "binary": "PyInstaller bundles the interpreter, the stdlib and the UI templates into one file.",
            "server": "http.server with an explicit handler, bound to an explicit host:port.",
            "daemon": "re-execs itself as `serve`, detached, with /_health as the source of truth for liveness.",
            "output": "JSON by default even on a TTY; --human is the opt-in, which is the inverse of the usual CLI default.",
            "contract": "agent-first: data on stdout, context on stderr, semantic exit codes, typed errors, an embedded guide.",
        },
        "loop": [
            "./build.sh — PyInstaller bundle, or run from source with python -m src.main",
            f"./{TOOL} serve — foreground on 127.0.0.1:8080",
            "open http://127.0.0.1:8080/ for the UI, or curl /api/status for JSON",
            f"./{TOOL} daemon start — background it instead",
            f"./{TOOL} daemon stop — stop it",
        ],
        "concepts": {
            "JSON by default": "Commands emit JSON on stdout with no flag. --human switches to prose for people.",
            "loopback default": "serve binds 127.0.0.1 unless --host says otherwise. Binding the whole network is deliberate.",
            "shutdown token": "off-loopback, POST /_shutdown requires X-Shutdown-Token matching $SHUTDOWN_TOKEN, or it answers 403 and keeps running.",
            "exit codes": "0 ok, 80-89 input, 90-99 state, 100-109 external, 110-119 internal. The code equals .error.code in the body.",
            "schemas": "--schema on a command prints its JSON Schema from schemas/, so an agent can validate before parsing.",
        },
        "commands": {
            "server": [
                f"{TOOL} serve [--host H] [--port N]",
                f"{TOOL} daemon start [--port N]",
                f"{TOOL} daemon stop [--port N]",
                f"{TOOL} daemon status [--port N]",
            ],
            "app": [
                f"{TOOL} greet [--name N]",
            ],
            "introspection": [
                f"{TOOL} guide [--human]",
                f"{TOOL} help-json",
                f"{TOOL} version [--json]",
            ],
        },
        "examples": [
            {"goal": "serve the UI on a custom port", "do": [f"./{TOOL} serve --port 3000"]},
            {
                "goal": "background it and confirm it is up",
                "do": [f"./{TOOL} daemon start --port 3000", f"./{TOOL} daemon status --port 3000"],
            },
            {
                "goal": "expose it on the LAN with a kill switch that needs a token",
                "do": [f"SHUTDOWN_TOKEN=s3cret ./{TOOL} serve --host 0.0.0.0 --port 8080"],
            },
        ],
        "gotchas": [
            "Output is JSON by default, including on a TTY. Pass --human if you are reading it yourself.",
            "serve binds 127.0.0.1 by default. If you expected it on the LAN, pass --host 0.0.0.0 — and then set SHUTDOWN_TOKEN, or /_shutdown answers 403 to everyone.",
            "daemon start is idempotent: called twice it reports the running instance instead of racing a second process onto the port.",
            "daemon stop against a stopped daemon exits 0 — a no-op success, not an error.",
            "Server logs go to stderr. An agent parsing stdout sees only data.",
        ],
        "see_also": ["https://cli-specs.intrane.fr"],
    }


def guide_json() -> str:
    return json.dumps(guide_dict())


def guide_markdown() -> str:
    return f"""# {TOOL}

An agent-first Python CLI with an embedded web UI and a JSON HTTP API.

## Model

- One PyInstaller binary: interpreter, stdlib and UI templates bundled in.
- http.server bound to an explicit host:port.
- The daemon re-execs itself as `serve`, detached; /_health is liveness.
- JSON on stdout by default; `--human` is the opt-in for people.

## Loop

1. `./build.sh`
2. `./{TOOL} serve`
3. Open http://127.0.0.1:8080/ or curl /api/status.
4. `./{TOOL} daemon start` to background it.
5. `./{TOOL} daemon stop` to stop it.

## Commands

- `serve [--host H] [--port N]`
- `daemon start|stop|status [--port N]`
- `greet [--name N]`
- `guide [--human]`, `help-json`, `version [--json]`

## Gotchas

- Output is JSON by default, even on a TTY. `--human` switches to prose.
- `serve` binds 127.0.0.1 by default; `--host 0.0.0.0` is deliberate.
- Off-loopback, `POST /_shutdown` needs `X-Shutdown-Token` = `$SHUTDOWN_TOKEN`.
- `daemon start` twice is idempotent; `daemon stop` when stopped exits 0.
"""


def llms_txt() -> str:
    return f"""# {TOOL}

An agent-first Python CLI with an embedded web UI.

## Drive it

    {TOOL} serve [--host H] [--port N]
    {TOOL} daemon start|stop|status [--port N]

JSON on stdout, context on stderr, exit 0/80-119.

## Learn it

    {TOOL} guide      # embedded, JSON
    {TOOL} help-json  # command catalog

HTTP: GET /  GET /api/status  GET /_health  POST /_shutdown  GET /guide
"""


def help_json() -> str:
    return json.dumps(
        {
            "version": "1.0",
            "tool": TOOL,
            "tool_version": VERSION,
            "commands": [
                {
                    "name": "serve",
                    "summary": "run the HTTP server in the foreground",
                    "flags": [
                        {"name": "--host", "summary": "bind address", "default": "127.0.0.1", "env": "BOILERPLATE_HOST"},
                        {"name": "--port", "summary": "port", "default": "8080", "env": "BOILERPLATE_PORT"},
                    ],
                },
                {"name": "daemon start", "summary": "start the server in the background (idempotent)"},
                {"name": "daemon stop", "summary": "stop the background server (no-op success if stopped)"},
                {"name": "daemon status", "summary": "report background server status"},
                {
                    "name": "greet",
                    "summary": "greet someone",
                    "flags": [{"name": "--name", "summary": "name to greet"}],
                },
                {
                    "name": "guide",
                    "summary": "the embedded operator guide",
                    "flags": [{"name": "--human", "summary": "markdown instead of JSON"}],
                },
                {"name": "help-json", "summary": "this machine-readable command catalog"},
                {
                    "name": "version",
                    "summary": "print the version",
                    "flags": [{"name": "--json", "summary": "JSON output (the default)"}],
                },
            ],
            "endpoints": [
                {"method": "GET", "path": "/", "summary": "the embedded web UI"},
                {"method": "GET", "path": "/api/status", "summary": "app status JSON"},
                {"method": "GET", "path": "/_health", "summary": "liveness: {ok,service,pid}"},
                {"method": "POST", "path": "/_shutdown", "summary": "stop the server; token-gated off-loopback"},
                {"method": "GET", "path": "/guide", "summary": "the guide over HTTP"},
                {"method": "GET", "path": "/llms.txt", "summary": "the short agent-facing README"},
            ],
            "exit_codes": {
                "0": "success",
                "85": "invalid argument or unknown command",
                "86": "bad permissions",
                "87": "validation error",
                "92": "resource not found",
                "105": "connection timeout",
                "110": "internal error",
            },
            "env": [
                {"name": "BOILERPLATE_PORT", "summary": "default port"},
                {"name": "BOILERPLATE_HOST", "summary": "default bind address"},
                {"name": "SHUTDOWN_TOKEN", "summary": "required by POST /_shutdown when bound off-loopback"},
                {"name": "NO_COLOR", "summary": "disable colour in --human output"},
            ],
            "see_also": [f"{TOOL} guide", "https://cli-specs.intrane.fr"],
        }
    )
