"""Optional Studio sync: POST /api/sync."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class SyncResult:
    ok: bool
    status_code: int | None
    message: str
    body: Any = None


def post_sync(sync_url: str, *, timeout: float = 120.0) -> SyncResult:
    """POST to Studio sync endpoint. Does not touch media files."""
    url = sync_url.strip()
    if not url:
        return SyncResult(ok=False, status_code=None, message="empty sync-url")

    data = b"{}"
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            code = getattr(resp, "status", None) or resp.getcode()
            try:
                body = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                body = raw
            return SyncResult(ok=True, status_code=code, message="sync ok", body=body)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)
        return SyncResult(ok=False, status_code=exc.code, message=f"sync HTTP {exc.code}: {raw[:500]}")
    except urllib.error.URLError as exc:
        return SyncResult(ok=False, status_code=None, message=f"sync connection failed: {exc.reason}")
    except TimeoutError:
        return SyncResult(ok=False, status_code=None, message="sync timed out")
