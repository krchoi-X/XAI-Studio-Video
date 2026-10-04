# New-flow experiments (Creative Treatment → Hermes Production Director), Lee Suan + Jun

- Date: 2026-10-04 ~23:40 KST (renders overnight)
- Active editor: Claude Code (claude-opus-5-5), real actor `claude`; Hermes (`meromero26b-a4b-hermes`) as Production
  Director / prompt author / submitter / first reviewer per `docs/creative-treatment-contract.md`
- Status: ACTIVE

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

(updated as work proceeds)
