# Scoped Task — Control Tower: requester attribution for Grok Bot (v0.1.1)

Owner / Active editor: Claude Code (Control Tower subsystem owner, see `docs/agent-development-production-roles.md`)
Root task link: root `TASK.md` is Codex's documentation task (COMPLETE); the v0.1 record is archived in
`docs/task-archive/2026-09-07-control-tower-task-snapshot.md`. This file is the durable state for `control_tower/**`.
Status: COMPLETE — implemented, unit-tested, live-verified on this PC (2026-09-07); awaiting user review from the tablet
Started / completed: 2026-09-07

## Goal

Show WanGP work started by Grok Bot as Grok's work (requester and agent activity), instead of `requested_by: unknown`
and an unrecognised process. Keep every attribution honest: say how it was determined.

## Findings (2026-09-07)

- Grok Bot is an Electron app (`C:\Program Files\Grok Bot\Grok Bot.exe`) whose child `local-exec-daemon\main.cjs`
  (pid in `~/.grokbot/local-exec-daemon.json`) runs local commands. It keeps no command log.
- Grok drove WanGP through the repository tools (`tools/local_wangp.py submit`) from its own orchestrator scripts
  (`tmp/wangp_queue_dyn_motion_trio.py`, `D:\AI_Studio\workspace\lia_*.py`). Sessions
  `VIDEO-20260906-233747-lia-intro-10s-trio` and `VIDEO-20260907-074621-lia-dynamic-motion-trio` are Grok's; their
  `handoff.json` / `sequence-status.json` carry no actor field and are written with a UTF-8 BOM.
- `local_wangp.py submit` detaches the worker, so parent-PID lineage breaks once `submit` exits. Environment variables
  survive: Grok's daemon children carry `SAND_LOCAL_EXEC_GENERATION` / `SAND_DATA_ROOT`; Claude Code children carry
  `CLAUDECODE` / `CLAUDE_CODE_SESSION_ID`; Codex children `CODEX_*`; Hermes children `HERMES_SPAWN` /
  `HERMES_PARENT_PID`. (`HERMES_HOME` / `HERMES_GIT_BASH_PATH` are user-wide and must be ignored.)
- The Hermes venv python is the PATH python, so "python path contains hermes-agent" must not classify a process as
  the Hermes agent (fixed: only `hermes_cli` does).
- The CLI `--actor` enum still lacks `grok`/`claude` (Codex follow-up); Control Tower must not edit `tools/`.

## Delivered

1. `Grok Bot.exe` classified as `grok-desktop` / `grok-desktop-helper` / `grok-exec-daemon`, agent `grok`, in the
   AGENTS panel after Hermes.
2. Environment-marker probe (`detect_env_agent`, names only, cached per process lifetime) for python/node/shell
   processes → `launched_by` + `launched_by_basis` (`env` | `lineage`). A process launched by an agent counts toward that
   agent's CPU/GPU activity, so Grok reads **Working · GPU** while its WanGP worker renders.
3. Monitor attribution for WanGP runs whose records say `unknown`: persisted observation → live worker process
   (`process-env` / `process-lineage`, stored in SQLite table `attributions`) → manual file
   `D:\AI_Studio\control-tower\attributions.json` (`manual`). Runs with a parent batch/web job get basis `parent`.
4. Explicit provenance keys honoured with basis `record`: `invoked_by` / `requested_by` / `actor` / `created_by` /
   `requester` in `run.json`, `batch.yaml` session, `prompt-trace.json`, `handoff.json`, `sequence-status.json`;
   JSON is read with `utf-8-sig`.
5. An agent whose requested job is `running` is shown Working with the note that the activity is inferred from the job.
6. API: `requested_by_basis` on jobs, `details.attribution_evidence`, `launched_by` / `launched_by_basis` on processes.
   UI: basis label next to the requester, `*` on manual attributions in RECENT RESULTS, "launched by" in the process
   list, "Working · job" on agent cards.
7. Manual file seeded with the two Grok trio sessions.

## Verification

- `python -X utf8 -m unittest discover -s tests -p "test_control_tower*.py"`: 41 tests pass (new:
  `tests/test_control_tower_attribution.py` — env-marker attribution persisting across completion and restart,
  lineage attribution, agent-working-from-job, manual file, explicit keys incl. BOM; Grok classification and
  marker-priority tests in `test_control_tower_processes.py`).
- Live: the six runs of the two Grok trio sessions show `grok (manual)`; Grok Bot appears as an agent with its
  desktop + exec-daemon processes; a simulated detached worker carrying `SAND_LOCAL_EXEC_GENERATION` (no GPU use) was
  attributed `grok (process-env)` within one job scan, the Grok card switched to Working, the attribution row was
  written to SQLite and remained after the worker was killed. Simulation records and rows were removed afterwards;
  the server runs with default configuration on port 8790.
- Remaining `unknown` requesters: 35 of 115 WanGP runs (older sessions without any provenance).

## Must NOT Do (held)

- No edits to `tools/`, `schemas/`, `skills/`, Codex-owned root docs, or Grok's `external_media_import/`.
- No writes into `characters/**`, library, Gallery data, or Grok's app data; the Grok credential file was not read.
- Environment variable values are never read into state; only names are inspected.

## Contract impact

None to shared contracts: read-only over existing records; optional provenance keys are only *read* if present.
Control Tower API additions are additive. Own files only: SQLite table `attributions`, `attributions.json` next to
the DB. Rollback = revert the v0.1.1 commit and delete `attributions.json`.

## Next (suggested)

- Codex: add `grok` / `claude` to `tools/character_scene.py --actor` and have Grok's orchestrators write
  `requested_by` into `handoff.json` so future runs are `record`-based instead of observed.
- If Grok starts using the WanGP Web UI directly (no run record), only the untracked-workload banner and the Grok
  agent card will reflect it; a Web UI queue adapter would be a separate task.
