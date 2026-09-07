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
