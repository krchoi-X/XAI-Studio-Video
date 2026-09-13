#!/usr/bin/env python3
"""Run a named list of shots through the local WanGP worker, one at a time, and record the result.

    python tools/identity_batch.py --session-dir SESSION --output-dir OUT --shots turn-01 turn-02

Each shot is `<session>/<shot>.txt` plus `<session>/<shot>.settings.json`, the pair `local_wangp.py submit`
already expects. The batch submits one, waits for it to reach a terminal state, then submits the next: the
worker holds a GPU lock. A submission made while another worker holds it fails immediately,
so the batch waits for the lock (see `wait_for_lock`) rather than spending the shot.

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


def keep_awake() -> str:
    """Ask Windows not to sleep while the batch runs, for the life of this process only.

    On 2026-09-13 an overnight batch of twenty shots lost about seven hours: the laptop entered Modern
    Standby at 00:53 and did not leave until 07:56 (System log, Kernel-Power 506/507). One shot was
    throttled to 62 minutes against a 45 minute deadline and the next was frozen mid-render for 406. Neither
    is a fault in the stall detection - there was nothing running to detect.

    This is a process-scoped request, not a change to the machine's power settings: it is dropped the moment
    this process exits, and it does not survive a lid close or a manual sleep. A batch that must survive
    those needs the operator to change the power plan themselves.
    """
    if os.name != "nt":
        return "not Windows; no sleep request made"
    import ctypes
    # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED
    if ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000040):
        return "sleep suppressed for the life of this batch"
    # Away mode is refused on some machines; the plain system request is enough on those.
    if ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001):
        return "sleep suppressed (away mode refused)"
    return "WARNING: could not suppress sleep; an unattended batch may be interrupted"


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


LOCK_MESSAGE = "already holds the GPU lock"


def wait_for_lock(session: Path, shot: str, output_dir: Path, requested_by: str,
                  wait_minutes: int) -> dict[str, Any]:
    """Submit, and if another worker holds the GPU lock, wait for it instead of burning the shot.

    Submitting against a held lock fails instantly. A batch queued behind a render that is still running
    therefore does not wait its turn - it fails every shot in a couple of minutes and the night is gone.
    That happened on 2026-09-13: twenty vlog shots were queued while a single clip was still rendering and
    all twenty failed inside six minutes.
    """
    deadline = time.time() + wait_minutes * 60
    announced = False
    while True:
        try:
            return submit(session, shot, output_dir, requested_by)
        except subprocess.CalledProcessError as error:
            if LOCK_MESSAGE not in (error.stderr or "") or time.time() > deadline:
                raise
            if not announced:
                log(f"{shot}: another worker holds the GPU lock - waiting up to {wait_minutes} min")
                announced = True
            time.sleep(60)


def held_by_another(record: dict[str, Any]) -> bool:
    """True when a run failed only because another worker held the GPU lock.

    `submit` spawns a detached worker and returns before that worker touches the GPU, so this failure never
    reaches the caller as a non-zero exit - it is written into the run record a second later. Checking the
    submit call alone is not enough, which is how twenty shots were spent in six minutes on 2026-09-13.
    """
    if record.get("status") not in {"failed", "interrupted"}:
        return False
    text = json.dumps(record, ensure_ascii=False)
    return LOCK_MESSAGE in text


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
    parser.add_argument("--lock-wait-minutes", type=int, default=90,
                        help="how long to wait for another worker to release the GPU lock before failing "
                             "the shot; a batch queued behind a running render would otherwise fail every "
                             "shot within minutes")
    parser.add_argument("--result", help="where to write the batch record (default <session>/batch-result.json)")
    args = parser.parse_args()

    session = Path(args.session_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = Path(args.result) if args.result else session / "batch-result.json"

    log(keep_awake())

    results = []
    for shot in args.shots:
        log(f"{shot}: {unload_ollama()}")
        started = time.time()
        try:
            submitted = wait_for_lock(session, shot, output_dir, args.requested_by,
                                      args.lock_wait_minutes)
        except subprocess.CalledProcessError as error:
            log(f"{shot}: submit refused - {(error.stderr or '').strip().splitlines()[-1:]}")
            results.append({"shot": shot, "status": "failed", "error": (error.stderr or "").strip()[-2000:]})
            continue
        run_dir = Path(submitted["run_dir"])
        log(f"{shot}: {submitted['run_id']} pid {submitted['worker_pid']}")
        record = wait(run_dir, args.timeout_minutes, args.stall_minutes, submitted.get('worker_pid'))
        lock_deadline = started + args.lock_wait_minutes * 60
        while held_by_another(record) and time.time() < lock_deadline:
            log(f"{shot}: the worker lost the GPU lock race - retrying in 60 s")
            time.sleep(60)
            submitted = wait_for_lock(session, shot, output_dir, args.requested_by,
                                      args.lock_wait_minutes)
            run_dir = Path(submitted["run_dir"])
            record = wait(run_dir, args.timeout_minutes, args.stall_minutes,
                          submitted.get("worker_pid"))
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
