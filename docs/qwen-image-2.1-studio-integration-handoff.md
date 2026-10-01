# Qwen Image 2.1 Studio integration — Claude Code handoff

- Date: 2026-09-28
- Assigned implementation editor: Claude Code, by direct user decision
- Handoff author: Codex
- Status: READY FOR IMPLEMENTATION — no adapter or Studio code has been changed yet
- Primary checkout: `${PROJECT_ROOT}`
- Studio checkout: `${STUDIO_ROOT}`
- Shared authority: `${SHARED_AUTHORITY_ROOT}`

## User objective

Make the installed local Qwen Image 2.1 uncensored GGUF a first-class, explicitly selectable Studio character-image engine. Hermes, Claude and the web app must be able to bind an already selected face master and request reconstruction, profile views, wardrobe changes and other controlled variations through the same durable Character Manager, WanGP recorder, Library and Gallery contracts used by Krea2.

Qwen must not silently become the default engine, replace Krea2, change canonical Character DNA, or promote a generated profile/master without human review.

## Read before changing files

From `${PROJECT_ROOT}`, read in this order:

1. `AGENTS.md`, `TASK.md`, this handoff and `docs/qwen-image-2.1-character-pilot-TASK.md`.
2. `${SHARED_AUTHORITY_ROOT}/control/generated/claude.md` and `${SHARED_AUTHORITY_ROOT}/control/agents/production-roles.md`.
3. Resolve and read the current Character Manager source, not the project adapter:

   ```powershell
   python tools/shared_resources.py --skill character-manager
   ```

4. Read `docs/artifact-and-review-contract.md`, `docs/shared-agent-workflow.md`, `docs/verification.md`, `docs/wangp-recorder.md` and `docs/wangp-models.md`.
5. Before changing the web app, read `${STUDIO_ROOT}/AGENTS.md`, the Studio `TASK.md`, `DESIGN.md`, `docs/shared-agent-contract.md` and the private/public boundary document required by its AGENTS instructions.
6. Inspect Git status and diffs in all three repositories. The XAI Studio worktree already contains unrelated user/agent work. Do not clean, reset, move or rewrite it.

The user assigned the Qwen implementation to Claude Code. Update the applicable task record to name Claude Code as Active editor before implementation. Keep the contract checkpoint reviewable; do not push unless the user separately asks.

## Verified runtime state

The WanGP setup itself is complete and working.

| Item | Verified value |
|---|---|
| WanGP root | `${WANGP_ROOT}` |
| Updated WanGP revision | `91301f0e` (v13.14 UI) |
| Active environment | `${WANGP_ROOT}/env_uv` |
| Finetune ID / `model_type` | `qwen_image_21_uncensored_q4_k_m` |
| Display name | `Qwen Image 2.1 Uncensored Q4_K_M` |
| Architecture | `qwen_image_21_7B` |
| Transformer | `${MODEL_ROOT}/image-generation/qwen/qwen-image-2.1-UC-Q4_K_M.gguf` |
| Transformer size | 4,604,558,112 bytes |
| Transformer SHA-256 | `E79C8A009F2ECBDB6C70FD663D9AEA9EE304A0D91F347E4169A756B8AD141B41` |
| Finetune definition | `${WANGP_ROOT}/finetunes/qwen_image_21_uncensored_q4_k_m.json` |
| Qwen VAE | `${WANGP_ROOT}/ckpts/qwen_image_21/qwen_image_21_vae.safetensors` |
| Text/vision encoder | `${WANGP_ROOT}/ckpts/Qwen3-VL-8B-Instruct/Qwen3-VL-8B-Instruct_int8_convrot.safetensors` |
| Conservative settings | 832x608, 40 steps, CFG 4, batch 1, FlowMatch Euler, KV cache disabled, RGBA disabled |
| Global config fixes | `clear_file_list: 5`, `deepy_enabled: 0`, selected model set to the finetune |

Read-only model discovery already succeeds:

```powershell
python tools/wangp_models.py --check qwen_image_21_uncensored_q4_k_m
```

It reports `status: usable`, the GGUF path, 40 steps and guidance 4. Do not vendor or copy the model into the repository.

The text-to-image smoke test passed end to end: custom GGUF load, Qwen3-VL prompt encoding, 40 denoising steps, tiled VAE decoding, JPEG persistence and gallery display. The output is:

```text
${WANGP_ROOT}/outputs/images/2026-09-28-10h59m54s_seed198617917_A red ceramic teapot on a wooden table, soft windo.jpg
```

The first run's total UI time was 17m14s because it included companion downloads and initial loading. The 40 denoising steps took 1m49s. This proves the model can render; it does **not** yet prove reference-image identity preservation.

WanGP also retains a local scalar-scale compatibility change in `shared/qtypes/int8_convrot.py`. Its patch backup is `${WANGP_ROOT}-int8-convrot-local-20260928.patch`, and a related stash was recorded as `stash@{0}` at setup time. Preserve it. Do not run a destructive update/reset or blindly pop the stash.

## Current repository bases and dirty-state warning

Observed when this handoff was written:

- `${PROJECT_ROOT}`: `4ee2b7802180150de855882e0c9939de682395b8`, branch `main`.
- `${STUDIO_REPOSITORY_ROOT}`: `3d3194e9db2641aa520e2926b981edd15e9cb1b3`, branch `master`.
- `${SHARED_AUTHORITY_ROOT}`: `9608ade07096fa561ced581f73b8d68fe15f7935`.

The XAI Studio checkout contains many modified and untracked files unrelated to Qwen, including character sessions and another active drive-export scope. Preserve all of them. Restrict the implementation to the files named below plus task/docs/tests that are necessary for this contract.

## Current blocking assumptions in code

Qwen is usable in WanGP but Studio rejects it before submission:

1. `tools/character_scene.py`
   - `ENGINES` contains only `z-image` and `krea2`.
   - the identity-reference guard requires exactly `engines == ["krea2"]`.
   - `apply_identity_reference()` always rewrites to `krea2_turbo_edit` and the Krea checkpoint.
   - CLI help says identity reference requires Krea2.
2. `tools/local_wangp.py`
   - `validate_reference_settings()` accepts only `KREA2_EDIT_MODELS`.
   - its error and cardinality rules are Krea-specific even though the path/hash validation is reusable.
3. `tools/hermes_night_batch.py`
   - `ENGINES` contains only `z-image` and `krea2`.
   - a reference-bound item requires `engines == ["krea2"]`.
4. `${STUDIO_ROOT}/backend/app/schemas.py`
   - normal and night-batch engine literals contain only `z-image` and `krea2`.
5. Studio backend `app/main.py`
   - identity-reference submission explicitly requires Krea2 alone.
   - the reference-transformation/variation endpoint identifies only Krea2 Identity Edit.
6. Studio frontend `src/apps/production/model.ts`
   - `defaultEngineOptions` contains only Z-Image and Krea2.
   - enabling identity reference narrows the selection to Krea2.
7. `tools/reference_variation_worker.py`
   - settings, dependencies, output directory, trace, manifest text and progress messages are all hard-coded to Krea2.
8. The canonical Character Manager skill still describes reference-bound production and night batches as Krea2-only.

Hermes and Claude actor attribution is already implemented. `tools/character_scene.py --actor` accepts `hermes` and `claude`; do not add a second agent-specific generation path.

## Stable engine and model naming

Use a stable logical engine ID separate from the replaceable model checkpoint:

- Recommended engine ID and output directory: `qwen21`
- User-facing label: `Qwen Image 2.1`
- Current concrete `model_type`: `qwen_image_21_uncensored_q4_k_m`

Do not use the full finetune ID as the public engine name. The engine contract should survive a later Q5/BF16 or corrected checkpoint while each run continues to record the exact `model_type`, checkpoint path/hash when available and quantization.

If existing repository naming rules make a different slug materially safer, document the decision before writing persisted sessions. Do not create two aliases for the same engine.

## Implementation phases

### Phase 1 — common CLI adapter and reference contract

Implement the smallest first-class route in XAI Studio:

1. Add `qwen21` to the scene engine registry with a dedicated settings template. Do not reuse or mutate the Krea2 template.
2. Split Krea2-specific reference compilation from the common reference resolver. A reference-bound Qwen job must keep:
   - exact reference path;
   - SHA-256 and byte count captured during preparation;
   - optional approved Gallery asset ID;
   - `allow_text_fallback: false`;
   - real requested actor;
   - exact Qwen `model_type` and settings.
3. Generalize `local_wangp.validate_reference_settings()` to an explicit capability/model registry. Do not permit arbitrary models merely because they contain `image_refs`.
4. Fail before starting the worker when the reference is missing, unsupported, changed after preparation or not allowed by the selected engine.
5. Preserve the existing Krea2 settings byte-for-byte where practical and behaviorally in all cases. Ordinary Z-Image/Krea2 jobs and old sessions must remain valid.
6. Store Qwen outputs under the existing character/session Library hierarchy in `outputs/qwen21`. Do not create an agent-specific or standalone WanGP output silo.
7. Record the exact model as `qwen_image_21_uncensored_q4_k_m` in settings, run provenance and manifests. Record engine/provider/model separately.

Start from the verified finetune JSON, but create a repository-owned minimal runtime template containing only fields accepted by WanGP's API. Expected core values are:

```json
{
  "model_type": "qwen_image_21_uncensored_q4_k_m",
  "base_model_type": "qwen_image_21_uncensored_q4_k_m",
  "image_mode": 1,
  "resolution": "832x608",
  "image_refs": ["<hash-bound face master>"],
  "remove_background_images_ref": 0,
  "num_inference_steps": 40,
  "guidance_scale": 4.0,
  "batch_size": 1,
  "repeat_generation": 1,
  "qwen21_kv_cache": "Disabled",
  "rgba": "Disabled",
  "prompt_enhancer": ""
}
```

Do not assume `video_prompt_type: KI`, Krea LoRA fields or the Krea checkpoint path apply to Qwen. Confirm the exact API fields with a prepared settings inspection and one bounded live run.

### Phase 2 — controlled identity gate

Before exposing Qwen as generally production-ready, run the fixed gate from `docs/qwen-image-2.1-wangp-pilot.md` using a user-selected face master or `character-default` that already exists:

1. neutral reconstruction;
2. clothing-only edit;
3. 45-degree view;
4. 90-degree profile;
5. two fixed seeds per case.

Use `strict_translation`, identical reference bytes and the same base identity wording. Record input hash, seed, size, steps, guidance, duration, run directory and output path. Keep all eight images as candidates/derivatives. Do not modify Stable DNA or create an approved angle master automatically.

Stop after two materially similar failures. Diagnose rather than changing packages, quantization or several settings at once.

The profile gate measures stable and user-acceptable invented geometry; a frontal master cannot prove ground-truth side geometry. Human selection is required before a profile becomes an angle master.

### Phase 3 — Hermes night batch

After the common route passes:

1. Add `qwen21` to night-batch validation and verification.
2. Permit a reference-bound item only when it selects one reference-capable engine on its own (`krea2` or `qwen21`), unless a later explicit contract defines independent per-engine references.
3. Preserve the existing 48-item/240-image limits, sequential GPU execution, durable attempts, GPU lock and post-run sync.
4. Verify model type, reference basis and artifacts under `outputs/qwen21` before marking an item complete.

Do not run Krea2 and Qwen concurrently on the 8 GB GPU.

### Phase 4 — Studio Production UI

In the private Studio:

1. Expand backend request schemas and validation to accept `qwen21` without breaking old request JSON.
2. Add `Qwen Image 2.1` to the existing engine selector. Do not add a new navigation destination or a separate Qwen page.
3. Replace the Krea-only identity-reference reducer rule with a capability-aware single-engine rule.
4. Keep `use_identity_reference` backward compatible. If a new field is necessary, make the reader accept old records and document the migration/rollback in the Studio task.
5. Continue to submit through `web_generation_worker.py` → `character_scene.py`; do not bypass the common CLI.
6. Sync results through the existing `/api/sync` and verify Library/Review. Gallery derives engine filters from imported assets and should learn `qwen21` from the data; do not hard-code a parallel gallery.
7. Keep infrastructure/model detail under advanced information, consistent with `DESIGN.md`.

### Phase 5 — Transformation Lab parity

This is needed for full Krea2-equivalent Studio behavior but can be a separate checkpoint after Phase 4:

1. Generalize `reference_variation_worker.py` into engine-specific settings/dependency adapters.
2. Let the plan/capability response identify Krea2 or Qwen rather than claiming Krea2 unconditionally.
3. Preserve the existing reference-transformation v1/v2 normalization and old Krea2 records.
4. Record the selected engine/model in request, trace, batch and run records.
5. Keep pose/hand/large recomposition blocked unless the Qwen identity gate actually verifies those capabilities. Do not relabel an unverified route as supported.

## Expected file scope

Primary implementation and tests are expected in:

```text
${PROJECT_ROOT}/tools/character_scene.py
${PROJECT_ROOT}/tools/local_wangp.py
${PROJECT_ROOT}/tools/hermes_night_batch.py
${PROJECT_ROOT}/tools/reference_variation_worker.py        # Phase 5
${PROJECT_ROOT}/tests/test_character_scene.py
${PROJECT_ROOT}/tools/test_local_wangp.py
${PROJECT_ROOT}/tests/test_hermes_night_batch.py
${PROJECT_ROOT}/tools/test_reference_variation_worker.py   # Phase 5
${PROJECT_ROOT}/examples/character-lab/...                 # one Qwen settings template
${STUDIO_ROOT}/backend/app/schemas.py
${STUDIO_ROOT}/backend/app/main.py
${STUDIO_ROOT}/backend/tests/test_api.py
${STUDIO_ROOT}/frontend/src/apps/production/model.ts
${STUDIO_ROOT}/frontend/src/apps/production/model.test.tsx
${SHARED_AUTHORITY_ROOT}/shared-skills/character-manager/SKILL.md
```

`web_generation_worker.py`, shared TypeScript request types and UI interaction tests may also require bounded changes after inspecting the actual contract. If the scope expands materially beyond these files, pause and update the task before continuing.

## Contract impact to record before implementation

The task document must name these boundaries:

- Producers: Character Manager scene compiler, Studio Production API, Hermes night-batch plan, Transformation Lab when Phase 5 begins.
- Consumers: local WanGP submit/worker, recorder, creation-record snapshot, Library importer/sync, Gallery/Review, Control Tower job projection and old session readers.
- New persisted value: logical engine `qwen21` and output directory `outputs/qwen21`.
- Concrete model: `qwen_image_21_uncensored_q4_k_m`.
- Compatibility: old `z-image`, `krea2`, Krea2-only transformation records and sessions continue to load without migration.
- Rollback: remove Qwen from new engine/capability registries and UI choices; retain existing Qwen session/output/run records as readable historical evidence.
- Publication: unchanged; all new results remain restricted and `needs_review` until human action.

## Deterministic tests required

Add tests that prove:

1. `qwen21` prepares the exact model type and conservative settings.
2. reference path/hash/byte count and optional asset ID survive preparation and submission.
3. a missing or modified reference fails before the GPU worker starts.
4. Qwen reference jobs never fall back to text-only generation.
5. `--actor hermes` and `--actor claude` are recorded truthfully.
6. ordinary Z-Image and Krea2 settings and reference behavior remain unchanged.
7. old sessions without Qwen fields remain readable.
8. night-batch budget/count/GPU-lock rules remain unchanged.
9. Studio API accepts Qwen, rejects invalid mixed reference selections and still accepts old Krea2 payloads.
10. frontend selection/count/reducer behavior is covered for Z-Image, Krea2 and Qwen.
11. Gallery import/sync derives the Qwen engine from `outputs/qwen21` without damaging review/favorite state.

Use deterministic tests before any live generation. Do not call an LLM to review assertions that tests can settle.

Suggested focused commands, adjusted to the actual environment:

```powershell
Set-Location ${PROJECT_ROOT}
python -m pytest tests/test_character_scene.py tools/test_local_wangp.py tests/test_hermes_night_batch.py tools/test_reference_variation_worker.py -q
python tools/wangp_models.py --check qwen_image_21_uncensored_q4_k_m
python tools/character_manager.py validate
git diff --check
```

For Studio, first verify module resolution from its backend directory as required by its AGENTS file, then run the affected backend tests. From `frontend/`, run at least:

```powershell
npm test
npm run build
```

Run lint only if the repository has a working ESLint configuration; the existing task history records that this was previously absent.

## Live acceptance checks

Implementation is not complete merely because the model appears in a dropdown.

1. `character_scene.py prepare` produces a Qwen settings file with the exact face-master path/hash and no Krea fields.
2. One reference-bound local generation completes through `local_wangp.py`, not through manual WanGP UI clicks.
3. `run.json`, effective settings, `batch.yaml`, prompt trace and artifacts all identify requester, executor, engine, exact model and reference.
4. Output exists under the returned Library session's `outputs/qwen21`.
5. Studio sync discovers the session; the image appears in the existing Library/Review surface with `needs_review` and the Qwen engine label.
6. A Hermes request records `hermes`; a Claude-run request records `claude`. Neither path impersonates `web`.
7. Existing Krea2 reference generation still completes or at minimum its deterministic fixtures and settings comparison pass if another paid/long live render is not justified.
8. The fixed identity gate is reviewed by the user before Qwen is described as identity-stable or promoted to a default.

## Must preserve / must not do

- Preserve the selected face master bytes and canonical Stable DNA.
- Treat wardrobe, pose, expression, camera, lighting and profile candidates as Scene Delta or derived assets.
- Keep identity masters distinct from continuity frames and contact sheets.
- Preserve all Krea2 evidence and old sessions.
- Do not infer the newest file as a face master; use `reference_defaults.identity` or an explicit path.
- Do not silently switch engines when Qwen is missing or fails.
- Do not auto-promote generated outputs, mark them approved, publish them or write directly to the Studio database.
- Do not add a Qwen-specific Gallery or per-agent output hierarchy.
- Do not download another quantization, update WanGP, change packages or edit the local Int8 patch unless a concrete failure requires a separately recorded decision.
- Do not push repositories or delete generated/user files without separate user direction.

## Completion report expected from Claude

Claude should leave durable state, not only a chat response:

- task status and Active editor;
- exact changed files in each repository;
- contract and compatibility decision;
- deterministic test commands and counts;
- live session/run IDs, reference hash, exact model, output paths and sync/review state;
- identity-gate results separated into observation, inference and human decision;
- remaining blocked/unverified phases;
- rollback instructions.

## Short prompt the user can give Claude Code

```text
Continue the Qwen Image 2.1 Studio integration assigned to Claude Code. Start in ${PROJECT_ROOT} and read AGENTS.md, TASK.md, docs/qwen-image-2.1-studio-integration-handoff.md and the catalog-resolved Character Manager skill. Inspect the actual dirty worktrees before editing and preserve unrelated changes. Implement the handoff in phases, beginning with the common Character Manager/local WanGP Qwen reference adapter and deterministic tests. Use the existing finetune qwen_image_21_uncensored_q4_k_m; do not download or update models. Keep Krea2/Z-Image backward compatible, use the existing Library/Gallery/recorder contracts, and do not promote any generated identity asset without my review.
```
