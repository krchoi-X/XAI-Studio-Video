# Scoped Task — Autostart, face-discovery requester, task/verification hygiene (v0.1.4)

Owner / Active editor: Claude Code (Control Tower subsystem + the provenance work explicitly assigned 2026-09-07)
Status: COMPLETE — implemented and verified 2026-09-07
Working mode: Codex is coordination/final-integration only for the next three days; commit only my own scope,
hand other scopes over with a reproduction, keep one GPU job at a time, no push or deployment.

## Goal

Three small, self-contained items the user approved. Explicitly **out** of scope by the user's decision:
the Gallery status widget and a ComfyUI adapter.

1. **Autostart** — Control Tower currently runs only because a session started it; a reboot loses the tablet
   dashboard. The Gallery already has a scheduled task; Control Tower has none.
2. **face-discovery requester** — `tools/face_discovery.py` takes no `--actor` and writes no `created_by`, so
   face sessions (including tablet-triggered ones through `web_generation_worker.py`) record a null requester and
   show as `unknown`. Reproduction: `python tools/face_discovery.py produce --character ch-harim --direction X …`
   then read the session `batch.yaml`; `session.created_by` is absent.
3. **Records** — my scoped TASK.md lacks commit ids and a "next actions" section; `docs/verification.md` does not
   list the Control Tower suites, so they are missing from the shared regression selection.

## Plan

1. `control_tower/start.ps1`, `supervisor.ps1`, `stop.ps1`, `register-autostart.ps1` mirroring the Gallery pattern
   (idempotent guard, restart loop with a stop marker, logon + standby-resume triggers). State and logs live in
   `D:\AI_Studio\control-tower\`, which Control Tower already owns.
2. `face_discovery.py --actor` (same choices as the scene pipeline, default `codex`), `created_by` in its session
   record, and `--actor web` from `web_generation_worker.py`; tests.
3. TASK.md commit ids + next actions; add the Control Tower suites to `docs/verification.md`.

## Contract impact

- Autostart: new scripts under `control_tower/` only; no repository launch script or existing task is touched. The
  scheduled task is new (`XAI Control Tower`) and does not overlap the Gallery's. Rollback:
  `schtasks /Delete /TN "XAI Control Tower"` plus `control_tower/stop.ps1`.
- face-discovery: `--actor` is optional with today's behaviour as the default, and `created_by` is an additive
  session key that the Control Tower and the requester resolver already read. Old sessions are unaffected; nothing
  is relabelled. Producers: `face_discovery.py`, `web_generation_worker.py`. Consumers: requester resolver,
  Control Tower session context.
- `docs/verification.md` is Codex's shared file; the edit is additive (one section) and reported for their review.

## Delivered

| File | Change |
|---|---|
| `control_tower/start.ps1` | idempotent launcher; asks `/api/health` instead of checking the port, because `tailscale serve` also listens on 8790 to proxy the tablet |
| `control_tower/supervisor.ps1` | restart loop, resolves the interpreter (`-Python`, `$XAI_CT_PYTHON`, the Hermes venv, then PATH), logs to `D:\AI_Studio\control-tower\` |
| `control_tower/stop.ps1` | writes the stop marker and stops the server and supervisor |
| `control_tower/register-autostart.ps1` | registers/removes the `XAI Control Tower` scheduled task (logon + Modern Standby resume), least privilege, interactive token |
| `tools/face_discovery.py` | `--actor` (same choices as the scene pipeline, default `codex`); `created_by` in `batch.yaml` session and `metadata.json` |
| `tools/web_generation_worker.py` | passes `--actor web` for tablet-triggered face discovery |
| `tests/test_character_scene.py` | face-discovery actor test |
| `docs/verification.md` | Control Tower service-lifecycle section; `tools/test_requester_provenance.py` added to the regression selection (Codex's file: additive edit, flagged for review) |
| `docs/control-tower-v0.1.md` | autostart section; HTTPS tailnet URL; removed the now-verified tablet limitation |

## Verification

- `control_tower\start.ps1` started the supervisor and `/api/health` answered; killing the server process
  (pid 31260) had the supervisor restart it within ~14 s (new pid 17904, health OK, logged in `supervisor.log`).
- `schtasks /Run /TN "XAI Control Tower"` returned `LastTaskResult 0` and started no duplicate: the guard saw the
  healthy service and exited. Task state `Ready`, action `start.ps1`, working directory `control_tower`.
- Face discovery end to end: `face_discovery.py prepare --actor grok` wrote `created_by: grok` into both
  `batch.yaml` and `metadata.json`, and `wangp_recorder.session_requester()` resolved `grok`; the temporary
  session directory was deleted afterwards (`ch-harim` session count 12 before and after).
- `tests/test_character_scene.py` 17 pass; Control Tower suites unaffected by this change.
- Not verified: behaviour across an actual reboot (only logon-task on-demand execution was exercised).

## Commits

`a0c7895` Control Tower v0.1 · `4167b6d` Grok attribution · `87ce3a2` submit-time requester ·
`d8366f4` session provenance record · this task's commit added below on completion.

## Next actions

1. Nothing outstanding in this scope. Remaining Control Tower limits stay deferred by the user's decision:
   Gallery status widget and ComfyUI adapter are explicitly **not wanted**; live preview thumbnails and a WanGP
   Web UI queue adapter remain open but unrequested.
2. 35 old runs keep `unknown` requesters by design; add entries to
   `D:\AI_Studio\control-tower\attributions.json` only if the user asks.
3. The user's stated direction is character finalization, then an automated video pipeline, then story-driven
   comic/novel work — one at a time. No work started on those; they need their own scoped task when chosen.

---

# Scoped Task — Session provenance record for real production (v0.1.3)

Owner / Active editor: Claude Code (same explicit assignment as v0.1.2)
Status: COMPLETE — implemented, unit-tested, live-verified with Korean text (2026-09-07)

## Goal

Close the last gap: when Grok Bot (or any agent) actually **produces**, the session itself must carry a durable,
uniform record of who asked, what executed it, which engine/model, and the verbatim request — not just the per-run
`requested_by` added in v0.1.2. Then document the rule and the exact calls, and write a handover note for Grok.

## Findings

- Grok already writes a rich `handoff.json` per video session with `requested_by`, `requesting_agent`,
  `user_request_verbatim`, `provenance`, `character`, `target_renderer`, `model`, `prompts[]`, `results[]`. The
  convention exists but is ad hoc, undocumented and unsupported by any tool, so each agent invents its own shape.
- That file even contains Grok's own note that `--actor` had no `grok` choice and `submit` had no requester flag
  (both fixed in v0.1.2).
- Scene sessions get `batch.yaml` with `session.created_by`; manual/video sessions get nothing tool-written.
- Studio importer consumes only `batch.yaml`; nothing consumes a new session file, so adding one is additive.

## Plan

1. `tools/wangp_recorder.py session` writes/updates a canonical `<session>/session-provenance.json`
   (schema_version 1; merge-friendly; never rewrites `handoff.json`, which stays Grok's own).
2. `tools/local_wangp.py submit` inherits the requester from that record (then `handoff.json`, `batch.yaml`
   `created_by`, `prompt-trace.json` `invoked_by`) when `--requested-by`/`XAI_REQUESTED_BY` are absent. A value read
   from an explicit session record is a record, not a guess; nothing is invented when all are absent.
3. Control Tower reads `session-provenance.json` first among session provenance candidates.
4. Tests for the writer, the inheritance chain, and the Control Tower read.
5. Docs: `docs/wangp-recorder.md` production recording rules + exact calls; `GROK.md` rules; a handover note for Grok.

## Contract impact

- Producers: `wangp_recorder.py session` (new, optional), agents writing sessions by hand.
- Consumers: `local_wangp.py submit` (requester inheritance), Control Tower `WangpRunAdapter` (session context).
- New optional file `session-provenance.json`; no existing file is rewritten; `handoff.json`, `batch.yaml`,
  `prompt-trace.json` keep their current meaning and remain readable. Sessions without it behave exactly as today.
- Studio importer reads only `batch.yaml` and is unaffected. No migration. Rollback: revert the commit; the extra
  file is inert for every other consumer.
- Deterministic verification: `unittest discover -s tools`, `-s tests`, plus a no-GPU submit that inherits the
  requester from a session record and reads back as `record` in the running Control Tower.

## Delivered

| File | Change |
|---|---|
| `tools/wangp_recorder.py` | `session` subcommand writes/updates `<session>/session-provenance.json` (merge-friendly, idempotent, requires a requester only the first time); `session_requester()` / `requester_in()` read the priority chain incl. nested `provenance` blocks and BOM files |
| `tools/local_wangp.py` | `submit` inherits the requester from the session record when the flag and env are absent |
| `tools/wangp_recorder.py`, `tools/local_wangp.py` | `force_utf8_stdio()`: JSON output is UTF-8 whatever the console code page — found live, a Korean `--user-request` produced cp949 bytes that callers decoding UTF-8 could not read |
| `control_tower/adapters/wangp_runs.py` | reads `session-provenance.json` first for requester, title and character |
| `tools/test_requester_provenance.py` | +7 tests (writer, idempotent update, required-first-time, priority chain, batch `created_by`, submit inheritance, flag override) |
| `tests/test_control_tower_attribution.py` | session-provenance read incl. losing competing `handoff.json` |
| `docs/wangp-recorder.md` | "Recording a production session": rules, record shape, resolution order |
| `docs/grok-production-recording-note.md` (new) | the handover note for Grok, in Korean |
| `GROK.md` (Codex's untracked file, working tree only) | production recording rules and exact calls |

## Verification

- `tools`: 28 tests pass. `tests`: 75 run, 74 pass + the pre-existing `test_reference_transformation_contract`
  import error (needs pytest, unrelated).
- Live, no GPU: registered a session with `wangp_recorder.py session --requested-by grok` (Korean title and request),
  then submitted **with no flag and no environment variable**. The run inherited `grok`, and after a Control Tower
  restart it reads `grok (record)` with executor `local-wangp-worker`, engine `WanGP`,
  model `minimax_h3_ref2va_pruned`, character `ch-lia`, and the Korean title intact.
- Grok's real render running during this work continued to display as `grok (record)`; nothing was disturbed.

---

# Scoped Task — Explicit requester provenance on the WanGP submit path (v0.1.2)

Owner / Active editor: Claude Code (explicitly assigned by the user on 2026-09-07 for this task: `tools/local_wangp.py`,
`tools/wangp_recorder.py`, `tools/character_scene.py`, related tests and docs, in addition to `control_tower/**`)
Root task link: root `TASK.md` is Codex's documentation task; this file is the durable state for this work.
Status: COMPLETE — implemented, unit-tested, and verified live on this PC (2026-09-07)
Started / completed: 2026-09-07

## Goal

Record **who requested** a WanGP run at submit time so Control Tower shows Grok Bot (and Claude, Codex, Hermes, web)
with basis `record` instead of relying on live observation. Requester, executor, engine and model stay separate.

## Path confirmed

```text
Grok Bot local-exec-daemon
  → Grok's orchestrator (tmp/wangp_queue_dyn_motion_trio.py; D:\AI_Studio\workspace\lia_*.py)
  → python tools/local_wangp.py submit --runs-root … --prompt-file … --settings-file … --project-id … --prompt-id …
      → wangp_recorder.prepare_run()  writes <run>/run.json (status queued) + events.jsonl
      → Popen(DETACHED_PROCESS) python local_wangp.py worker --run-dir …   (parent exits immediately)
          → worker: load_run → status running → WanGP session → attach/fail → save_run (whole record preserved)
  → Control Tower WangpRunAdapter reads run.json / events.jsonl; explicit_requester(run) already honours a
    top-level `requested_by` key (basis `record`).
```

Repository callers of `submit`: `tools/character_scene.py` (scene pipeline; `--actor codex|hermes|web`),
`tools/reference_variation_worker.py` (Gallery Krea2 variation, web), `tools/run_character_audition_queue.py`
(legacy manual script). Grok calls `submit` directly.

## Plan

1. `wangp_recorder.py`: `prepare --requested-by <actor> [--executor <name>]`; `normalize_actor()`; `run.json` gains
   optional top-level `requested_by` and `executor` (null when not given); the `queued` event carries `requested_by`.
2. `local_wangp.py submit --requested-by <actor>` (default from env `XAI_REQUESTED_BY`, else null), `--executor`
   default `local-wangp-worker`; the flag is also placed on the detached worker command line; worker/attach/fail keep
   the record intact; `submit`/`status` output includes `requested_by`.
3. `character_scene.py`: `--actor` accepts `grok` and `claude`; the session `batch.yaml` records `created_by`; `submit()`
   forwards `--requested-by` from `batch.yaml` → `prompt-trace.json` `invoked_by` fallback; nothing invented.
4. `reference_variation_worker.py`: forwards `--requested-by web`.
5. Control Tower: prefer `run.json` `executor` when present; test `requested_by` from `run.json` → `record`.
6. Grok's orchestrator script and the shared guidance (`docs/wangp-recorder.md`, `GROK.md` pointer) pass
   `--requested-by grok`.
7. Tests: recorder, local_wangp end-to-end with a fake WanGP `shared.api` (no GPU, real detached worker), scene actor
   plumbing, Control Tower record basis. Live no-GPU verification through the running Control Tower incl. restart.

## Must NOT Do

- Do not guess a requester when none is given: `requested_by` stays null and Control Tower falls back to observation.
- Do not change `schema_version` semantics; fields are additive and optional. Old `run.json` files keep working.
- Do not revert or commit other agents' uncommitted edits (root docs, `external_media_import/`, `GROK.md`,
  `docs/grok-bot-handoff.md` are Codex/Grok working-tree files; my edits there stay uncommitted and are reported).

## Contract impact

- Producers: `wangp_recorder.prepare` (CLI + `prepare_run`), `local_wangp.submit`, `character_scene.prepare/submit`,
  `reference_variation_worker`, Grok orchestrators.
- Consumers: Control Tower `WangpRunAdapter` (reads `requested_by`, `executor`), `local_wangp.status`, Gallery
  importer (`personal-prompt-studio` reads `run.json` artifacts only; unaffected by extra keys), `character_scene`
  wait loop (reads `status`/`artifacts` only).
- Old persisted examples: 115 existing `run.json` files without the keys (`characters/**/runs/*/run.json`); a fixture
  test covers the absent-key case. `batch.yaml` sessions without `created_by` still submit (flag omitted).
- Compatibility: readers treat missing/null as unknown; `schema_version` stays 1. No migration.
- Rollback: revert the commit; records written meanwhile keep two harmless extra keys.
- Deterministic verification: `python -X utf8 -m unittest discover -s tools -p "test_*.py"`,
  `python -X utf8 -m unittest discover -s tests -p "test_control_tower*.py"`, `tests/test_character_scene.py`,
  plus a live no-GPU submit through a fake WanGP root observed by the running Control Tower.

## Delivered

| File | Change |
|---|---|
| `tools/wangp_recorder.py` | `normalize_actor()`; `prepare --requested-by/--executor`; `run.json` gains optional top-level `requested_by` / `executor`; the `queued` event carries them |
| `tools/local_wangp.py` | `submit --requested-by` (default `$XAI_REQUESTED_BY`, else null) and `--executor` (default `local-wangp-worker`); flag echoed on the detached worker command line and in `submit`/`status` JSON |
| `tools/character_scene.py` | `--actor` accepts `grok`, `claude`, `user`; `batch.yaml` session records `created_by`; `session_requester()` (batch `created_by` → `prompt-trace.json` `invoked_by`, BOM-tolerant) forwards `--requested-by` to the runner |
| `tools/reference_variation_worker.py` | submits as `web` |
| `control_tower/adapters/wangp_runs.py` | honours a recorded `executor`; `requested_by` from the record reads as basis `record` |
| `control_tower/adapters/night_batch.py`, `web_jobs.py` | set `requested_by_basis` for consistency |
| `control_tower/monitor.py` | a generic GPU process is only "untracked" when no tracked job explains the utilization (fixed a false banner seen live) |
| `tools/test_requester_provenance.py` (new) | 9 tests incl. a real `submit` → detached worker → record end-to-end against a fake WanGP root |
| `tests/test_character_scene.py`, `tests/test_control_tower_attribution.py`, `tests/test_control_tower_api.py` | actor plumbing, record basis, null-key handling, untracked regression |
| `docs/wangp-recorder.md`, `docs/control-tower-v0.1.md` | calling convention and basis table |
| working tree only (not committed): `GROK.md` (Codex's untracked file, requester line added), `tmp/wangp_queue_dyn_motion_trio.py`, `tmp/run_home.py` (Grok's scripts: `--requested-by grok`, `XAI_REQUESTED_BY=grok`, `--actor grok` instead of `codex`), root `TASK.md` (pointer line appended) | |

## Verification

- `tools`: 21 tests pass (`python -X utf8 -m unittest discover -s tools -p "test_*.py"`), including a real detached
  worker run: requester survives submit → worker rewrite → `needs_review`, and `status` echoes it. Invalid actor tokens
  are rejected before any run directory is created. No flag and no env → `null`, never a guess.
- `tests`: 45 Control Tower tests and 16 character-scene tests pass; whole-suite `unittest discover -s tests` is 71 pass
  + the pre-existing `test_reference_transformation_contract` import error (needs pytest, unrelated).
- Live, no GPU: `local_wangp.py submit --requested-by grok` against a fake WanGP root produced a completed run that the
  Control Tower — restarted afterwards — showed as `grok (from record)` with executor `local-wangp-worker`, engine
  `WanGP`, model `minimax_h3_ref2va_pruned`.
- Live, real: Grok Bot's own run `VIDEO-20260907-181254-lia-sundress-shift-cat` (started 18:21, on the GPU during this
  work) displays as `grok (from record)` because Grok now writes `requested_by` into its session `handoff.json`.
  It was not disturbed.
- Regression: 125 existing runs still parse; basis mix `record` 78, `manual` 6, `parent` 2, none 35 (older sessions
  with no provenance anywhere — left as `unknown` by design).

---

# Previous scoped task — requester attribution for Grok Bot (v0.1.1) — COMPLETE 2026-09-07

Delivered: Grok Bot classification (desktop / helper / exec daemon → agent `grok`), environment-marker and lineage
`launched_by` on processes, attribution of unknown runs from the live worker (`process-env` / `process-lineage`,
persisted in SQLite `attributions`), manual `D:\AI_Studio\control-tower\attributions.json` (seeded with the two Grok
trio sessions), explicit provenance keys read with basis `record`, "Working · job" agent state, API/UI basis display.
Verified with 41 unit tests and a live no-GPU simulation; commit `4167b6d`. Details: `docs/control-tower-v0.1.md`
§"Requester attribution".
