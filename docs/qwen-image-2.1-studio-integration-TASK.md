# Qwen Image 2.1 Studio integration

Active editor: Claude Code (assigned by direct user decision, 2026-09-28)
Status: PHASES 1-5 IMPLEMENTED AND LIVE-VERIFIED — human review of all Qwen candidates pending; Qwen is not a default
Date: 2026-09-28
Return handoff to Codex: [Claude → Codex](qwen-image-2.1-claude-to-codex-handoff.md) · Handoff: [integration handoff](qwen-image-2.1-studio-integration-handoff.md) · [pilot record](qwen-image-2.1-character-pilot-TASK.md) · [operator runbook](qwen-image-2.1-wangp-pilot.md)

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

## Phase 1b scope (user decision 2026-09-28)

The user chose portrait orientation, a `--seed` option, and Qwen multi-reference support.

- `qwen21.settings.json` resolution becomes `608x832` (same pixel count as the verified 832x608; both are multiples of the 32-pixel VAE block).
- `--seed N` on `prepare`/`produce`: the first selected engine uses exactly N, the next N+1, and so on. Without it, seeds stay timestamp-derived. Refused with `--session-dir`.
- Repeatable `--reference ROLE=PATH` (roles: `wardrobe`, `object`, `background`, `style`) for `qwen21` only. It requires `--identity-reference`; the face master is always `<image1>` and extra references follow in the given order as `<image2>`… A `REFERENCE IMAGES` map in the prompt tells the model what to take from each. At most 4 references in total (WanGP allows 10; kept at 4 for the 8 GB card until measured). Each extra reference is hash-bound like the identity reference.
- Night batch items may carry `additional_references` and `seed`, with the same restrictions.
- Contract additions: `_xai.reference_roles` (Qwen only), extra entries in `reference_inputs`, optional `session.requested_seed` in `batch.yaml`. Krea2 `_xai` keys and single-reference prompts are unchanged.

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
shared-authority repository (uncommitted, layered on Codex's uncommitted Krea2 reference-route edit): `shared-skills/character-manager/SKILL.md` (reference route, compiler engine sentence, night-batch rule), `shared-skills/qwen21-reference-engine-TASK.md`.
Studio: no changes yet.

## Progress

- Read AGENTS/TASK/handoff/pilot, governance init (ok), production roles, catalog-resolved Character Manager skill, WanGP qwen/qwen21 handlers and `shared/api.py` settings merge.
- `python tools/wangp_models.py --check qwen_image_21_uncensored_q4_k_m` → `status: usable`, GGUF weights, 40 steps, guidance 4.

- Phase 1 committed as `d20178d` (contract checkpoint). `ENGINES["qwen21"]`, `REFERENCE_ENGINES` (krea2/qwen21 compilers over common `reference_provenance`), `SINGLE_IMAGE_BATCH_ENGINES`, additive job `engine` key; `local_wangp.REFERENCE_MODELS` + `reference_model()`; `KREA2_EDIT_MODELS` kept as a derived alias.
- Phase 3: night batch accepts `qwen21`; a reference-bound item needs exactly one of `krea2`/`qwen21`; `verify_session(..., reference_bound)` also checks settings `model_type` equals the prepared job model and that a reference-bound run carries `image_refs`, `allow_text_fallback: false` and a hashed `reference_inputs` record. 48-item/240-image limits and GPU-lock retry unchanged.
- Canonical Character Manager skill wording updated for `qwen21` (Private, uncommitted).

## Verification

- Interpreter: Studio backend venv `${STUDIO_ROOT}/backend/.venv/Scripts/python.exe` (pytest 8.4.2) with `PYTHONPATH=tools;tests;<Hermes site-packages for jsonschema>`, CWD `${PROJECT_ROOT}`.
- Focused: `tests/test_qwen21_engine.py tests/test_character_scene.py tools/test_local_wangp.py tests/test_creation_records.py` → 67 passed; `tests/test_hermes_night_batch.py tests/test_qwen21_engine.py` → 26 passed.
- Broad selection from `docs/verification.md` (tests, external_media_import/tests, recorder, local_wangp, requester provenance, reference variation worker, gpu-worker provision) → 342 passed, 2 skipped.
- `python tools/character_manager.py validate` → all OK; `python tools/shared_resources.py --skill character-manager` resolves the Private shared skill; `git diff --check` clean on changed files.
- Not covered: Studio backend/frontend (Phase 4), reference_variation_worker Qwen adapter (Phase 5).

## Live run (Phase 1 acceptance)

- Session `SCENE-20260928-113627-mizuki-reika-neutral-reconstruction-of-the-same` at `${XAI_WORKSPACE_ROOT}/library/characters/ch-example-alpha/generations/…`; prepared with `--engines qwen21 --count 1 --identity-reference character-default --actor claude --strategy strict_translation`, submitted with `produce --session-dir`.
- Run `run-20260928-113701-b973b2c4`: `requested_by: claude`, `executor: local-wangp-worker`, renderer WanGP, settings `model_type: qwen_image_21_uncensored_q4_k_m`, effective `video_prompt_type: I`, `variation.engine: qwen21`, status `needs_review`. Seed 928113628, 832x608, 40 steps, CFG 4.
- Reference: Reika `face-09-editorial-1.png` (user-selected default), SHA-256 `ba3411fb8db4ac28aa5ce2807a1ac56e32fb9e47da4c357d4ac13734010a33b7`, 1,990,236 bytes, hash re-verified at submit.
- Duration: submit 11:37:01, denoising ~5 s/step, completed 11:40:55 (~4 min incl. load). VRAM was idle beforehand (no Ollama model loaded).
- Output: `outputs/qwen21/run-20260928-113701-b973b2c4.jpg` (SHA-256 `ca23e7ad…99e5`).
- Studio `POST /api/sync` → imported 1, skipped 1227. Asset `asset-example-unreviewed`: engine `qwen21`, no decision (unreviewed), favorite false. `asset.model` is null, same as existing Krea2 assets (pre-existing importer behavior, not Qwen-specific).
- Observation: the reference reached the model (same black blazer, long black hair, grey backdrop). The request asked for head-and-shoulders but the render is full-body on the landscape 832x608 canvas, so the face is too small to judge identity.
- Inference (untested): the landscape canvas plus the Stable DNA body paragraph pushes full-body framing. Candidate single-variable change for the gate: portrait resolution (e.g. 608x832) at the same pixel count.
- Human decision: none yet; the image is a candidate only.

## Phase 1b verification (commit `db635db`)

- Tests: focused `test_qwen21_engine`, `test_hermes_night_batch`, `test_character_scene`, `tools/test_local_wangp` → 93 passed. Broad selection from `docs/verification.md` → 354 passed, 2 skipped. `git diff --check` clean.
- Live run: session `SCENE-20260928-115541-mizuki-reika-upper-body-portrait-of-the`, run `run-20260928-115542-d9427e3b`, `--engines qwen21 --count 1 --identity-reference character-default --reference wardrobe=${PROJECT_ROOT}/_tmp_refs/uniform-175243_1.jpg --seed 20260928 --actor claude`. Effective settings 608x832, seed 20260928, `video_prompt_type: I`, two `image_refs`; run record `reference_inputs` roles identity (SHA `ba3411fb…`) and wardrobe (SHA `2376ce1d…`), `requested_by: claude`. Duration 11:55:42 → 12:01:04 (~5m22s, two references). Output `outputs/qwen21/run-20260928-115542-d9427e3b.jpg` 608x832. Studio sync imported 1; asset `asset-example-multiref`, engine `qwen21`, no decision, favorite false.
- Observation: the white logo polo and navy skirt from `<image2>` transferred; the `<image2>` model's face (bangs, rounder face) did not leak; the grey studio from the request replaced the store background; the bracelet was not copied. Framing is about three-quarter body although the request said upper-body.
- Inference (untested): the Stable DNA body paragraph (height, long legs) pulls toward full-body framing on both orientations. Test by one variable, e.g. a Scene Spec `camera` value for a close framing, before changing settings.
- Human decision: none; both live outputs are candidates.

## Phase 2 identity gate results (run by Claude at the user's request, 2026-09-28)

Setup: Reika `character-default` (face-09, SHA `ba3411fb…`), 4 cases x seeds 20260928/20260929 on `qwen21` (608x832, 40 steps, CFG 4) and on the `krea2` Identity Edit baseline (768x1024, 8 steps), all `strict_translation`, actor `claude`, plus one added variable for both engines: Scene Spec `camera` = tight head-and-shoulders close-up. 16/16 renders completed. Runner, manifest, scores and sheet: `${XAI_WORKSPACE_ROOT}/reports/ch-example-alpha/qwen21-gate-20260928/` (`run_gate.py`, `gate-manifest.json`, `gate-results.json`, `gate-score.json`, `crossseed-*.json`, `gate-contact-sheet.jpg`). Studio sync imported 16 (all unreviewed).

Measurement: `tools/identity_score.py` (SFace + ArcFace on the same aligned crop) against prototype `prototype-reika-face-09.json`; thresholds from `docs/identity-scoring-calibration.json` (same >= 0.83/0.84, different <= 0.551). All faces 166-328 px, above the 150 px floor.

| case | Qwen21 s28 (SF/AF) | Qwen21 s29 | Krea2 s28 | Krea2 s29 |
|---|---|---|---|---|
| reconstruction (frontal) | 0.916/0.892 same | 0.876/0.856 same | 0.739/0.680 drift | 0.744/0.686 drift |
| clothing only (frontal) | 0.881/0.896 same | 0.901/0.873 same | 0.815/0.731 drift | 0.749/0.716 drift |
| 45-degree (three-quarter) | 0.839/0.767 drift | 0.801/0.763 drift | 0.665/0.670 drift | 0.628/0.582 drift |
| 90-degree profile | 0.496/0.454 uncalibrated | 0.477/0.580 uncalibrated | 0.431/0.572 uncalibrated | 0.363/0.517 uncalibrated |

Cross-seed consistency (seed 28 vs seed 29, same engine and case), SF/AF: Qwen reconstruction 0.882/0.835, clothing 0.875/0.857, 45-degree 0.783/0.795, profile 0.796/0.717; Krea2 0.855/0.810, 0.885/0.826, 0.736/0.754, 0.799/0.739.

- Observation: Qwen21 reached the calibrated "same" band on all four frontal images; Krea2 Identity Edit stayed in "drift" on all eight. The clothing edit changed only the garment on Qwen. At 45 degrees Qwen is SFace-borderline and ArcFace-drift (0.76-0.77), still ahead of Krea2. Qwen produced true side profiles (one bucketed deep three-quarter); Krea2 produced deep three-quarter views, not profiles.
- Limits: profile and deep three-quarter buckets have no calibrated threshold (recognisers lose accuracy off-axis), so those numbers are not a verdict. Recognisers are trained on real photos; n=2 seeds per cell; one character. The Krea2 baseline differs in resolution/steps by design (its standard edit route).
- Inference: for frontal identity preservation from one face master, Qwen21 is materially better than the current Krea2 Identity Edit route on this character. Angled views remain the weak point for both.
- Human decision: pending. No profile or output is promoted; the gate outputs stay unreviewed candidates.
- Producer finding: preparing the same request with different `--seed` values within one second collided on session ID (refused safely, "shared session already exists"; 5 of 16, retried later). Fixed after the gate by appending the seed to new seeded session IDs.

## Phase 4 — Studio engine selection (Studio commit `b886111`)

- Backend: `ImageEngine` literal adds `qwen21` (max 3 engines); identity image requires exactly one of `IDENTITY_REFERENCE_ENGINES` (krea2, qwen21).
- Frontend: `Qwen Image 2.1` offered in the existing selector. Found and fixed: `ProductionApp` preselected every offered engine, which would have made Qwen a silent default; now `initialEngines()` selects only `defaultSelectedEngines` (Z-Image + Krea2). Identity reducer keeps a single selected reference engine, falls back to Krea2, and switches Krea2<->Qwen without dropping the identity image.
- Also fixed 5 pre-existing `tests/test_api.py` failures (same 5 fail on clean HEAD): stub repos lacked `tools/character_manager.py`, so this workstation's live shared authority returned 409. Test-only fix following the suite's existing stub convention.
- Checks: backend 135 passed; frontend 549 passed then 553 after Phase 5; `npm run build` OK. Studio server restarted via its supervisor (kill uvicorn; supervisor relaunches) and `/api/health` OK.
- Live: `POST /api/characters/ch-example-alpha/generation-jobs` with `engines: ["qwen21"], use_identity_reference: true` → job `gen_69968d2f…` completed through `web_generation_worker` → `character_scene`; session `SCENE-20260928-130646-mizuki-reika-same-person-facing-the-camera`, run `run-20260928-130647-ed514f3e`, `requested_by: web`, hash-bound identity reference, `outputs/qwen21`, auto-synced. Mixed `["qwen21","krea2"]` with identity → 422 live.
- Observation: that request asked for a soft smile + turtleneck; score SF 0.753 / AF 0.661 (drift, 209 px frontal face), visibly softer face. n=1; expression change is a candidate cause, untested.

## Phase 5 — Transformation Lab (XAI `96b593b`, Studio `7758cd3`)

- `reference_variation_worker.py`: per-engine adapters (settings, dependencies, output dir, labels); `engine_id` absent = Krea2, so old records are unchanged. Qwen adapter: `video_prompt_type: I`, hash-bound `_xai` (passes the `local_wangp` registry gate), 608x832 or 832x608 by source orientation, dependencies read from the WanGP finetune definition. Pose/hand recomposition still `blocked_capability` for both engines.
- Studio: `ReferenceVariationRequest.engine` (default krea2); request keeps historical `engine`/`preferred_engine` values for Krea2 and adds `engine_id`; plan capability/queue text/summary name the engine; form offers a chip row. Tests: worker 8 passed; Studio API 13 passed; frontend 553 passed.
- Live: plan preview for Reika face master `asset-example-face-master` with a wardrobe operation → `identity_edit`, capability `Qwen Image 2.1 (reference)`, binding SHA `ba3411fb…`. Variation `var_123579bd…` completed: session `VARIATION-20260928-041321-cd812c7d`, run `run-20260928-131322-728cddc5`, `requested_by: web`, reference role `source`, `outputs/qwen21`, synced to `ses-variation-20260928-041321-cd812c7d`.
- Observation: identity SF 0.913 / AF 0.935 (same). Edit compliance partial: the inner top became a white shirt but the black jacket the request also asked to replace was kept.

Sheets: `${XAI_WORKSPACE_ROOT}/reports/ch-example-alpha/qwen21-gate-20260928/gate-contact-sheet.jpg`, `studio-paths-sheet.jpg`.

## Remaining checks closed (2026-09-28, user asked to proceed)

- Browser UI (built-in browser, `http://127.0.0.1:8787`, desktop and 768x1024 tablet): Production shows `Qwen Image 2.1` under 고급 설정, not preselected ("예상 4장"); turning on 지정된 얼굴 narrows to Krea2; clicking Qwen switches to Qwen and keeps the face image ("예상 2장"); adding Z-Image releases it. Transformation Lab shows the 엔진 chip row (Krea2 default) and the plan's engine line follows the choice live (Krea2 Identity Edit -> Qwen Image 2.1 (reference)). Nothing was submitted from the browser.
- Genuine Hermes request: Hermes itself (`hermes -z`, local 27B model) wrote `${XAI_WORKSPACE_ROOT}/workspace/hermes-plans/qwen21-check-20260928.json` and ran `hermes_night_batch.py create --no-start` -> `NIGHT-20260928-175511-763302` (`created_by: hermes`). It took Hermes several hours on its local model. Claude waited until Hermes' model left VRAM (7.9 GB -> 0) and then ran the queue's own `run`, so the requester record is truthful and the render did not share the GPU.
- Qwen night batch live: item completed and passed `verify_session(..., reference_bound=True)`; session `SCENE-20260928-175554-mizuki-reika-same-person-facing-the-camera-s20260930` (seed suffix), run `run-20260928-175555-d3048b4c`, `requested_by: hermes`, executor `local-wangp-worker`, identity reference role recorded, `outputs/qwen21`, post-run sync without error. Score SF 0.828 / AF 0.872, 205 px frontal -> recognisers disagree (SFace just under 0.83); goes to human review.

## Next

1. Human review in Studio of the gate (16), Studio (1) and Transformation Lab (1) candidates; nothing is promoted automatically.
2. Open questions worth one-variable tests: expression changes vs identity drift on Qwen; 45-degree drift (AF ~0.76); whether `KI` edits preserve collateral detail better than `I` for Transformation Lab.
3. Studio multi-reference UI is not built (CLI and night batch support it). Seed is not exposed in Studio.
4. Commit the Private skill wording once the Codex-owned uncommitted edit beneath it is committed.
5. Earlier item kept for history: Phase 2 identity gate with `--seed` (e.g. 20260928 and 20260929) on 608x832, Reika default, four cases. Consider a Scene Spec `camera` close-framing value first, because face size currently limits identity judgement.
2. Phase 4 Studio (schemas/main/model.ts) and Phase 5 Transformation Lab remain unstarted.
3. Commit the Private skill wording after the Codex-owned uncommitted edit underneath it is committed or accepted.

## Blockers / uncertainties

- Whether `I` mode preserves identity well enough is unverified until the Phase 2 gate; `KI` remains an untested alternative (change one variable at a time).
