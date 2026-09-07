# Current Task — XAI Control Tower v0.1

Owner: Claude Code (explicit per-project exception, see `docs/agent-development-production-roles.md`)
Status: COMPLETE — v0.1 (M0–M3) implemented, tested, and running locally; awaiting user review from the tablet
Started / completed: 2026-09-06

The previous `TASK.md` (publish/audit task plus three completed generation snapshots) is preserved verbatim in
`docs/task-archive/2026-09-06-pre-control-tower-task-snapshot.md`. Its open item (audit and push the pending
generation records under `characters/`) is **not** part of this task and remains for the user/Codex. Those pending
records were left untouched and are not included in the Control Tower commit.

## Goal

Build the local-first observability web app described in `docs/control-tower-local-job-observability.md`:
answer "what is the RTX 4070 doing right now, who started it, how far is it, when will it finish, what did it produce"
from a tablet over Tailscale, using host telemetry + process observation + a canonical Job model fed by the existing
WanGP run records. Declare v0.1 at M3.

## Result

Run, access, API, verification and limits: `docs/control-tower-v0.1.md`.

```bash
python -X utf8 -m control_tower            # http://127.0.0.1:8790/  ·  tailnet http://100.122.180.40:8790/
python -X utf8 -m control_tower --check    # one-shot sample, no server
python -X utf8 -m unittest discover -s tests -p "test_control_tower*.py"   # 35 tests
```

## Scope delivered (v0.1)

- M0 Host monitor: GPU utilization, VRAM, temperature, power, clocks, GPU process list via `nvidia-smi`; failures
  reported as `ok:false` + reason, never as zeros.
- M1 Process observatory: Claude Code / Codex / Hermes / WanGP / ComfyUI / Ollama / Gallery / XAI tools / other
  Python classified; elapsed, CPU, GPU presence; agent working/idle/offline with 45 s grace; untracked GPU workload
  with heuristic identification; idle desktop helpers on the GPU are not counted as workload.
- M2 Job model + adapters: canonical Job (`requested_by` ≠ `executor` ≠ `engine` ≠ `model`), progress types
  `step`/`items`/`exact` (measured) vs `phase`/`activity`/`unknown` (inferred), ETA from recent step EMA or learned
  per-workstation history with explicit basis, outputs, dead-worker → `interrupted`, stale-event note; adapters for
  WanGP recorder runs, Hermes night batches, Gallery web jobs; parent linking; SQLite WAL history.
- M3 Tablet UI: NOW RUNNING / GPU / AGENTS & PROCESSES / QUEUE / RECENT RESULTS, SSE live updates (full snapshot only
  on change, tiny host ticks otherwise), job detail dialog, inline outputs with Range support, restricted-session
  thumbnails blurred until tapped, single-column layout on tablet width.

## Constraints honoured

- Read-only over `characters/**`, `D:\AI_Studio\library`, Gallery data, night-batch and web-job dirs; own state only in
  `D:\AI_Studio\control-tower\control_tower.sqlite3` (outside the repo, safe to delete).
- No fabricated percentages; measured vs inferred is explicit in API (`progress.measured`) and UI.
- No cloud GPU, job creation, process kill/restart, notifications, auth, or Prometheus stack.
- No edits to `tools/*`, `schemas/*`, `skills/*`, README, or Tailscale serve config.
- Only packages already in the Hermes venv (fastapi, uvicorn, sse-starlette, psutil, pydantic, httpx, PyYAML).

## Verification

- 35 Control Tower unit tests pass (`unittest`; pytest is not installed in either local interpreter).
- Whole-repo `unittest discover` : 58 pass, 1 pre-existing import error (`test_reference_transformation_contract`
  needs pytest) unrelated to this work; `tools/test_wangp_recorder.py` + `tools/test_local_wangp.py` (8) pass.
- Live: 111 jobs discovered from existing records; real stale run `run-20260905-194403-2748fb0b` surfaced as
  `interrupted`; simulated running job (fixture + sleeping worker, no GPU use) showed measured step progress, ETA
  from recent steps, then `interrupted` after the worker exited; SSE mix verified with curl; MP4 Range → 206;
  reachable on the tailnet IP from the host; tablet viewport checked in the in-app browser.
- `git status`: the four pre-existing modified files under `characters/ch-lia/.../Lia_Vlog_Test_Session` were already
  modified before this task began; the service changed nothing under `characters/`.

## Decisions

- Package `control_tower/` at repo root (bounded subsystem; `tools/` stays Codex CLI space).
- `nvidia-smi` CSV polling (2 s) instead of pynvml; per-process VRAM is unavailable on Windows WDDM anyway.
- SSE with two event types (`overview`, `host`) to keep tablet traffic small; JSON polling fallback in the UI.
- Port 8790; bind `0.0.0.0` so the tailnet IP works without `tailscale serve` (command documented for HTTPS).
- Job IDs `wangp:<run_id>`, `night:<batch_id>`, `web:<gen_id>`; timing key `model|resolution|steps|frames[|bN]`.
- The TestClient cannot close an infinite SSE response without deadlocking, so SSE is tested through `sse_frame()`
  plus a live curl check, not through the streaming endpoint.

## Contract impact

None to shared contracts. Control Tower only reads `run.json` / `events.jsonl` / `artifact-manifest.json` /
`batch.yaml` / `prompt-trace.json` / night-batch `status.json` + `plan.json` / web `status.json` + `request.json`.
Its own API (`/api/*` on 8790) is consumed only by its bundled UI. Rollback = delete `control_tower/`, the four
`tests/test_control_tower_*.py` files, `docs/control-tower-v0.1.md`, and the SQLite file.

## Next (suggested, not started)

1. User opens `http://100.122.180.40:8790/` on the tablet; optionally `tailscale serve --bg --https=8790 http://127.0.0.1:8790`.
2. Autostart: add a scheduled task / supervisor like `personal-prompt-studio/register-studio-autostart.ps1` (integration-owned; Codex).
3. If useful: a voluntary phase-event file for Claude Code / Codex, ComfyUI adapter, WanGP Web UI queue reading,
   Gallery status widget linking here (`docs/control-tower-local-job-observability.md` §13, §17).

## Blockers / Uncertainties

- Tailscale reachability from the tablet itself is unverified in this session (host-side check only). Windows Firewall
  may prompt once for python.exe.
- Older sessions without `invoked_by` show `requested_by: unknown` by design.
