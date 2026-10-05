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

## Open questions for the next round

1. Who reviews first? Needs a vision-verified reviewer (human or confirmed-image model); Hermes for checklist only.
2. Packet checklist enforcement: anchors per clip, object counts after cuts, hand-action source/destination, dish features.
3. Is Hermes's expressiveness worth its identity/object losses if the checklist closes those gaps? Re-run jjigae with the checklist.
4. Plan-gate support for runtime chain frames (Codex).
5. Duo stage 2 (handing an object) and speaker verification by ear.
7. Validator check for camera consistency (anchor vs framing; ban vs movement) and face visibility at key beats.
6. Gallery visibility of local renders (`restricted` by default) — user decision.
