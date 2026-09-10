# Lia identity turnaround — the angles the still engine cannot invent

Reference: resolved automatically from `characters/ch-lia/character.json` →
`reference_defaults.identity` → candidate #4,
`D:\AI_Studio\library\characters\ch-lia\imports\inbox\GPT\ChatGPT Image 2026년 9월 4일 오후 10_31_54.png`
(sha256 `e2df3450…`). No `image_refs` is written in any settings file here; the run record carries the
injected reference and its hash as evidence.

## Why video

Phase 1 measured both Krea2 edit paths against a 45-degree turn and a 90-degree profile. Both invented a
different skull, and RAW was no better than turbo, so the failure is missing information rather than bad
reproduction. A front photograph does not contain the profile. A clip does: temporal consistency carries one
face continuously through the intermediate angles. The clip is therefore not the deliverable — the frames
are, and `tools/video_frame_harvest.py` is what picks them.

## Shots

Each clip changes exactly one thing and pins the rest to the reference, the same single-axis discipline the
Phase 1 still batch used. Every prompt states the framing as head-and-shoulders: at 576x768 a full-body turn
leaves a face roughly 100 px across, which is too small to serve as a reference or as a training image.

| id | frames | axis under test |
|---|---|---|
| `turn-01-calibration` | 61 | cost calibration and face size: front to three-quarter only |
| `turn-02-profile-left` | 121 | front through three-quarter to a full profile, turning to her left |
| `turn-03-profile-right` | 121 | the same turn to her right, so both profiles exist and can be compared |
| `turn-04-half-turn` | 181 | a full half circle, front to the back of the head |
| `look-05-expression-range` | 121 | frontal throughout; expression and gaze only, no rotation |

Engine `minimax_h3_ref2va_pruned` at 576x768, 20 steps, guidance 1.0, flow shift 12, euler. One clip at a
time; the worker holds a GPU lock.

## Measured cost

`turn-01-calibration`, 61 frames: 25.3 s per denoising step, 20 steps. See `batch-result.json` for the
wall-clock time of every shot, which includes model load and VAE decode.

## What happens to the frames

`tools/video_frame_harvest.py` extracts every frame, detects the face, buckets it by the yaw proxy from
`tools/identity_score.py`, ranks within the bucket by identity score and then by focus, and writes the
survivors as stills with `harvest.json`. The pairwise block in that record is the point of the exercise
beyond the images themselves: frames of one continuous clip are the same person by construction, so their
cross-bucket scores are the only same-identity profile measurements available without a human labelling
them — which is exactly what `docs/identity-scoring-calibration.json` lists as missing.
