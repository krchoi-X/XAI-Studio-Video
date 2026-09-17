# XAI Control Tower v0.1 — Run, Access, Verification, Limits

Status: **v0.1 implemented** (M0 host monitor → M1 process observatory → M2 Job model + WanGP → M3 tablet UI)  
Implemented: 2026-09-06 by Claude Code (project-specific ownership exception)  
Design reference: `docs/control-tower-local-job-observability.md`

## What it is

A read-only local web app on the RTX 4070 workstation that answers, from a tablet over Tailscale:
what is the GPU doing, who requested the work, what executed it, how far along it is (measured or only inferred),
when it will likely finish, and what it produced.

It observes. It never starts, stops, or edits jobs, and it never writes into `characters/`, `D:\AI_Studio\library`,
the Gallery database, night-batch or web-job directories.

## Run

From the repository root, with the Hermes venv Python 3.11 that is on `PATH` (it already has fastapi, uvicorn,
sse-starlette, psutil, PyYAML, httpx):

```bash
python -X utf8 -m control_tower
```

Defaults: bind `0.0.0.0:8790`, SQLite at `D:\AI_Studio\control-tower\control_tower.sqlite3`, WanGP scan roots
`D:\AI_Studio\library\characters` (current shared records), `D:\codex\XAI-studio\characters`, `runs`, and `examples` (legacy/fallback),
night batches at `D:\AI_Studio\workspace\hermes-night-batches`, Gallery web jobs at
`D:\codex\personal-prompt-studio\personal-prompt-studio\data\workspace\generation-jobs`.

When the same `run_id` exists in the shared Library and a legacy tree, the shared Library record wins. Archived
`historical-records` trees are not scanned, so storage migrations do not duplicate Recent Results.

### Autostart (registered 2026-09-07)

The scheduled task **XAI Control Tower** starts it at logon and after a standby resume, mirroring the Gallery's task:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File control_tower\register-autostart.ps1
```

`control_tower\start.ps1` launches `supervisor.ps1`, which restarts the server if it exits and stops when
`D:\AI_Studio\control-tower\control-tower.stop` appears. `control_tower\stop.ps1` writes that marker and stops both.
Logs: `D:\AI_Studio\control-tower\supervisor.log`, `server.stdout.log`, `server.stderr.log`. Remove the task with
`register-autostart.ps1 -Unregister`. Both start and the task are idempotent: they do nothing when `/api/health`
already answers.

One-shot health check without serving:

```bash
python -X utf8 -m control_tower --check
```

Useful flags: `--port`, `--host`, `--db`, `--scan-root <dir>` (repeatable; replaces the default), `--night-batch-root`,
`--web-job-root` (repeatable), `--gallery-url`, `--wangp-root`, `--host-interval`, `--job-interval`, `--log-level`.
Environment overrides: `XAI_CT_DB`, `XAI_CT_GALLERY_URL`, `XAI_CT_SCAN_ROOTS` (`;`-separated).

`-X utf8` matters on this PC: the default code page is cp949 and the run records are UTF-8.

## Access

| From | URL |
|---|---|
| this PC | http://127.0.0.1:8790/ |
| tablet / phone on the tailnet | https://artxorn.tailf10079.ts.net:8790/ (or http://100.122.180.40:8790/) |
| API docs | http://127.0.0.1:8790/api/docs |

The server binds `0.0.0.0`, so the tailnet IP works without extra configuration. The HTTPS tailnet name is already
served (`tailscale serve --bg --https=8790 http://127.0.0.1:8790`), which is why `tailscaled` also listens on 8790 -
a plain port check is therefore not a valid "is Control Tower running" test; ask `/api/health` instead.

The **Open Gallery** link follows how the dashboard was opened: the loopback URL on this PC, the tailnet URL from a
tablet. The tailnet address is detected at startup by asking `tailscale serve status` which origin publishes the
Gallery's local port, so no hostname is hard-coded. Override either side with `--gallery-url` /
`--gallery-tailnet-url` (or `XAI_CT_GALLERY_URL` / `XAI_CT_GALLERY_TAILNET_URL`); when Tailscale is not serving the
Gallery, both fall back to the local URL.

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | liveness, GPU sampling ok/error, adapter errors |
| `GET /api/overview` | everything the dashboard shows in one snapshot |
| `GET /api/host?history_minutes=30` | GPU sample + recent utilization history + untracked workloads |
| `GET /api/processes` | classified processes and per-agent working/idle/offline state |
| `GET /api/jobs?status=&source=` | canonical jobs (active first) |
| `GET /api/jobs/{job_id}` | one job with the last 25 run events |
| `GET /api/jobs/{job_id}/outputs/{i}` | inline image/video output (supports HTTP Range) |
| `GET /api/jobs/history` | persisted job snapshots (SQLite) |
| `GET /api/timings` | learned per-workstation step timings |
| `GET /api/events` | SSE stream: `overview` on process/job change, small `host` event on GPU ticks |

Job IDs: `wangp:<run_id>`, `night:<batch_id>`, `web:<gen_id>`.

## Honesty rules implemented

- `progress.type` is `step` / `items` / `exact` (measured, blue solid bar) or `phase` / `activity` / `unknown`
  (inferred, purple striped bar). `progress.measured` is explicit in the API and labelled in the UI.
- WanGP's own `progress` percent from preview events is shown only as "runtime reports N%", secondary to steps.
- ETA is `null` unless ≥2 step durations were observed (`eta_basis=recent_steps`) or timing history exists for the
  same model/resolution/steps/frames/batch (`eta_basis=history`). Decode/post-processing phases carry no ETA.
- Agents show "Working" only from measured CPU/GPU activity with a 45 s grace; the API note says so. No percentage
  is ever derived for Claude Code / Codex / Hermes.
- A run whose `run.json` says `running` but whose worker PID is gone is reported `interrupted` with the reason.
- `requested_by` comes from the session's `prompt-trace.json` (`invoked_by`) or the parent night batch / web job.
  Sessions that never recorded it show `unknown` rather than a guess.
- Untracked GPU work is listed with `confidence: heuristic` (or `none` when no process can be tied to the load).
  Desktop apps that idle on the GPU (e.g. the Codex on-device model helper) are not counted as workload.

## Verification performed (2026-09-06)

Deterministic:

```bash
python -X utf8 -m unittest discover -s tests -p "test_control_tower*.py"
```

35 tests: nvidia-smi CSV parsing incl. `[N/A]` → null; process classification for every actor observed on this PC
(Claude Code, Claude desktop, Codex CLI/desktop, Hermes agent/desktop, WanGP worker/Web UI, ComfyUI, Ollama, Gallery,
XAI tools, Control Tower itself); child-process folding; working/idle grace; WanGP adapter on fixture run dirs
(measured steps, ETA from recent steps, ETA from history, ETA unavailable, decoding phase, dead worker → interrupted,
stale-but-alive note, completed outputs incl. missing file, failure with error, multi-item repeat, cache reuse,
skipping `outputs/` trees); night-batch and web-job adapters; parent linking; ETA math; SQLite round trip; API
endpoints via TestClient including untracked-workload cases and GPU-failure reporting; SSE frame logic.

Live on this workstation:

- `nvidia-smi` telemetry for the RTX 4070 Laptop GPU (driver 610.88) sampled every 2 s; `power.limit` is `[N/A]` on
  this laptop and is reported as `null`.
- 111 jobs discovered from existing records (106 WanGP runs across 4 characters, 3 night batches, 2 web jobs);
  one real stale run (`run-20260905-194403-2748fb0b`) correctly surfaced as `interrupted`.
- Requester split over the existing runs: hermes 54, web 9, codex 7, unknown 36 (older sessions without `invoked_by`).
- Timing history learned from completed runs (e.g. H3 Ref2VA 576x768/20 steps/243 frames ≈ 61 s per step).
- A simulated run (fixture record + sleeping worker process, no GPU use) showed the NOW RUNNING card with
  step 8/20 · 40% · ETA from recent steps · elapsed · PID; after the worker exited the run flipped to `interrupted`.
- SSE: full `overview` (~60 KB) only when processes/jobs change, `host` (~0.7 KB) on GPU ticks; Range requests on
  MP4 outputs return 206; reachable on `http://100.122.180.40:8790/` from the host itself.
- Tablet viewport (768×1024) stacks to one column; restricted sessions' thumbnails are blurred until tapped.
- `git status` shows no changes under `characters/` caused by the service; the Gallery, Hermes, Codex, Claude and
  Ollama processes were left untouched.

## Requester attribution (v0.1.1, 2026-09-07)

`requested_by` now carries a `requested_by_basis` that says how it was determined, in this priority order:

| basis | source |
|---|---|
| `record` | an explicit key in the run/session records: `requested_by` written at submit time by `tools/local_wangp.py submit --requested-by …`, `invoked_by` (scene `prompt-trace.json`), or `actor` / `created_by` / `requester` in `run.json`, `batch.yaml` session, `handoff.json`, `sequence-status.json` (BOM-tolerant) |
| `parent` | the run belongs to a Hermes night batch or a Gallery web job |
| `process-env` | observed live: the worker process environment carries an agent marker (Grok Bot `SAND_LOCAL_EXEC_GENERATION` / `SAND_DATA_ROOT`, Claude Code `CLAUDECODE` / `CLAUDE_CODE_SESSION_ID`, Codex `CODEX_*`, Hermes `HERMES_SPAWN` / `HERMES_PARENT_PID`). Only variable names are read. The observation is persisted in the Control Tower database, so it survives run completion and restarts. |
| `process-lineage` | observed live: a classified agent process is an ancestor of the worker |
| `manual` | `D:\AI_Studio\control-tower\attributions.json` (`sessions.<session_id>` / `runs.<run_id>`), for work that finished before Control Tower could observe it; shown with `*` in RECENT RESULTS |

Grok Bot (`C:\Program Files\Grok Bot\Grok Bot.exe`, local exec daemon `local-exec-daemon\main.cjs`) is classified as agent
`grok` and appears in AGENTS / PROCESSES. Processes it launches (including WanGP workers, which are detached from their
parent by `tools/local_wangp.py`) are credited to Grok via the environment marker, so Grok shows **Working · GPU** while its
render runs. Any agent whose requested job is running is shown as Working with the note that the activity is inferred from
the job. The two Grok trio sessions from 2026-09-06/07 are attributed manually because they finished before this version.

### Recording the requester at submit time (v0.1.2, 2026-09-07)

The submit path now records the requester instead of leaving it to observation. `tools/local_wangp.py submit` and
`tools/wangp_recorder.py prepare` take `--requested-by <actor>` (default from `XAI_REQUESTED_BY`, else `null`) and an
optional `--executor` (default `local-wangp-worker`). Both land in `run.json` as top-level `requested_by` / `executor`,
in the `queued` event, and in the JSON printed by `submit` / `status`; the value is also placed on the detached
worker's command line. `tools/character_scene.py --actor` now accepts `grok` and `claude` in addition to
`codex` / `hermes` / `web` / `user`, writes `created_by` into the session `batch.yaml`, and forwards it to the runner.
`tools/reference_variation_worker.py` submits as `web`.

Requester, executor, engine and model stay four separate fields: `requested_by` (who asked), `executor` (what ran it),
`renderer` (WanGP), and `settings.value.model_type` (the model). A missing requester stays `null`; it is never guessed,
and Control Tower falls back to the observation bases below. See `docs/wangp-recorder.md` for the calling convention.

## Known limits (v0.1)

- Live previews: the recorder stores only a PIL repr for WanGP preview frames, so a running job has no thumbnail;
  outputs appear when the run finishes.
- Manually launched WanGP Web UI jobs (`wgp.py`, port 7860) are visible only as an untracked/WanGP process; their
  progress is not readable because the Web UI writes no run record.
- ComfyUI has no adapter; it is classified as a process and, when on the GPU, appears as untracked workload.
- `requested_by` is `unknown` for sessions created before `prompt-trace.json` recorded `invoked_by`, and for the
  VIDEO sessions driven directly from Claude Code / Codex CLI (no trace file).
- Per-process VRAM is not available on Windows WDDM; nvidia-smi lists the process but not its memory.
- Agent "working" state is CPU/GPU-based; a coding agent waiting on the network reads as idle after 45 s.
- ETA ignores model load time and decode/encode overhead; it is a step-based estimate only.
- Single-instance service; no auth (tailnet-only by design); no notifications; no job control.
- The SQLite file is a cache/history, safe to delete; timing history is rebuilt from completed runs on restart.

## Files

```text
control_tower/
  __main__.py      CLI entry (`python -m control_tower`, `--check`)
  app.py           FastAPI routes, SSE, output serving
  monitor.py       background sampler, snapshot publishing, untracked detection, parent linking
  gpu.py           nvidia-smi collector
  processes.py     psutil classifier + agent activity
  jobs.py          canonical Job / Progress / Output model
  eta.py           step-duration EMA + timing keys
  db.py            SQLite (WAL): jobs, step_timings, host_samples
  adapters/        wangp_runs.py, night_batch.py, web_jobs.py
  static/index.html  tablet dashboard
tests/test_control_tower_{gpu,processes,adapters,api}.py
```
