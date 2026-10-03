# Lee Suan reference-derived storyboards (Draft 0)

- Date: 2026-10-04
- Active editor: Claude Code (claude-opus-5-5), real actor `claude`
- Status: RENDERED — four finals + reel in needs_review (2026-10-04 04:55 KST); human review pending
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

## Results (2026-10-04 04:55 KST)

Finals (1280x720, 24 fps, 48 kHz, loudnorm -18 LUFS, ~1 s title card, burned Korean subtitles):
- B 「잡혔다」 22.9 s — `VIDEO-20261004-002600-suan-b-rooftop-radio/outputs/B-rooftop-radio-final.mp4`
- A 「비 오는 저녁」 19.9 s — `VIDEO-20261004-002601-suan-a-rain-evening/outputs/A-rain-evening-final.mp4`
- C 「처음 끓여본 된장찌개」 22.9 s — `VIDEO-20261004-002602-suan-c-first-jjigae/outputs/C-first-jjigae-final.mp4`
- D 「말없이, 빛만」 8.4 s — `VIDEO-20261004-002603-suan-d-silent-light/outputs/D-silent-light-final.mp4`
- Reel B→A→C→D 74.0 s — `BATCH-20261004-suan-reference-set/suan-reference-set-reel.mp4`

Per-clip Intent Fidelity review and failure attribution: `BATCH-20261004-suan-reference-set/review.md`. Summary:
B pass (warnings: wide framing, mid-turn updo). A re-staged to rev 4 after A1 order swap and A3 back-to-camera;
A3 retake drifted 0.5-2.5 s, so the editor uses A3 3.0 s→end behind a cut (needs_human_review). C3 rev 4 retake fixed
lens-addressed line. D rev 4 retake fixed the missing tears and visible card text. Attempt-1 clips kept in
`outputs/attempt1/`. Rejected portrait B1 kept. 14 renders total, 1 lost (C2, worker killed at the 2 h background-task
limit; recorded failed).

Findings filed via `shared_skill_feedback.py` (adaptive-video-production): Ref2VA output aspect follows the first
reference (repeated); third chained FL2VA clip with a follow move drifted (candidate).
Unverified: Korean speech content (no Whisper weights; not downloaded), audio heard by a human, Gallery sync/import
(not run).

## Next

1. User picks pieces and revises beats (Draft 1).
2. On approval: freeze storyboard revision, write contract JSON per clip (to the schema current at that time —
   Codex's WIP adds `locked.prompt_segments` and `creative_envelope.allowed_values`), compute hashes, acknowledge.
3. Optional rough boards / one sample clip per piece through the gated WanGP path (`--methodology intent-preserving-v1`).
