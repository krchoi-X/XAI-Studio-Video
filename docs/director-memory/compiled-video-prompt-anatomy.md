# Compiled Video Prompt Anatomy — Field Notes from a Strong 30s Vlog Prompt

## Status

Reference analysis for Director Memory / Prompt Compiler design.

This is not a universal prompt template and should not be copied verbatim into every production. The value of the reference is that it appears to encode many previously encountered failure modes into a reusable production structure.

## Why this reference matters

A strong multi-shot prompt of this type is best understood as a **compiled production prompt**, not as a prose prompt written from scratch.

Its structure strongly suggests an iterative history of failures and corrections:

- unintended cuts or timing drift;
- character/wardrobe/hair inconsistency;
- over-performed candid shots;
- arbitrary camera behavior;
- unwanted neon/cyan night grading;
- physically implausible steam/leaves/reflections;
- dialogue appearing in intended silent B-roll;
- generic or unstable motion between shots.

The transferable lesson is not the wording. The transferable lesson is the architecture used to lock fragile decisions.

## Main structural layers observed

The prompt separates production concerns into explicit sections:

- `SCENE CONTEXT`
- `ACTIVE REFERENCES`
- `FORMAT MODE`
- timed shot boundaries / hard cuts
- `OPTICS`
- `CAMERA`
- `ACTION`
- `PERFORMANCE`
- `PHYSICS`
- `LIGHTING`
- `COLOR GRADE`
- `WARDROBE`
- `AUDIO`
- `STYLE`
- `OUTPUT SETTINGS`
- `POSITIVE LOCKS`

This is useful because each section answers a different class of failure.

## Key interpretation

### 1. Shot timing is treated as a contract

Explicit ranges such as `0.0s–4.0s`, `4.0s–8.0s`, etc. are not cosmetic. They constrain the renderer so it does not invent its own pacing or cuts.

**Design implication:** maintain exact shot boundaries upstream in the approved storyboard and compile them into the renderer prompt only when the target engine benefits from explicit timing.

### 2. Optics, camera behavior, and actor action are separated

Do not collapse all motion language into one paragraph.

A shot has at least three different control problems:

- what field of view / compression should look like;
- how the camera behaves;
- what the character or object does.

**Design implication:** keep these as separate fields in shot state, then lower them into engine-specific prose at compile time.

### 3. Positive locks are a reusable continuity layer

The reference ends with explicit global locks such as:

- same person / build;
- same wardrobe and necklace;
- same hair;
- cuts only at approved times;
- selected shots remain dialogue-free;
- approved color family remains intact.

These are effectively a compact **continuity contract**.

**Design implication:** the compiler should have a distinct global lock layer rather than repeatedly embedding the same identity constraints inside every shot.

Suggested fields:

```yaml
positive_locks:
  identity_lock:
  wardrobe_lock:
  hair_lock:
  color_lock:
  cut_rule:
  dialogue_lock:
  awareness_lock:
```

### 4. Global rules and shot-local exceptions are separated

The prompt is globally consistent but allows targeted exceptions:

- only one shot uses half-speed slow motion;
- only selected shots are explicitly candid/unaware;
- different lighting models are allowed per shot;
- individual camera behavior changes by shot.

**Design implication:** preserve strong global continuity but express exceptions locally and return to baseline afterward.

### 5. Failure-prone visual states are described positively

The reference does use some negatives, but most control is expressed as observable desired states:

- warm autumn palette;
- realistic handheld tremor;
- steam rises and dissipates naturally;
- leaves catch briefly in hair/fabric then fall;
- streetlight bands move with correct parallax;
- train sway subtly shifts body weight.

This is consistent with the project's signal-density principle.

**Design implication:** prefer physical state descriptions over long prohibition lists. Use negatives only when a known renderer failure repeatedly survives positive description.

### 6. Candidness is treated as a production state, not a vague style word

The reference does not merely say `candid`.

It specifies:

- the subject is unaware of the camera in selected shots;
- the camera appears delayed in noticing;
- there is no dialogue;
- reactions remain restrained and unperformed.

**Design implication:** `candid` should become a structured field such as `camera_awareness_mode`, with implementation consequences.

Example:

```yaml
camera_awareness_mode: unaware
performance_mode: restrained
spoken_dialogue: false
```

### 7. Physics notes are useful when the scene depends on them

The reference explicitly controls:

- leaf weight/drift;
- steam dissipation;
- streetlight parallax;
- train-induced body sway.

These notes should not be mandatory for every shot.

**Design implication:** add `physics_notes` only when physical behavior is narratively visible or renderer-risky.

## Recommended Shot Contract

The current project should consider the following as an optional richer shot contract for compiled video prompts:

```yaml
shot_id: S01
duration_s: 4.0
shot_function: establish_and_depart
framing: medium_wide
optics: 63_degree_wide
camera_behavior: handheld_phone_height_walk
camera_awareness_mode: briefly_acknowledges_camera
dominant_action: exits building and adjusts bag strap
dialogue_policy: one_short_line
lighting: warm_low_morning_sun
color: warm_autumn
physics_notes:
  - leaves move with light wind
performance_mode: restrained_natural
continuity_anchor:
  - identity
  - burgundy_sweater
  - silver_flower_necklace
renderer_risk: low
```

Do not make every field mandatory in the canonical storyboard. The canonical storyboard should stay lightweight; this richer contract belongs at the production / compiler boundary when needed.

## Proposed Compiler Layers

The prompt should be assembled from five conceptual layers:

```text
1. Approved storyboard / shot contract
2. Global continuity locks
3. Shot-local exceptions
4. Renderer profile
5. Failure-memory injections relevant to this exact scene
            ↓
Compiled production prompt
```

The result may look long, but the user and upstream agents should not manually author it from scratch.

## Failure Memory relationship

A strong production prompt often contains hidden evidence of previous failures. Therefore, when a recurring failure is observed, record the failure itself first rather than immediately expanding the universal prompt.

Example:

```yaml
failure_id: candid_overposing
symptom: subject looks directly at camera and performs despite intended observational shot
likely_scope: candid_broll
mitigation:
  - camera_awareness_mode: unaware
  - spoken_dialogue: false
  - performance_mode: restrained
promotion_rule: only inject when scene intent requires candid observation
```

This prevents prompt bloat and keeps mitigation conditional.

## Important caution

Do **not** turn this reference into one huge mandatory template.

Reasons:

- different renderers have different prompt tolerances;
- short/simple shots do not need every layer;
- smaller local models such as Meromero may lose priority ordering in an oversized prompt;
- some constraints are only relevant after a failure has been observed;
- a compiled prompt should be renderer-specific, while the storyboard remains renderer-neutral.

The desired behavior is **selective compilation**, not template inflation.

## Hermes / Meromero implication

For smaller local models, do not ask the model to recreate this full structure from free-form prose in one pass.

Prefer:

```text
storyboard-cutboard skill
→ structured shot YAML
→ continuity-check skill
→ technique selection if needed
→ renderer profile
→ video-prompt-compiler skill
```

Meromero should fill bounded fields and then compile, rather than reason over a long cinematic handbook each time.

## Practical interpretation for XAI-Studio-Video

The project should distinguish:

- **Director Memory**: durable failures, principles, preferences;
- **Storyboard / Cutboard**: renderer-neutral visual plan;
- **Shot Contract**: production-ready shot state;
- **Renderer Profile**: engine-specific syntax/length/tolerance;
- **Compiled Prompt**: final transient execution artifact.

The compiled prompt is not the source of truth. It is a disposable output that can be regenerated from the approved storyboard plus current renderer knowledge.

## Recommendation

Use this reference as a strong example of how repeated production failures can be transformed into reusable control structure.

Do not copy its exact sections by default. Instead, let the compiler add only the layers needed for the current shot and renderer.

A useful initial schema addition is:

```yaml
shot_contract:
  duration_s:
  optics:
  camera_behavior:
  dominant_action:
  dialogue_policy:
  camera_awareness_mode:
  lighting:
  color:
  physics_notes:
  performance_mode:

positive_locks:
  identity_lock:
  wardrobe_lock:
  hair_lock:
  cut_rule:
  color_lock:
```

## Bottom line

The reference is valuable because it appears to encode **experience-derived constraints**, not because it is long.

The project should reproduce the process that creates such prompts:

```text
production result
→ identify concrete failure
→ record failure memory
→ convert repeated failure into conditional structured rule
→ compiler injects only when relevant
```

That is more scalable than manually writing increasingly large prompts.
