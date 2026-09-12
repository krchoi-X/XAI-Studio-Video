# Character record and tooling changes made by Claude Code — 2026-09-10 to 2026-09-12

Written for the Codex storage/repository reorganization, whose **Stage 2** reconciles the character registry
and preserves DNA histories. Everything below happened in `D:\codex\XAI-studio` while that reorganization was
in progress, so Stage 2's inventory will find records whose versions and hashes moved after Phase 0 was
captured. This document is the explanation.

Operator direction on 2026-09-12: canonical DNA edits by Claude Code are authorized ("내 생각도 자주 바뀌는데"),
with the requirement that each change be recorded so Codex can understand it later. Every change below also
carries its reason in `provenance.change_reason` inside the record itself; this file is the index.

Nothing here was pushed. No public export. No `approved_references` was set for any character.

## Why the records changed at all

Two days of measurement established one thing that the DNA documents did not reflect: **a written description
pins a type, not a face.** Text-only generation produced a different person every time, measured — two GPT
profile images from one prompt scored 0.353 against each other's source, and a 30-image set from two engines
split cleanly into two different people by which engine made each image.

The corollary is that a DNA document has to carry the traits a generator will otherwise choose for itself.
Both edits below add exactly those.

## Record changes

| Character | Version | Hash | What changed |
|---|---|---|---|
| `ch-lia` | 2 → 3 | `420c615ac285` | Added `stable_dna.face.nose_profile` and `stable_dna.face.chin_profile` |
| `ch-shindo-noa` | 1 → 2 | `161a5aea608b` | Added `body.bust/waist/pelvis_hips/lower_body/body_hair`, `distinctive_marks`, `scene_defaults.posture`; extended `skin` to the whole body |

Both promoted through `character_manager.py promote --allow-stable-change --reason ...`. Older generation
records still reference the previous hash, which is correct: that is the DNA those renders actually used. No
historical record was rewritten.

### ch-lia v3 — the profile the record never had

Every face attribute in that record described the face from the front. Nothing specified the line of the nose
bridge or how far the chin sits forward, which exist only in profile. The operator rejected the first profile
set as an aquiline nose and a jutting chin — traits the record had never forbidden, so the model was free to
choose them. Wording is positive-first because the guidance-0 edit path this project uses ignores negative
prompts entirely. The frontal `nose` and `jaw` entries are unchanged and still correct; these extend them.

### ch-shindo-noa v2 — the body, and one mark

`ch-shindo-noa` arrived from `krchoi-X/XAI-Studio-Private` (`44f83f0`,
`XAI-Studio-Video/characters/ch-shindo-noa`) and **did not validate against this repository's schema**: it was
missing `distinctive_marks` and five `body` fields, and it carries three fields this schema does not define —
`recognition_anchors`, `flexible_variables`, `forbidden_drift`. The two schemas have diverged; Stage 2 should
decide which is authoritative rather than treating either as damage.

The missing fields were supplied by the operator verbatim on 2026-09-12 and are not invented. `height_impression`
is deliberately unchanged at 171-173 cm: the operator briefly said 165 cm and corrected it as a confusion with
another character, so the record never moved. The distinctive mark is a large mole beside the navel — placed on
the torso rather than the face because the operator had rejected facial moles after seeing image models enlarge
and multiply them.

`reference_defaults.identity` points at the portrait the operator chose from 17 candidates, with its face crop
recorded alongside as the second reference the turnaround recipe uses. It is a runtime default, not an approval.

## Tooling changes — two silent-failure bugs in `character_manager.py`

`character_manager.py` is integration-owned by Codex. Both edits below are scoped, and each was verified by
regenerating every character's `01_prompts/base_appearance.txt` and diffing, so the blast radius is exact.

**1. The prompt renderer named six face attributes literally.** A seventh could be promoted into the DNA, pass
validation, and never reach a single prompt. That is what happened to `ch-lia`'s `nose_profile` and
`chin_profile` until it was checked. It now renders every face attribute in stored order. Verified: of eleven
characters, only `ch-lia` changed, because only `ch-lia` had attributes beyond the six.

**2. `distinctive_marks` reached no prompt at all.** The field that exists to pin identity was inert for every
character. Five carried one and none of them ever appeared in a generated line: Lia's bracelets, Rio's single
earring, Aoi's signature earring, Suan's ribbon, and Noa's mole. Verified: of twelve characters, exactly those
five changed and the other seven are byte-identical.

Both are one-line changes in `render_base_prompt`. If Codex prefers a different mechanism, the DNA fields stand
on their own and only the renderer need change.

## New tools, and why they exist

All under `tools/`, all runnable with the WanGP interpreter, none of them touching the Studio database or the
importer contracts.

| Tool | Purpose |
|---|---|
| `identity_score.py` | Two recognisers, prototype references, yaw bucketing, three-band verdicts |
| `video_frame_harvest.py` | ffmpeg extract, detect, bucket, rank, write stills plus a durable record |
| `turnaround_report.py` | Cross-clip analysis and off-axis threshold derivation |
| `identity_set_builder.py` | Assemble admitted clips into a character identity set with a manifest |
| `reference_set_check.py` | Ask whether a folder of candidate references is one person, before any GPU time |
| `identity_batch.py` | Sequential shot runner with an Ollama unload and a stall guard |
| `pairwise_preference.py` | Local forced-choice page for operator preference data |
| `test_identity_score.py` | 17 unittest cases over the bucketing, verdicts and calibration loader |

`docs/identity-scoring-calibration.json` holds the thresholds and the evidence for them. The short version:
same-character and different-character score distributions do not overlap and nothing lands between 0.551 and
0.831, so OpenCV's documented 0.363 line sits inside the different-person distribution and must not be used on
this material.

## Two environment facts worth carrying into the reorganization

**GPU contention silently ruins timing.** Ollama's resident model costs several gigabytes of an 8 GB card.
`krea2_raw_edit` measured 2.89 min/step with it loaded and 23 s/step with the card clear — 7.5x. A Phase 1
conclusion that RAW costs 60-90 minutes per image, which was one of two stated reasons to rent a GPU, was
purely this. `identity_batch.py` unloads before every shot.

**Heavy CPU work during an offloading render is worse.** On 2026-09-11 concurrent analysis drove free RAM to
1 GiB and one clip's step time went from 29 seconds to 36 minutes. The batch runner now kills a stalled worker
rather than leaving it holding the GPU lock, and treats a blocked status read as a stall.

## What Stage 2 will find, in one list

- `ch-lia` at v3 and `ch-shindo-noa` at v2, both later than Phase 0's capture, both with reasons in provenance.
- `ch-shindo-noa` present in this repository, copied from the private one, with a schema divergence to resolve.
- Five characters whose `base_appearance.txt` changed because `distinctive_marks` now renders.
- `ch-lia` and `ch-shindo-noa` carrying `reference_defaults.identity`; `approved_references` empty everywhere.
- New generation sessions under `characters/ch-lia/02_generations/` and `characters/ch-shindo-noa/02_generations/`,
  and four `IMPORT-20260910-lia-identity-*` sessions that were imported into the Gallery and synced.
- Derived reference material under `D:\AI_Studio\library\characters\<id>\imports\derived\`, including two dated
  identity sets for `ch-lia` and one for `ch-shindo-noa`. The 2026-09-10 Lia set is superseded by the 2026-09-11
  one; only the older set was imported into the Gallery.
- Reports under `D:\AI_Studio\reports\lia-identity-phase2\` and `D:\AI_Studio\reports\noa\`. These hold primary
  harvested frames as well as reports, which is a placement worth reconsidering during the storage transition.
- `D:\AI_Studio\inbox\operator-picks\` — created by Claude Code as a drop folder for operator-supplied images.
  It is not part of any existing convention and should probably be folded into the importer inbox.
