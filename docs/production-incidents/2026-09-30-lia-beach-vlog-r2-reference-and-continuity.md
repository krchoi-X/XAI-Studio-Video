# Production incident — Lia beach vlog r2 reference and pack continuity

Status: REVIEWED
Date: 2026-09-30
Recorded by: Codex from Grok production records
Requested reviewer: Codex or Claude when a fix is assigned
Review authority: review-only; no r3 render, DNA edit or shared-skill edit authorized
Evidence level: repeated across r2 variants; reference-pixel findings directly verified

## Summary

Three Lia beach-vlog remakes strengthened the right-wrist, landscape, opening-frame and one-way story locks. Individual variants improved different constraints, but no r2 variant satisfied all of them. The reference packet itself contains contradictions: files named `rightwrist` appear to place bracelets on Lia's anatomical left wrist, portrait subjects remain centered inside padded landscape canvases, and every independent pack receives sit/stand/walk references together.

## Production identity

| Field | Value |
|---|---|
| session family | `VLOG-20260930-064041-lia-beach-vlog-v{1,2,3}-r2` |
| primary evidence session | `VLOG-20260930-064041-lia-beach-vlog-v1-r2` |
| session path | `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2` |
| GO / approval state | r2 was user-approved; r3 is held pending new user GO |
| requester | `grok` |
| orchestration / relay note | recorded as a user-GO relay in the local know-how; not a Hermes still-production path |
| executor | `local-wangp-worker` |
| engine | `WanGP` |
| model | `minimax_h3_ref2va_pruned` |
| prompt mode | `FG`, enhancer off |

## Character and reference contract

| Character | DNA source + version/hash | Mandatory anchors | Selected references + roles | Known conflicts |
|---|---|---|---|---|
| `ch-lia` | Private canonical record v3, `420c615ac2852edf5a354768c81d541be911ff36c801db6d80a57df78e5f0d76` | elongated oval face, dark-brown eyes, near-black hair with full bangs, three thin red/blue bracelets on anatomical right wrist | sit half-body, stand half-body, walk-side body/identity refs | apparent left-wrist bracelets; portrait-centered padded composition; sit ref passed to later packs |

## Expected acceptance criteria

- Three thin red-and-blue bracelets remain on Lia's anatomical right wrist only.
- Opening is a landscape MW/FS beach view, not a face-fill close-up.
- Visible content remains full-frame landscape without pillarbox/portrait remaps.
- Story proceeds once through sit→stand→look→stroll→notice→call→run.
- Phone appears only on the call beat.
- Cast remains Lia alone with the friend offscreen.

## Observed result

| Variant | Improvement | Remaining failure |
|---|---|---|
| v1-r2 | wardrobe, cast and container dimensions held | left-wrist/unstable bracelets, CU opening, portrait remaps, early call/phone and broken ladder |
| v2-r2 | opening, right-wrist bracelet and action ladder reviewed as passing | intermittent portrait remaps and CU inserts |
| v3-r2 | true landscape fill passed | left-wrist bracelets, CU montage, fragmented ladder, ocean-axis and early-phone failures |

## Direct evidence

- Primary provenance: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2\session-provenance.json`
- Final Pack A prompt: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2\A.txt`
- Pack settings/reference list: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2\A.settings.json`
- Sit reference: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2\refs\01-lia-sit-half-body-rightwrist-832x480.png`
- Stand reference: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2\refs\02-lia-stand-half-body-rightwrist-832x480.png`
- Walk reference: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2\refs\03-lia-walk-side-rightwrist-832x480.png`
- v1-r2 review: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v1-r2\CONTINUITY-1pass-RESULT.txt`
- v2-r2 review: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v2-r2\CONTINUITY-1pass-RESULT.txt`
- v3-r2 review: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v3-r2\CONTINUITY-1pass-RESULT.txt`
- Canonical Lia record: `D:\codex\XAI-Studio-Private\characters\ch-lia\character.json`

## Facts

- Final prompts repeatedly require the anatomical right wrist and one-way story ladder.
- Visual inspection of all three r2 refs found the bracelets on the apparent anatomical left wrist despite `rightwrist` filenames.
- The references are portrait compositions padded into landscape canvases with blurred side-fill.
- The same three references, including the sit image, are listed in every pack's settings.
- A–D are separate H3 jobs followed by hard-cut concatenation; no actual prior-pack frame is supplied as temporal memory.
- Saved reviews record failures across multiple r2 variants, while also recording partial improvements.

## Hypotheses

- Contradictory reference laterality is a major driver of left-wrist output. A one-variable corrected-reference comparison is required to establish engine causality.
- Portrait-centered padded refs encourage close-up/pillarbox visual grammar even when the output container is `832x480`.
- Passing a sit reference to later packs encourages state reset despite textual prohibitions.
- Independent pack generation explains causal discontinuity; hard concatenation alone cannot preserve story state.

## Attempts already made

| Attempt | What changed | Result | Evidence |
|---|---|---|---|
| r2 | stronger text locks, three half-body refs, reduced ref count, landscape padding, one-way ladder language | partial improvement; no single variant cleared all constraints | three r2 review files |

## Decision and current hold

- Current decision: preserve v1/v2/v3 and r2 evidence; do not start r3 automatically.
- Rerender authority: not granted.
- Must preserve: successful cast/wardrobe constraints and per-variant improvements.
- Must not do: rename a wrong-side file as a fix, reuse all state refs in every pack, overwrite r2 outputs or change Lia DNA.

## Questions for Codex/Claude

1. Should reference preflight store anatomical laterality and reject filename/pixel disagreement?
2. Should the next packet use native-landscape state keyframes, first/last frames or fewer jobs?
3. Which checks can be deterministic before authorizing one sample render?

## Proposed smallest correction

Create a future packet, only after user GO, with visually verified anatomical-right bracelets, native-landscape composition and pack-specific references. Remove the sit reference after Pack A. Use one overlap/boundary frame or fewer independent packs. Test one representative pack before a full remake.

## Verification plan

1. Human preflight of reference laterality, composition and per-pack roles; record hashes.
2. Deterministic comparison that later packs omit prior-state references and final prompts contain the required anchors.
3. After explicit user GO, one sample pack; review visible aspect, opening scale and wrist before any r3 batch.

## Resolution

Final status: REVIEWED; r3 not authorized
Owner: unassigned
Changed files/commits: none
Checks: repository/session evidence and reference-pixel review
Later production evidence: none
Remaining uncertainty: relative contribution of contradictory pixels, reference composition and H3 model behavior
