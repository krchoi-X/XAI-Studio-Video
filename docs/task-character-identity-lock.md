# Scoped Task — Character identity lock (master reference → identity image set)

Owner / Active editor: Claude Code
Status: IN PROGRESS — Phase 1 (measurement) complete and parked since 2026-09-08 03:54.
Phase 2 plan written 2026-09-10; awaiting the operator's decisions listed at the end of this document.
Started: 2026-09-07 · Phase 2 planned: 2026-09-10
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

### Engine comparison on the no-change baseline — measured (2026-09-08 02:25)

Same master, same "change nothing" prompt, three engine settings:

| setting | cosine vs master | wall clock |
|---|---|---|
| Krea2 **RAW**, 20 steps, guidance 2, negative prompt | **0.913** | 59 min |
| Krea2 Turbo, 8 steps, guidance 0 | 0.779 | 9 min |
| Krea2 Turbo + NAG 1.5 + negative prompt | 0.691 | 7 min |

**RAW is the answer to the floor.** Round-trip loss falls from 0.22 to 0.09, and the eye shape the operator cares
about survives visibly — the elongated eyes stay elongated instead of rounding. Sheet:
`D:\AI_Studio
eports\lia-identity-candidates\compare-engine-baseline.jpg`.

**NAG made it worse and is dropped.** Pushing away from "generic idealized AI beauty" also pushed away from the
master, which shares those traits. A far narrower negative might work, but the wide one is counterproductive.

**RAW costs 2.89 min per step, 59 min per image on this laptop.** My earlier 20-minute estimate was wrong: the
undistilled model is heavy and 8 GB forces constant offloading. A twelve-image set would be about twelve hours
locally. This is now a second, independent reason to rent a GPU: on a 32 GB card RAW runs without offloading, so
both the identity set *and* the LoRA training become practical there. The pod is no longer only a training story.

Correction: the batch record first showed `rw-00-rebuild-same` as failed. That was my waiter giving up at 45
minutes, not the run; it completed normally at 58.8 minutes and the record has been fixed.

### RAW does not fix rotation — measured (2026-09-08 03:54)

| shot | engine | cosine vs master |
|---|---|---|
| no change | RAW | 0.913 |
| turn 45 | RAW | 0.542 |
| turn 45 | turbo | 0.580 |

RAW is no better than turbo at a 45-degree turn, and the two turned images land in the same "other person"
territory. This separates two failure modes that were previously confused:

1. **Reconstruction fidelity** — how much identity is lost simply passing through the model. RAW fixes this
   (0.779 → 0.913).
2. **Novel-view synthesis** — inventing a view the reference does not contain. Neither engine fixes this, and a
   bigger model will not either, because the information is absent rather than badly reproduced.

That settles the architecture. The edit route can produce *variation* of the same person (expression, hair,
wardrobe, lighting, framing) but not *angles*. Angles have to come from something that carries one identity
through the intermediate views — the H3 video turnaround — or from a LoRA that has learned the identity.

Note on the bootstrap: a character LoRA does **not** need multi-angle training images to produce multi-angle
output. The base model already knows how faces rotate; the LoRA supplies identity. Angle coverage in the dataset
improves the result but is not a precondition. So the set can be built as: RAW for same-person variation, video
turnaround for whatever angle coverage it yields, then train.

Cost note: this run took 86.8 minutes, against 58.8 for the no-change shot. Budget 60–90 minutes per RAW image
on this laptop.

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

---

# Phase 2 — restart plan (2026-09-10)

Phase 1 measured the problem and then stopped. Nothing has run since `rw-02-turn-45` finished at
2026-09-08 03:54. This section is the plan to restart, written after re-verifying the machine rather than
trusting the notes above.

## State verified on disk today, not remembered

| Claim | Verified state |
|---|---|
| Master chosen | Candidate **#4** = `D:\AI_Studio\library\characters\ch-lia\imports\inbox\GPT\ChatGPT Image 2026년 9월 4일 오후 10_31_54.png` (recorded in the IDENTITY session README) |
| Master registered | **No.** `characters/ch-lia/character.json` still has `approved_references: []`, `status: candidate`, `version: 2` |
| Face crop for dual reference | Exists: `D:\AI_Studio\library\characters\ch-lia\imports\derived\lia-master-facecrop.png` |
| Cheapest unspent lever | `dr-00` / `dr-02` (dual reference) were **written but never run**; so was `rw-03-profile-90`. 11 runs exist: 7 `ax-*`, 2 `ng-00`, `rw-00`, `rw-02` |
| Krea2 RAW checkpoint | **Downloaded** — `D:\AI\WanGP\ckpts\Krea2Raw_quanto_bf16_int8.safetensors`. The "not downloaded yet" note above is stale |
| Identity Edit LoRA | `D:\AI\WanGP\loras\krea2\krea2_identity_edit_v1_2.safetensors`, 1.83 GB |
| H3 video engine | `MiniMax-H3-Ref2VA-pruned_rank8_int8_convrot.safetensors` present; `minimax_h3_ref2va_pruned` is a valid `model_type` |
| Scoring stack | OpenCV **5.0.0** with `FaceRecognizerSF` in the WanGP interpreter; YuNet + SFace ONNX in `D:\AI_Studio\models\face` |

Since Phase 1 the repository also gained a mechanism this plan depends on: `character.json.reference_defaults.identity`,
resolved automatically for `*_ref2va*` submissions by `tools/local_wangp.py` (commit `8dab741`). Jun already has one.
Lia does not. That record — not `approved_references` — is what makes a locked master actually reach the GPU.

## What Phase 1 settled, and what it left open

Settled, and not worth re-measuring:

- Identity has to come from pixels. Written DNA does not pin a face.
- `krea2_turbo_edit` loses ~0.22 cosine just passing the face through with nothing requested. `krea2_raw_edit`
  cuts that to ~0.09. RAW is the fidelity path.
- **Neither engine can rotate a face.** 45° lands at 0.54–0.58 on both. That is missing information, not bad
  reproduction, so a bigger model does not fix it.
- NAG at 1.5 with a wide negative prompt made identity *worse*. Dropped.
- RAW costs 60–90 min per image on this 8 GB laptop. A 12-image RAW set is a 12-hour night.

Left open, and the reason this is a new phase rather than a resume:

1. **The similarity number is not yet trustworthy enough to automate on.** One recogniser, one reference image,
   one threshold that the operator's eye already contradicted. It ranked well; it cannot yet decide.
2. **The video route was never run.** It is the only proposed answer to rotation and it has zero measurements.
3. **There is no tool between a video file and a scored candidate frame.** Frames were pulled by hand once
   (`VIDEO-20260905-lia-icecream-hi-pilot/frame-00*.png`); nothing in `tools/` does it.

## Design change 1 — make the similarity score decidable, not just rankable

The score's job changes in Phase 2. In Phase 1 it explained a failure to a human. In Phase 2 it has to cull
hundreds of video frames without a human looking at each one. Four fixes, in this order:

**1a. Calibrate the threshold on our own faces (no GPU, ~30 min of operator time).**
Take the images already produced — the 11 identity-lock outputs, the Lia candidate pool, and a handful of images
of *other* characters — and have the operator label pairs "same person" / "different person". Compute the score
distribution for each label and pick the operating point from our data. OpenCV's 0.363 line is calibrated on real
photographs of real people; on synthetic faces from one prior it passes almost everything. The output is a single
number recorded in this document, plus the evidence for it. Without this step every later automated cull is
guessing.

**1b. Score against a centroid, not a single image.**
One master embedding carries that image's lighting and expression. Once 3–5 images are accepted as Lia, average
their embeddings into an identity prototype and score against that. Cheap, and it is what makes the set converge
instead of orbiting one photograph.

**1c. Bucket by yaw before comparing.**
Phase 1 already noticed that master-vs-profile scores are depressed by the *measurement*, and that
profile-vs-profile is the fair comparison — but nothing implements it. YuNet returns five landmarks; the
eye/nose offsets give a coarse yaw estimate, enough to bucket frames into frontal / three-quarter / profile /
back-of-head. Each bucket then gets its own threshold from step 1a. Comparing a 90° frame to a frontal master
and calling 0.45 a failure is a measurement error, and this is where the video route would be wrongly discarded.

**1d. Add a second, independent recogniser — without touching the render environment.**
SFace agreeing with itself is not corroboration. The WanGP interpreter already carries `onnxruntime 1.25`, and
SFace's `alignCrop` produces an aligned 112×112 crop of the kind ArcFace expects, so a single ArcFace ONNX weight
file (`glintr100` / `w600k_r50`, ~90–260 MB) can be run directly through `onnxruntime` with **no pip install**
into the render venv. `insightface` is not installed and should not be installed there. Two recognisers that
agree is strong evidence; where they disagree the frame goes to the operator instead of being auto-culled.
Verify the crop geometry against the ArcFace preprocessing before trusting the first numbers.

Optional, only if hair and silhouette start drifting while faces hold: `open_clip 3.3.0` is already present in
that interpreter and gives a whole-image similarity axis that a face recogniser is blind to. Deferred — it needs
a weights download and it is not the current failure.

**1e. Persist the scores.** `tools/face_identity_check.py` prints JSON to stdout and writes a JPG. Phase 2 needs
a scored record written next to the session so a later agent can reconstruct why a frame was accepted, per the
handoff protocol. Same tool, one added output path.

## Design change 2 — the video route is a *harvest*, not a clip

The insight from Phase 1 is that temporal consistency carries one identity through angles the still model has to
invent. The consequence, which Phase 1 did not draw, is that the video's value is the **frames**, and the
frame-selection step is the actual product.

Sequence: calibration clip → turnaround clip → automated harvest → operator review → RAW re-render of the
survivors.

- **Calibrate before committing.** The cost notes conflict badly: 124 frames estimated at ~10 min, a 243-frame
  clip measured at 128 min. Shoot one short clip (~61 frames, 576×768, the existing pilot settings) purely to get
  a real seconds-per-frame number on this GPU before scheduling anything longer.
- **Frame the turn for the face, not the body.** H3 output is 576×768. In a full-body turn the head is perhaps
  100 px, which is too small to be a training image or a reference. Shoot the turnaround as head-and-shoulders so
  the face fills the frame; a separate full-body clip can come later if the wardrobe/silhouette set needs it.
- **One axis in the clip too.** Slow continuous rotation, locked camera, fixed neutral light, neutral expression,
  no wardrobe change, no cut. Every extra instruction is latitude, and latitude is where the prior gets in.
- **Harvest, then re-render.** Extracted frames give *geometry* — the profile that no front photograph contains —
  at video quality. Feed the accepted profile frame back into `krea2_raw_edit` as the reference to get it at still
  quality. That is the combination Phase 1 implied but never stated: **video supplies the angle, RAW supplies the
  texture.** It also caps RAW usage at a handful of canonical anchors instead of a whole set.

New tool required: `tools/video_frame_harvest.py` — ffmpeg extract → YuNet detect → yaw bucket → sharpness rank
within bucket → score against the identity prototype → contact sheet + JSON record. This is the single largest
piece of new code in Phase 2 and everything downstream waits on it.

## Design change 3 — sequence by measured cost, not by ambition

At 60–90 min per RAW image the plan has to spend that budget deliberately:

| Purpose | Engine | Budget |
|---|---|---|
| Canonical anchors (front, ¾, profile, back) | `krea2_raw_edit` from master or from a harvested frame | ~4 images, one overnight |
| Variation (hair, wardrobe, expression, framing) | `krea2_turbo_edit` at ~9 min | cheap, run after anchors hold |
| Angle coverage | H3 Ref2VA harvest | 1 calibration + 1–2 turnarounds |
| Durable fix | Lia LoRA, ≥24 GB card | out of scope here; this phase produces its training set |

The deliverable of Phase 2 is unchanged from Phase 1's conclusion: **20–40 images that are unambiguously one
person**, plus the calibrated measurement that proves it. The LoRA is a separate, rented-GPU task.

## Step plan with gates

Each step names the gate that must pass before the next one runs. A failed gate stops the phase rather than
triggering a retry.

| # | Step | GPU | Gate to continue |
|---|---|---|---|
| 0 | Register master #4 as Lia's `reference_defaults.identity` (path + sha256 + provenance). Leave `approved_references` alone — that needs the operator's explicit approval workflow | none | `tools/local_wangp.py` resolves it for a Ref2VA submission without an explicit `image_refs` |
| 1 | Threshold calibration (1a) + centroid + yaw bucketing (1b, 1c) + second recogniser (1d) + persisted record (1e) | none | Operator-labelled pairs separate cleanly at a stated threshold, per yaw bucket. If they do not separate, the score cannot automate the cull and the video harvest reverts to manual review |
| 2 | Run the two prepared dual-reference shots `dr-00` / `dr-02` | ~18 min turbo | Does the face crop as a second reference beat 0.779 / 0.580? Free information, already written |
| 3 | H3 calibration clip, ~61 frames, head-and-shoulders, slow turn | ~10–40 min, unknown | A real seconds-per-frame number, and a face large and clean enough to detect |
| 4 | Build `tools/video_frame_harvest.py` against the calibration clip | none | Bucketed, scored, sharpness-ranked frames plus a contact sheet from an existing file |
| 5 | Full turnaround clip; harvest; operator picks the canonical ¾ / profile / back | 1 clip | The operator accepts that this is Lia at those angles. If not, the video route is closed and the fallback is choosing one invented profile and making it canon |
| 6 | RAW re-render of the accepted angles at still quality | 60–90 min each, overnight | Cosine against the prototype at or above the calibrated line, and the operator's eye agrees |
| 7 | Turbo variation set from the anchors; score-cull; assemble the 20–40 image training set | ~9 min each | Set is one person under the calibrated measure |

Steps 0, 1 and 4 need no GPU at all and are the bulk of the remaining engineering. They can proceed while the
GPU is busy with Hermes work.

## Readiness on this PC — checked 2026-09-10

### Ready

| Item | State |
|---|---|
| GPU | RTX 4070 Laptop, 8188 MiB, driver active |
| Disk | D: 1.4 TB free — no download pressure |
| Krea2 Turbo + RAW checkpoints | Both present; RAW no longer needs a download |
| Krea2 Identity Edit v1.2 LoRA | Present |
| MiniMax H3 Ref2VA pruned | Present; validated `model_type` |
| Face detector + recogniser | YuNet + SFace present; OpenCV 5.0.0 with `FaceRecognizerSF` confirmed in `D:\AI\WanGP\env_uv\Scripts\python.exe` |
| ffmpeg | Two independent copies: on PATH (8.1.1) and `D:\AI\WanGP\ffmpeg_bins\ffmpeg.exe` |
| Submission path | `tools/local_wangp.py submit` with a GPU lock — a second worker is refused, not queued behind a crash |
| Reference default resolution | Shipped and tested; Jun's record is the working example |
| Contact sheets | `tools/character_candidate_sheet.py`; Lia's 118-image index already built |
| Services | Control Tower on `:8790` (also on the tailnet), Studio on `:8787`, both listening |
| Precedent run | Hermes's Jun Ref2VA run at 2026-09-10 08:26 reached `needs_review`, so the whole submit path works today |

### Gaps that must be closed before the plan can run

| Gap | Why it blocks | Effort |
|---|---|---|
| **Ollama holds VRAM on the same 8 GB card** | `meromero26b-a4b-hermes` was resident at ~3.7 GB of VRAM during this check (~6.1 GB of the card in use). A RAW job on 8 GB already offloads constantly; sharing the card with a 25B LLM will slow it badly or fail it. Needs an explicit unload (`keep_alive: 0` or stopping the model) before any GPU batch, and a check in the batch runner | small, but must be done every time |
| **No frame-harvest tool** | Step 4; the whole video route depends on it | ~half a day |
| **Score is uncalibrated** | Step 1; without it nothing can be auto-culled | operator labelling + ~half a day |
| **Only one recogniser** | Needs one ArcFace ONNX weight file downloaded to `D:\AI_Studio\models\face`; no pip install | small download |
| **Lia has no `reference_defaults.identity`** | Ref2VA submissions for Lia will fail exactly the way Jun's did on 2026-09-10 07:37 ("You must provide at least one Reference Image") | minutes |
| **`approved_references` still empty for every character** | Not blocking Phase 2 — the runtime default is enough — but the canonical approval remains a separate, explicit operator decision and should not be silently skipped forever | operator decision |
| **No batch runner in `tools/`** | Phase 1's `batch.log` / `batch-result.json` came from an ad-hoc script that is not in the repository. Re-running Phase 1's method today means rewriting it. Worth committing this time | small |
| **Hermes night batches share the GPU** | Hermes ran Jun jobs at 18:18, 23:00 and 08:26, and one of them already failed on the GPU lock. Any overnight RAW work needs an agreed window, not an assumption | coordination |

### Not needed, contrary to earlier notes

- No model download. RAW is on disk.
- No `insightface` install. ArcFace runs on the `onnxruntime` already in the render venv.
- No new venv. `D:\AI\WanGP\env_uv\Scripts\python.exe` carries OpenCV 5, torch 2.10, onnxruntime and open_clip.
- No rented GPU for Phase 2. The pod is for LoRA training, which is Phase 3.

## Open decisions for the operator

1. **Which character.** This entire record is Lia's. Jun and Rio now have five OpenAI close-ups each and Jun has a
   working reference default, so they are arguably better starting material — but none of Phase 1's measurements
   apply to them. Continuing with Lia reuses the evidence; switching restarts it.
2. **The off-prior anchor.** Phase 1's conclusion was that a face built only from prior-compatible traits will
   always be recoverable by the prior, and that the eye shape is where Lia keeps collapsing. Deciding what makes
   this face *not* the default beautiful face is an authorship decision, and it is cheaper to make before spending
   twelve GPU-hours than after.
3. **How much manual labelling.** Step 1 needs the operator to judge same/different on a set of existing pairs.
   Fewer pairs means a weaker threshold and more frames escaping to manual review later.
4. **GPU window.** Which nights are Lia's and which are Hermes's.

## Next

No GPU work starts until decisions 1 and 4 are answered. Steps 0, 1 and 4 are the no-GPU engineering and can begin
as soon as the character is chosen.

---

# Phase 2 execution log — 2026-09-10

Operator decisions, given 2026-09-10 morning: **continue with Lia**; Ollama and Hermes may be killed; build or
install whatever the frame harvest needs; then produce varied views of the master image by video or any other
means and score them. A follow-up during execution: **repeat the rotation in several different directions and
analyse it**, and keep a good record of everything.

Active editor: Claude Code. Scope: ch-lia identity set. No push, no publication, no media deletion, no
canonical DNA edit, no reference approval.

## Environment changes made

| Change | Detail |
|---|---|
| GPU freed | `meromero26b-a4b-hermes` was holding ~3.7 GB of the 8 GB card. Unloaded through Ollama's own `keep_alive: 0`; the card went to 0 MiB. The Hermes desktop app was left running - it was the resident model that mattered, and killing the operator's app was not needed once VRAM was free. `tools/identity_batch.py` now unloads Ollama before every shot, so this cannot silently come back. |
| ArcFace weights | `D:\AI_Studio\models\face\arcface_w600k_r50.onnx`, 174 MB, from the `immich-app/buffalo_l` mirror of the InsightFace model. Weights only - no `insightface` package was installed into the render environment, and none is needed: the file runs on the `onnxruntime 1.25` already in `D:\AI\WanGP\env_uv`. |

Confirmed rather than assumed: SFace's `alignCrop` returns exactly the 112x112 crop ArcFace expects, so both
recognisers read the same pixels.

## New tools

| Tool | What it does |
|---|---|
| `tools/identity_score.py` | Two recognisers, prototype references, yaw bucketing, three-band verdicts, durable JSON. Successor to `face_identity_check.py`, which stays as the single-recogniser sheet builder. |
| `tools/video_frame_harvest.py` | ffmpeg extract, detect, bucket by yaw, rank by identity then focus, write the survivors as stills plus `harvest.json` including the within-clip pairwise block. |
| `tools/identity_batch.py` | Sequential shot runner with the Ollama unload and a durable `batch-result.json`. Phase 1's batch script was never committed; this is that gap closed. |
| `tools/test_identity_score.py` | 15 unittest cases over the bucketing, the verdict bands and the calibration loader. All pass. |

## Step 0 — the master is now resolvable

`characters/ch-lia/character.json` gained `reference_defaults.identity` pointing at candidate #4 with its
sha256. `approved_references` is untouched and still empty: that needs the operator's explicit approval
workflow, and a runtime default is not an approval. Verified end to end - the first turnaround run carries
`"basis": "character-default"` and the matching hash in its run record, with no `image_refs` written in any
settings file.

## Step 1 — the score is now calibrated, and it contradicts the borrowed threshold

No operator labelling was available, so the labels came from the repository: the positive set is within-character
pairs among the ch-jun and ch-rio close-up sets, where portraits 02-05 were generated from portrait 01 as the
reference and accepted as that character; the negative set is every cross-character pair. 24 images, 276 pairs,
both recognisers. Full record: `docs/identity-scoring-calibration.json`.

| | n | SFace min / median / max | ArcFace min / median / max |
|---|---|---|---|
| same character | 20 | 0.831 / 0.881 / 0.976 | 0.838 / 0.902 / 0.964 |
| different character | 165 | 0.042 / 0.244 / 0.551 | -0.019 / 0.154 / 0.533 |

**The distributions do not overlap and nothing at all lands between 0.551 and 0.831.** That empty gap is the
finding. OpenCV's documented 0.363 same-identity line for SFace sits *inside* the negative distribution here, so
Phase 1 was right to distrust it and can now say why. Scoring is therefore three bands, not a pass/fail line:

* **same** - at or above the positive floor;
* **drift** - inside the gap: not another person, not this person either. This is the beauty-prior collapse the
  operator has been describing, and it now has a numeric address;
* **different** - at or below the negative ceiling.

Thresholds are per yaw bucket. `frontal` and `three_quarter` are calibrated at 0.83 / 0.84. `deep_three_quarter`
and `profile` are deliberately left uncalibrated: no same-identity pair at that yaw exists yet, and a recogniser
trained on real photographs loses accuracy off-axis, so applying the frontal line there would reject correct
frames. The tools report `uncalibrated` rather than guess.

### Yaw bucketing works, and it corrects two Phase 1 readings

The proxy is the nose tip's displacement from the eye midpoint along the eye axis, in inter-ocular units. On the
Phase 1 batch, whose shots carry a known requested angle, it separates cleanly: the five no-change and
wardrobe shots land at 0.007-0.095, the requested 45-degree turns at 0.39-0.70, the two requested 90-degree
profiles at 0.74 and 1.08.

Two corrections fall straight out of it:

1. **`ax-05-hair-ponytail-only` was not a hair-only shot.** Its yaw proxy is -0.401, the same as the requested
   45-degree turn. Phase 1 charged its 0.591 to the hair axis; most of that loss was rotation.
2. **`rw-02-turn-45` and `ax-02-turn-45-only` were not the same angle.** RAW turned to -0.701 where turbo turned
   to -0.391. Phase 1 compared their scores directly and concluded "RAW is no better than turbo at a 45-degree
   turn". The two shots are not comparable; RAW was asked for the same thing and did roughly twice the rotation.
   The conclusion that *neither* engine can invent a novel view still stands - it just does not rest on that
   comparison any more.

### Phase 1 re-scored against the prototype

The prototype is the mean of two embeddings: master #4 and `rw-00-rebuild-same`, the only Krea2 output that
measures as the same person. Both are prototype members, so their own 0.975/0.980 is self-reference, not
evidence. Sheet: `D:\AI_Studio\reports\lia-identity-phase2\phase1-rescored.jpg`.

| shot | bucket | SFace | ArcFace | verdict |
|---|---|---|---|---|
| `ax-01-wardrobe-only` | frontal | 0.885 | 0.849 | **same** |
| `ax-00-rebuild-same` (turbo, no change) | frontal | 0.785 | 0.687 | drift |
| `ng-00-rebuild-same` (turbo + NAG) | frontal | 0.738 | 0.563 | drift |
| `ax-06-neutral-studio` | frontal | 0.706 | 0.668 | drift |
| `rw-02-turn-45` | deep_three_quarter | 0.630 | 0.616 | uncalibrated |
| `ax-02-turn-45-only` | three_quarter | 0.568 | 0.586 | drift |
| `ax-05-hair-ponytail-only` | three_quarter | 0.561 | 0.630 | drift |
| `ax-03-profile-90-a` | deep_three_quarter | 0.506 | 0.456 | uncalibrated |
| `ax-04-profile-90-b` | profile | 0.388 | 0.498 | uncalibrated |

Exactly one Krea2 edit besides the RAW baseline holds the identity, and it is the wardrobe change - the one axis
that never asks the model to re-synthesise the face.

### The "Lia import family" is not one person

Phase 1 read imports #1-#11 as one more-defined adult face. Measured, they are not:

| pair | SFace | ArcFace | |
|---|---|---|---|
| #2 (08_19_10) x #4 (10_31_54) | 0.767 | 0.794 | drift - close, but below the same-person floor |
| #4 x gemini | 0.403 | 0.298 | different person |
| #2 x gemini | 0.303 | 0.264 | different person |
| 08_20_39 x #4 | 0.490 | 0.433 | different person |

The operator named #2 and #4 together as close to what they imagined, which is a statement about the impression,
not about the face. Only #4 is Lia for measurement purposes, and the prototype is built from it alone plus the
one image that measures as it.
