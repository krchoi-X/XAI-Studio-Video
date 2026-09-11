#!/usr/bin/env python3
"""Run a named list of shots through the local WanGP worker, one at a time, and record the result.

    python tools/identity_batch.py --session-dir SESSION --output-dir OUT --shots turn-01 turn-02

Each shot is `<session>/<shot>.txt` plus `<session>/<shot>.settings.json`, the pair `local_wangp.py submit`
already expects. The batch submits one, waits for it to reach a terminal state, then submits the next: the
worker holds a GPU lock, so overlapping submissions fail rather than queue.

Before every shot it asks Ollama to unload. On an 8 GB card a resident local LLM costs several gigabytes,
and the Krea2 RAW path already offloads constantly at that size - two large models on one laptop GPU is the
difference between a slow render and a failed one. The unload is best-effort: no Ollama, no problem.

Phase 1 ran its batch from a script that was never committed, so its method could not be repeated. This is
that script, kept.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
TERMINAL = {"succeeded", "needs_review", "failed", "cancelled", "interrupted", "timed_out"}
OLLAMA_UNLOAD = "http://127.0.0.1:11434/api/generate"


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(message: str) -> None:
    print(f"[{now()}] {message}", flush=True)


def unload_ollama() -> str:
    """Best effort: ask every loaded model to leave VRAM, then confirm."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/ps", timeout=10) as response:
            loaded = json.loads(response.read()).get("models", [])
    except (urllib.error.URLError, OSError, ValueError):
        return "ollama not reachable"
    for model in loaded:
        payload = json.dumps({"model": model["name"], "keep_alive": 0}).encode()
        request = urllib.request.Request(OLLAMA_UNLOAD, data=payload, headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(request, timeout=60).read()
        except (urllib.error.URLError, OSError):
            pass
    return f"unloaded {len(loaded)} model(s)" if loaded else "nothing loaded"


def submit(session: Path, shot: str, output_dir: Path, requested_by: str) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(TOOLS / "local_wangp.py"), "submit",
         "--runs-root", str(session / "runs"),
         "--prompt-file", str(session / f"{shot}.txt"),
         "--settings-file", str(session / f"{shot}.settings.json"),
         "--project-id", session.name, "--prompt-id", shot,
         "--output-dir", str(output_dir), "--requested-by", requested_by],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return json.loads(result.stdout)


def stop_worker(pid: int | None) -> str:
    """Kill the worker this batch started.

    Giving up on a run is not the same as ending it. The worker is detached and holds an exclusive GPU lock,
    so a batch that merely stops waiting leaves every later shot to fail instantly against that lock - which
    is exactly how one stalled clip consumed nine of twelve shots on 2026-09-11. Time out, then kill.
    """
    if not pid:
        return "no pid recorded"
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True, check=False)
        else:
            os.kill(pid, signal.SIGKILL)
    except OSError as error:
        return f"could not kill {pid}: {error}"
    time.sleep(10)
    return f"killed worker {pid}"


def wait(run_dir: Path, timeout_minutes: int, stall_minutes: int, pid: int | None) -> dict[str, Any]:
    deadline = time.time() + timeout_minutes * 60
    last, last_change = None, time.time()
    while time.time() < deadline:
        # Time the read itself. When the machine starts thrashing, these calls block for minutes at a time,
        # which is how a 30 minute deadline once let a shot run for 92: the deadline is only tested between
        # iterations, so a single blocked iteration outlives it. A read that slow is itself the symptom.
        tick = time.time()
        try:
            record = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            time.sleep(10)
            continue
        if time.time() - tick > stall_minutes * 60:
            log(f"  {run_dir.name}: a status read blocked for "
                f"{(time.time() - tick) / 60:.0f} min - {stop_worker(pid)}")
            return {"status": "timed_out", "note": "the machine stalled while the shot was running"}
        if record.get("status") in TERMINAL:
            return record
        progress = (record.get("status"), (run_dir / "worker.stderr.log").stat().st_size
                    if (run_dir / "worker.stderr.log").is_file() else 0)
        if progress != last:
            if progress[0] != (last or (None, 0))[0]:
                log(f"  {run_dir.name}: {progress[0]}")
            last, last_change = progress, time.time()
        # A healthy H3 clip writes a progress line every 25-30 seconds. Silence for many minutes means the
        # weights are thrashing rather than working, and waiting out the full timeout only wastes the night.
        if time.time() - last_change > stall_minutes * 60:
            log(f"  {run_dir.name}: no output for {stall_minutes} min - {stop_worker(pid)}")
            return {"status": "timed_out", "note": f"stalled: no worker output for {stall_minutes} minutes"}
        time.sleep(20)
    log(f"  {run_dir.name}: timeout - {stop_worker(pid)}")
    return {"status": "timed_out", "note": f"batch stopped waiting after {timeout_minutes} minutes"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--session-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--shots", nargs="+", required=True)
    parser.add_argument("--requested-by", default="claude")
    parser.add_argument("--timeout-minutes", type=int, default=180)
    parser.add_argument("--stall-minutes", type=int, default=12,
                        help="give up on a shot whose worker has written nothing for this long")
    parser.add_argument("--result", help="where to write the batch record (default <session>/batch-result.json)")
    args = parser.parse_args()

    session = Path(args.session_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = Path(args.result) if args.result else session / "batch-result.json"

    results = []
    for shot in args.shots:
        log(f"{shot}: {unload_ollama()}")
        started = time.time()
        try:
            submitted = submit(session, shot, output_dir, args.requested_by)
        except subprocess.CalledProcessError as error:
            log(f"{shot}: submit refused - {(error.stderr or '').strip().splitlines()[-1:]}")
            results.append({"shot": shot, "status": "failed", "error": (error.stderr or "").strip()[-2000:]})
            continue
        run_dir = Path(submitted["run_dir"])
        log(f"{shot}: {submitted['run_id']} pid {submitted['worker_pid']}")
        record = wait(run_dir, args.timeout_minutes, args.stall_minutes, submitted.get('worker_pid'))
        minutes = round((time.time() - started) / 60, 1)
        artifacts = [item.get("path") for item in record.get("artifacts", []) if item.get("path")]
        log(f"{shot}: {record.get('status')} in {minutes} min -> {artifacts}")
        results.append({"shot": shot, "status": record.get("status"), "run_id": run_dir.name,
                        "run_dir": str(run_dir), "minutes": minutes, "artifacts": artifacts,
                        "error": (record.get("error") or {}).get("message")})
        result_path.write_text(json.dumps(
            {"session": session.name, "updated_at": now(), "results": results}, ensure_ascii=False, indent=2
        ) + "\n", encoding="utf-8")
    log(f"batch finished: {sum(1 for item in results if item['status'] in {'succeeded', 'needs_review'})}"
        f"/{len(results)} produced an artifact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
