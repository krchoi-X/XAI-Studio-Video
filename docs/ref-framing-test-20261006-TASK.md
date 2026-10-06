# Reference face-size vs seated head crop — controlled test (2026-10-06 night)

- Active editor: Claude Code (claude-opus-5-5), real actor `claude`; Hermes compiles prompts for new routines.
- Status: ACTIVE
- User request (2026-10-06 ~23:xx): "진행해줘. 자야할 시간이라 끝나면 비슷한 패턴으로 다른 캐릭터로 2개쯤 더 만들어서 가설을 검증해봐"
  — run the identity-reference test proposed in Grok's record, then verify on two more characters.

## Hypothesis (from Grok's 2026-10-06 record, sharpened)

Seated-line c3 head cropping depends on the identity reference. Measured face height / 480 px of the references used:
Noa 0.67 (head kept) vs Suan 0.37-0.40 and Lia 0.34-0.46 (head cropped). H: a reference whose face fills ~0.65 of the
frame keeps the whole head in the seated c3; ~0.40 crops it. Alternative: c3 inherits the scale of Picture 2 (the
previous clip's last frame).

## Design

- References: `ch-lee-suan/generations/BATCH-20261006-ref-framing-test/make_refs.py` builds loose (face 0.40) and tight
  (face 0.65) 832x480 refs from each character's default identity image with one rule (scale + pad; same face centre);
  measured fractions in `refs/refs-manifest.json`.
- Part A (existing scenes, only image_refs[0] and seed vary; prompt, contract, Picture 2 unchanged):
  Suan v5 c3, Noa v1 c3 (reverse test: loose), Lia v1 c3; two seeds for Suan and Noa.
- Part B (new characters, same routine pattern as Grok's Noa/Lia, Hermes-compiled): Reika (gyoza) and Jun (kimchi
  fried rice): c1 Ref2VA, c2 FL2VA, c3 rendered twice with the same seed and Picture 2 — loose vs tight.
- Measure: YuNet face detection at 2 fps on every c3 — face-top / frame-height, frames with the face cut at the top;
  plus Claude's frame review. Approval delegated as before; renders one at a time; intermediates outside sessions.

## Must NOT Do

No DNA or approval changes, no Codex-owned file edits, no direct DB writes, no push.

## Progress
- 23:0x refs built (make_refs.py; YuNet face fraction: every loose 0.40-0.45, every tight 0.65-0.72). Part A launched
  detached (8 c3 variants; reftest.py). Part B batches built from Grok's Noa routine (build_partB.py; c3 camera wording
  verbatim from Noa; gender/pronoun adaptation for Jun) and `routine.py setup v1` run for Reika and Jun.
- Baseline metric (measure.py, YuNet 4 fps, top_cut% = face box within 6% of the frame top): Suan v5 c3 56%, Lia v1 c3
  83%, Noa v1 c3 14% — matches the frame reviews.
- 23:20 suan-tight-s1 (ref face 0.65, same seed): top_cut 56% / first-2s 100% — identical to the loose baseline. The
  tight reference alone did not keep Suan's head. Picture 2 check: Suan's and Lia's c2-last frames already have the
  crown at/over the top edge; Noa's has headroom — matches the baselines (first-2s cut: Suan 100, Lia 100, Noa 0).
  Added Part A2 (`pad_p2.py`, `partA2.py`): original ref + seed, ONLY Picture 2 replaced by a headroom-padded c2-last
  (shrunk 0.82, top band = edge replication + blur; caveat: the blurred band is not real content). Queued after Part A.
  measure.py now also reports cut2s% (first 2 s, before the lean-in moves the face down).
- 23:36 noa-loose-s1 (Noa c3, ref 0.41 instead of 0.67, same seed/Picture 2): cut2s 100% / top_med 0.008 vs the
  tight baseline 0% / 0.108. Frames: same composition, but the loose run sits ~10% of frame height higher and the crown
  leaves the frame. So the reference face size moves the framing for Noa (but did not for Suan). Note Noa's c3 is a
  different set-up (seated at the table) than its c2-last (at the stove), so Picture 2 is not the opening frame there.
- 00:08 Lia: loose (0.45) cut 100% / first-2s 100%; tight (0.72) cut 72% / first-2s 100%. Both open with the face out
  of frame (camera on torso + bowl); tight only shows slightly more forehead later. Tally so far (seed 1): tight ref
  clearly helps Noa, slightly Lia, not Suan. The reference is at most a secondary factor; the per-scene c3 opening
  framing (prompt camera + Picture 2) dominates. Seed-2 runs and Part A2 pending.
- 01:11 Part A done. Seed 2 (+1000): Suan loose/tight both open with the face out of frame (face% 52 / 38); Noa
  loose/tight both cut 100% (first 2 s), frames near-identical. Noa tight-s2 = the exact baseline condition (tight ref,
  same prompt/Picture 2), only the seed changed, and it lost the headroom the baseline had.

  Part A conclusion: identity-ref face size is NOT a reliable control of seated-c3 head crop. For a fixed seed, loose vs
  tight give near-identical compositions (small vertical shifts, at most ~10% of frame height, not always in the
  helpful direction); changing the seed moves the framing more than changing the ref. Grok's observation (Noa kept the
  head) is explained by a favourable seed, not by the tight ref. Part A2 (Picture 2 headroom) launched 01:13.
- 01:44 Part A2 done: Picture 2 headroom (original ref + seed) did not help: Suan p2pad opens with the face out of
  frame (face% 55), Lia p2pad first-2s cut 100% (top_cut 84%). Neither ref face size nor Picture 2 framing controls the
  seated head crop.
- New hypothesis H2: every cropped c3 asks for "band of wall above the head + whole head + upper body + WHOLE table top"
  in one 16:9 frame; the model keeps the (detailed) table and gives up the head. Part B redesigned per character:
  c3 loose ref (Noa wording), c3 tight ref, c3 H2 (spec v2 = c3 only, ONLY camera contract changed: head first in the
  upper third, level camera not tilted down, near half of the table may leave the bottom; `build_v2.py`). All three
  same seed and same Picture 2 (v1 c2 last frame). Queue: `partB_run.py` (detached).
- Part B spec fixes before compile: Noa leftovers (egg/rice/chopsticks/pierce) in the copied specs; setup re-run.
- Hermes compile: round 0 copied the guide placeholder "then her hair ... written from the brief" verbatim, claimed
  "<Picture 2> shows her at the table" (it is the stove frame), and omitted kitchen/wardrobe (Claude review caught the
  last two; lint caught the first). Round 1 dropped the experiment's own framing words ("band of wall") in Reika c3 and
  wrote "from the chest up" in Jun c3 — the control-condition text needs a Claude read every round.
