"""
Daemon lifecycle (cli-daemon-spec §4).

The tool has an embedded HTTP server, so /_health is the source of truth for
whether the daemon is up — not the pid file, which goes stale when a process
dies without cleaning up. Every subcommand is idempotent.

The health probe uses urllib from the stdlib: no dependency, and the request is
one round trip on loopback.
"""

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

from .errors import (
    EXIT_CONNECTION_TIMEOUT,
    EXIT_INTERNAL_ERROR,
    CLIError,
)

PID_FILE = os.environ.get("BOILERPLATE_PID_FILE", "/tmp/boilerplate-cli-ui-python.pid")
LOG_FILE = os.environ.get("BOILERPLATE_LOG_FILE", "/tmp/boilerplate-cli-ui-python.log")


def _emit(payload: dict) -> None:
    print(json.dumps(payload))


def probe_health(port: int) -> bool:
    """True when something answers 200 on /_health."""
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/_health", timeout=0.5
        ) as resp:
            return resp.status == 200
    except Exception:
        return False


def wait_for(port: int, want: bool) -> bool:
    """Polls every 100ms for up to 5s, rather than sleeping a fixed amount (§4)."""
    for _ in range(50):
        if probe_health(port) == want:
            return True
        time.sleep(0.1)
    return False


def _self_command() -> list:
    """The argv prefix that re-invokes this tool.

    Under PyInstaller sys.executable *is* the tool; from source it is the
    interpreter and the package has to be named explicitly.
    """
    if getattr(sys, "frozen", False):
        return [sys.executable]
    return [sys.executable, "-m", "src.main"]


def start(host: str, port: int) -> None:
    """Idempotent: an already-healthy port means report it and succeed, rather
    than racing a second process onto it (§4)."""
    if probe_health(port):
        _emit({"ok": True, "running": True, "already_running": True, "port": port})
        return

    try:
        log = open(LOG_FILE, "ab")
    except OSError as e:
        raise CLIError(
            code=EXIT_INTERNAL_ERROR,
            error_type="log_unwritable",
            message=f"cannot open {LOG_FILE}: {e}",
            recoverable=False,
            suggestions=["check permissions on /tmp"],
        )

    cmd = _self_command() + ["serve", f"--host={host}", f"--port={port}"]

    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=log,
            start_new_session=True,
            cwd=os.getcwd(),
        )
    except OSError as e:
        raise CLIError(
            code=EXIT_INTERNAL_ERROR,
            error_type="spawn_failed",
            message=f"cannot start the daemon: {e}",
            recoverable=False,
            suggestions=[f"boilerplate-cli-ui-python serve --port {port}"],
        )

    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

    if not wait_for(port, True):
        process.kill()
        _remove_pid()
        raise CLIError(
            code=EXIT_CONNECTION_TIMEOUT,
            error_type="daemon_unhealthy",
            message=(
                f"started pid {process.pid} but /_health never answered on port "
                f"{port} (see {LOG_FILE})"
            ),
            recoverable=True,
            retry_after=2,
            suggestions=[f"boilerplate-cli-ui-python serve --port {port}"],
        )

    _emit(
        {
            "ok": True,
            "running": True,
            "already_running": False,
            "pid": process.pid,
            "port": port,
            "log": LOG_FILE,
        }
    )


def stop(port: int) -> None:
    """A no-op success when nothing is running: an agent stopping an
    already-stopped daemon has got what it asked for (§4)."""
    if not probe_health(port):
        _remove_pid()
        _emit({"ok": True, "running": False, "stopped": False, "port": port})
        return

    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/_shutdown", data=b"", method="POST"
    )
    token = os.environ.get("SHUTDOWN_TOKEN", "")
    if token:
        req.add_header("X-Shutdown-Token", token)

    try:
        with urllib.request.urlopen(req, timeout=2) as resp:
            status = resp.status
    except urllib.error.HTTPError as e:
        raise CLIError(
            code=EXIT_CONNECTION_TIMEOUT,
            error_type="shutdown_refused",
            message=f"POST /_shutdown returned {e.code}",
            recoverable=False,
            suggestions=["set SHUTDOWN_TOKEN if the daemon is bound off-loopback"],
        )
    except Exception as e:
        raise CLIError(
            code=EXIT_CONNECTION_TIMEOUT,
            error_type="shutdown_failed",
            message=f"POST /_shutdown failed: {e}",
            recoverable=True,
            retry_after=1,
            suggestions=[f"boilerplate-cli-ui-python daemon status --port {port}"],
        )

    if status != 200:
        raise CLIError(
            code=EXIT_CONNECTION_TIMEOUT,
            error_type="shutdown_refused",
            message=f"POST /_shutdown returned {status}",
            recoverable=False,
            suggestions=["set SHUTDOWN_TOKEN if the daemon is bound off-loopback"],
        )

    wait_for(port, False)
    _remove_pid()
    _emit({"ok": True, "running": False, "stopped": True, "port": port})


def status(port: int) -> None:
    """Status only ever reads — it never carries the shutdown token (§4)."""
    if not probe_health(port):
        _emit({"ok": True, "running": False, "port": port})
        return

    pid = 0
    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip() or 0)
    except (OSError, ValueError):
        pid = 0

    _emit({"ok": True, "running": True, "pid": pid, "port": port, "log": LOG_FILE})


def _remove_pid() -> None:
    try:
        os.remove(PID_FILE)
    except OSError:
        pass
