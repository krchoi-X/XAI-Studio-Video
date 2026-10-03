# Lee Suan reference-derived storyboards (Draft 0)

- Date: 2026-10-04
- Active editor: Claude Code (claude-opus-5-5), real actor `claude`
- Status: ACTIVE — Draft 0 delivered for user review; no approval yet
- Deliverable: [storyboard-draft-lee-suan-reference-set.md](storyboard-draft-lee-suan-reference-set.md)

## Goal

The user asked (2026-10-04) to restart video production: re-read the changed methodology, select 3–4 good references
from the earlier reference research, and draft storyboards (콘티) with their character 이수안 (`ch-lee-suan`).

## Scope

Storyboard Spec Draft 0 plus draft Intent Contracts per clip, following
`docs/intent-preserving-video-methodology.md`, `docs/video-intent-contract.md` and the shared
`storyboard-director` / `video-intent-contract` skills. References come from `docs/reference-state-analyses.md`.

## Constraints / Must Preserve

- Stable DNA of `ch-lee-suan` unchanged (updo + black-and-white ribbon are recognition anchors); wardrobe, wetness,
  makeup and pose are Scene Deltas only.
- Identity reference: `reference_defaults.identity` (`BATCH-004 … gpt-image-09.png`), unchanged.
- Contracts stay `draft`; storyboard/contract hashes are bound only at user approval.
- Codex's uncommitted `tools/video_intent_contract.py` change (prompt template, `allowed_values`) is not touched.

## Must NOT Do

No render, GPU job, rough-board generation, DNA/approval change, Gallery write, push, or edit of other scopes.

## Next

1. User picks pieces and revises beats (Draft 1).
2. On approval: freeze storyboard revision, write contract JSON per clip (to the schema current at that time —
   Codex's WIP adds `locked.prompt_segments` and `creative_envelope.allowed_values`), compute hashes, acknowledge.
3. Optional rough boards / one sample clip per piece through the gated WanGP path (`--methodology intent-preserving-v1`).
