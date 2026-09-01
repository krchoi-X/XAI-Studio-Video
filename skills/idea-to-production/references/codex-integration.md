# Integration Note for Codex

Package C3 delivered workflow prose, templates, and deterministic fixtures only. No adapter, queue, API, or schema file was created or modified. This note lists what still has to be wired on the Codex side and the assumptions C3 made while waiting for it.

## Schema version used

All four v1 schemas as committed in `bee2f16`, unmodified:

- `schemas/idea-production-request-v1.schema.json`
- `schemas/storyboard-candidates-v1.schema.json`
- `schemas/renderer-job-request-v1.schema.json`
- `schemas/production-job-result-v1.schema.json`

Plus the pre-existing `schemas/scene-spec-v1.schema.json`, used unmodified as the shape for the free-form `scene_spec` and `structured_scene_spec` objects.

## Assumptions C3 made

These are conventions chosen inside the space the schemas leave open. Each is enforced by `tests/fixtures/idea-to-production/validate_fixtures.py`. If Codex decides differently, change the fixture expectations and this note together.

| # | Assumption | Where it lives |
|---|---|---|
| 1 | `sample_request` = `renderer-job-request-v1` fields minus `job_id` and `prompt_trace`, with `stage: "sample"`. The queue mints both at submission. | `shot.sample_request` |
| 2 | `scene_spec` and `structured_scene_spec` use `scene-spec-v1` field names, and `scene_spec.mode` equals `prompt_strategy`. | free-form objects |
| 3 | `after_constraint_validation` uses the shape `{ok, precedence, applied_constraints, conflicts, dropped_enrichment, errors}`. | free-form object |
| 4 | `continuity` uses stable keys (`carries_from`, `location`, `time_of_day`, `wardrobe`, `hair_state`, `props`, `emotional_state`) so a reviewer can diff shots. `carries_from` is `null` on the first shot. | free-form object |
| 5 | `exact` mode clamps `candidate_count` to one storyboard with one shot. Producing variants would require rewriting the prompt, which contract rule 3 forbids. | `SKILL.md` |
| 6 | Error `code` vocabulary as listed in `references/failure-modes.md`. The schemas accept any non-empty string. | `errors[].code` |
| 7 | Sample stage defaults to `engines: ["z-image"]`, `count: 2`; final to `engines: ["z-image", "krea2"]`, `count: 4`. Taken from `tools/character_scene.py` and `tools/hermes_night_batch.py`. | templates |
| 8 | `progress.total == count × len(engines)`. | fixtures |
| 9 | `result_session_id` is prefixed `sess_`, `asset_ids` `asset_`. Neither is pattern-constrained by the schema. | fixtures |
| 10 | A retry is a new `job_id` under the same `request_id`, with a byte-identical prompt. | `references/failure-modes.md` |

Assumptions 1–3 are the ones that constrain Codex's implementation. The rest are cosmetic and cheap to change.

## Remaining Codex work

### 1. Adapter resolution contract

C3 specifies *that* references resolve through an approved adapter and *that* an unresolved ID is fatal, but there is no adapter interface yet — `adapters/` holds only a README. Needed:

- a resolve call taking a list of character and asset IDs and returning per-ID resolved/not-found/access-denied;
- a stable mapping from that result to the `character_not_found` / `reference_not_found` / `reference_access_denied` / `adapter_unavailable` codes;
- restricted-media gating, so `reference_access_denied` is distinguishable from `reference_not_found`.

### 2. Durable job ID minting

Contract rule 5 requires a job ID before execution. Needed: the enqueue call that mints `job_[A-Za-z0-9_-]+`, persists the request, and returns the ID before the renderer starts. The fixtures assume this exists and never generate an ID locally.

### 3. Result persistence and state transitions

`queued → running → completed | failed | interrupted`, with `interrupted` set by crash recovery rather than by the worker. Needed: partial `asset_ids` retention, real `progress` counts on failure, and `result_session_id` assignment as soon as the first asset lands so a partial batch is reviewable.

### 4. `result_session_id` to Gallery

Rule 6 makes this the Gallery handoff key. Needed: the lookup that turns it into a reviewable set, and confirmation that the frontend never treats it as a path. C2's `GenerationJobSummary.resultSessionId` is the consumer.

### 5. Retry semantics

Needed: a retry entry point that reuses `request_id`, `storyboard_id`, `shot_id`, `stage`, and prompt while minting a new `job_id`, and that leaves the failed result on record.

### 6. Wiring the validator into CI

`validate_fixtures.py` is deliberately not named `test_*.py`, so `pytest tests/` does not collect it and the existing suite is unchanged. To run it in CI, either add a one-line `tests/test_idea_to_production_fixtures.py` that shells out to it, or rename it — both touch files C3 does not own.

### 7. Skill routing

`skills/README.md` lists only `storyboard-director` and is not owned by C3. Add an `idea-to-production` entry when this skill goes live, and decide the routing rule between the two: `storyboard-director` designs beats, `idea-to-production` carries a request through the contracts. `HERMES.md` may also want a pointer.

## What C3 deliberately did not do

- No adapter, queue, API, or persistence code.
- No modification to `tools/`, `adapters/`, `schemas/`, or any existing test.
- No new schema and no change to a field name or enum.
- No Character DNA read or write. The identity text in the fixtures is illustrative prose, not a canonical DNA dump, and the fixtures pass without any character record being present.
- No renderer invocation. Every render outcome in the fixtures is a hand-written example of an adapter result, not a recorded run.

## Known limitations

- The fixtures encode one shot per submitted job. Multi-shot candidates imply one job per shot; that fan-out is not exercised.
- `output_intent: "video"` and `"mixed"` are accepted by the request schema but no fixture covers them, and neither templates nor `SKILL.md` describe a video-specific compile path.
- No fixture covers `status: "queued"` or `"running"` in `production-job-result-v1`, since C3 has no queue to observe them from. `needs_user_choice` as a *result* status is likewise unexercised — C3 uses it only on `storyboard-candidates-v1`.
- Conflict detection between two level-1 constraints is specified as a rule and shown as a fixture, but the actual detection is a judgement the skill makes at runtime; there is no deterministic conflict-matrix implementation.
- The validator checks documents, not behavior. It cannot prove the skill never edits Stable DNA; that guarantee rests on the skill text plus the existing `character_manager.py` guard.
