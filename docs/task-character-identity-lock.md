# Scoped Task — Character identity lock (master reference → identity image set)

Owner / Active editor: Claude Code
Status: IN PROGRESS — step 1 (master selection) awaiting the operator's pick
Started: 2026-09-07
First character: **ch-lia** (chosen by the user)

## Goal

Turn a written-DNA character into a **locked visual identity**: one approved master image, then a coherent image set
that reads as the same person across front / three-quarter / side / back, clothed and unclothed, several poses and
hair states. This unblocks the automated video pipeline and the story-driven comic/novel work that follow.

## Diagnosis (2026-09-07)

- Every character record has `approved_references: []`. All 9 characters are text-DNA only.
- Consequently every image so far was generated from words. Text pins a *description*, not a face, so a side view or
  a new pose resamples a different person. This is the root cause of the failed attempts, not prompt wording.
- The existing Lia material contains **at least two different faces** under one DNA hash
  (`bd4d3767…`): the imported portraits (#1–#11, gemini/GPT/venice-chroma) read as a more defined adult face, while
  the generated neutral portraits (#66–#69, #110–#114) read younger and softer. Choosing a master therefore also
  means choosing which face is Lia.

## Lia — concept as stated by the operator (2026-09-07)

- **Origin**: a woman living quietly alone by the sea. This is the true register.
- **Impression**: limpid and unaffected, quietly pure, yet slightly sharp with a slim oval face.
- **"Urban" was a stray**: it came from a possible future idea of putting Lia in a girl group, not from the
  character. It has been removed from the identity prompts; if the girl-group direction is taken later it belongs
  to a scene or era, not to the face.
- **Concept reference**: a Japanese actress. Her name appears in no prompt and no record. The face must not
  resemble her, and `character.json` already requires "a globally neutral original identity with no resemblance to
  a specific real person". Only the quality is described.
- The existing DNA v2 already matches this: "faint quiet unposed natural smile", "fresh translucent pale skin",
  "slim slightly elongated oval face … never a sharp V-line". The written DNA was not the problem.

## The real failure mode: collapse into the beauty prior

Reported symptom (2026-09-07): a face the operator likes appears, then the next image is a generic "AI beauty"
face; changing the angle or the clothes yields a different person, or that same generic face.

That is not seed noise. It is the model falling back to its own attractor whenever the conditioning leaves room.
Written DNA cannot prevent it, because every trait in the DNA — large soft eyes, clear pale skin, slim oval face,
small refined nose — also describes that attractor. `docs/character-face-discovery-workflow.md` already named this
as *separability*: characters that are distinct in text but not visually separated.

What actually reduces the latitude, in order of effect:

1. **Condition on pixels** (already the plan): the reference image plus the identity LoRA.
2. **Change one axis at a time.** Asking for a new angle *and* new light *and* new clothes hands the model reason
   to resynthesise the whole face. The validation batch was rebuilt as single-axis shots for this reason.
3. **Hold the reference harder.** `krea2_turbo_edit` runs at 8 steps and guidance 0 — a distilled fast path where
   negative prompts do nothing. `krea2_raw_edit` (same Identity Edit v1.2 LoRA on the undistilled Krea2 RAW)
   defaults to 20 steps and guidance 2, so the reference is weighted more and negative prompts become effective.
   The RAW checkpoint is not downloaded yet; the turbo one is 13.5 GB, so expect a comparable download.
4. **Give the face something off-prior.** A face made only of prior-compatible traits will always be recoverable
   by the prior. Long-term, Lia needs at least one feature the prior does not produce by default. Her only current
   `distinctive_marks` entry is the wrist bracelets, which do nothing for the face.

A bigger cloud model reduces (3) but does not fix (4), and does not create the missing profile information.

## Measured result: the baseline already drifts (2026-09-07 22:14)

`ax-00-rebuild-same` asked for **no change at all** and still moved the face. Operator's verdict: hard to see as the
same person; explainable partly by lighting or a relaxed expression, but "the eyes softened and became rounder, so
the impression became softer".

That is the decisive measurement. At 8 steps and guidance 0 the turbo edit path cannot hold this face even with
nothing requested, so every later drift in this batch has that baseline underneath it.

**The drift axis is the eye shape.** The DNA calls for "slightly elongated" eyes; the prior pulls toward larger,
rounder eyes. That single feature is where Lia is recoverable by the prior, and it is now named explicitly in the
follow-up prompts. It is also the strongest candidate for the off-prior anchor the character still lacks.

Cost correction: a shot takes ~9 minutes, not ~1. The 13.5 GB checkpoint is reloaded per run and offloads heavily
on 8 GB of VRAM. The seven-shot batch is therefore about an hour.

### Seven-shot single-axis batch — measured (2026-09-07 23:09)

All seven produced an image; every mechanical edit worked (wardrobe, rotation, hair, background). Only identity
failed. Cosine similarity to the master, measured with OpenCV SFace via `tools/face_identity_check.py`:

| shot | cosine vs master |
|---|---|
| 01 wardrobe only | 0.810 |
| 00 no change asked | 0.779 |
| 06 background + light + wardrobe | 0.712 |
| 05 hair only | 0.591 |
| 02 turn 45 | 0.580 |
| 03 profile 90 seed A | 0.455 |
| 04 profile 90 seed B | 0.348 |

Three things this establishes.

1. **There is a floor.** Asking for *no change* still costs about 0.22. The turbo edit path cannot round-trip this
   face, so every other number sits on top of that loss. Raising this ceiling is what RAW and NAG are for.
2. **The prior attractor is now measured, not just described.** The drifted images resemble *each other* more than
   they resemble the master: 02↔03 = 0.703, 02↔05 = 0.684, 03↔04 = 0.784, while each scores 0.455–0.591 against the
   master. Given latitude, the model converges on a common face that is not Lia. That is exactly the operator's
   complaint, quantified.
3. **The profile is not random.** Two seeds of the same profile prompt agree at 0.784 — as close as the no-change
   baseline is to the master. Naming the profile geometry did constrain the invention, so a canonical profile can be
   established this way *if the operator likes the face it proposes*. The competing reading is that both seeds simply
   fell into the same prior profile; the data cannot separate those, only the eye can.

Caveats: SFace is trained on real photographs and degrades on 90-degree profiles, so master-vs-profile scores are
depressed by the measurement as well as by drift; profile-vs-profile is the fair comparison. OpenCV's 0.363
"same identity" line is far too permissive here — every shot but one passes it while the operator's eye rejects
them. Read the ranking and the gaps.

Sheets: `D:\AI_Studio\reports\lia-identity-candidates\compare-single-axis-batch.jpg` (full frames) and
`compare-faces-single-axis.jpg` (faces at matched scale with scores).

### New capability: measurable culling

`tools/face_identity_check.py` (run with the WanGP interpreter, which carries OpenCV 5) builds the face sheet and
scores every image against a reference. Models: YuNet + SFace, 37 MB, in `D:\AI_Studio\models\face`. This is the
tool that makes the LoRA training set practical — the culling step stops being pure eyeballing.

### NAG: negative prompts do work on the distilled path

WanGP applies NAG only when `NAG_scale > 1`, and every settings file this project has ever written left it at 1 —
so no negative prompt has ever had any effect here. The first attempt at `NAG_scale: 3` was rejected in validation
("NAG Scale must be at most 1.5") in 20 seconds without touching the GPU, and the batch stopped rather than
retrying. Corrected to 1.5, which is the cap and still above the activation threshold.

### Prepared, not yet run

`dr-00-rebuild-same` and `dr-02-turn-45` repeat the baseline and the 45-degree turn with **two** references: the full
photograph plus a tight face crop (`imports/derived/lia-master-facecrop.png`), which weights identity harder. The
model accepts up to two reference images. This is the last free lever before a download.

### Next levers, in cost order

1. Dual reference (prepared above) — free, ~18 min.
2. `krea2_raw_edit`: 20 steps, guidance 2, negative prompts effective. The RAW checkpoint is **not** downloaded;
   selecting it triggers an automatic multi-gigabyte download (the turbo one is 13.5 GB), so it needs an explicit go.
3. H3 video turnaround — solves angles, not the beauty-prior pull.
4. Character LoRA on a rented 5090 — the durable fix, and the only one that makes the face a mode of the model
   rather than a description. Requires a training set that is genuinely one person, which is what this work produces.

## Krea 2 LoRA training is feasible — researched 2026-09-07

The operator knows a creator who does exactly what we want: one character, many poses, identity holding. Direct
information from that creator: they trained LoRAs, moved from SD to Krea 2 a few months ago, work mainly in stills
(video only recently), and combine several LoRAs with weights. An earlier guess of mine — that they avoid hard
angles and lean on video — was wrong and is retracted.

What the research establishes:

- **Krea 2 LoRA training is supported**: ostris ai-toolkit and kohya's musubi-tuner both train it, plus wrapper
  projects and published character recipes.
- **Train on RAW, infer on Turbo.** LoRAs trained on Krea 2 Raw transfer strongly to Turbo. This is a lucky fit:
  the RAW checkpoint is being downloaded tonight for better editing, and it is the same file training needs, while
  Turbo stays the fast inference path.
- **VRAM: 18–20 GB at 768 with gradient checkpointing**; 12 GB is possible with musubi-tuner using fp8 and caching.
  **8 GB is out**, so this cannot be trained on this laptop. A 24 GB card suffices at 768; a rented 5090 (32 GB) is
  comfortable. A hosted trainer API also exists as a paid alternative to provisioning a pod.
- **Sampler caveat worth testing on our own drift**: the res_2s sampler family common for Krea 2 aesthetics is
  reported to drift faces; reverting to Euler with the simple scheduler is the first thing to try before blaming
  training. Whether WanGP exposes the sampler for `krea2_turbo_edit` has not been checked.
- **Multi-LoRA weighting** is already available here: the settings this project writes carry `activated_loras` and
  `loras_multipliers`, currently empty. Beyond stacking a character LoRA with style LoRAs at inference, blending
  character LoRAs at fractional weights is a known way to *manufacture* an off-prior face — plausibly how that
  creator obtained a distinctive character rather than a prior-average one.

This makes the target architecture explicit: **the deliverable of this identity work is a training set, and the
durable fix is a Lia LoRA.** Everything else — the edit experiments, the video turnaround — is a means of producing
20–40 images that are unambiguously one person.

## Why the side view keeps failing

A front photograph does not contain the profile. Nose-bridge height and line, chin projection, forehead slope and
the jaw angle seen from the side are absent from the pixels. Any model asked for a side view must invent them, and
each invention is a different skull, which the eye reads instantly as a different person. Prompt wording cannot fix
this; the information is not there. Two consequences:

1. The profile has to be **established once and then reused**, not re-derived per image. The validation batch names
   the profile geometry explicitly and renders it twice with different seeds: if the two disagree, the edit model is
   inventing and this route is closed.
2. The reliable mechanism is the **H3 video turnaround**, which carries one face continuously through the
   intermediate angles instead of re-imagining it at 90 degrees.

## Approach

Identity must come from pixels, not words. Two mechanisms are already installed and measured on this PC:

| Mechanism | Model | Measured cost | Use |
|---|---|---|---|
| Identity edit | `krea2_turbo_edit` + `krea2_identity_edit_v1_2` LoRA, conditioned on `image_refs` | 8.5 s/step × 8 ≈ 70 s per image | hair, wardrobe, expression, framing, moderate angle change |
| Video turnaround | `minimax_h3_ref2va_pruned`, reference image → video | 124 frames ≈ 30 s/step × 20 ≈ 10 min stepping (uncertain; a 243-frame clip measured 128 min total) | true side and back views of the same person, then extract frames with ffmpeg |

The video route is what solves "옆모습이 딴 사람" — temporal consistency enforces one identity across the turn.

## Plan

1. **Master selection (no GPU).** Contact sheets built from existing material; the operator names one number.
   `tools/character_candidate_sheet.py` writes the sheets plus `index.json` mapping number → absolute path.
2. **Register the master** as the character's approved reference (`approved_references` is empty today). Codex owns
   `tools/character_manager.py` promotion rules; if a code change is needed there, hand it over rather than edit.
3. **Identity edit set (~12 images, ~20 min GPU).** Krea2 edit from the master: hair states, wardrobe states,
   body-visible views, expressions, framing, three-quarter angle.
4. **Turnaround clip (1 clip).** H3 Ref2VA from the master with a slow turn; calibrate with a short clip first
   because the 5 s cost estimate is extrapolated. Extract front / ¾ / side / back frames.
5. **Review and lock.** The accepted images become the character reference pack; record it so later video and
   comic work conditions on those pixels.

## Constraints

- One GPU job at a time; Grok is rendering until roughly 22:40 today. No automatic retry beyond approved counts.
- Read-only over existing generations; never relabel or overwrite past records.
- Sessions stay `visibility: restricted`; body-visible material is part of the requested set and the Control Tower
  blurs restricted thumbnails.
- Requester provenance: submit as `--requested-by claude` / `--actor claude` for anything I run.

## Progress

- [x] Diagnosis; mechanisms and costs confirmed from measured timing history.
- [x] `tools/character_candidate_sheet.py` written; Lia sheets built at
      `D:\AI_Studio\reports\lia-identity-candidates\` (118 images, 5 sheets + index.json).
- [ ] Operator picks the master number.
- [ ] Register master, build the edit set, calibrate and shoot the turnaround, review and lock.

## Next

Operator names one candidate number. Then steps 2–5 in order, one GPU job at a time.
