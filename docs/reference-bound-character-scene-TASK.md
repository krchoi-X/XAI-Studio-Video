# Reference-bound character still generation

Active editor / integration owner: Codex / GPT-6 Astra
Status: COMPLETE — common hash-bound Krea2 Identity Edit route verified
Date: 2026-09-16

## Goal

Make an explicitly requested character identity reference reach local Krea2 still generation for Codex, Hermes, Grok, Claude, web and user actors through the shared `character_scene.py` route. A reference-bound request must use Krea2 Identity Edit, preserve the exact reference path and hash, and fail before GPU work rather than silently falling back to text-only generation.

## Scope

- `tools/character_scene.py`
- `tools/local_wangp.py`
- `tests/test_character_scene.py`
- focused local documentation for Character Manager
- shared Character Manager skill and its scoped task record
- Reika's existing user-selected default identity-reference record in the Private authority

## Constraints / Must Preserve

- Preserve existing text-only Z-Image/Krea2 behavior when no identity reference is requested.
- Preserve Stable DNA, scene precedence, actor attribution, immutable session/output history, Gallery review state and existing reference-transformation jobs.
- Do not infer the newest image or mark an image approved. A character default must be explicitly recorded; an explicit path overrides it for that run.
- Record the actual reference path, SHA-256, byte count, role and optional asset ID in the prepared session and final run.

## Must NOT Do

- No GPU render, service restart, database write, publication, push, media deletion or rewrite of existing sessions.
- No silent text-to-image fallback when an identity reference was requested.
- No automatic reference selection from filenames, timestamps or directory scans.
- Do not absorb unrelated dirty-tree work.

## Contract impact

Producer: `tools/character_scene.py prepare|produce` gains an optional `--identity-reference` (`character-default` or an explicit local image path) and optional `--reference-asset-id`. Consumer: every supported production actor uses the same CLI through the catalog-resolved Character Manager skill. Reference-bound jobs accept only Krea2, switch that job to `krea2_turbo_edit`, write hash-bound `image_refs` and `_xai` provenance, and keep existing session fields while adding reference metadata. `tools/local_wangp.py` verifies an optional prepared reference hash before submission. Old commands, sessions and reference-variation requests remain valid. Rollback removes the new optional arguments/metadata and Reika default without touching generated assets.

## Plan

1. Add deterministic identity-reference resolution and settings compilation to `character_scene.py`.
2. Persist reference evidence in prompt trace, scene record, batch job and WanGP run; reject missing, unsupported, changed or incompatible references before GPU work.
3. Add Reika's explicitly user-selected face-09 image as `reference_defaults.identity` without changing human approval state.
4. Update the shared Character Manager instructions so Codex, Hermes, Grok, Claude and web use the same command and never silently fall back.
5. Add focused regression tests and run the repository's deterministic verification only.

## Progress

- Confirmed the failed Reika nude run included full Stable DNA but used `krea2_turbo_moody_krea` with no `image_refs` or `reference_inputs`.
- Confirmed ordinary `character_scene.py` had no reference argument, while the separate Krea2 transformation worker uses `krea2_turbo_edit` and hash-recorded `image_refs`.
- Confirmed Reika's canonical record had no default or approved reference even though the user had selected face-09 as the likeness to use.
- Added `--identity-reference` and optional `--reference-asset-id` to the shared scene CLI for every supported actor. A bound reference requires Krea2 only and compiles to `krea2_turbo_edit`; ordinary no-reference behavior is unchanged.
- Persisted role, basis, path, SHA-256, byte count, optional asset ID and actor in the scene record, prompt trace, batch job/settings and final WanGP run. The runner rejects a missing, unsupported or changed reference before worker execution.
- Extended Hermes night-batch plan normalization and preparation so its items forward the same common reference contract. Grok, Claude, Codex, web and user use the same CLI with their real actor value.
- Recorded the operator-selected Reika face-09 editorial image as `reference_defaults.identity` in the shared Private authority and refreshed the character index without changing Stable DNA or `approved_references`.
- Updated the shared Character Manager instructions, including reference-bound night-batch fields and the hard no-fallback rule.

## Next

Use `--engines krea2 --identity-reference character-default` for the next explicitly reference-bound Reika still. Review that first real output before generalizing Krea2 identity performance. No production render was part of this implementation task.

## Verification

- Studio venv: 71 passed across Character Scene, Hermes night batch, local WanGP, reference variation/transformation, creation records and shared-authority tests.
- Python compilation passed for changed runtime and test modules.
- Character Manager validation: `ch-mizuki-reika` v1 passed; Stable DNA hash remained `11ce5b950157...`.
- Shared resolver returns the current Character Manager skill.
- Read-only real-default check resolved `face-09-editorial-1.png`, SHA-256 `ba3411fb8db4ac28aa5ce2807a1ac56e32fb9e47da4c357d4ac13734010a33b7`, 1,990,236 bytes.
- Read-only Grok compilation check produced `krea2_turbo_edit`, the exact image path/hash and `allow_text_fallback: false`.
- Scoped `git diff --check` passed. No GPU render, service restart, database write, publication, push or media deletion occurred.
