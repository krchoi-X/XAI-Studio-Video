"""FastAPI application: JSON snapshot endpoints, SSE live stream, read-only artifact serving, bundled UI."""
from __future__ import annotations

import asyncio
import json
import logging
import mimetypes
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response, StreamingResponse

from . import __version__
from .config import Config
from .monitor import MonitorService

log = logging.getLogger("control_tower.app")
STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app(config: Config | None = None, monitor: MonitorService | None = None) -> FastAPI:
    config = config or Config.from_env()
    service = monitor or MonitorService(config)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        service.start()
        try:
            yield
        finally:
            service.stop()

    app = FastAPI(title="XAI Control Tower", version=__version__, lifespan=lifespan, docs_url="/api/docs", redoc_url=None)
    app.state.monitor = service
    app.state.config = config

    # ------------------------------------------------------------------ pages
    @app.get("/", include_in_schema=False)
    async def index() -> HTMLResponse:
        page = STATIC_DIR / "index.html"
        return HTMLResponse(page.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------ api
    @app.get("/api/health")
    async def health() -> dict[str, Any]:
        host_ok = bool(service.host and service.host.ok)
        return {
            "ok": True,
            "version": __version__,
            "monitor_alive": bool(service._thread and service._thread.is_alive()),
            "snapshot_version": service.version,
            "gpu_ok": host_ok,
            "gpu_error": None if host_ok else (service.host.error if service.host else "not sampled yet"),
            "jobs_total": len(service.jobs),
            "adapter_errors": service.job_errors,
        }

    @app.get("/api/overview")
    async def overview() -> dict[str, Any]:
        return service.overview()

    @app.get("/api/host")
    async def host(history_minutes: float = Query(30.0, ge=1, le=360)) -> dict[str, Any]:
        data = service.host.to_dict() if service.host else {"ok": False, "error": "not sampled yet", "gpus": []}
        data["history"] = service.db.recent_host_samples(minutes=history_minutes)
        data["untracked"] = service.untracked()
        return data

    @app.get("/api/processes")
    async def processes() -> dict[str, Any]:
        return service.procs.to_dict() if service.procs else {"processes": [], "agents": [], "scanned_at": None, "total_processes": 0, "error": "not scanned yet"}

    @app.get("/api/jobs")
    async def jobs(status: str | None = None, source: str | None = None, limit: int = Query(200, ge=1, le=2000)) -> dict[str, Any]:
        rows = [j.to_dict() for j in service.jobs]
        if status:
            rows = [r for r in rows if r["status"] == status or r["outcome"] == status]
        if source:
            rows = [r for r in rows if r["source"] == source]
        rows.sort(key=lambda r: (0 if r["is_active"] else 1, r.get("finished_at") or r.get("updated_at") or r.get("created_at") or ""), reverse=False)
        active = [r for r in rows if r["is_active"]]
        done = sorted((r for r in rows if not r["is_active"]), key=lambda r: r.get("finished_at") or r.get("updated_at") or "", reverse=True)
        return {"jobs": (active + done)[:limit], "total": len(rows)}

    @app.get("/api/jobs/history")
    async def job_history(limit: int = Query(100, ge=1, le=2000), status: str | None = None, source: str | None = None) -> dict[str, Any]:
        return {"jobs": service.db.list_jobs(limit=limit, status=status, source=source)}

    @app.get("/api/jobs/{job_id:path}/outputs/{index}")
    async def job_output(job_id: str, index: int, request: Request) -> Response:
        job = _find_job(service, job_id)
        if job is None:
            raise HTTPException(404, "job not found")
        outputs = job.outputs
        if index < 0 or index >= len(outputs):
            raise HTTPException(404, "output index out of range")
        path = Path(outputs[index].path)
        if not path.is_file():
            raise HTTPException(404, "output file missing on disk")
        media_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        return FileResponse(str(path), media_type=media_type, filename=path.name, content_disposition_type="inline")

    @app.get("/api/jobs/{job_id:path}")
    async def job_detail(job_id: str) -> dict[str, Any]:
        job = _find_job(service, job_id)
        if job is None:
            stored = service.db.get_job(job_id)
            if stored is None:
                raise HTTPException(404, "job not found")
            stored["from_history"] = True
            return stored
        data = job.to_dict()
        if job.run_dir and job.source == "wangp-run":
            events_path = Path(job.run_dir) / "events.jsonl"
            if events_path.is_file():
                lines = events_path.read_text(encoding="utf-8", errors="replace").splitlines()
                tail = []
                for line in lines[-25:]:
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    event.pop("preview", None) if not isinstance(event.get("preview"), dict) else event["preview"].pop("image", None)
                    tail.append(event)
                data["recent_events"] = tail
        return data

    @app.get("/api/timings")
    async def timings() -> dict[str, Any]:
        return {"step_timings": service.db.list_step_timings()}

    @app.get("/api/events")
    async def events(request: Request) -> StreamingResponse:
        async def stream():
            version = -1
            full_version = -1
            loop = asyncio.get_running_loop()
            yield ": connected\n\n"
            while not service._stop.is_set():
                if await request.is_disconnected():
                    break
                frame, version, full_version = await loop.run_in_executor(None, sse_frame, service, version, full_version, 5.0)
                yield frame

        return StreamingResponse(stream(), media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"})

    @app.exception_handler(Exception)
    async def unhandled(_: Request, exc: Exception) -> JSONResponse:
        log.exception("unhandled error")
        return JSONResponse({"error": str(exc)}, status_code=500)

    return app


def sse_frame(service: MonitorService, version: int, full_version: int, timeout: float) -> tuple[str, int, int]:
    """Block until the monitor publishes a newer snapshot (or timeout) and return one SSE frame.

    A full `overview` event is sent when processes/jobs changed; a small `host` event when only the
    GPU sample changed; a comment keepalive on timeout.
    """
    new_version = service.wait_for_change(version, timeout)
    if new_version == version:
        return ": keepalive\n\n", version, full_version
    if service.full_version != full_version:
        payload = json.dumps(service.overview(), ensure_ascii=False)
        return f"event: overview\nid: {new_version}\ndata: {payload}\n\n", new_version, service.full_version
    payload = json.dumps(service.host_view(), ensure_ascii=False)
    return f"event: host\nid: {new_version}\ndata: {payload}\n\n", new_version, full_version


def _find_job(service: MonitorService, job_id: str):
    for job in service.jobs:
        if job.job_id == job_id:
            return job
    return None
