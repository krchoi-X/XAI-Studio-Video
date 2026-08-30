# Design Reference — Asynchronous Image Production, Review, and Ephemeral GPU Workflow

Updated: 2026-08-30

Status: `DESIGN REFERENCE — NOT AN IMPLEMENTATION ORDER`

This note captures the current design thinking for how XAI-Studio may evolve from an image-review tool into an asynchronous creative-production loop. It is intentionally a reference document for future Codex work. It should not override `docs/current-priorities.md` unless priorities are explicitly changed later.

## Why this exists

The immediate product value discovered during image-curation work is not "AI asset management" in the abstract. A relatively small amount of UI improvement can make the actual creative workflow much easier:

```text
generate many images
→ review comfortably on tablet
→ shortlist / hold / reject
→ leave short actionable comments
→ use those decisions to define the next batch
```

The key operational idea is to separate expensive generation time from human judgment time.

```text
night: models / GPU work
day: human reviews and decides
next night: models generate from the updated direction
```

This creates an asynchronous human-AI production loop instead of requiring the user to stay attached to the generation UI.

---

## Long-term product position

XAI-Studio should not be designed around one model, one vendor, or one generation UI.

The preferred abstraction is:

```text
XAI-Studio
   ↓
Generation Job / Session
   ↓
replaceable generation backends
   ↓
normalized results
   ↓
Review / Workbench / Library
```

The studio should preserve creative state, review decisions, lineage, and reusable assets. Renderers should remain replaceable.

Possible backends include:

- WanGP-hosted local/open-weight image models
- ephemeral RunPod or Vast GPU pods
- Codex image-generation capability
- future API or service adapters
- future local image/video engines

Do not make Nano Banana, Grok, Venice, GPT Image, Krea, Z-Image, or any other single provider a structural dependency.

---

## Current practical image providers

### WanGP lane

WanGP is a strong production foundation because it already supports image generation, queues, headless processing, and API-style automation.

Current useful image candidates include:

- Krea 2
- Z-Image
- Qwen Image
- Flux-family models
- future compatible open-weight models

The important design assumption is not that Krea or Z-Image will remain the best models. It is that WanGP or a similar local generation host can expose replaceable models behind a stable job interface.

### Codex lane

Codex can also produce GPT Image outputs through its image-generation capability.

For early experiments, Codex can be treated as another generation backend rather than requiring a custom OpenAI Image API integration.

Important distinction:

```text
Codex can generate images
≠
Codex is already proven as a reliable unattended high-volume batch renderer
```

The exact stable batch size and unattended behavior should be measured empirically.

### Optional external services

Services such as:

- Gemini / Nano Banana
- Grok Image
- Venice / Chroma

may be useful for comparison or special cases.

Do not build brittle browser automation around them merely to increase the provider count. Prefer official automation paths when available. If none exist, treat them as optional/manual comparison tools until a stable integration path appears.

---

## Production architecture direction

For serious content production, the preferred long-term execution model is ephemeral high-end GPU compute.

```text
XAI-Studio
   ↓
Night Batch Manifest
   ↓
RunPod / Vast ephemeral pod
   ↓
WanGP / generation runtime
   ↓
image / video outputs
   ↓
durable local or Drive storage
   ↓
XAI-Studio review
   ↓
pod termination
```

The user should not pay for idle high-end GPU compute.

### Separate compute from durable assets

Recommended structure:

```text
Persistent storage
├─ models
├─ LoRAs
├─ runtime configuration
├─ reusable templates
└─ optional caches

Ephemeral pod
├─ GPU
├─ temporary runtime state
└─ temporary outputs
```

The pod may be destroyed after the work is recovered, while models and reusable state remain on persistent storage when economically sensible.

The final durable outputs should live outside the disposable pod.

---

## Night Batch concept

The first automation layer should remain small.

Do not begin by building a complete Render Broker or automatic multi-cloud scheduler.

Start with one explicit batch/session manifest.

Example:

```yaml
session:
  id: hae-won-cafe-2026-08-30
  title: Jung Hae-won cafe portrait exploration

jobs:
  - backend: wangp
    model: krea
    prompt_ref: prompts/cafe-a.txt
    count: 20

  - backend: wangp
    model: z-image
    prompt_ref: prompts/cafe-a.txt
    count: 20

  - backend: codex
    model: gpt-image
    prompt_ref: prompts/cafe-a.txt
    count: 10
```

A later version may include:

- reference images
- LoRA set and weights
- resolution
- sampler / steps
- seed policy
- adapter-specific settings
- output naming rules
- retry policy
- maximum cost / GPU-hour guardrails

Do not require all of these in the first version.

---

## Session is a first-class object

Session grouping is valuable from the beginning because review usually concerns an experiment, not isolated files.

Minimal session metadata:

```text
session_id
name
created_at
generator/backend
base_prompt or prompt_ref
notes
```

Assets should be linked to the session that created them.

Example:

```text
Session A: beach cafe upper-body
Session B: indoor natural-light full-body
Session C: expression variation
Session D: casual outfit variation
```

This makes next-day evaluation meaningful and enables later statistics such as shortlist rate by session or recipe.

---

## Review-first operating loop

The near-term success condition is not sophisticated orchestration. It is a comfortable review loop.

Recommended flow:

```text
overnight generation
↓
Morning Queue
↓
single-image fast review
↓
SHORTLIST / HOLD / REJECT / FAVORITE
↓
short actionable comment
↓
later comparison / workbench
```

### Morning Queue

Potential landing state inside Studio:

```text
Morning Queue

New overnight results      124
Needs review               124
Hold                        18
Final comparison             6
```

The user should be able to begin reviewing immediately without navigating generation folders.

### Review comments

Comments should be useful as future generation instructions rather than merely subjective reactions.

Good examples:

- face strong, eye reflections still artificial
- composition good, body proportions drift from character
- keep this lighting, retry with simpler hand pose
- strong character identity, candidate for reference reuse
- outfit works, background too polished
- possible LoRA candidate

The objective is to turn review into future production input.

---

## Review → feedback compilation

A later, valuable automation is to compile human review decisions into the next generation direction.

Example:

```text
KEEP
- quiet expression
- natural-light skin texture
- current hairstyle
- current face shape

IMPROVE
- eye reflections
- hand anatomy
- body consistency
- neck/shoulder transition
```

This may eventually become:

```text
review decisions
→ feedback compiler
→ next batch recipe
```

Do not build this before the manual review loop proves useful.

---

## Provider normalization

Different generation backends will expose different metadata.

Do not force fake uniformity.

Use a common envelope with nullable provider-specific fields.

Minimal result record:

```text
asset_id
session_id
backend
model_name
prompt
reference_set
seed_or_equivalent
created_at
output_path
status
raw_metadata
```

Rules:

- missing values stay missing
- never invent a seed/model/prompt value
- preserve raw provider metadata when available
- normalized fields are convenience fields, not a replacement for raw provenance
- image binaries do not belong in SQLite

---

## Suggested backend abstraction

Conceptually:

```text
GenerationBackend
├─ submit(job)
├─ get_status(job_id)
├─ cancel(job_id)
├─ collect_results(job_id)
└─ normalize_metadata(result)
```

Possible implementations:

```text
WanGPBackend
CodexImageBackend
FutureRunPodWorkerBackend
FutureVastWorkerBackend
FutureServiceAdapter
```

This interface is a design direction, not a requirement to create an abstract framework immediately.

Avoid building inheritance-heavy architecture before at least two real backends are working.

---

## Local vs cloud execution

A useful medium-term split:

```text
XAI Job
   │
   ├─ local 4070
   │    └─ cheap / small / low-resolution exploration
   │
   └─ cloud GPU pod
        └─ high-throughput / high-resolution / heavy model production
```

The same logical job/session format should ideally survive the move from local to cloud.

This is more important than perfect provider automation.

---

## RunPod / Vast role

RunPod and Vast should be treated as disposable compute providers rather than creative-system owners.

Preferred lifecycle:

```text
choose provider/GPU
→ attach persistent storage if needed
→ start known runtime
→ submit night batch
→ monitor status
→ copy/register results to durable storage
→ verify recovery
→ terminate pod
→ verify compute billing stopped
```

Start with a manual-but-repeatable lifecycle if needed.

Only automate steps that repeatedly create real friction.

---

## Image curation remains the first product loop

The existing three-surface direction remains valid:

```text
1. REVIEW
2. WORKBENCH
3. LIBRARY
```

### REVIEW

Purpose:
- reduce hundreds of images quickly
- tablet-first
- minimal metadata friction

### WORKBENCH

Purpose:
- understand why shortlisted outputs work
- compare candidates
- inspect prompt/model/settings
- assign roles such as Base Image / Face Master / LoRA Candidate
- manage lineage

### LIBRARY

Purpose:
- preserve only durable, approved assets
- expose assets to video, comic, LoRA, and later project workflows

Do not collapse all three workflows into one dense screen.

---

## XAI-Studio and the future AI Portal

XAI-Studio is expected to become a submenu / production module inside a broader personal AI Portal.

This should not complicate current implementation.

The only useful design requirement now is that Studio can later expose small summary state to a parent dashboard.

Possible landing-page card:

```text
XAI Studio

Overnight Generations   86
Needs Review            64
Shortlisted             14
Master Candidates        3

Latest Session
Jung Hae-won / Cafe Portrait
```

The portal should initially act as a dashboard and deep-link surface, not duplicate Studio functions.

Potential summary fields:

```text
new_count
needs_review_count
shortlist_count
favorite_or_master_count
latest_session_id
latest_session_title
latest_session_created_at
```

A small JSON endpoint or local state file is enough when portal integration becomes relevant.

---

## Repository naming direction

The current repository name is `XAI-Studio-Video`, but its content has already expanded toward:

- image curation
- storyboarding as a medium-neutral IR
- comic / illustration outputs
- future novel-related concepts
- broader creative-production management

The long-term conceptual name `XAI-Studio` is therefore more accurate.

However, repository rename and directory migration should happen only when useful. Do not turn naming cleanup into a blocking reorganization project.

---

## Scope-control rules

This project is vulnerable to over-design because many future ideas are valid.

Use these rules:

1. Build the smallest loop that saves real time.
2. Prefer actual production pain over hypothetical future requirements.
3. Do not add a provider simply because it exists.
4. Do not build browser automation when a stable API/CLI/headless path exists.
5. Do not build a cloud scheduler before one manual cloud workflow is repeatable.
6. Do not build feedback automation before manual review comments are useful.
7. Do not build full lineage visualization before lineage data is actually being recorded.
8. Keep renderers replaceable.
9. Keep originals durable and independent from disposable GPU environments.
10. Promote only repeatedly useful concepts into permanent schema.

---

## Recommended implementation sequence when this direction becomes active

### Phase A — Review loop

1. Index one real image folder read-only.
2. Generate thumbnails.
3. Build tablet-friendly single-image review.
4. Add SHORTLIST / HOLD / REJECT / FAVORITE.
5. Add undo.
6. Store decisions in SQLite.
7. Add session grouping.
8. Validate on a real 50–100 image Jung Hae-won batch.

### Phase B — Local night batch

1. Define a tiny batch/session manifest.
2. Use WanGP to run Krea and Z-Image jobs.
3. Record exact prompt/settings/output path.
4. Auto-register results into the Studio review queue.
5. Measure reliability and failure behavior.
6. Experiment with Codex GPT Image as a third backend.

### Phase C — Cloud ephemeral production

1. Run the same logical manifest on a RunPod pod.
2. Use persistent model/LoRA storage where appropriate.
3. Recover outputs to durable local/Drive storage.
4. Verify pod cleanup and billing stop.
5. Repeat until the lifecycle is boring and predictable.
6. Repeat on Vast only after the RunPod flow is understood.

### Phase D — Feedback loop

1. Add concise actionable review comments.
2. Summarize common keep/improve patterns.
3. Generate the next batch recipe from approved human feedback.
4. Add simple session-level metrics such as shortlist rate.

### Phase E — Portal integration

1. Expose Studio summary status.
2. Add an XAI-Studio card to the AI Portal landing page.
3. Deep-link to Review / Workbench / Library.
4. Do not duplicate Studio functionality inside the portal.

---

## Success criteria

A practical first full-loop success case:

```text
evening:
define 3 image experiments

night:
Krea / Z-Image / optional GPT Image generate automatically

morning:
tablet opens Morning Queue

day:
user reviews 50–100 images comfortably
and leaves a few actionable comments

evening:
next batch is created from the surviving direction
```

If this loop feels effortless, the system is already valuable even before advanced lineage, LoRA automation, portal integration, or full cloud orchestration exists.

---

## Core decision

The preferred long-term direction is:

```text
replaceable generation backends
+
ephemeral high-performance compute
+
durable creative memory
+
tablet-first human review
+
iterative feedback into the next batch
```

The first product to prove is still the review experience.

Do not start by building the final Content OS. Let repeated use of the review and night-batch loop reveal which larger XAI-Studio capabilities deserve to exist.
