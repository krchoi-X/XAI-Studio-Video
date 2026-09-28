# Qwen Image 2.1 — Codex acceptance review

- Date: 2026-09-28
- Reviewer: Codex
- Reviewed handoff: `docs/qwen-image-2.1-claude-to-codex-handoff.md` at `f0334fa`
- Contract checkpoints: XAI-studio `4ee2b78..f0334fa`; personal-prompt-studio `3d3194e..d3122c5`; XAI-Studio-Private `9608ade..1803e32`
- Decision: accept phases 1–5. Do not repeat the identity gate or reimplement the completed phases. Human review of the generated candidates remains the production gate.

## What was accepted

The logical `qwen21` engine is additive and is not a default. The scene compiler binds the selected identity image by path, SHA-256 and byte count; the local WanGP adapter rejects an unregistered model, an engine/model mismatch, a changed reference, a missing reference, too many references, or a Qwen request whose `video_prompt_type` does not contain `I`. Qwen-only options remain nested under `custom_settings`. The detached run record preserves requester, executor, concrete model settings and verified reference inputs.

Existing Krea2 behavior and old records remain readable. Studio offers Qwen without preselecting it, narrows an identity-bound request to one capable engine, and keeps Krea2 as the default for old Transformation Lab requests.

The stored live evidence was inspected rather than regenerated. The sample Qwen run contains `model_type=qwen_image_21_uncensored_q4_k_m`, `base_model_type=qwen_image_21_7B`, `video_prompt_type=I`, the selected identity path and hash, and a matching `run.json.reference_inputs` entry. Its result remains `needs_review`, as required.

## Open-question decisions

### 1. Night-batch requester provenance — fix next, correctness issue

A Studio-created batch must record the requester as `web`, while Hermes is the planner/worker or executor. `created_by: hermes` and `--actor hermes` currently collapse those roles and make the requester record inaccurate.

Make this a small backward-compatible contract patch before relying on new Studio night-batch provenance for audit. Add an optional requester field to the plan/create path, default old plans to `hermes`, have Studio explicitly send `web`, and forward that value to `character_scene.py --actor`. Keep the executor identity separate. Do not rewrite historical records.

This does not block direct Studio generation, Transformation Lab, CLI Qwen generation, or human review of the existing candidates.

### 2. Gallery `asset.model` is null — separate importer repair

Treat this as a pre-existing provenance/display gap shared by Krea2 and Qwen, not as a Qwen integration failure. Repair the importer in a separate scoped change so per-asset model is derived deterministically from the matching `jobs[].model` or the recorded effective/run settings. Preserve old records and allow an idempotent sync to backfill missing metadata; do not infer a model from an engine name.

### 3. Multi-reference and seed controls — defer UI, keep the current advanced paths

Do not enlarge the completed integration now. The CLI and night-batch plan already provide repeatable references and seed control, and Transformation Lab provides the normal face-master workflow. Add Studio controls only as a separate UX task after the current candidate review shows which controls are used often enough to deserve first-class UI. When added, the UI must show ordered roles, the total-reference limit, the resolved identity master, and the exact seed before submission.

### 4. Next controlled experiments — human review first, then one variable at a time

After the operator reviews the existing contact sheets, run experiments in this order:

1. expression-only changes at fixed prompt, seed, framing and reference;
2. 45-degree turn at the same fixed settings, because current Qwen results show drift there;
3. `I` versus `KI`, only after confirming the current WanGP meaning of `K` and changing no other setting;
4. profile/deep-three-quarter threshold calibration only after enough human-labelled off-axis pairs exist.

Do not promote the current frontal similarity scores into a universal profile threshold. The existing profile results are correctly marked uncalibrated.

### 5. Hermes 27B VRAM retention — add a render preflight, never kill an unknown process

Treat this as an operational P1. Before starting WanGP, check whether the configured Hermes local runtime still owns significant VRAM. Prefer a host-specific graceful unload/release operation. If the runtime cannot be released safely, wait or fail with a visible actionable message; do not start competing renders and do not terminate an unidentified process. The existing WanGP file lock prevents two WanGP workers but does not protect against a separate LLM runtime consuming VRAM.

This should be implemented as a separate bounded task because the correct release mechanism depends on the Hermes runtime, not on the Qwen adapter.

## Verification performed during acceptance

- XAI-studio focused deterministic suite: `56 passed` for Qwen engine, local WanGP reference validation, Hermes night batch and reference-variation worker.
- Studio focused frontend suite: `137 passed` across production engine selection, Gallery model behavior and Transformation Lab interactions.
- Studio backend rerun: `21 passed`; two unrelated lifecycle tests failed while reopening a SQLite database under the temporary test root in this Windows checkout. All Qwen identity/engine cases in that focused run passed. Claude's checkpoint records the earlier clean full backend run as `135 passed`.
- Contract-range `git diff --check`: implementation ranges were clean except one trailing Markdown line break in `docs/qwen-image-2.1-wangp-pilot.md`; it is non-functional.

No GPU generation, identity gate, model download, push, history rewrite or cleanup of unrelated working-tree changes was performed during this review.
