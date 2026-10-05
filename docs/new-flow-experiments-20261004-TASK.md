# New-flow experiments (Creative Treatment → Hermes Production Director), Lee Suan + Jun

- Date: 2026-10-04 ~23:40 KST (renders overnight)
- Active editor: Claude Code (claude-opus-5-5), real actor `claude`; Hermes (`meromero26b-a4b-hermes`) as Production
  Director / prompt author / submitter / first reviewer per `docs/creative-treatment-contract.md`
- Status: DONE — 16 clips rendered, reviewed, assembled, registered (needs_review); awaiting user viewing

## Goal

User request (2026-10-04 23:3x): run experiment set 1-5 under the updated methodology (b855520 role split, dbd4637
native H3 adapter). User delegated the production-packet approval to Claude for this run ("이번엔 위임"); every approval
record says so. Partner for the two-person test: 준 (`ch-jun`).

| # | piece | question |
|---|---|---|
| 1 | 비 맞고 귀가 v2 (Suan) | does the new flow work end-to-end; are coat removal and the wet look delivered |
| 2 | 된장찌개 v2 (Suan), two arms | Hermes vs Claude as Production Director from the same treatment, same seeds |
| 3 | 비 그친 창가 (Suan), L1 vs L2 | does granting a named camera technique (rack focus) improve cinematography without breaking intent |
| 4 | 2인 1단계 (Suan + Jun) | identity separation, speaker assignment, gaze assignment, static two-shot, 3 seeds |
| 5 | 작가 비교 (no render) | Hermes vs Claude scenario from a one-line idea |

## Design decisions

- Claude authors Creative Treatments only (v1 schema, validated by `tools/creative_treatment.py`). Hermes authors the
  Production Storyboard, v2 Intent Contracts with `prompt_segments` and `engine_prompt_profiles` (h3_ref2va_v1 /
  h3_fl2va_v1). Exp 2 arm B: Claude authors the same artifacts (role deliberately swapped; recorded as such).
- Approval: delegated to Claude; contract approval records `approved_by: "user (delegated to claude, chat 2026-10-04)"`.
  Role-attribution sidecars are written and validated, but sessions are registered with `--methodology
  intent-preserving-v1` only, not the treatment/production-plan gate: the plan gate requires every reference hash at
  approval time, which FL2VA chaining (previous clip's last frame) cannot provide. Filed as feedback.
- Tools: current HEAD (dbd4637) `tools/` (no pinned snapshot). Deterministic H3 adapter compiles every prompt.
- One pass per arm; the independent Hermes review runs first, then Claude's review; failure attribution
  storyboard | compiler | renderer | edit. A second attempt only through the documented repair path.
- Intermediates outside Library sessions; finals written once (Gallery legacy import rule).

## Must NOT Do

No DNA/approval change, no edits to Codex-owned methodology/tools/schemas, no direct DB write, no push.

## Progress

- 23:50 four Creative Treatments (Claude) written and validated; delegation recorded in
  `BATCH-20261004-new-flow-experiments/approval-delegation.md`. Jun landscape reference derived (crop+pad, provenance).
- Hermes as Production Director: storyboard.md + packet.json per piece (authoring folders under
  `D:/AI_Studio/reports/suan-new-flow-20261004/`); deterministic converter `newflow.py build` writes v2 contracts with
  `engine_prompt_profiles`, IR v2, native H3 prompts via `--render-prompt`; all checks pass.
- Approval review (`approval-review.md`): jjigae2_h approved as-is (A/B conflict of interest; predictions recorded);
  duo, rain2, window returned once each and approved after revision. Hermes needed one validator-fix round for rain2 and
  window and reported "OK" once while files still failed. jjigae2_c authored by Claude.
- ~1 h lost to a wait loop on hermes.exe (desktop app stays resident).
- 02:01 Hermes (operator) launched `newflow.py render` for 16 clips; first run passed the v2 local gate.
- 06:06 all 16 clips rendered (one pass). Claude frame review: `D:/AI_Studio/reports/suan-new-flow-20261004/render-review.md`.
- Results:
  - Exp 1 rain2: coat removal and wet look delivered; c2 towel ends covering the face; coat colour drift; window reflection artifact.
  - Exp 2 A/B (same seeds): Claude arm kept ribbon updo and ttukbaegi across the cut; Hermes arm livelier but lost the
    ribbon (c2-c3) and the ttukbaegi at the table (its continuation text omitted both). Both arms had spoon issues.
  - Exp 3 window: L2 allowance broke no locks; rack focus clearly visible in 1 of 2 seeds; an in-clip framing jump
    before the final reach appeared in 3 of 4 takes regardless of level.
  - Exp 4 duo (Suan + Jun): identity separation, screen sides and mutual gaze held in 3/3 seeds; two speech bursts at
    the expected times, speaker assignment probable from mouth crops, not verified by ear.
  - Exp 5 writer: both scenarios in `writer/`; judgement left to the user.
- Hermes independent first review restated the packets instead of the images (passed all 16, invented objects and a
  second person) — the role-split's first-review step is not viable without verified image access. Filed as feedback.
- Finals, comparisons (`BATCH-20261004-new-flow-experiments/compare-*.mp4`) registered: sync imported 30 assets.
- User review (2026-10-05): improved overall, camera good; jjigae issues added (Hermes arm: not reading as doenjang-jjigae,
  two rice bowls, no ttukbaegi, spoonful still rice; Claude arm: tastes from the side plate instead of the stew because
  the event line named no source). Recorded in render-review.md and filed as feedback.
- Gallery check: 112/112 session videos registered with working preview and Range playback; all `restricted`
  (hidden in the default feed). Consolidated record: [video-experiments-20261004-summary.md](video-experiments-20261004-summary.md).
