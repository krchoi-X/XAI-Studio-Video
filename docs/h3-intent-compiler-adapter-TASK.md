# H3 engine-specific Intent Contract compiler adapter

- Date: 2026-10-04
- Active editor: Codex / GPT-6 Astra
- Status: COMPLETE — deterministic adapter correction implemented; controlled render comparison remains pending

## Goal

Correct methodology v1.1 so its deterministic prompt compiler preserves the native MiniMax H3 prompt grammar instead of submitting the generic contract/debug representation. Support the verified Ref2VA six-section form and FL2VA three-section form, including sound and music, while keeping management metadata out of renderer prompt text.

## Constraints / Must Preserve

- Keep Intent Contract schema v1 readable and existing v2 generic fixtures compatible.
- Preserve exact template equality, source hashes, locked meaning, approved values, submission gating, and the user approval boundary.
- Preserve the generic template for non-H3 adapters; do not claim one universal renderer syntax.
- H3 Ref2VA uses `subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music` in that order.
- H3 FL2VA uses `integrated_multimodal_description / overall_soundscape / non_diegetic_music` in that order.
- Do not touch unrelated untracked character, output, reference-review, or storyboard files.

## Must NOT Do

- No GPU job, render, service restart, Gallery/database write, character mutation, public push, or quality claim from unit tests alone.
- Do not put `target_model`, template IDs, creative-choice bookkeeping, hashes, or other management metadata in H3 runtime prompt prose.
- Do not promote a same-seed quality comparison as completed; it still requires a separately approved production run.

## Plan

1. Add closed H3 Ref2VA and FL2VA prompt profiles to the approved locked packet.
2. Make compiler-template selection engine-specific and reject generic-template use for exact H3 model types.
3. Deterministically serialize only native H3 sections and verify that ordered event lines occur once and in order in the H3 narrative section.
4. Add regression fixtures for Ref2VA structure/audio, FL2VA structure/audio, metadata exclusion, mismatch rejection, and legacy compatibility.
5. Update methodology, contract, recorder guidance, shared skill, and private remote authority; leave empirical A/B rendering pending.

## Contract impact

Producer: Hermes Production Director authors an engine-specific H3 prompt profile inside the same locked Intent Contract before user approval. Consumers: deterministic compiler, semantic checker, local WanGP submission gate, Hermes Runtime, and independent review. Existing v1 and v2 contracts remain readable; old generic v2 prompts remain valid for non-exact/legacy adapter targets but are rejected for `minimax_h3_ref2va*` and `minimax_h3_fl2va*`. Rollback removes the optional profiles and H3 serializers while retaining the prior generic compiler. Deterministic verification covers both native formats, audio fields, metadata exclusion, template/target compatibility, hash binding, and existing submission tests.

## Progress

- Reproduced Claude's finding in `tools/video_intent_contract.py`: `intent-prompt-v1` emits generic labels and management metadata and has no audio/music or FL2VA-specific structure.
- Confirmed installed WanGP defaults and existing repository guidance use the six-section Ref2VA and three-section FL2VA formats; Claude's format diagnosis is correct.
- Added closed H3 Ref2VA and FL2VA engine profiles to Intent Contract/IR v2 without invalidating existing v1 or generic v2 readers.
- Added deterministic native serializers, approved creative-value slots, exact target/template compatibility checks, event occurrence/order checks, and exclusion of management metadata from H3 prompt prose.
- Updated canonical methodology, contract examples, Creative Treatment handoff, private remote authority, and both affected shared skills.
- Verification: 75 focused tests passed and 1 skipped; the only warning is an upstream FastAPI test-client deprecation. Python compilation, JSON parsing, diff checks, and both shared-skill validations passed.

## Next

Use a user-approved pilot or same-seed comparison to evaluate the corrected native adapter against a manually authored native H3 prompt. Record video/audio quality and failure attribution before claiming empirical superiority or making the treatment-backed flow universal.
