# Measuring a generated image against its reference — runnable procedure

Status: **Procedure. Part A is validated and in routine use; Part B is deliberately incomplete and says so.**
Last updated: 2026-09-16
Audience: any production agent or model on this workstation — Codex, Claude, Hermes, Grok
Method and rationale: `personal-ai-knowledge/wiki/character-identity-pipeline.md`

Two different questions get confused constantly, and they need different instruments:

| Question | Instrument | Part |
|---|---|---|
| "Is this the same person as the reference?" | face-recognition embeddings | **A** |
| "Does this have the nose the operator dislikes?" | geometry, made visible | **B** |

**Embedding similarity cannot answer the second one.** Two images can score 0.95 against each other and one
of them still has the trait the operator rejects. That is not a defect in the recogniser; identity and
preference are different properties.

---

# Part A — quantitative identity similarity

## A1. What runs it

```
interpreter   D:\AI\WanGP\env_uv\Scripts\python.exe        (OpenCV 5, onnxruntime)
models        D:\AI_Studio\models\face\
                face_detection_yunet_2023mar.onnx          detector
                face_recognition_sface_2021dec.onnx        recogniser 1
                arcface_w600k_r50.onnx                     recogniser 2
tool          D:\codex\XAI-studio\tools\identity_score.py
thresholds    D:\codex\XAI-studio\docs\identity-scoring-calibration.json
```

Two recognisers, both reading the **same** SFace-aligned 112×112 crop so their numbers are comparable.
Two independently trained models are used on purpose: when they disagree, that is information, and a single
number from a single model has no way to express doubt.

## A2. Build a prototype from the reference

A prototype is the reference side of the comparison. Give it every image you accept as that character at
the same angle — usually just the chosen portrait.

```bash
D:/AI/WanGP/env_uv/Scripts/python.exe -X utf8 tools/identity_score.py prototype \
  --label noa-21 \
  --out D:/AI_Studio/reports/<character>/prototype-noa-21.json \
  D:/AI_Studio/library/characters/ch-shindo-noa/imports/derived/noa-21-portrait.jpg
```

## A3. Score new images against it

```bash
D:/AI/WanGP/env_uv/Scripts/python.exe -X utf8 tools/identity_score.py score \
  --prototype D:/AI_Studio/reports/<character>/prototype-noa-21.json \
  --thresholds docs/identity-scoring-calibration.json \
  --out D:/AI_Studio/reports/<character>/score.json \
  --sheet D:/AI_Studio/reports/<character>/score.jpg \
  IMAGE [IMAGE ...]
```

Each item in `score.json` carries `scores` (both recognisers), `yaw_proxy`, `yaw_bucket`, `pitch_proxy`,
`face_pixels`, `sharpness` and a `verdict`.

For a video, `tools/video_frame_harvest.py` does extract → detect → bucket → rank → score in one pass.

## A4. Read the result correctly — three rules, all learned the hard way

**Rule 1 — check `face_pixels` before reading the score.**
Below roughly **150 px** the number measures framing, not identity. Measured, monotone:

| face in frame | ArcFace |
|---|---|
| 375 px | 0.83–0.84 |
| 205 px | 0.82–0.84 |
| 106 px | 0.81–0.84 |
| 85 px | 0.60–0.77 |
| 47 px | 0.38–0.53 |

A clip once reported as possible drift at 0.51 had a 47 px face; reframed with nothing else changed it
measured 0.76–0.81. Below the threshold the correct verdict is **"not measurable"**, never "different".
Full-body shots (face ≈ 100 px) can never be judged on identity — judge them on the body.

**Rule 2 — only compare inside the same yaw bucket.**
Buckets: frontal ≤0.12, three-quarter ≤0.45, deep three-quarter ≤0.80, profile >0.80. The *same person in
the same clip* measured **0.07** frontal-against-profile. A profile is compared to a profile prototype or
not at all. `pitch_proxy` is recorded but has no thresholds — the proxy is yaw-confounded — so do not use it
to explain away a low score without checking it against a known-good frame.

**Rule 3 — never use a recogniser's published threshold without calibrating it here.**
OpenCV documents 0.363 as its same-identity line. On this project's material:

| | n | SFace | ArcFace |
|---|---|---|---|
| same character | 20 | 0.831 – 0.976 | 0.838 – 0.964 |
| different character | 165 | 0.042 – **0.551** | −0.019 – **0.533** |

No overlap, and nothing between **0.551 and 0.831**. 0.363 sits *inside* the different-person distribution;
using it accepts strangers.

## A5. How to calibrate for new material

No new labelling is needed — the project already carries the labels implicitly.

1. **Positives:** pairs within one character that the project already accepted as that character.
2. **Negatives:** every cross-character pair.
3. `identity_score.py matrix --out matrix.json IMAGE...` gives the full pairwise cosine table.
4. The usable band is the **gap between the two distributions**. Set the same-person threshold near the
   bottom of the positive range and the different-person ceiling at the top of the negative range.
5. Anything between the two is `drift` — not a pass and not a rejection.

Recalibrate when the material changes (a new engine, a new resolution, real photographs instead of
generated ones). Record the n, the distributions and the method beside the numbers, as
`docs/identity-scoring-calibration.json` does.

## A6. A clip is admitted, not a frame

For turnaround footage, score the **frontal** frames against the frontal prototype and admit or reject the
whole clip on those. The off-axis frames of an admitted clip inherit that admission by temporal continuity —
they are the same person because it is the same continuous take. Scoring them individually would reject
exactly the frames the set exists to collect (Rule 2).

---

# Part B — measuring shape, which similarity cannot see

## B1. Why this exists

The operator rejected a profile set for an **aquiline nose and a jutting chin**. Those images were not
failing identity — the record had simply never forbidden those traits, so the model chose them. No identity
score can surface this: the recogniser is trained to be invariant to exactly the kind of variation that
carries the preference.

So the instrument had to change: **from comparing embeddings to making geometry legible.**

## B2. What was actually built

`D:\AI_Studio\reports\noa\profile-contours.jpg` — for each candidate:

- the **deepest-yaw frame** the candidate produced, found from harvest data;
- the same frame with its **face silhouette edge-detected and overlaid** in high-contrast green;
- **horizontal reference lines** dropped from landmarks at brow/nose-tip and at lip level, so nose
  projection and chin projection are read against a straight line rather than by eye;
- `yaw` and `face_pixels` printed per row, so the reader knows the frames are comparable.

Side by side, the differences between candidates became obvious and the operator could reject on shape in
one pass. **The contour did the work — not a number.**

## B3. What was not built, and should be

**There is no numeric nose or chin classifier.** No such tool was ever committed. Anyone reading a claim
that shape was "measured and filtered automatically" should treat it as false.

The obvious next step, if it is worth the effort:

- sample the silhouette between the nasion and the nose tip, fit a line, and report the **maximum
  perpendicular deviation** in inter-ocular units — positive is convex (a dorsal hump), negative is concave;
- report **chin projection** as the horizontal distance from the lower-lip vertical to the chin point, in
  the same units.

Both are single numbers from a contour that is already being extracted. Calibrate them the same way as
Part A: measure the images the operator has already accepted and already rejected, and use the gap.

## B4. The durable control turned out to be the record, not a filter

The filter that actually stopped the problem recurring was **adding the traits to the character record** —
`face.nose_profile` and `face.chin_profile`, describing the profile line positively, because the guidance-0
edit path used here ignores negative prompts entirely.

Two failures were found on the way and both are fixed:

1. `character_manager.py`'s prompt renderer named six face attributes literally, so a seventh could be
   promoted into the DNA, pass validation and reach **no prompt at all**. That is what happened to these
   two fields until it was checked.
2. `distinctive_marks` reached no prompt either, for any character.

**The lesson generalises: after adding a DNA field, verify it appears in the rendered prompt.** Promotion
succeeding is not evidence that the field is in use.

## B5. Where preference and identity must stay separate

Recorded because it cost time: no measure available correlated with the operator's preference — every
candidate ranked at chance. A forced-choice comparison page was built to gather preference data directly.

**The measurements exist to reject confidently bad frames, not to choose good ones.** Choosing is the
operator's, and a pipeline that hides that behind a score will produce a character they do not want.
