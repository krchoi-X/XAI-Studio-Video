# Qwen Image 2.1 character-identity pilot

Active editor: Codex (pilot record and handoff author)
Assigned next editor: Claude Code, by direct user decision
Status: HANDOFF READY — text-to-image smoke passed; reference adapter and identity A/B pending
Date: 2026-09-28

## Goal

Evaluate whether a local Qwen Image 2.1 uncensored GGUF can reduce the identity drift seen when an approved face master is reused for character-sheet views and controlled edits. Make this the next experiment before expanding the video workflow.

## Constraints / Must Preserve

- The user supplied the uncensored GGUF and later explicitly authorized WanGP configuration, required companion downloads, and a local smoke generation. Do not use hosted generation credits.
- Preserve the current `D:/AI/WanGP` models, settings, profiles, sessions, outputs, environment selection, and local Int8 ConvRot patch. Update that checkout's tracked application code and its active `env_uv` through the normal updater after stashing the tracked patch. A separate dependency environment is optional, not required.
- Keep the approved face master immutable. Generated angles and sheets are candidates or derivatives until the user reviews them.
- Keep the identity master separate from continuity frames and human-facing contact sheets. Feed individual source images to the model.
- Preserve the current Krea2 evidence and use it as the comparison baseline rather than overwriting it.

## Must NOT Do

- Do not treat “uncensored” as evidence of better identity fidelity.
- Do not promote a newly generated profile or sheet to canonical DNA automatically.
- Do not add Qwen to the production Character Manager route before the local smoke test passes.
- Do not delete or relocate existing WanGP runtime data. Do not run its update script while the tracked local patch is unstashed, because this version's failed-pull recovery performs a hard reset.

## Plan

1. The operator preserves the local WanGP source patch, updates the existing checkout and active environment through WanGP's updater, and downloads the Q4_K_M uncensored transformer.
2. Register that checkpoint as a finetune derived from WanGP's built-in `qwen_image_21_7B` model.
3. Run a minimal load and one low-risk image-edit smoke test.
4. Run the fixed identity gate: reconstruction, clothing-only edit, 45-degree view, and 90-degree profile, with two fixed seeds each.
5. Compare against the existing Krea2 Turbo/RAW results and record identity, edit isolation, geometry, speed, VRAM/RAM, and failures.
6. Only after a pass, add a Qwen image engine adapter to `tools/character_scene.py` and the shared Character Manager contract.

## Progress

- Synchronized the local knowledge repository with `origin/main`; its September backlog identifies this model as the intended local A/B candidate.
- Confirmed the current machine has an RTX 4070 Laptop GPU with 8 GB VRAM.
- Updated the existing `D:/AI/WanGP` checkout from `01a67f0a` to upstream `91301f0e` with the official updater. The active `env_uv` requirements completed successfully; existing models, settings, profiles, outputs, and configuration remain in place.
- Preserved the local Int8 ConvRot scalar-scale fix as `D:/AI/WanGP-int8-convrot-local-20260928.patch` and `stash@{0}`, then reapplied it cleanly to the updated source.
- Verified the new Qwen 2.1 default definition and handler are present and syntax-parse successfully. The existing WanGP catalog still reports the default Qwen model as missing weights until the external uncensored GGUF is registered as a finetune.
- Verified `D:/AI/Models/image-generation/qwen/qwen-image-2.1-UC-Q4_K_M.gguf`: 4,604,558,112 bytes, SHA-256 `E79C8A009F2ECBDB6C70FD663D9AEA9EE304A0D91F347E4169A756B8AD141B41`.
- Inspected current upstream WanGP source without downloading weights. Qwen Image 2.1 support exists, its handler accepts GGUF checkpoints, and custom checkpoints can be registered through the Finetune Creator.
- Confirmed the selected community checkpoint is `qwen-image-2.1-UC-Q4_K_M.gguf` (4.60 GB). It still requires Qwen3-VL encoder/vision and VAE support files.
- Added the operator runbook and fixed experiment matrix in [Qwen Image 2.1 WanGP pilot](qwen-image-2.1-wangp-pilot.md).
- Registered the supplied GGUF in WanGP as finetune ID `qwen_image_21_uncensored_q4_k_m`, display name `Qwen Image 2.1 Uncensored Q4_K_M`, derived from `qwen_image_21_7B`. The unrelated built-in Int8 transformer download was aborted before using it.
- Downloaded the required Qwen 2.1 VAE and Qwen3-VL 8B Int8 ConvRot encoder/vision support files through WanGP. The supplied GGUF remains the image transformer.
- Migrated the updated WanGP configuration by persisting `clear_file_list: 5` and disabling the incompatible legacy Deepy/Florence setup (`deepy_enabled: 0`). This removed the gallery refresh failure after restart while preserving the existing output path and model selection.
- Saved a conservative per-model default: 832x608 (4:3), one image, 40 steps, CFG 4, FlowMatch Euler, KV cache disabled, RGBA disabled, no control/reference image, and no LoRA. Prompt enhancement remains manual-only and was not invoked for the test.
- Completed an end-to-end local smoke generation using the exact prompt `A red ceramic teapot on a wooden table, soft window light, detailed product photograph.` The 40 denoising steps completed in 1m49s, VAE decoding completed, and the output was saved at `D:/AI/WanGP/outputs/images/2026-09-28-10h59m54s_seed198617917_A red ceramic teapot on a wooden table, soft windo.jpg`.
- Restarted WanGP after configuration migration and verified the custom finetune is selected, the service reports `Ready`, and the generated image appears as the single item in the default gallery.
- The user assigned subsequent Studio integration to Claude Code. Added the self-contained [Claude Code integration handoff](qwen-image-2.1-studio-integration-handoff.md) with runtime state, contract impact, file scope, phases, tests, live acceptance checks and a copyable startup prompt. No production adapter or Studio code was changed in this handoff step.

## Contract impact

No runtime contract changes are authorized in this preparation task. A later adapter would affect Character Manager engine selection, WanGP model discovery, generation manifests, and Gallery provenance. That implementation must retain backward compatibility for `z-image` and `krea2`, identify the exact Qwen checkpoint/quantization in each run, and add deterministic tests before it can become a production route.

## Next

Claude Code takes the implementation lease after inspecting repository state and updating the applicable task record. Follow the [integration handoff](qwen-image-2.1-studio-integration-handoff.md): implement and deterministically test the common Qwen reference adapter first, then run the controlled identity gate, then add night-batch and Studio UI support. Keep every result as a candidate and compare it with the existing Krea2 baseline before any canonical promotion. Stop after two materially similar failures and diagnose instead of repeating downloads or installs.

## Verification

- End-to-end local verification passed: custom GGUF load, Qwen3-VL prompt encoding, 40-step denoising, tiled VAE decoding, JPEG persistence, and gallery display after restart.
- Verify documentation formatting with `git diff --check`.
