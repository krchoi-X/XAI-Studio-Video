# Production incident — Reika/Suan morning-care identity and prop continuity

Status: REVIEWED
Date: 2026-09-29
Recorded by: Codex from Grok production records
Requested reviewer: Codex or Claude when a fix is assigned
Review authority: review-only; no rerender, DNA edit or shared-skill edit authorized
Evidence level: verified prompt conflict; output behavior remains run-scoped evidence

## Summary

The four-pack morning-care video largely preserved cast, coverage, aspect and action order, but Suan's defining updo/ribbon was absent in Pack A and appeared in Pack B. Food and the oil bottle also appeared before their approved story states. The canonical DNA and selected images contained Suan's ribbon; the runtime prompt weakened the hair contract to vague natural morning hair.

## Production identity

| Field | Value |
|---|---|
| session ID | `VLOG-20260929-142724-reika-suan-morning-care` |
| session path | `D:\AI_Studio\library\characters\ch-mizuki-reika\generations\VLOG-20260929-142724-reika-suan-morning-care` |
| user request | recorded in `session-provenance.json` |
| GO / approval state | original production completed; remake held pending user approval |
| requester | `grok` |
| orchestration / relay note | not durably recorded; do not infer Hermes from conversation memory |
| executor | not present in this session's provenance |
| engine | `WanGP` |
| model | `minimax_h3_ref2va_pruned` |
| prompt mode | `FG`, enhancer off in settings |

## Character and reference contract

| Character | DNA source + version/hash | Mandatory anchors | Selected references + roles | Known conflicts |
|---|---|---|---|---|
| `ch-mizuki-reika` | Private canonical record v1, `11ce5b9501577c82d60051075ab7b4301297e858c137866711ff92711c0447c1` | long sleek jet-black hair, elongated oval face, dark-brown almond eyes | face-09 editorial; nude body Soft | no identity conflict identified in the saved review |
| `ch-lee-suan` | Private canonical record v1, `6aace2be7b8330432ed905127f840dfdfbc4d3e4168caac17b45a6e53eae0d4b` | rounded ash/milk-tea updo, large black-and-white ribbon, grey-brown eyes | face master; clothed full-body Soft | prompt says `Soft natural morning hair` and omits the required updo/ribbon lock |

The selected Suan references visibly contain the ribbon. They are landscape containers built from portrait-oriented subject images; the full-body reference has black side areas.

## Expected acceptance criteria

- Suan's rounded updo and black-and-white ribbon remain present from Pack A through D.
- No toast, coffee, plates, cups or trays appear.
- The oil bottle first appears only at the C9 fetch beat.
- Existing passes for cast, coverage, landscape aspect and washcloth/towel order remain intact.

## Observed result

| Pack/shot/run | Timestamp/frame | Observation | Severity |
|---|---|---|---|
| Pack A | start to ~0:13 | Suan ribbon absent | HARD identity |
| Pack B | ~0:13 | ribbon appears, producing a continuity pop-in | HARD identity/continuity |
| Pack A | ~0:08 | toast and coffee invented bedside | HARD prop continuity |
| Pack A/B | ~0:00 and ~0:13 | oil bottle exists before C9 | HARD story-state continuity |

## Direct evidence

- Provenance: `D:\AI_Studio\library\characters\ch-mizuki-reika\generations\VLOG-20260929-142724-reika-suan-morning-care\session-provenance.json`
- Final Pack A prompt: `D:\AI_Studio\library\characters\ch-mizuki-reika\generations\VLOG-20260929-142724-reika-suan-morning-care\A.txt`
- Pack A settings and exact references: `D:\AI_Studio\library\characters\ch-mizuki-reika\generations\VLOG-20260929-142724-reika-suan-morning-care\A.settings.json`
- Review result: `D:\AI_Studio\library\characters\ch-mizuki-reika\generations\VLOG-20260929-142724-reika-suan-morning-care\CONTINUITY-1pass-RESULT.txt`
- Suan canonical record: `D:\codex\XAI-Studio-Private\characters\ch-lee-suan\character.json`
- Composite: `D:\AI_Studio\library\characters\ch-mizuki-reika\generations\VLOG-20260929-142724-reika-suan-morning-care\edit\reika-suan-morning-care-v1.mp4`

## Facts

- Canonical Suan DNA names the updo and ribbon as recognition anchors.
- Both selected Suan references show the updo/ribbon.
- The final prompt labels Suan hair as vague `Soft natural morning hair` rather than preserving the canonical anchors.
- The saved continuity review records ribbon absence/pop-in and premature food/oil props.

## Hypotheses

- The weakened runtime hair line allowed H3 to treat the ribbon/updo as optional despite the pixel references. Test by changing only the compiled hair/identity contract in a future user-approved single-pack sample.
- The bedside context and prior production history may have encouraged food/oil props, but this is not verified. A future controlled prompt should remove prop ambiguity while preserving the same references.

## Attempts already made

No remake is recorded for this incident. The Continuity Reviewer stored proposed HARD locks and held further rendering.

## Decision and current hold

- Current decision: preserve outputs and review evidence; diagnose before another run.
- Rerender authority: not granted.
- Must preserve: cast=2, Reika nude/Suan clothed roles, landscape aspect, wet cloth→dry towel order, care tempo and accepted gaze beat.
- Must not do: silently change either character's Stable DNA, rerender automatically or overwrite prior prompts/outputs.

## Questions for Codex/Claude

1. Should mandatory recognition anchors be checked mechanically in the final video prompt before submit?
2. Does the fix belong in the prompt compiler/generation packet or only in this session's future remake packet?
3. What is the cheapest way to verify prop-state timing without rerendering all four packs?

## Proposed smallest correction

For a future approved sample, restore Suan's explicit updo+ribbon identity lock in the final prompt, keep the same DNA/reference sources, and test Pack A only with food and early oil explicitly absent. Do not edit canonical DNA.

## Verification plan

1. Deterministically compare the compiled prompt with both characters' mandatory recognition anchors.
2. Visually verify reference roles and native composition.
3. Only after user GO, render one Pack A sample and review ribbon presence plus food/oil absence before any remaining packs.

## Resolution

Final status: REVIEWED; fix not implemented
Owner: unassigned
Changed files/commits: none
Checks: repository/session evidence review only
Later production evidence: none
Remaining uncertainty: causal weight of text conflict versus H3 reference adherence
