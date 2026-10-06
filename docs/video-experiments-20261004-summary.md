# Lee Suan video experiments, 2026-10-04 → 05 — consolidated record

Author: Claude Code (claude-opus-5-5). All media are in the Studio Gallery under 이수안 (`ch-lee-suan`), sessions
`VIDEO-20261004-*` and `BATCH-20261004-*` — **visibility `restricted`, decision `needs_review`**: turn on "show
restricted" to see them. 112 videos registered; preview and Range playback verified for every one (2026-10-05).

## Runs

| # | run | who did what | sessions / records |
|---|---|---|---|
| R1 | Reference set A–D (rain evening, rooftop radio, first jjigae, silent light) | Claude: storyboard, contracts (v1 pinned gate), prompts, review, edit | `VIDEO-20261004-00260{0..3}-*`; `BATCH-20261004-suan-reference-set/review.md`; [task](lee-suan-reference-storyboards-TASK.md) |
| R2 | Compile comparison A–D | Same contracts; Hermes compiled prompts from a prose-free brief; one pass | `VIDEO-20261004-09000{0..3}-*-hermes`; `BATCH-20261004-suan-hermes-comparison/{compile,render}-review.md`, `compare-*`; [task](hermes-compile-comparison-TASK.md) |
| R3 | New pieces E (첫눈), F (이거요) | Claude directed; Hermes compiled + launched render; one recompile of E1 | `VIDEO-20261004-11000{0,1}-*`; `BATCH-20261004-suan-hermes-originals/notes.md` |
| R4 | New-flow experiments 1–5 | Claude treatments; Hermes Production Director (storyboard, v2 contracts, H3 profiles); delegated approval by Claude; deterministic H3 adapter; Hermes operator; Hermes "independent" review | `VIDEO-20261004-23550{1..6}-*`; `BATCH-20261004-new-flow-experiments/compare-*`; `D:/AI_Studio/reports/suan-new-flow-20261004/{approval-review,render-review,hermes-first-review}.md`; [task](new-flow-experiments-20261004-TASK.md) |

## Measured results

- First-pass intent (Claude scoring, not blind): R1 6/10 pass; R2 Hermes-compiled 6/10 with different failures
  (Hermes better on event order/gaze, worse on objects/omissions).
- R4 Exp 2 A/B (same treatment, same seeds): Claude-directed arm kept identity (ribbon updo) and the ttukbaegi;
  Hermes-directed arm was livelier with better camera, but lost the ribbon, the ttukbaegi at the table and the dish
  identity. User: both much better than R1; jjigae still the hardest piece.
- R4 Exp 3: granting L2 (rack focus) broke no locks; technique visible in 1/2 seeds.
- R4 Exp 4: two registered identities (Suan + Jun) stayed separate with correct sides and mutual gaze in 3/3 seeds.
- User judgement across runs: Hermes's camera movement and wet-look were clearly better; Claude over-locked camera and
  wrote state changes that fought the identity text.

## Verified or repeated findings (evidence level)

| finding | level | where filed |
|---|---|---|
| H3 Ref2VA output aspect follows the first reference image | repeated | skill feedback 2026-10-03T19:49 |
| FL2VA chains of 2 clips are seamless; the 3rd clip with a large move drifts identity | candidate (several cases) | feedback |
| State changes (wet hair) must be declared in subject definition / retention "new", not contradicted by "stays the same" | candidate (user-judged) | feedback |
| Continuation text (fl / ref_cont) must restate recognition anchors and key objects with counts | candidate (A/B) | feedback |
| Hand actions must name source and destination objects; food needs its defining visible features | candidate (user-observed) | feedback |
| Real-person realism (take the wet coat off) beats render-risk omission | candidate (user) | feedback |
| Hermes cannot serve as a visual reviewer (restated packets, passed 16/16, invented objects/person) | observed once, strong | feedback |
| Hermes reports ("validator OK", "detached pid") must be verified from files | repeated | memory |
| Treatment-backed plan gate cannot express a runtime chain frame (FL2VA) | design gap | feedback |
| Deterministic template was not H3-native (fixed by Codex `dbd4637`) | resolved | feedback |

## Round 2 (2026-10-05)

- 된장찌개 v3 (Hermes director, merged camera rule "move for a reason, keep an anchor" + review checklist): content
  logic fixed (dish, spoon source, table counts, identity); face visibility regressed through framing choice.
- 창가 연장: two FL2VA clips chained from the best window take; the motivated push-in to her face on the sky is the
  clearest success of the merged camera rule.
- Hermes revises large JSON packets unreliably; per-clip files + merge solved it.

## Round 3 (2026-10-06, Grok director + Hermes compiler) — Claude cross-check

Record: [experiments-jjigae-v4v5-and-char2-hermes-20261006.md](experiments-jjigae-v4v5-and-char2-hermes-20261006.md)
(v4, v5, r1 remake; Lia ramyeon; Noa egg-rice). Claude re-checked the three jjigae finals from contact sheets and
agrees with Grok's verdicts: v4 is the most balanced jjigae so far (front-on stove camera, face readable through the
nervous check and the taste, doenjang-jjigae reads correctly, sweatshirt and ribbon kept) with the c3 ghost spoon and
forehead crop; v5 fixed the ghost spoon (spoon put down at the end of c2) but lost the face in c1-c2 and the stew reads
less like doenjang; r1 (plain white top) went to side profile in c1-c2, while c3 shows the face during the line but
gained an extra spoon. All 30 round-3 session videos are registered in the Gallery.

## Round 4 (2026-10-06/07 night, Claude) — seated head-crop test

Task record: [ref-framing-test-20261006-TASK.md](ref-framing-test-20261006-TASK.md). 18 c3 renders over 5 characters
(Suan, Noa, Lia re-renders of existing c3s; new Hermes-compiled kitchen routines for Reika and Jun), measured with YuNet
(`metrics.json`, overview `D:/AI_Studio/reports/ref-framing-test-20261006/overview-c3-head-crop.jpg`).

- Identity-ref face size (0.40 vs 0.65 of the frame): NOT a reliable control. Same seed → near-identical composition
  for Suan/Lia/Reika; Noa and Jun changed, but in opposite directions to the seed effect (Noa's own baseline condition
  lost the head on seed 2). Grok's "tight ref keeps the head" was a favourable seed.
- Picture 2 headroom (ref_cont): no effect (Suan, Lia).
- Seed changes framing more than any tested input.
- Every cropped clip has a high camera looking DOWN at the dish; every kept head has a near-eye-level camera.
  "level camera, not tilted down" fixed Jun (0% cut) but the same contract's shot-scale words ("level medium shot",
  "head in the upper third") pushed Reika closer (62% cut, from 0%). Shot-scale words pull the camera in.
- Hermes (2 fix rounds) still: copied the guide placeholder, misdescribed Picture 2 as the table, dropped the
  experiment's control wording; Claude phrase-level post-edits logged in `*.claude-postedit.json`.
- Jun's routine shows a spoon in hand plus a spoon still on the rest (duplicate utensil after pick-up).

## Open questions for the next round

1. Who reviews first? Needs a vision-verified reviewer (human or confirmed-image model); Hermes for checklist only.
2. Packet checklist enforcement: anchors per clip, object counts after cuts, hand-action source/destination, dish features.
3. Is Hermes's expressiveness worth its identity/object losses if the checklist closes those gaps? Re-run jjigae with the checklist.
4. Plan-gate support for runtime chain frames (Codex).
5. Duo stage 2 (handing an object) and speaker verification by ear.
7. Validator check for camera consistency (anchor vs framing; ban vs movement) and face visibility at key beats.
6. Gallery visibility of local renders (`restricted` by default) — user decision.
8. Seated framing: test Noa wording + "camera at eye level, level, not tilted down" with NO shot-scale words, 2 seeds
   each on Suan and Lia; and/or render 2 seeds per seated dialogue clip and pick with the YuNet head-crop metric.
