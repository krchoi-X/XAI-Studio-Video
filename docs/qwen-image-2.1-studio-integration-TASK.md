# Qwen Image 2.1 Studio integration

Active editor: Claude Code (assigned by direct user decision, 2026-09-28)
Status: IN PROGRESS — Phase 1 (common CLI adapter and reference contract)
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

## File scope (Phase 1)

`tools/character_scene.py`, `tools/local_wangp.py`, `examples/character-lab/experiments/BATCH-002-harim-white-studio/qwen21.settings.json`, `tests/test_character_scene.py`, `tools/test_local_wangp.py`, this task file, root `TASK.md` pointer.

## Progress

- Read AGENTS/TASK/handoff/pilot, governance init (ok), production roles, catalog-resolved Character Manager skill, WanGP qwen/qwen21 handlers and `shared/api.py` settings merge.
- `python tools/wangp_models.py --check qwen_image_21_uncensored_q4_k_m` → `status: usable`, GGUF weights, 40 steps, guidance 4.

## Next

Implement Phase 1 code and tests.

## Blockers / uncertainties

- Whether `I` mode preserves identity well enough is unverified until the Phase 2 gate; `KI` remains an untested alternative (change one variable at a time).
