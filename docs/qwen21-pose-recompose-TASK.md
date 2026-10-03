# Qwen Image 2.1 pose recomposition — 2026-09-30

- Status: COMPLETE — bounded worker gate and deterministic verification passed
- Active editor: Codex
- Studio consumer: `D:/codex/personal-prompt-studio/personal-prompt-studio`

## Goal

Permit the existing hash-bound Qwen Image 2.1 reference worker to execute a bounded `pose`-only
`recompose_with_reference` plan, including editable runtime anatomy safeguards supplied through the existing pose
instruction. Preserve all unsupported recomposition gates.

## Evidence

- Controlled Reika run `run-20260930-214120-5f059ec9` used the exact face master, frozen Stable DNA, Qwen reference mode,
  one fixed seed, and produced the requested kneeling/table/wardrobe/scene composition.
- The sample also produced an implausible long cylindrical neck/shoulder connection. This supports limited execution plus
  mandatory review and pose-conditioned safeguards, not a general quality claim.

## Constraints / Must Preserve

- Qwen only; Krea2 recomposition stays blocked.
- Permit only plans whose recomposition kind is `pose`. Block `hand_gesture`, `camera`, `framing`, and `staged`.
- Exact reference path/hash/byte count, frozen Stable DNA, no text fallback, restricted visibility, truthful actor/model,
  Prompt Trace, and `needs_review` remain mandatory.
- No automatic retry, keep/favorite decision, DNA edit, master replacement, or promotion.

## Contract impact

- Producer: Studio plan/create records existing `engine_id=qwen21`, `resolved_strategy=recompose_with_reference`, and the
  existing typed operations.
- Consumer: `tools/reference_variation_worker.py` uses the same predicate before reference/GPU access.
- Persistence: no new required field. `effective_strength` uses profile `qwen21-pose-recompose-20260930-v1` and mode
  `prompt_only_limited_validation`; old records remain readable.
- Rollback: remove the Qwen pose predicate and restore the previous non-identity-edit block. Existing results remain review
  history and require no migration.

## Plan

1. Add one shared-in-behavior capability predicate to Studio preview/create and the worker.
2. Record the resolved strategy/profile in Prompt Trace and renderer metadata.
3. Test allowed Qwen pose and blocked Krea2/hand/camera/staged cases without rendering.

## Progress

- Architecture boundary and limited validation basis recorded before implementation.
- Added `supports_plan` and a truthful effective-strength profile. Qwen `recompose_with_reference` passes only when a
  typed `pose` operation is present and `hand_gesture`, `camera`, and `framing` are absent. Krea2 and `staged` remain blocked.
- Prompt Trace records the real resolved strategy; Qwen settings continue to carry exact source hash/bytes, Stable DNA,
  `video_prompt_type: I`, and `allow_text_fallback: false`.
- Verification with Studio pytest plus Hermes `jsonschema` path: worker and transformation contract 19 passed.
- Studio live preview verified Reika exact master binding and profile `qwen21-pose-recompose-20260930-v1`; no new render.

## Next

- Review the next human-triggered Qwen pose candidate. Expand the rule set only from a concrete failure and keep each
  added anatomy correction bounded to explicit pose evidence.
