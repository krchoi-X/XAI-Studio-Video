# Hermes as Production Director again — Lia 라면 with time ellipsis (2026-10-07)

Active editor: Claude (actor `claude`, model claude-opus-5-5). Scope: one experimental production; no methodology,
schema, shared-skill or Codex-owned tool edits.

## Goal

User (2026-10-07): the methodology says frontier agents (Claude/Codex/Grok) write only the upper-level plan and Hermes
writes the detailed storyboard, but the 10-06 routines (Grok) and the 10-06 night reftest (Claude) had the frontier
agent write the whole storyboard and used Hermes only as a per-clip compiler. Also: cooking is compressed into one
7-second clip (ramyeon done in seconds) although the guidance already has ellipsis cuts (T-01, storyboard-cutboard).
"지금은 어떻게 해야 잘 나오는지를 알아보는 단계야. 진행해봐" — results decide later methodology changes.

Run the documented flow: Claude writes only the Creative Treatment → Hermes (Production Director) writes the
Production Storyboard incl. the cut plan, then one packet file per clip → structural validation → delegated approval
(Claude review, return items, no rewriting) → deterministic contracts/IR → semantic check → render → review.

Test questions: (1) given the cut/ellipsis guidance as input, does Hermes plan a time-passage cut by itself?
(2) does Hermes-as-director keep the strengths the user liked (camera, story) with the round-2 checklist and this
week's failure lessons? (3) object/utensil duplication and skipped start poses.

## Constraints / Must preserve
- Lia identity/wardrobe/kitchen facts from Grok's lia-kitchen-routine spec (r2); identity ref
  `ch-lia/generations/BATCH-20261006-lia-kitchen-routine/refs/identity-front-832x480.png` (sha 729bc8db…).
- One spoken line 맛있겠다. (Korean). 16:9, title card, burned subtitle as before. Renders one at a time, detached.
- Treatment must not prescribe clip count or shots; Hermes decides (cap 5 clips).
- Record real roles: treatment_author claude, storyboard/prompt author hermes, approval delegated.

## Must NOT do
No DNA/approval changes, no direct Gallery DB writes, no push, no edits to Codex-owned methodology/tools, no Claude
rewriting of Hermes's words (return items only; phrase-level fixes only if Hermes fails twice, logged).

## Plan
1. Batch `ch-lia/generations/BATCH-20261007-lia-ramyeon-hermes-director/` (`hdir.py` adapted from the 10-04
   `newflow.py`); authoring folder `D:/AI_Studio/reports/lia-ramyeon-hermes-director-20261007/`.
2. Inputs for Hermes: treatment, characters, PACKET-FORMAT, CHECKLIST (round-2 + this week's lessons), h3-guide,
   CUT-PLANNING (T-01 ellipsis, storyboard-cutboard boundary rules, real-time vs clip-length check).
3. Hermes call 1: storyboard.md (cut plan). Claude review → return items if needed. Calls 2..N: one cN.json each.
4. validate → build → render (detached) → finish → sheets → Claude review + YuNet head metric → Gallery sync.

## Progress
- 10:35 task recorded. Inputs written (treatment without clip count; CUT-PLANNING from T-01/T-30/storyboard-cutboard/
  xai-shot-menu + real-time check; CHECKLIST round-2 + this week's lessons; Lia h3-guide; hdir.py from newflow.py).
- 11:0x Hermes storyboard v0 (253 s): did its own time check (noodles ~4 min > 7 s clip) and planned an ELLIPSIS
  c1 noodles in → c2 cooked; 4 clips (ref, ref_cont, ref_cont, ref). Defects: invented a pot lid without placing it,
  cut plan vs c2 text disagreed (window/clock glance), no face in c1/c2, chopsticks source/exit missing.
- Revise 1 (128 s) fixed part; revise 2 (82 s) resolved lid/one-action but wrote the file in its read-tool view
  ('N|' prefixes, literal backslash-n) and gave c3 three held objects. Retry limit reached: format-only repair (word-identical,
  checked) + remaining items moved into `approval-review.md` conditions for the per-clip files (no Claude rewording).
- Per-clip files: round 0 — c3 reported written but missing; c1/c2/c4 structural errors. Rounds 1-2 left c1-c3 with
  the same structural errors (unused lens_family placeholder, duplicated/missing event sentence, no <Picture 2>); c1
  ignored the face-in-frame condition; c3 put the chopsticks on the side plate (pick-up off screen). c4 round 2 fixed
  the content but collapsed h3 into one string. Claude post-edits (16, logged in `ramyeon/claude-postedit.json`,
  originals `cN.hermes.json`, `c4.hermes-r2-flat.json`): structure + approval conditions only.
- 11:2x validate OK; build: semantic check pass c1-c4; treatment schema fixed (approved_by user, idea sha).
  Session `ch-lia/generations/VIDEO-20261007-110000-lia-ramyeon-hdir`. Render detached 11:26 (4 clips, ~64 min).

## Next
Finish (subs), sheets, review + YuNet, Gallery sync, report.

## Result (12:27 renders, 12:30 final)

Final `ch-lia/generations/VIDEO-20261007-110000-lia-ramyeon-hdir/outputs/ramyeon-final.mp4` (30.3 s: title + 4 clips,
subtitle 맛있겠다. at c4 0.6-1.9 s from silencedetect). Contact sheets in
`D:/AI_Studio/reports/lia-ramyeon-hermes-director-20261007/work/`.

| clip | what happened | YuNet face% / first-2s crown cut |
|---|---|---|
| c1 ref | lifts the noodle block with chopsticks into the pot — works; camera above, face cut above the mouth | 41 / 100 |
| c2 ref_cont | lid on the pot, waits, side profile; DIFFERENT kitchen layout from c1 | 45 / 67 |
| c3 ref_cont | lid on the counter, one pair of chopsticks in hand, noodles from the pot into the bowl, push-in — best clip; third kitchen layout; face leaves frame | 31 / 62 |
| c4 ref | one bowl, one pair, line then slurp; crown cut at the start | 100 / 100 |

Findings:
- With the cut-planning guidance as input, Hermes-as-director planned the time ellipsis itself (time check table) —
  the ramyeon is no longer "done in seconds". Cut-level story reads.
- Object continuity improved: one pair of chopsticks throughout, no duplicate (start-in-hand condition).
- Hermes is weak at format/structure (numbered-view file, false "written" report, same structural error twice, h3
  collapsed to a string) and at honouring framing conditions (face in frame) — Claude post-edits needed (16, logged).
- Place continuity broke: each ref_cont clip re-invented the kitchen (island → sink wall → counter). Picture 2 alone
  does not hold the set; the scene text per clip was too thin (no island/hob/window anchors restated).
- Faces: weak in 3 of 4 clips; camera above at the stove and at the table.

## Round 2 — clip cards (story/format split), 2026-10-07 afternoon

User: "좋아" to splitting by field, not by video: Hermes writes judgement (cut plan, actions, object places, camera
intent, line moment, sound) as plain-text clip cards; a deterministic converter (`card2packet.py`, batch folder only)
adds everything fixed or exact (identity/wardrobe from the character file, place anchors from a place file every
clip, tags, section names, event ids, exact event-sentence copy, <d> wrapping, empty creative envelope, JSON).
Validator failures go back to Hermes only as "which card field is empty/invalid".
Comparison control: same approved storyboard + approval conditions, same seeds (2026100751..54), same identity ref.
Measures: place continuity across clips, Claude post-edits needed, Hermes calls/time, faces (YuNet), story.
Piece key `ramyeon_card`, session `VIDEO-20261007-130000-lia-ramyeon-card-hdir`.
- Round 2 authoring: Hermes wrote 4 cards in 4 calls / 6 min (143+92+69+63 s), all converted and validated on the
  first try; 0 Claude post-edits (round 1: 12 Hermes calls for clip files + 16 post-edits). Converter sentence joins
  fixed once (camera/gaze/exit phrasing; format side). c3 card leaves her face out of the start/end framing (Hermes's
  choice for the serving insert; kept). Semantic check pass c1-c4. Render detached (same seeds as round 1).

## Round 2 result (14:38 renders)

Final `ch-lia/generations/VIDEO-20261007-130000-lia-ramyeon-card-hdir/outputs/ramyeon_card-final.mp4` (30.3 s);
side-by-side `.../outputs/compare-round1-vs-round2.mp4` (left round 1, right round 2).

| clip | round 1 face% / first-2s crown cut | round 2 face% / first-2s crown cut | round 2 notes |
|---|---|---|---|
| c1 | 41 / 100 | 100 / 0 | frontal, both hands lower the block, same kitchen |
| c2 | 45 / 67 | 100 / 0 | frontal, covered pot, waits; SAME kitchen as c1 |
| c3 | 31 / 62 | 38 / 50 | same kitchen; push-in to the bowl (Hermes's choice, face leaves frame) — best food shot |
| c4 | 100 / 100 | 100 / 0 | whole head with wall above; window on screen left as in the kitchen |

Place continuity: round 1 had three different kitchens; round 2 keeps one kitchen (window left, counter, hob, tiles)
in c1-c3 — the converter restates the place anchor and the camera relation in every clip.
Authoring cost: round 2 = 4 Hermes calls / 6 min, 0 post-edits, story unchanged (same storyboard + seeds).

Conclusion (candidate, n=1 piece): split by FIELD, not by video — Hermes writes judgement in plain-text cards;
a deterministic converter owns identity, place anchors, camera-sentence shape, tags, ids and JSON. Next: repeat on
a different character/place to confirm, then propose for the methodology (Codex-owned).

## User review of round 2 (2026-10-07)

c3 serving FAILED: the bowl already holds ramyeon before she pours (object state change shown on screen; the model
renders the end state early — same class as duplicated chopsticks and the re-formed yolk). User: show only lifting the
pot and starting to pour, then cut. Hermes did not think of it: CUT-PLANNING said "a difficult transition happens at
the cut" with carrying/pick-up examples only. Added for the next round: CUT-PLANNING section 6 (state changes happen at
the cut: attempt → CUT → result), CHECKLIST 12, and a `state_change` card field — a clip with a state change must end
before the change completes.
