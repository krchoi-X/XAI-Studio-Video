# Source-independent reference transformation authority

Active editor: Codex
Status: COMPLETE — deterministic compiler and Studio parity verified; no GPU run
Date: 2026-10-01

## Goal

Compile every selected transformation operation as an authoritative target replacement without requiring the operator to identify the source image's current pose, garment, background, or other mutable state.

## Constraints / Must Preserve

- The exact source remains bound for identity and visual context; canonical Stable DNA remains identity authority.
- Only fields named by typed operations release their source locks. All effective preserve locks remain explicit.
- Existing request schemas and persisted v1/v2 records remain readable; no generation or record migration occurs.
- Preserve the other editors' current DNA-contract and Qwen pose-gate changes in the dirty working tree.

## Must NOT Do

- Do not infer or label source wardrobe from pixels.
- Do not weaken reference hash checks, capability gates, or text-fallback prohibition.
- Do not map semantic strength to unverified renderer parameters.

## Plan

1. Add deterministic per-operation target-authority wrappers and strength wording to the worker compiler.
2. Replace source-wide pixel/composition authority with identity/context authority plus typed mutable-field release.
3. Record the Qwen profile revision and cover source-independent wardrobe/pose compilation with tests.
4. Run focused contract/worker tests and the corresponding Studio tests/build.

## Contract impact

Producer: Studio v2 typed operation requests and `reference_variation_worker.compile_edit_instruction`.
Consumers: Krea2/Qwen reference-edit prompts, Prompt Trace, Studio plan capability display, and persisted run settings.
No payload or database field changes. Existing records compile under the new wording only when newly executed. Profile version changes from `qwen21-pose-recompose-20260930-v1` to `qwen21-source-independent-recompose-20261001-v2`; old profile strings remain readable. Rollback restores the previous compiler wording and profile constant. Deterministic verification covers operation wrappers, preserve locks, and profile parity across Studio and worker.

## Progress

- Diagnosed Lia session `VARIATION-20261001-032140-e3b3be93`: the wardrobe operation was present and its lock released, but all four outputs retained the source swimsuit.
- Confirmed strength is currently prompt-only and the compiler gives the exact source broad pixel/composition authority.
- Replaced broad source authority with identity/starting-context authority and per-operation released-field target authority.
- Added deterministic strength wording and affirmative unclothed target interpretation without classifying the source garment.
- Updated the Qwen profile to `qwen21-source-independent-recompose-20261001-v2` in Studio and worker.
- Replayed the recorded Lia request through the compiler without rendering and verified all four selected fields are released while identity and body proportions remain preserved.
- Verification: XAI contract/worker 20 passed; Studio backend transformation/API 21 passed; focused frontend 76 passed; full frontend 568 passed; frontend build passed.

## Next

Review the next real output as production evidence. Numeric engine-strength mapping remains gated on a separate controlled calibration.
