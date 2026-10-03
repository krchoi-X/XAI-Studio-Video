# Scoped task — Still-image DNA and master-reference contract

Active editor: Codex
Status: COMPLETE — deterministic checks passed; no generation performed
Date: 2026-09-30

## Goal

Extend the Grok/Hermes production guidance and Studio reference-transformation path so character stills do not
silently omit canonical DNA or the explicitly selected master. Support long reusable wardrobe/pose prompts without
letting them replace identity authority.

## Scope

- Image-production additions to the Grok/Hermes playbook and wardrobe still guidance.
- Studio Reference Transformation Lab request/trace contract and text limits.
- XAI `reference_variation_worker.py` consumption of the additive character contract.
- Focused deterministic tests and structured shared-skill feedback.

## Constraints / Must Preserve

- Canonical records are read from the configured Private shared authority and remain unchanged.
- The exact selected source asset remains hash-bound; explicit master/reference selection is never replaced by a
  newest-file guess.
- Existing v1/v2 transformation requests remain readable; missing additive fields retain legacy behavior.
- No GPU generation, service restart, media mutation, database migration, approval, publication or push.
- A collected wardrobe/pose prompt is scene intent, not Stable DNA.

## Must NOT Do

- Do not claim a source image or textual DNA alone guarantees identity.
- Do not auto-promote any result to face master, Stable DNA or Visual Canon.
- Do not bypass the current block on unverified pose/hand/recomposition strategies.

## Contract impact

Producer: Studio transformation API records a `character_contract` containing canonical path, version, Stable-DNA
SHA-256 and rendered Stable-DNA prompt. Consumer: the XAI reference-variation worker compiles it into the final
edit instruction and Prompt Trace. The field is additive and optional for old records. Rollback removes the new
consumer/compiler field; existing records and source-reference binding remain valid. Deterministic tests cover
snapshot creation, prompt inclusion, text limits and old-record compatibility.

## Plan

1. Add canonical DNA/master rules to the still-image production guide.
2. Freeze canonical DNA into new reference-transformation requests and surface it in plan preview/trace.
3. Raise matching Studio/API text limits for long wardrobe and pose prompt modules.
4. Verify without generation and submit shared-skill feedback rather than editing the canonical skill without scope.

## Progress

- Confirmed current transformation jobs bind the selected asset and its hash but compile only an abstract `identity`
  lock; no Stable DNA description reaches the renderer.
- Confirmed the frontend truncates far below the backend limits (400/200 versus 2,000/1,000 characters).
- Added still-image guidance that requires literal Stable DNA for every character still and requires both DNA and
  the exact hash-bound source for “transform this image.” Wardrobe/pose/camera prose is explicitly a Scene Delta.
- Added the optional v2 `character_contract` schema and worker validation/Prompt Trace propagation. Current canonical
  path, ID, version and Stable-DNA hash are rechecked before GPU work; old requests remain readable.
- Studio now freezes the full character contract, exposes DNA evidence in plan preview, and accepts 10,000-character
  request and typed-operation text.
- Verification: 17 XAI schema/worker tests passed; Studio backend contract/API 7 passed; Studio transformation UI
  65 passed; frontend build passed. No GPU job, service restart, migration, publication or push was performed.
- Submitted structured Character Manager feedback `skillfb-20260930T091850Z-1e3fa67e`; did not edit the canonical
  shared skill directly.

## Next

Optional follow-up: define a canonical source/taxonomy for the user's collected prompt modules before building a
searchable prompt shelf. Keep pose/hand/large recomposition blocked until a calibrated reference engine exists.
