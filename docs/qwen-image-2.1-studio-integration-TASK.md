# Qwen Image 2.1 Studio integration

Active editor: Claude Code (assigned by direct user decision, 2026-09-28)
Status: PHASE 1 + PHASE 3 DONE (deterministic + one live run) — Phase 2 gate and Phases 4-5 pending
Date: 2026-09-28
Handoff: [integration handoff](qwen-image-2.1-studio-integration-handoff.md) · [pilot record](qwen-image-2.1-character-pilot-TASK.md) · [operator runbook](qwen-image-2.1-wangp-pilot.md)

## Goal

Make the installed local Qwen Image 2.1 uncensored GGUF an explicitly selectable Character Manager engine that can bind an already selected face master through the same hash-bound reference, recorder, Library and Gallery contracts used by Krea2 Identity Edit.

## Constraints / Must Preserve

- Qwen is never the default engine; `--engines` default stays `z-image,krea2`.
- Krea2 and Z-Image settings, the Krea2 Identity Edit compile and old sessions stay unchanged.
- Face-master bytes, canonical Stable DNA and review/visibility decisions are not modified.
- Unrelated dirty work in this checkout (drive-media-export scope, character sessions, staging folders) is preserved untouched.
- WanGP checkout, `env_uv`, the local Int8 ConvRot patch and `stash@{0}` are left alone.

## Must NOT Do

- No model download, quantization change, WanGP update or package change.
- No auto-promotion of generated profiles/masters; no direct Studio DB writes; no push.
- No agent-specific output silo or Qwen-specific gallery; no second engine alias.

## Decisions

- Logical engine ID and output directory: `qwen21` (`outputs/qwen21`). Label `Qwen Image 2.1`. Concrete `model_type`: `qwen_image_21_uncensored_q4_k_m`, WanGP architecture `qwen_image_21_7B`.
- Reference binding uses `video_prompt_type: "I"` ("Reference Images Are People or Objects"). Verified in WanGP source: `wgp.py` discards `image_refs` unless `video_prompt_type` contains `I`, and the qwen21 handler offers only `""`, `KI` (first image is the main subject/canvas) and `I`. `KI` is not assumed, per handoff.
- Qwen custom options are sent as `custom_settings: {"qwen21_kv_cache": "Disabled", "rgba": "Disabled"}`. WanGP reads them only from the `custom_settings` dict (`collect_custom_settings_from_inputs`); the handoff's top-level `qwen21_kv_cache` key would be silently ignored.
- Qwen jobs render one image per batch (`batch_size: 1`, `repeat_generation: count`) to respect the verified conservative 8 GB setting; Krea2/Z-Image keep `batch_size: count`.
- `local_wangp.validate_reference_settings()` accepts only models in an explicit `REFERENCE_MODELS` registry (engine, architecture, maximum reference count, required `video_prompt_type` letter). Qwen identity binding allows exactly one reference until a later contract widens it.

## Contract impact

- Producers: `tools/character_scene.py` (prepare/produce), later Studio Production API, Hermes night-batch plan, Transformation Lab (Phase 5).
- Consumers: `tools/local_wangp.py` submit/worker, `wangp_recorder` run records, creation-record snapshot, Library importer/sync, Gallery/Review, Control Tower job projection, old session readers, `tools/face_discovery.py` (shares `ENGINES`).
- New persisted values: logical engine `qwen21`, output directory `outputs/qwen21`, settings file `qwen21.settings.json`, `_xai.engine`/`_xai.model_type` in Qwen reference provenance, additive `engine` key on new batch jobs.
- Compatibility: old `z-image`/`krea2` sessions, Krea2 Identity Edit settings and Krea2-only transformation records load unchanged; the reader treats a missing job `engine` as the `output_dir` name, as before.
- Rollback: remove `qwen21` from `ENGINES`, `REFERENCE_ENGINES` and `REFERENCE_MODELS`; keep any Qwen session/output/run records as readable history.
- Publication: unchanged — restricted, `needs_review` until human action.

## Plan

1. Phase 1 — `qwen21` engine + template, split Krea2/Qwen reference compilers over a common provenance builder, registry-based reference validation, deterministic tests, one bounded live reference-bound run.
2. Phase 2 — fixed identity gate (8 images) with a user-selected face master; human review.
3. Phase 3 — night-batch validation for `qwen21`.
4. Phase 4/5 — Studio UI and Transformation Lab (separate checkpoints).

## File scope (Phases 1 and 3)

XAI-studio: `tools/character_scene.py`, `tools/local_wangp.py`, `tools/hermes_night_batch.py`, `examples/character-lab/experiments/BATCH-002-harim-white-studio/qwen21.settings.json`, `tests/test_qwen21_engine.py` (new), `tests/test_hermes_night_batch.py`, this task file, root `TASK.md` pointer.
XAI-Studio-Private (uncommitted, layered on Codex's uncommitted Krea2 reference-route edit): `shared-skills/character-manager/SKILL.md` (reference route, compiler engine sentence, night-batch rule), `shared-skills/qwen21-reference-engine-TASK.md`.
Studio: no changes yet.

## Progress

- Read AGENTS/TASK/handoff/pilot, governance init (ok), production roles, catalog-resolved Character Manager skill, WanGP qwen/qwen21 handlers and `shared/api.py` settings merge.
- `python tools/wangp_models.py --check qwen_image_21_uncensored_q4_k_m` → `status: usable`, GGUF weights, 40 steps, guidance 4.

- Phase 1 committed as `d20178d` (contract checkpoint). `ENGINES["qwen21"]`, `REFERENCE_ENGINES` (krea2/qwen21 compilers over common `reference_provenance`), `SINGLE_IMAGE_BATCH_ENGINES`, additive job `engine` key; `local_wangp.REFERENCE_MODELS` + `reference_model()`; `KREA2_EDIT_MODELS` kept as a derived alias.
- Phase 3: night batch accepts `qwen21`; a reference-bound item needs exactly one of `krea2`/`qwen21`; `verify_session(..., reference_bound)` also checks settings `model_type` equals the prepared job model and that a reference-bound run carries `image_refs`, `allow_text_fallback: false` and a hashed `reference_inputs` record. 48-item/240-image limits and GPU-lock retry unchanged.
- Canonical Character Manager skill wording updated for `qwen21` (Private, uncommitted).

## Verification

- Interpreter: Studio backend venv `D:/codex/personal-prompt-studio/personal-prompt-studio/backend/.venv/Scripts/python.exe` (pytest 8.4.2) with `PYTHONPATH=tools;tests;<Hermes site-packages for jsonschema>`, CWD `D:/codex/XAI-studio`.
- Focused: `tests/test_qwen21_engine.py tests/test_character_scene.py tools/test_local_wangp.py tests/test_creation_records.py` → 67 passed; `tests/test_hermes_night_batch.py tests/test_qwen21_engine.py` → 26 passed.
- Broad selection from `docs/verification.md` (tests, external_media_import/tests, recorder, local_wangp, requester provenance, reference variation worker, gpu-worker provision) → 342 passed, 2 skipped.
- `python tools/character_manager.py validate` → all OK; `python tools/shared_resources.py --skill character-manager` resolves the Private shared skill; `git diff --check` clean on changed files.
- Not covered: Studio backend/frontend (Phase 4), reference_variation_worker Qwen adapter (Phase 5).

## Live run (Phase 1 acceptance)

- Session `SCENE-20260928-113627-mizuki-reika-neutral-reconstruction-of-the-same` at `D:/AI_Studio/library/characters/ch-mizuki-reika/generations/…`; prepared with `--engines qwen21 --count 1 --identity-reference character-default --actor claude --strategy strict_translation`, submitted with `produce --session-dir`.
- Run `run-20260928-113701-b973b2c4`: `requested_by: claude`, `executor: local-wangp-worker`, renderer WanGP, settings `model_type: qwen_image_21_uncensored_q4_k_m`, effective `video_prompt_type: I`, `variation.engine: qwen21`, status `needs_review`. Seed 928113628, 832x608, 40 steps, CFG 4.
- Reference: Reika `face-09-editorial-1.png` (user-selected default), SHA-256 `ba3411fb8db4ac28aa5ce2807a1ac56e32fb9e47da4c357d4ac13734010a33b7`, 1,990,236 bytes, hash re-verified at submit.
- Duration: submit 11:37:01, denoising ~5 s/step, completed 11:40:55 (~4 min incl. load). VRAM was idle beforehand (no Ollama model loaded).
- Output: `outputs/qwen21/run-20260928-113701-b973b2c4.jpg` (SHA-256 `ca23e7ad…99e5`).
- Studio `POST /api/sync` → imported 1, skipped 1227. Asset `ast_4fa4b9dd5ebb361bf9067ebc`: engine `qwen21`, no decision (unreviewed), favorite false. `asset.model` is null, same as existing Krea2 assets (pre-existing importer behavior, not Qwen-specific).
- Observation: the reference reached the model (same black blazer, long black hair, grey backdrop). The request asked for head-and-shoulders but the render is full-body on the landscape 832x608 canvas, so the face is too small to judge identity.
- Inference (untested): the landscape canvas plus the Stable DNA body paragraph pushes full-body framing. Candidate single-variable change for the gate: portrait resolution (e.g. 608x832) at the same pixel count.
- Human decision: none yet; the image is a candidate only.

## Next

1. Phase 2 identity gate needs two decisions from the user: orientation/resolution for the gate (current 832x608 landscape produced full-body framing) and whether to add a `--seed` option so both fixed seeds are identical across the four cases (today seeds derive from the preparation timestamp). Then run 4 cases × 2 seeds with the Reika default and review.
2. Phase 4 Studio (schemas/main/model.ts) and Phase 5 Transformation Lab remain unstarted.
3. Commit the Private skill wording after the Codex-owned uncommitted edit underneath it is committed or accepted.

## Blockers / uncertainties

- Whether `I` mode preserves identity well enough is unverified until the Phase 2 gate; `KI` remains an untested alternative (change one variable at a time).
