# Production incident — Night batch 20260930 home/cvstore (all packs miss intent)

Status: OPEN
Date: 2026-10-01
Recorded by: grok (비서실장)
Requested reviewer: Codex / Claude / user later review
Review authority: review-only (no remake without user GO)
Evidence level: repeated (4/4 packs user-rejected as not properly realized)

## Summary

User GO night batch of four MiniMax H3 Ref2VA clips finished `needs_review`, but the user judged that **nothing came out properly**. This dossier freezes (1) original user intent, (2) 비서실장 final prompts, (3) what Contents Creator actually submitted, (4) Soft Soft / settings / outputs — so later review can separate prompt complexity vs adapter/ref remap vs model limits.

## Production identity

| Field | Value |
|---|---|
| batch root | `D:\AI_Studio\library\videos\night-batch-20260930-home-cvstore\` |
| NOTES | `...\NOTES.md` |
| intent prompts | `...\prompts\01..04-*.txt` (비서실장 final) |
| GO time | 2026-09-30 ~23:06 JST via 비서실장 |
| user check | 2026-10-01 ~06:40 JST — user: nothing properly realized |
| requester | grok |
| orchestration | 비서실장 → Contents Creator |
| executor | local-wangp-worker |
| engine | WanGP |
| model | `minimax_h3_ref2va_pruned` (full `minimax_h3_ref2va` weights absent) |
| prompt mode | FG, enhancer off |
| remake | Continuity remake not authorized overnight |

### Packs

| # | Session | Soft Soft | Settings res | Output primary | Alias |
|---|---|---|---|---|---|
| 01 cvstore Suan | `D:\AI_Studio\library\characters\ch-lee-suan\generations\VLOG-20260930-231906-night-batch-01-cvstore-suan` | BATCH-004 gpt-image-09 → `refs\soft-soft-identity.png` (portrait) | 480x832 | ~30.1s **512x768** | `outputs\01-cvstore-suan.mp4` |
| 02 hood Suan | `...\VLOG-20261001-002850-night-batch-02-hood-suan` | same Soft Soft portrait | **832x480** requested | ~30.1s **512x768** (remap) | `outputs\02-hood-suan.mp4` |
| 03 hood Reika | `D:\AI_Studio\library\characters\ch-mizuki-reika\generations\VLOG-20261001-013725-night-batch-03-hood-reika` | face-09-editorial-1 → `refs\soft-soft-identity-832x480.png` | 832x480 | ~30.1s **832x480** OK | `outputs\03-hood-reika.mp4` |
| 04 hood Lia | `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20261001-024543-night-batch-04-hood-lia` | character-default → `refs\soft-soft-identity-832x480.png` | 832x480 | ~30.1s **832x480** OK | `outputs\04-hood-lia.mp4` |

Successful run IDs: 01 `run-20260930-232048-0cbc60be` (prior submit failed sliding_window>481) · 02 `run-20261001-002858-dd38b1f7` · 03 `run-20261001-013733-8314a79a` · 04 `run-20261001-024550-cf751c8c`

## Intent chain (what was asked)

### A. Convenience store

User pasted unmanned CV-store 2AM / 9:16 phone / A+B / prop ledger (kimbap, screen digits 4→6→7, shrimp crackers from tote without pickup, coffee handoff, door knock, milk) / Korean dialogue / staging for model limits.

비서실장 adapted to 이수안 Soft Soft + beige cardigan HARD, Soft goals for digits/reflection, dialogue allowlist, B=hands only → intent file `prompts\01-cvstore-suan.txt`.

### B. Neighborhood MiniDV (three variants)

User pasted 30s HARD-CUT home-video with bag/coins/pastry/peach ledger, then asked sexy variants for Suan / Reika / Lia.

비서실장 finals:
- `02-hood-suan.txt` — red thin-strap crop + white shorts; sexy Beat3 strap slip; hug Beat4
- `03-hood-reika.txt` — cream linen + beige midi; Beat4 shoulder-touch (no hug); sexy Beat6 skirt lift; ending "잘 가~"
- `04-hood-lia.txt` — coral strap crop; plum not peach; sexy Beat1 strap + Beat7 hem

Full text: the four files under `prompts\` (canonical intent).

## What was actually submitted (vs intent)

Diffs: `_dump\*-intent-vs-session.diff.txt`

**Prompt body = intent.** Contents Creator only prepended Soft Soft / aspect lines:

| Pack | Prepend |
|---|---|
| 01 | Picture 1 = Lee Suan IDENTITY Soft Soft; Outfit HARD wins |
| 02 | same Suan Soft Soft preamble |
| 03 | Reika Soft Soft on 832x480 canvas + HARD ASPECT landscape / forbid portrait remap |
| 04 | Lia Soft Soft on 832x480 + HARD ASPECT + HARD PROP plum |

Session copies live next to each VLOG session (`01-cvstore-suan.txt` etc.).

`run.json` stores prompt by path+sha. Artifact metadata shows `prompt_exact_match: false` / `prompt_normalized_match: false` on all packs — flag for later (metadata embedding), not proof wrong file was used; session txt = prepended intent.

## Character and reference contract

| Character | Soft Soft source | Composition | Known conflict |
|---|---|---|---|
| ch-lee-suan (01,02) | BATCH-004 gpt-image-09 | Portrait still | Pack 02 settings 832x480 but output 512x768 |
| ch-mizuki-reika (03) | face-09-editorial-1 composited to 832x480 | Landscape canvas | Landscape out OK |
| ch-lia (04) | character-default composited to 832x480 | Landscape canvas | Landscape out OK |

## Expected acceptance criteria

- 01: 9:16 phone CV store; deadpan Suan; ledger + allowlisted Korean; digits Soft-fallback OK
- 02–04: landscape MiniDV; HARD CUT beat ladder; prop ledger; short sexy gestures; allowlisted dialogue only
- Identity Soft Soft; wardrobe Outfit HARD

## Observed result

| Pack | Observation | Severity |
|---|---|---|
| 01–04 | User: nothing properly realized vs intent | HARD |
| 01 | Output 512x768 vs settings 480x832; first sliding_window fail | Soft/ops |
| 02 | Wanted 832x480 → got 512x768 | HARD (aspect) |
| 03–04 | Aspect OK 832x480; creative still rejected | HARD (content) |
| all | Single FG ~30s, video_length=720, dense multi-beat prompt | Hypothesis driver |

## Direct evidence

- Intent: `D:\AI_Studio\library\videos\night-batch-20260930-home-cvstore\prompts\`
- Sessions/runs/settings/outputs: pack paths above
- Compare: `...\night-batch-20260930-home-cvstore\_dump\compare-summary.json`
- Executor notes: `...\NOTES.md`
- mk scripts: `...\_mk_pack01.py` … `_mk_pack04.py`

## Facts

1. User GO'd all four; Continuity remake forbidden overnight.
2. Intent body preserved; only Soft Soft (and aspect) preambles added.
3. Model was pruned Ref2VA, not full weights.
4. Pack 02 landscape settings ≠ portrait output (Soft Soft portrait remap).
5. Packs 03–04 Soft Soft on 832x480 kept landscape.
6. All four finished needs_review with ~30.1s mp4 on disk.
7. User rejected creative result across the board (not only aspect).
8. Prompt style = dense English ledger + multi-beat HARD CUT + Korean allowlist in one FG shot.

## Hypotheses (not facts)

1. Complexity overload: one 30s FG cannot hold 6–7 beats + ledger + dialogue + sexy → model averages.
2. Wrong packaging: should be multi-pack (one beat/cut per submit) then edit.
3. Soft Soft clothes bleed defeated Outfit HARD despite preamble.
4. Pruned model weaker at multi-shot story / digits / reflections.
5. Aspect remap (01/02) destroyed Suan framing.
6. MiniDV/phone look tokens fight Soft Soft photoreal stills.

## Attempts already made

| Attempt | What changed | Result | Evidence |
|---|---|---|---|
| 1 | Night batch 01–04 as above | User reject | this incident |
| — | Remake | not run (no GO) | NOTES |

## Decision and current hold

- Preserve all outputs + prompts; **no remake** until user reviews this dossier.
- Rerender authority: not granted.
- Must not delete failed mp4s; no silent DNA edits.

## Questions for later review

1. Failure mainly prompt density or adapter/ref (Soft Soft aspect, pruned H3)?
2. Split CV/hood templates into 5–7 short FG packs with Spec ledger?
3. Refuse landscape submit if Soft Soft pixel aspect ≠ target?
4. Smallest experiment: one beat only (e.g. bakery pay) with same Soft Soft?

## Proposed smallest correction (proposal only)

Gate landscape Ref2VA on Soft Soft canvas matching target aspect (as 03/04); split story into per-beat submits; keep dialogue allowlist; defer full ledger until beat packaging works.

## Verification plan

1. Diff intent vs session — done (preamble only).
2. Human watch of four alias mp4s against beat checklist — user.
3. Optional one-beat sample only after GO.

## Resolution

Final status: OPEN
Owner: 비서실장 / user
Checks: prompt compare automated; creative QA pending user
Remaining uncertainty: which failure mode dominated

## Appendix — file index

```
D:\AI_Studio\library\videos\night-batch-20260930-home-cvstore\
  README.md
  NOTES.md
  REVIEW-intent-vs-actual.md
  prompts\01-cvstore-suan.txt
  prompts\02-hood-suan.txt
  prompts\03-hood-reika.txt
  prompts\04-hood-lia.txt
  _dump\compare-summary.json
  _dump\*-intent-vs-session.diff.txt
```

Codex incident copy: `D:\codex\XAI-studio\docs\production-incidents\2026-10-01-night-batch-home-cvstore-prompt-vs-actual.md`
