# noa-21 figure reference in swimwear

Character `ch-shindo-noa`, reference `noa-21` portrait plus its face crop, engine
`minimax_h3_ref2va_pruned`, rendered locally. Five clips, 181 frames each. Nothing approved, nothing pushed.

These exist because the five clothed body clips could not answer the operator's own specification: a bust
"fuller and well-shaped for her slender build" and hips that "give a clear hip line" do not read through a
loose tee or a blazer. They are figure references of the costume-fitting kind — plain studio, even light,
the record's own posture, a slow half turn for front, side and back — and the garments are deliberately
plain so that the clothing does not answer the question the shot is asking.

| Shot | Garment | Seed |
|---|---|---|
| `figure-swim-1` | plain black one-piece | 1347119 |
| `figure-swim-2` | plain black one-piece | 1408273 |
| `figure-twopiece` | plain black two-piece, midriff bare | 1469327 |
| `figure-activewear` | plain fitted sports top and shorts | 1530481 |
| `figure-twopiece-b` | as `figure-twopiece`, **same seed**, mole wording changed | 1469327 |

## What they settled

**Hips: the record was right and the clothing was hiding it.** In the clothed clips the silhouette ran
nearly straight from waist to thigh; in swimwear the hip line is clearly present.

**Bust: the record and the render disagree.** The record says "a little larger than average for an East
Asian frame"; what renders is average. The body sentences were reordered for these clips so that bust and
hips come *before* "slender", on the theory that the model acts readily on "slender" and was letting it
override the rest. That made no difference. **Recorded rather than fixed**: the operator's instruction was
to stop iterating and confirm, and everything else in the block delivers. One line changes it if wanted.

Everything else — waist, legs, height, alignment — matches, and matches across two seeds and four garments,
which is what actually matters for a character.

## The mole, and a mistake worth recording

`figure-twopiece` was the first clip this character has ever had with a bare midriff, so it was the first
test of `distinctive_marks` reaching a render at all. It did, in the same place in every frame — which also
confirms the `character_manager.py` renderer fix, since that field reached no prompt at all before
2026-09-12.

It came out **roughly the size of the navel**. On first review this was reported as acceptable; the operator
corrected it, and they were right. The record said "a noticeably large mole", which is an instruction to
make it prominent and the opposite of the intent — the operator had already said, about facial moles, that
image models blow them up. The DNA moved to **v3 (`2c87bc3f17c4`)** with an explicit size bound and a
never-enlarged/never-repeated guard; `figure-twopiece-b` re-renders at the same seed so the wording is the
only variable.

A mirrored frame must never be used where the midriff is bare: the mark sits on one side and a flip moves it.
