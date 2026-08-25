from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


STATE_FILE = Path(os.environ.get("XAI_WORKER_STATE_FILE", "/workspace/worker-state.json"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/healthz":
            self.send_error(404)
            return
        payload = {"status": "starting"}
        if STATE_FILE.exists():
            try:
                payload = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                payload = {"status": "unknown", "error": str(exc)}
        if payload.get("status") == "started":
            for pid in payload.get("pids", []):
                try:
                    os.kill(int(pid), 0)
                except (OSError, ValueError):
                    payload = {**payload, "status": "failed", "dead_pid": pid}
                    break
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        status = 200 if payload.get("status") == "started" else 503
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


if __name__ == "__main__":
    port = int(os.environ.get("HEALTH_PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
