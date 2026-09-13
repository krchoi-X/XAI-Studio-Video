# noa-21 full body, and the gaze-corrected angle reruns

Character `ch-shindo-noa` at v2 (`161a5aea608b`), reference `noa-21` portrait plus its face crop, engine
`minimax_h3_ref2va_pruned`, rendered locally. Eleven clips, 181 frames each, about 18 minutes apiece.
Nothing here is approved; nothing was pushed.

## Group 1 — `body-*`, five clips

This is the first work to use the `body` block added to the record on 2026-09-12. Every body sentence in the
prompt is that block plus `scene_defaults.posture` rewritten as prose — height, bust, waist, hips, legs,
whole-body skin, and the even two-footed stance with no cocked hip and no crossed legs. Nothing was invented
for the prompt.

| Shot | Framing | Wardrobe | Seed |
|---|---|---|---|
| `body-full-1` | full length | plain fitted sleeveless knit + slim trousers | 224737 |
| `body-full-2` | full length | as above | 302299 |
| `body-knee-up` | head to below the knee | fitted rib-knit dress below the knee | 366421 |
| `body-tee-jeans` | full length | white T-shirt, straight indigo denim | 428399 |
| `body-blazer` | full length | black tailored blazer, slim trousers, ankle boots | 490463 |

`body-full-1` and `-2` are plain and close-fitting on purpose: the question is the silhouette, so the
clothing must not answer it. The other three come from `scene_defaults.wardrobe_direction`. `body-knee-up`
exists because a knee-up frame keeps the face near 200 px while still showing the bust-waist-hip line, which
is the framing most short-form work actually uses.

**These clips are not identity evidence and must not enter the identity set.** At full length the face
measures around 100 px, well under anything either recogniser can read; the Lia work established that and it
has not changed. They are judged by eye, on whether the body is the one the operator described. All midriffs
are covered, so the `distinctive_marks` mole beside the navel is deliberately not in play here.

## Group 2 — `gaze-*`, six clips

One line of the angle recipe changed. The old prompt said:

> The chin stays level and **the gaze follows the direction of the turn**.

which is why the existing set's off-axis frames show the eyes swung sideways and upward. The operator
noticed this while reviewing the 2026-09-13 set. It was an instruction, not a model behaviour. It now reads:

> Her head stays level ... Her gaze stays **straight ahead along the direction her face is pointing**; it
> never follows the turn sideways and never drifts upward.

Three left turns and three right turns, new seeds. The left ones double as further attempts at a natively
generated left profile: this reference reaches the left-profile bucket about once in fourteen clips, and the
only known lever is seed count — see the previous session's README for the evidence that prompt wording,
clip length and reference yaw were each tested and ruled out.

## What to do with the results

1. Look at the five `body-*` clips and decide whether the body is right. If it is not, the fix is a `body`
   edit in `character.json`, not a prompt edit — the prompt is already a faithful rendering of the record.
2. Harvest the six `gaze-*` clips and compare their off-axis frames against the current set's. If the eyes
   are level, rebuild the identity set from the `gaze-*` clips in preference to the older angle clips for
   the off-axis buckets.
3. If any `gaze-L*` clip reaches the left-profile bucket natively, that frame replaces a mirrored member.

---

## Results, 2026-09-13

All eleven clips produced an artifact; none failed or stalled.

### Body — the posture worked, the shape did not

Across thirty sampled frames the stance is correct in every one: upright, weight even on both feet, **no
cocked hip anywhere**, no crossed legs. The `scene_defaults.posture` sentence did its job. Height reads tall,
limbs long, the half-circle turn worked in all five clips so front, side and back silhouettes are covered.

Two attributes came out under the record's own description:

- **Bust.** The record says "fuller and well-shaped for her slender build, a little larger than average for
  an East Asian frame". In the plain sleeveless clips it reads flat. Only the rib-knit dress shows any shape.
- **Hips.** The record says "well-developed hips that balance the bust and give a clear hip line". The
  silhouette runs close to straight from waist to thigh.

The prompt is a faithful rendering of the record, so the fix is in `body`, not in the prompt. The likely
cause is that "a little larger than average" is a comparison the model cannot resolve against any reference,
while "slender" is a word it acts on directly; replacing the comparative phrasing with direct description of
shape is the obvious next attempt. **Not attempted here — this is a canonical DNA change and the operator
has not seen the result yet.**

`body-knee-up` also ignored its framing instruction and came out full length like the other four.

### Gaze — the wording helps, it does not guarantee

Compared against the old clips at **matched yaw** rather than matched time, `gaze-L2` and `gaze-L3` hold a
noticeably more level gaze than `set-L1` and `set-L2` at the same head angle. `gaze-R1` is middling and
`gaze-L1` is no better than the old ones. So the change raises the hit rate rather than fixing the behaviour,
which is the same shape of result as every other lever tried on this reference.

Gaze direction is **not scored anywhere in this project and cannot be**: the detector returns five landmarks
whose eye points are eye *centres*, so there is no inner and outer corner to compute a pupil offset against.
This stays a visual judgement; `D:\AI_Studio\reports\noa\gaze\gaze-matched-yaw.jpg` is the fair comparison.

`gaze-L1` was the only clip of thirty-two rejected by admission (`disagree`, frontal ArcFace down to 0.640),
which agrees with the visual read.

### One thing gained for free

`gaze-L3` reached **−0.95**, a deeper native left profile than `set-L6`'s −0.82 and the second native
left-profile frame this reference has ever produced. The combined set now holds 2 native and 12 mirrored
left-profile frames.

The identity set was rebuilt over 31 admitted clips: **405 frames**, deep_3/4 59/59, frontal 53/48,
three_quarter 61/37, profile 14/74.
