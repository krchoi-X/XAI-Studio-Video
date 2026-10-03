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

## Production (2026-10-04 00:2x KST, user asleep)

User instruction (verbatim in each `session-provenance.json`): make all four in order (B, A, C, D), 16:9, smooth and
natural, dialogue as H3 audio plus subtitles, ~1 s title at start. Treated as approval of Storyboard Revision 2.

- Batch folder: `D:/AI_Studio/library/characters/ch-lee-suan/generations/BATCH-20261004-suan-reference-set/`
  (`spec.py` = Revision 2 source, `gen.py` builds sessions/contracts/checks, `run_piece.py clips <KEY>` renders,
  `finish.py <KEY>` assembles, `batch.log`).
- Sessions: `VIDEO-20261004-00260{0..3}-suan-{b,a,c,d}-*` beside it, each registered with
  `--methodology intent-preserving-v1`; every clip has contract, acknowledgement, compiler IR and passing check.
- Revision 2 change (Claude, under "smooth and natural"): clips after the first are H3 FL2VA from the previous final
  frame (seamless, verified 2026-09-14), so the operator turns to follow instead of cutting; C3 is Ref2VA after the
  line cut with C2's final frame as Picture 2; C2 pot-POV dropped.
- Gate tools: Codex is mid-edit on `tools/video_intent_contract.py`/schemas (v1.1/v2, uncommitted). Runs use a
  snapshot of committed HEAD `2ebbb7e` tools+schemas (`git archive`) in the Claude scratchpad, checker
  `video-intent-contract-v1`. Codex's working tree untouched.
- Known risks: `<d>[Korean]` speech untested on H3; tears/light sequence (D) untested.

## Next

1. User picks pieces and revises beats (Draft 1).
2. On approval: freeze storyboard revision, write contract JSON per clip (to the schema current at that time —
   Codex's WIP adds `locked.prompt_segments` and `creative_envelope.allowed_values`), compute hashes, acknowledge.
3. Optional rough boards / one sample clip per piece through the gated WanGP path (`--methodology intent-preserving-v1`).
