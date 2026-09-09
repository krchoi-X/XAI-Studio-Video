"""Discover the tailnet URL a locally served port is published under.

`tailscale serve status` prints one block per served origin:

    https://artxorn.tailf10079.ts.net (tailnet only)
    |-- / proxy http://127.0.0.1:8787

    https://artxorn.tailf10079.ts.net:8790 (tailnet only)
    |-- / proxy http://127.0.0.1:8790

So the tailnet address of a local port is the origin of the block whose root path proxies to it. Detecting this
keeps the tailnet hostname out of the code: the dashboard links the Gallery correctly on any machine, and simply
falls back to the local URL when Tailscale is not serving it.
"""
from __future__ import annotations

import re
import subprocess

ORIGIN = re.compile(r"^(https?://\S+)")
PROXY = re.compile(r"^\|--\s+(?P<path>\S+)\s+proxy\s+(?P<target>\S+)", re.IGNORECASE)


def parse_serve_status(output: str, local_port: int, path: str = "/") -> str | None:
    """Return the tailnet origin serving `path` for http://127.0.0.1:<local_port>, or None."""
    origin: str | None = None
    for raw in output.splitlines():
        line = raw.strip()
        if not line:
            continue
        matched = ORIGIN.match(line)
        if matched and not line.startswith("|--"):
            origin = matched.group(1).rstrip("/")
            continue
        proxied = PROXY.match(line)
        if proxied and origin and proxied.group("path") == path:
            target = proxied.group("target").rstrip("/")
            if target.endswith(f":{local_port}") and ("127.0.0.1" in target or "localhost" in target):
                return origin + "/"
    return None


def detect_served_url(local_port: int, executable: str = "tailscale", timeout: float = 5.0) -> str | None:
    """Ask the Tailscale CLI which tailnet URL publishes a local port. None when it cannot be determined."""
    try:
        result = subprocess.run(
            [executable, "serve", "status"], capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout, check=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return parse_serve_status(result.stdout or "", local_port)
