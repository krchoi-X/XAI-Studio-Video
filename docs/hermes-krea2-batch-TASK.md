# Hermes Krea2 character-image batch reliability

Active editor: Codex
Status: COMPLETE — 2026-09-16 follow-up plan-shape repair
Date: 2026-09-16

## Goal

Make the existing Hermes character-image night batch prepare each DNA-backed scene once, submit one GPU job at a time, observe the terminal result, retry only GPU-lock contention with bounded backoff, and verify the durable session/output records before moving to the next item.

## Scope

- `tools/hermes_night_batch.py`
- `tests/test_hermes_night_batch.py`
- `docs/character-manager.md`
- `batch-plan.json` (current Hermes input; structure only, prompts preserved)
- This task record

## Constraints / Must Preserve

- Use `character_scene.py` as the only prompt/settings/session producer so canonical Character DNA, Scene Spec precedence, actor provenance, shared creation-record storage, and Gallery sync remain unchanged.
- Preserve failed run directories and their logs as evidence. Retries create a new run under the same prepared session.
- Keep one active Hermes batch and sequential item execution.
- Explicit user prompt and structured scene fields remain runtime input; no canonical DNA edit or reference approval.
- Do not launch a GPU render while implementing or testing.

## Must NOT Do

- Do not delete failed `runs/` directories.
- Do not require `basis: character-default` for ordinary Krea2 still generation; that marker is currently the Ref2VA default-reference contract.
- Do not bypass `character_scene.py`, write the Gallery database directly, publish, or change model defaults.
- Do not absorb unrelated dirty working-tree changes.

## Contract impact

Producer: `tools/hermes_night_batch.py` will persist per-item `session_dir`, attempt history, and verification evidence in its existing `plan.json` queue record. Consumer: Hermes/operators and Control Tower continue to read existing batch/session/run records; added keys are backward-compatible. Existing plans remain accepted. Failed runs are retained, while a lock-only failure may create another unique run in the same session. Rollback is limited to reverting the scoped code/doc changes. Deterministic verification uses mocked subprocess/session fixtures and the existing selected test suite; no live GPU job.

## Plan

1. Split scene preparation from rendering so retries reuse one durable session.
2. Detect GPU-lock-only failures from the command result and recorded run error, then retry after 10, 20, and 40 seconds.
3. Verify prompt/settings, completed job/run status, artifact existence, and output containment before marking an item completed.
4. Add focused regression tests and update Hermes documentation.

## Progress

- Confirmed `character_scene.py` already writes prompt/settings and waits for each engine, but a GPU-lock failure marks the job failed and exits.
- Confirmed the existing night batch continues after that failure without retrying it.
- Confirmed failed run deletion would violate production evidence retention and is unnecessary because recorder run IDs are unique.
- Changed the batch to prepare each scene once, reuse that session for rendering, and retry only recorded GPU-lock failures after 10, 20, and 40 seconds.
- Added completion verification for prompt/settings, job/run state, artifact count, file existence, output containment, model type, and any recorded reference basis.
- Added durable per-attempt logs/history without deleting failed runs; documented the Ref2VA-only meaning of `character-default`.

## Next

Hermes may enqueue the validated `batch-plan.json` with the existing `create --plan-file` command. No queue or GPU run was started during the repair.

## Blockers / uncertainties

Live GPU behavior was not exercised in this implementation pass.

## Follow-up diagnosis

Hermes wrote one parent item containing five `scenes`, while the queue contract requires each scene to be a separate item with a direct `prompt`. The prompts were already long; `validate_plan` read the missing parent `prompt` as empty and emitted the generic `prompt is too short` message. Prompt expansion cannot fix this structural mismatch.

## Follow-up repair and verification

- Flattened `batch-plan.json` to five canonical items, preserved the five prompt strings, selected only `krea2`, and set one image per scene.
- Replaced the misleading generic error with a structural nested-scenes diagnostic and added a regression test.
- Read-only plan validation: 5 items, 5 expected images, all `krea2`, prompt lengths 301-345 characters.
- Studio venv: `pytest tests/test_hermes_night_batch.py tests/test_character_scene.py -q`: 25 passed.
- Python compile and scoped `git diff --check`: passed; no queue creation or GPU execution.

## Verification

- `python -m py_compile tools/hermes_night_batch.py tests/test_hermes_night_batch.py`: passed.
- Studio venv: `pytest tests/test_hermes_night_batch.py -q`: 7 passed.
- Studio venv: `pytest tests/test_character_scene.py tests/test_creation_records.py tools/test_reference_variation_worker.py tests/test_hermes_night_batch.py -q`: 40 passed.
- `git diff --check` on scoped files: passed (Git reported only existing LF-to-CRLF checkout notices).
- Read-only comparison against preserved production records confirmed the exact GPU-lock message matched by the retry detector.
- A combined run including `tools/test_local_wangp.py` had 10 passes and 5 environment-dependent failures because active shared authority overrides those older tests' temporary `cm.CHARACTERS`; none touched the changed batch code. The scoped shared-authority-aware tests above pass.
