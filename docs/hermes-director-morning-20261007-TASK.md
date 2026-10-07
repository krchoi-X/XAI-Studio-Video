# Hermes-director clip-card flow, 2nd piece — Lia morning routine (2026-10-07)

Active editor: Claude (actor `claude`). Scope: one experimental production; no methodology/schema/shared-skill or
Codex-owned tool edits.

## Goal

User: "비슷한 난이도의 다른 영상은 어때? 리아가 아침에 일어나서 잠옷바람으로 이를 닦고, 머리에 수건을 묶고 세수하고,
옷장으로 가서 갈아입을 옷을 고르고, 컷이 바뀌면서 외출복으로 갈아입고 현관으로 가는거야".
Second test of the round-2 flow from `hermes-director-ramyeon-20261007-TASK.md` on a different place set and with
many state changes (pajamas → towel on the hair → wet face → outfit), plus the new rule "object/wardrobe state changes
happen at the cut" (CUT-PLANNING 6, card field `state_change`).

## Flow
Claude: treatment + world file only (places, looks). Hermes: storyboard (cut plan) → one clip card per clip.
`card2packet.py` (generalised: per-clip `look` and `place` from world.json) → validate → build → render → review.

## Must preserve / must not
Lia identity (identity-front ref, sha 729bc8db…); adult, everyday, clothed, general audience — the change of clothes
happens at a cut (never on screen). No spoken line (none requested). No DNA/approval changes, no push, no Codex-owned
edits, no Claude rewording of Hermes's cards (structure-only fixes logged if ever needed).

## Measures
Hermes calls/time and Claude edits; place/look continuity per clip; state changes placed at cuts or not; faces (YuNet);
mirror handling in the bathroom.

## Progress
- task recorded.
- Inputs: treatment (no clip count), world.json (looks pajamas / pajamas_towel / outfit; places bathroom / bedroom /
  entrance with camera relation), CUT-PLANNING (+ wardrobe example in section 6), CHECKLIST, CLIP-CARD (+ `look`).
  Tools copied from the ramyeon batch: hdir.py (piece `morning`, seeds 2026100761..), card2packet.py (place + look).
- Hermes storyboard (1 call, 380 s): printed it in the reply instead of writing the file — saved unchanged as
  storyboard.md. All look changes placed at cuts without prompting (towel tied at cut 1, dressed at cut 3); face washing
  shown as the result (wiping water). Approval conditions: c1 one hand + one action; c4 no orbit, face readable.
- Cards: 4 calls / ~6 min, first-try valid, 0 Claude edits. Claude fixed its OWN world file: the entrance camera
  relation would have filmed her back (camera now beside the door, she walks toward it).
- Build pass c1-c4; render detached 16:30.

## Result (17:31 renders)

Final `ch-lia/generations/VIDEO-20261007-160000-lia-morning-hdir/outputs/morning-final.mp4` (title + 4 clips, no line).

| clip | result | face% / first-2s crown cut |
|---|---|---|
| c1 bathroom/pajamas | brushes teeth, three-quarter, mirror reflection present but natural | 100 / 0 |
| c2 bathroom/pajamas_towel (ref_cont) | FAIL: opens WITHOUT the towel, back to camera, then the towel appears on her hair; ends looking toward the lens | 48 / - |
| c3 bedroom/pajamas_towel | towel kept, touches the cream cardigan, window on screen left | 100 / 0 |
| c4 entrance/outfit | dressed, walks toward the camera to the door, face readable | 100 / 0 |

Findings:
- The card flow repeated: first-try valid cards, 0 Claude edits to Hermes text, places/looks held per clip.
- Hermes put every look change at a cut (rule worked at the plan level).
- NEW failure mode: a look change INTO a `ref_cont` clip. Picture 2 (previous clip's last frame) shows the old look
  (no towel), so H3 starts in the old look and performs the change on screen. Rule candidate: after a look/state
  change across a cut, the next clip is `ref` (no previous frame), or the previous frame must already show the new
  state. The converter/validator can enforce it: if `look` differs from the previous clip's look, `mode` must be `ref`.

## Title-card fix (2026-10-07, user report)
The shared assembly step (`ch-lee-suan/.../BATCH-20261004-suan-reference-set/finish.py`) had the subtitle name
'이수안' hard-coded on the title card, so the Lia finals showed 이수안. finish.py now takes `piece['char_name']`
(default 이수안); hdir.py passes 리아. Corrected finals written under new names (`*-final-titlefix.mp4`,
`compare-round1-vs-round2-titlefix.mp4`); the first finals stay registered (never overwritten) — hide/reject them in
Review. Grok's routines and the Reika/Jun reftest use `character_name_ko` and were not affected.
