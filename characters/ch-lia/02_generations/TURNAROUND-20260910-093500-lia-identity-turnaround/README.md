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

| id | axis under test |
|---|---|
| `turn-01-calibration` | cost calibration and face size. Framed as a mid shot; the face came out ~160 px, too small to use, so every later shot was reframed as a tight close-up and reached ~500 px |
| `turn-02-profile-left` | front through three-quarter towards a profile, turning to her left |
| `turn-03-profile-right` | the same turn to her right, so both profiles exist and can be compared |
| `turn-04-half-turn` | a full half circle, front to the back of the head |
| `turn-05-pitch-down-up` | the other rotation axis: chin down to the floor, then up past level |
| `turn-06-profile-left-seed-b` | `turn-02` again from a different seed. If the two profiles disagree the geometry is being invented per clip rather than read out of the reference |
| `look-07-expression-range` | frontal throughout; expression and gaze only, no rotation |
| `turn-08-structured-profile-left` | `turn-02`'s rotation and seed, written in the structured `subject_definitions` / `retention_analysis` format WanGP ships as this model's own default prompt. Tests the prompt format alone |
| `turn-09-structured-dual-ref` | `turn-08` plus the master face crop as a second reference. Tests the second reference alone |

Engine `minimax_h3_ref2va_pruned` at 576x768, 20 steps, guidance 1.0, flow shift 12, euler. One clip at a
time; the worker holds a GPU lock.

## Measured cost, and a setting that does nothing

25.3 s per denoising step at 20 steps, about 11 minutes per clip including model load and VAE decode. See
`batch-result.json` for the wall-clock time of every shot.

**`video_length` is not honoured literally.** Requesting 61 and requesting 121 both produced 107 frames at
24 fps - a 4.46 second clip - at the same step time, so within that range the number does nothing. Requesting
181 produced 175 frames and took 17 minutes instead of 11, so the setting is not ignored either; it appears to
snap to a small set of lengths this model supports. Plan in clips, not in frames: ask for a long clip only
when the motion genuinely needs one, because the extra length is paid for in wall clock.

The practical consequence is that a rotation has to fit the clip. `turn-04-half-turn` covers 180 degrees in
175 frames and therefore turns roughly twice as fast as the profile shots, which is visible in the harvest:
its faces are smaller and less sharp, but every bucket including the back of the head is populated.

## What happens to the frames

`tools/video_frame_harvest.py` extracts every frame, detects the face, buckets it by the yaw proxy from
`tools/identity_score.py`, ranks within the bucket by identity score and then by focus, and writes the
survivors as stills with `harvest.json`. The pairwise block in that record is the point of the exercise
beyond the images themselves: frames of one continuous clip are the same person by construction, so their
cross-bucket scores are the only same-identity profile measurements available without a human labelling
them — which is exactly what `docs/identity-scoring-calibration.json` lists as missing.
