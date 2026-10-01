# Qwen Image 2.1 integration — Claude Code → Codex handoff

- Date: 2026-09-28
- From: Claude Code (implementation editor by user assignment)
- To: Codex (integration steward for shared contracts)
- Detailed record: [integration task](qwen-image-2.1-studio-integration-TASK.md) · original brief: [Codex handoff](qwen-image-2.1-studio-integration-handoff.md)
- Nothing was pushed in any repository.

## What Codex needs to do

1. **Review the contract checkpoint.** Shared CLI, schema and API boundaries that are integration-owned by default were changed under the user's direct assignment. Review the commits below, especially the persisted-field additions under "Contract changes".
2. **Decide the open questions** at the end of this note; none of them block current use.
3. **Do not re-run the identity gate or re-implement phases.** All five handoff phases are implemented, tested and live-verified. Only human review of the candidates remains.

## Status against the original handoff

| Handoff item | State |
|---|---|
| Phase 1 — common CLI adapter and reference contract | Done, live-verified |
| Phase 2 — identity gate (4 cases x 2 seeds) | Run and measured; human review pending |
| Phase 3 — Hermes night batch | Done; live run requested by Hermes itself |
| Phase 4 — Studio Production UI | Done; API and browser (desktop + tablet) verified |
| Phase 5 — Transformation Lab parity | Done; live Qwen variation completed |
| Canonical Character Manager skill wording | Committed in Private (with Codex's earlier uncommitted Krea2 reference-route edit, at the user's direction) |
| User additions: portrait default, `--seed`, Qwen multi-reference | Done (CLI and night batch; not in Studio UI) |

## Commits

XAI-studio (base `4ee2b78`):

- `d20178d` qwen21 engine with hash-bound identity reference (Phase 1)
- `8ae692d` night batch accepts qwen21 and verifies reference-bound runs (Phase 3)
- `db635db` qwen21 portrait default, `--seed`, multi-reference
- `7cff8d3` seeded sessions of one request get distinct IDs
- `96b593b` Transformation Lab worker engine adapters (Phase 5)
- `605ebe1`, `5640194`, `d27a8fe`, `e3752bd` task-record updates
- `3c4ddf1` Codex's WanGP pilot runbook, committed unchanged

personal-prompt-studio (base `3d3194e`):

- `b886111` Qwen engine selection + capability-aware identity rule (Phase 4); also fixes 5 pre-existing `tests/test_api.py` fixture failures
- `7758cd3` Transformation Lab engine choice (Phase 5)
- `d3122c5` Studio TASK update

shared-authority repository (base `9608ade`):

- `1803e32` Character Manager skill: reference route for Krea2 and Qwen, including Codex's 2026-09-16 edit and both task records

## Contract changes

All additive; old sessions, requests and Krea2 records load unchanged. No migration was run.

- **Logical engine `qwen21`**, output directory `outputs/qwen21`, settings file `qwen21.settings.json`. Concrete `model_type`: `qwen_image_21_uncensored_q4_k_m` (architecture `qwen_image_21_7B`). Never a default.
- **`tools/character_scene.py`**
  - `ENGINES["qwen21"]`, `REFERENCE_ENGINES` (krea2, qwen21), per-engine reference compilers over a common `reference_provenance()`. Krea2 settings and `_xai` keys are unchanged (asserted in tests).
  - New CLI: `--reference ROLE=PATH` (repeatable; roles `wardrobe`, `object`, `background`, `style`; qwen21 only; requires `--identity-reference`; face master is always `<image1>`; max 4 images in total) and `--seed N` (first engine uses N exactly, next N+1…). Both are refused with `--session-dir`.
  - New persisted fields: job `engine` key in `batch.yaml`; optional `session.requested_seed`; Qwen-only `_xai.engine`, `_xai.model_type`, `_xai.reference_roles`; extra entries in `reference_inputs`. Seeded session IDs end in `-s<seed>`.
- **`tools/local_wangp.py`**: `REFERENCE_MODELS` registry replaces the Krea2-only set (`KREA2_EDIT_MODELS` kept as a derived alias). Qwen requires `video_prompt_type` containing `I`; up to 4 references; per-reference roles recorded.
- **`tools/hermes_night_batch.py`**: accepts `qwen21`; a reference-bound item uses exactly one of krea2/qwen21; new optional item fields `additional_references` and `seed`; `verify_session(..., reference_bound)` also checks the prepared model and hash-bound reference. Limits (48 items / 240 images), GPU lock and post-run sync are unchanged.
- **`tools/reference_variation_worker.py`**: dispatches on request `engine_id` (absent = krea2).
- **Studio backend**: `ImageEngine` literal (max 3 engines) for generation and night-batch requests; `IDENTITY_REFERENCE_ENGINES`; `ReferenceVariationRequest.engine` (default krea2); variation request record adds `engine_id` and keeps `engine`/`preferred_engine` = `krea2_identity_edit` for Krea2. `ReferenceVariationSummary.engine` added.
- **Studio frontend**: `defaultSelectedEngines` and `initialEngines()` separate offered engines from preselected ones; Transformation Lab draft carries `engine`.

**Rollback:** remove `qwen21` from `ENGINES`, `REFERENCE_ENGINES`, `REFERENCE_MODELS`, the night-batch sets, the Studio literals/options and `VARIATION_ENGINES`. Existing Qwen sessions stay readable as history.

## Verified WanGP facts (from WanGP source)

- `wgp.py` discards `image_refs` unless `video_prompt_type` contains `I`. The qwen21 handler offers `""`, `KI` (first image is the main subject/canvas) and `I` (references are people or objects). The integration uses `I`.
- Qwen options must be sent inside `custom_settings` (`qwen21_kv_cache`, `rgba`). The original handoff's top-level `qwen21_kv_cache` would be silently ignored.
- Qwen jobs render one image per batch and repeat it (8 GB setting). 608x832 and 832x608 are multiples of the 32-pixel VAE block.

## Bugs found and fixed

- Studio `ProductionApp` preselected every offered engine, so adding Qwen would have made it a silent default.
- Seed sweeps of one request inside one second collided on session ID (safely refused).
- 5 `tests/test_api.py` tests failed on clean HEAD on this workstation: stub repositories lacked `tools/character_manager.py`, so the live shared authority returned 409. Test-only fix using the suite's existing stub convention.

## Identity measurements

Tool: `tools/identity_score.py` (SFace + ArcFace) against the Reika face master `face-09-editorial-1.png` (SHA `ba3411fb…`), thresholds from `docs/identity-scoring-calibration.json` (same ≥ 0.83/0.84). All faces 166–328 px (above the 150 px floor) with a tight head-and-shoulders Scene Spec `camera` on both engines.

| Case | Qwen21 (2 seeds, SF/AF) | Krea2 Identity Edit (2 seeds) |
|---|---|---|
| Reconstruction | 0.916/0.892, 0.876/0.856 — same | 0.739/0.680, 0.744/0.686 — drift |
| Clothing only | 0.881/0.896, 0.901/0.873 — same | 0.815/0.731, 0.749/0.716 — drift |
| 45 degrees | 0.839/0.767, 0.801/0.763 — drift | 0.665/0.670, 0.628/0.582 — drift |
| 90-degree profile | uncalibrated bucket | uncalibrated bucket (Krea2 gave deep three-quarter, not profile) |

Other live results (all `needs_review`):

| Path | Requester | Result |
|---|---|---|
| Studio Production, smile + turtleneck | web | 0.753/0.661, drift (n=1; expression is a candidate cause, untested) |
| Transformation Lab, wardrobe edit | web | 0.913/0.935, same; edit only partly followed (jacket kept) |
| Night batch requested by Hermes | hermes | 0.828/0.872, recognisers disagree |

Evidence: `${XAI_WORKSPACE_ROOT}/reports/ch-example-alpha/qwen21-gate-20260928/` (`gate-manifest.json`, `gate-results.json`, `crossseed-*.json`, `gate-contact-sheet.jpg`, `studio-paths-sheet.jpg`, `score-*.json`).

Limits: one character, two seeds per cell, recognisers trained on real photographs; profile and deep three-quarter buckets have no calibrated threshold.

## Open questions for Codex

1. **Night-batch provenance.** `hermes_night_batch.py` always records `created_by: hermes` and prepares with `--actor hermes`, including batches created from the Studio UI. For this check Hermes itself created the batch (`NIGHT-20260928-175511-763302`), so the record is truthful, but web-created batches are not. Decide whether the plan should carry the real requester.
2. **Studio importer `asset.model` is null** for Qwen and for existing Krea2 assets alike (pre-existing). The engine is correct.
3. **Not built:** choosing multiple references and a seed in the Studio UI (CLI and night batch support both).
4. **Worth one-variable tests:** `KI` vs `I` for Transformation Lab collateral preservation; expression changes vs identity drift; 45-degree drift; an off-axis calibration from turnaround pairs.
5. **Operational note:** Hermes on its local 27B model took several hours for a one-item plan, and that model held 7.9 GB of VRAM afterwards. `character_manager.free_local_model_vram()` only unloads Ollama. A render started while it is resident will contend for the 8 GB card.

## Verification commands

XAI-studio (Studio venv has pytest; add Hermes site-packages for jsonschema):

```powershell
Set-Location ${PROJECT_ROOT}
$env:PYTHONPATH = "tools;tests;<hermes-site-packages>"
${STUDIO_ROOT}/backend/.venv/Scripts/python.exe -X utf8 -m pytest tests external_media_import/tests tools/test_wangp_recorder.py tools/test_local_wangp.py tools/test_requester_provenance.py tools/test_reference_variation_worker.py infra/gpu-worker/test_provision.py -q
python tools/wangp_models.py --check qwen_image_21_uncensored_q4_k_m
python tools/character_manager.py validate
```

Last results: 359 passed, 2 skipped; model check usable; validate all OK.

Studio: backend `python -m pytest` from `backend/` → 135 passed; frontend `npm test` → 553 passed; `npm run build` OK. The running Studio server was restarted through its supervisor after the backend changes.

## Preserved

- Unrelated dirty work in XAI-studio (drive-media-export scope, character sessions, staging folders) and in Private (character records, storyboard skills, new untracked skills) was not touched.
- WanGP checkout, `env_uv`, the Int8 ConvRot patch and `stash@{0}` were not touched. No model download or package change.
- No output was promoted, approved, published or written to the Studio database directly; all Qwen results are unreviewed candidates.
