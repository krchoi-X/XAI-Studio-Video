# Current Task

Status: ACTIVE — establish the Reference Transformation v2 contract and v1 compatibility checkpoint.

## Goal

Provide the execution-side contract for reliable reference-bound changes to face, pose/hands, clothing, background, lighting, camera, and framing. Normalize existing v1 Reference Variation records, deterministically resolve locks and strategies, and prevent unsupported or non-reference execution from reaching the GPU.

## Constraints / Must Preserve

- Keep every existing schema-v1 request readable and unchanged on disk.
- Krea reference editing remains `krea2_turbo_edit` with actual `image_refs` and source hash verification.
- No silent text-to-image fallback.
- Strategy and conflict resolution are deterministic; Hermes/MeroMero may translate prose but may not choose capability or remove locks.
- Do not enable uncalibrated numeric strength mappings.
- Generated media remains outside Git under `D:\AI_Studio\library`.

## Must NOT Do

- Do not run GPU calibration without the user's separate go-ahead for generation.
- Do not claim Z-Image reference editing until a local reference-bound path is proven.
- Do not mutate Character DNA or Visual Canon from a transformation result.
- Do not push private character metadata to the public upstream.

## Plan

1. Commit a v2 JSON Schema, a sanitized representative v1 fixture, and deterministic normalizer/strategy tests.
2. Update the worker to consume normalized v1/v2 plans and emit Prompt Trace v2 while retaining queued-v1 behavior.
3. Coordinate the private Studio backend v2 writer and dual reader.
4. Run a capped, fixed-source Krea calibration matrix only after user approval.
5. Integrate the tablet presentation and validate end to end.

## Progress

- [x] Verify the dedicated Krea2 edit model, Identity Edit preset, Qwen vision encoder, and reference hash guard.
- [x] Confirm current v1 strength is metadata-only and pose/hand requests need a distinct strategy.
- [x] Add schema, fixture, normalizer, and tests (`9 passed`, including existing worker tests).
- [x] Update the worker to normalize v1/v2, emit Prompt Trace v2 for identity edits, and block unverified recomposition before GPU submission.
- [ ] Calibrate and integrate.

## Next

Commit the worker integration checkpoint. Next, design the capped calibration run; do not execute GPU work without user approval.

## Contract Impact

- Producers: Personal Studio backend and future validated Hermes/MeroMero compiler.
- Consumers: `reference_variation_worker.py`, WanGP submission settings, Prompt Trace readers, Gallery lineage/sync, Personal Studio status UI, and future DNA evidence synthesis.
- Existing records: schema-v1 `request.json` files with `changes`, `preserve`, `strength`, and a resolved reference path/hash. A sanitized v1 fixture is required.
- Compatibility: a pure normalizer accepts v1 and v2. Existing queued v1 jobs retain behavior. V2 writing is not enabled by this checkpoint.
- Rollback: remove/disable v2 creation while retaining dual readers; no in-place migration.
- Verification: schema fixture validation, conflict/strategy tests, worker settings tests, and later API/end-to-end tests.

## Work Allocation

- **Codex:** this contract, worker/adapter, capability profile, and cross-repo integration.
- **Claude Code:** no execution-side files; it receives only the isolated C7 UI package after shared contracts land.
- **Hermes/MeroMero:** bounded operation suggestions validated against this contract.

## Blockers / Uncertainties

- A verified local reference-aware recomposition path for major pose/hand changes is not yet established; those plans must return `blocked_capability` until proven.
- Numeric denoising/masking behavior needs capped visual calibration.

## Relevant Files

- `schemas/reference-transformation-request-v2.schema.json`
- `tools/reference_transformation_contract.py`
- `tools/reference_variation_worker.py`
- `tests/fixtures/reference-transformation/**`
- `tests/test_reference_transformation_contract.py`
- `D:\codex\personal-prompt-studio\personal-prompt-studio\docs\architecture\reference-transformation-lab-v2.md`
