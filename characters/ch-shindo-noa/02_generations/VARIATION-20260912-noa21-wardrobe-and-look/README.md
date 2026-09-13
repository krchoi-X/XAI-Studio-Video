# noa-21 wardrobe, look, and the left-profile question

Character `ch-shindo-noa`, reference portrait `noa-21` plus its face crop, engine
`minimax_h3_ref2va_pruned`, all clips rendered locally. Nothing here is approved; nothing was pushed.

## What this session contains

| Shots | Purpose |
|---|---|
| `wear-blazer-L/R`, `wear-bomber-L/R`, `wear-hometee-L/R` | three outfits, both turn directions |
| `hair-tiedback-L`, `look-expression` | styling and expression variation |
| `fill-L1/2/3` | intended to fill the left profile — **misnamed, see below** |
| `left-half-1/2/3` | half-circle turn, unmirrored, 181 frames, seeds 517841 / 549193 / 583095 |

## The left profile: what was actually established

Coverage of the combined set was one-sided — 52 right-profile frames against 1 on the left — and three
separate attempts were made to fix it. The record of what each one proved:

1. **`fill-L1/2/3` did not fill the left side.** They were named "L" but carried mirrored settings, which
   produce a right turn. Measured after flip-back: +0.00 to +0.91 on every one of the three. This was my
   naming error, not a model behaviour.
2. **The pre-turned-reference hypothesis was wrong.** The reference portrait's own yaw measures +0.017,
   which is frontal. It is not starting the subject part-way through a turn.
3. **Re-wording the prompt to aim past the profile did not help.** `left-half-*` asked for a full half
   circle "on until the camera sees the back of their head", on the theory from the Lia work that a target
   beyond the profile makes the profile a waypoint. All three turned **right** instead: +0.88 to +0.97.
   The clips are good — they carry the largest frontal faces in the whole set at 406-430 px — but they
   answer the direction question in the negative.

**The direction is not blocked, it is seed-dependent.** `set-L6` reached −0.82, a genuine left profile, and
its shot file is **byte-identical to `set-L1` except for the seed** (331662 against 141421). `set-L1`
stopped at −0.50. Across every unmirrored left-turn clip rendered for noa-21 — 14 of them — exactly one
reached the profile bucket, so the hit rate is roughly 1 in 14 and there is no known lever other than
running more seeds. Other candidate portraits behaved differently: noa-01, noa-09 and noa-12 reached −0.84
to −0.98 readily. This is a property of this particular reference image.

## What was done instead

The left profile was filled by **horizontally flipping the best right-profile frames**, marked as such in
the set manifest. This is safe for this character specifically: `ch-shindo-noa` carries no asymmetric facial
feature, its hair styling is explicitly flexible in the DNA, and its one distinctive mark is on the abdomen
beside the navel, which no head-and-shoulders frame shows. A mirrored frame must never be used for a
midriff-bare shot, where that mark would move to the wrong side.

`consistency_rotation_test.md` in the character documentation already treats left and right as
interchangeable within natural facial asymmetry, so this does not contradict an existing decision.

## Open decision for the operator

If a natively generated left profile is wanted rather than a mirrored one, the only known route is to rerun
`set-L6`'s exact shot with more seeds; at ~1 in 14 that is roughly 8-12 clips for a handful of usable
frames, unattended. Until then the mirrored frames stand and are labelled.
