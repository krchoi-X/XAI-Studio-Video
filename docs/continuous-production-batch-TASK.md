# Continuous production batch recovery and controls

- Date: 2026-10-05
- Active editor: Codex
- Status: COMPLETE
- Direct user objective: recover the stalled Reika batch and implement items 1–7 from the diagnosis: safe orphan recovery, resume without duplicate preparation, Windows write retry, worker liveness, continuous-production naming, pause/resume/cancel/retry, and real character identity-reference delivery.

## Goal

Replace the time-of-day framing of the existing durable image batch with a time-independent sequential production queue, make stale workers unable to block the GPU, expose supported lifecycle controls, and bind the selected character's registered identity reference when requested.

## Constraints / Must Preserve

- Preserve existing batch directories, IDs, prepared sessions, attempts, outputs, failures, provenance and Gallery review state.
- Old `NIGHT-*` IDs and `/api/night-batches` routes remain readable for compatibility.
- Resume must reuse an item's recorded `session_dir`; it must not prepare or render a completed item again.
- Only a registered, existing character identity default may be sent. No arbitrary newest-image selection and no DNA/reference approval mutation.
- Preserve unrelated working-tree changes in both repositories.

## Must NOT Do

- No direct Gallery database edits, media deletion, canonical DNA change, publication, push, or silent engine fallback.
- Do not kill an unrelated process. A cancel request may terminate only the recorded live worker for that exact batch.
- Do not combine identity reference with engines that cannot bind it or with multiple engines in one item.

## Owned file scope

- `tools/character_manager.py`
- `tools/hermes_night_batch.py`
- `tests/test_hermes_night_batch.py`
- Personal Studio batch schemas/API/tests and Production batch/jobs UI/types/API/tests
- Personal Studio `DESIGN.md` wording for the user-approved time-independent queue
- This task record and a concise root `TASK.md` link

## Contract impact

- Producers: Studio Production form and existing callers of `hermes_night_batch.py create/run`.
- Consumers: batch worker, Studio batch list/GPU exclusion, Production job cards, Gallery sync.
- Persisted compatibility: existing schema-v1 plan/status files and `NIGHT-*` IDs stay readable. New lifecycle metadata (`worker_pid`, heartbeat, requested control state) is optional.
- Recovery: stale queued/running records are reconciled to `interrupted`; resume operates on the same directory and skips completed items. Retry resets failed/interrupted items but retains attempts and prior run records.
- Identity: a new optional request flag expands into `identity_reference: character-default` on each item only after the registered default exists and exactly one reference-capable engine is selected.
- Rollback: old readers ignore new optional fields; routes and file locations are unchanged. UI labels can revert independently.
- Deterministic verification: worker unit tests for atomic retry/liveness/resume/control/identity; Studio API tests for stale reconciliation and lifecycle routes; frontend interaction/model tests plus build.

## Plan

1. Harden atomic writes and worker terminal-state handling; add PID/heartbeat/stale reconciliation.
2. Add pause/cancel/resume/retry commands that preserve sessions and completed items.
3. Add compatible Studio API lifecycle routes and identity-reference validation/plan expansion.
4. Rename the operator surface to `연속 제작`, add identity control and wire job actions.
5. Recover the current orphaned Reika batch through the supported API/CLI, preserving its prepared session, then resume it with identity binding only if doing so does not rewrite the already prepared text-only session; otherwise interrupt it and create a corrected continuation without duplicate rendering.
6. Run focused backend/frontend/worker verification and update this record.

## Progress

- Verified incident `NIGHT-20261005-083733-55b211`: first item prepared, no renderer started, worker died on Windows `os.replace`, status remained `running`, GPU had no compute process or VRAM allocation.
- Recorded verified shared-skill feedback `skillfb-20261005T014626Z-f8c21a03`.
- Added bounded Windows atomic replace retries, PID/heartbeat ownership, stale-worker reconciliation, top-level failure finalization, and cooperative pause/cancel/resume/retry controls. Resume retains `session_dir`; completed items are skipped.
- Preserved `/api/night-batches` and historical `NIGHT-*` compatibility while new jobs use `BATCH-*` and the UI says `연속 제작`.
- Studio API validates registered identity defaults and one reference-capable engine before expanding `identity_reference: character-default` into every character-scene item. Production exposes the same choice and narrows engines to Krea2 or Qwen.
- Cancelled orphan `NIGHT-20261005-083733-55b211` after confirming 0 renders. Started corrected `BATCH-20261005-110125-df6b1a` with Krea2, two images per scene, and Reika's user-selected identity default. It completed 3/3 items and 6/6 artifacts; all three run records contain identity SHA-256 `ba3411fb8db4ac28aa5ce2807a1ac56e32fb9e47da4c357d4ac13734010a33b7`, `explicit-reference`, and `needs_review`.
- Studio was rebuilt/restarted. Live health is `ok`; the batch is newest in the API, its assets endpoint returns six IDs, and browser verification showed the `연속 제작` tab, completed 3/3 card, registered-face checkbox, and automatic Z-Image deselection when identity binding is enabled for Reika.

## Verification

- XAI interpreter: Hermes venv `python`, cwd `D:\codex\XAI-studio`: `python tests\test_hermes_night_batch.py` — 19 passed.
- Studio interpreter: `backend\.venv\Scripts\python.exe`, cwd `D:\codex\personal-prompt-studio\personal-prompt-studio\backend`; import resolved to this checkout. Focused continuous-batch/API/identity selection — 13 passed, one Starlette deprecation warning.
- Frontend, cwd `...\frontend`: `npm test -- --run` — 604 passed; `npm run build` passed (85 modules).
- `git diff --check` passed in both repositories (line-ending notices only).
- Live production verification: 3 completed sessions, two artifacts each, same registered identity hash; GPU returned to 0 MiB after completion.

## Next

Human review of the six restricted Reika results in Gallery. Cancellation is cooperative at safe item boundaries because the existing detached WanGP runner has no supported mid-render cancellation command; the current render is allowed to finish before the queue stops.
