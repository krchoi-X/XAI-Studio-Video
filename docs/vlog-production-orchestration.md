# Vlog Production Orchestration

Updated: 2026-09-06

## Purpose

This document captures a practical production direction for recurring-character AI vlogs using H3-class reference generation through WanGP or equivalent runtimes.

The objective is not to force every vlog into a fixed shot length or one giant character sheet. The system should:

1. preserve stable character identity and voice;
2. represent daily appearance as replaceable Look Packs;
3. let a story/director agent choose shot boundaries based on continuity vs retry cost;
4. compile only the references required for each shot;
5. send renderer-ready jobs to WanGP/H3;
6. regenerate only the smallest failed unit when possible.

> **Agent note — Codex / Claude Code / Hermes**
>
> Treat this as a production-design reference. `docs/current-priorities.md` still controls implementation priority. Do not turn this into a large new subsystem before real vlog experiments reveal which parts are actually necessary.

---

## 1. Character identity is broader than face identity

For a recurring vlog character, the long-lived identity layer should include more than appearance.

```text
CHARACTER DNA
├─ Face Identity
├─ Body Identity
├─ Hair Rules
├─ Acting DNA
├─ Voice DNA
└─ Stable accessories / identity markers
```

### Voice DNA

Voice is part of character identity, not merely post-production.

A practical Voice DNA model may include:

```text
Core Voice Identity
├─ perceived age
├─ pitch range
├─ timbre
├─ resonance
├─ breathiness
├─ brightness
└─ roughness

Prosody Profile
├─ speaking rate
├─ sentence-ending tendency
├─ pause frequency / length
├─ pitch variation
└─ emphasis style

Speech Habit Profile
├─ filler words
├─ sentence length
├─ diction style
├─ laughter style
└─ habitual breathing / hesitation

Emotional Range
├─ restrained vs expressive
├─ surprise
├─ laughter
├─ sadness
├─ anger
└─ embarrassment
```

Recommended canonical voice assets:

```text
VOICE_MASTER_NEUTRAL
VOICE_MASTER_CONVERSATION
optional: VOICE_ALT_LAUGH
optional: VOICE_ALT_SOFT_SAD
```

Do not assume every scene needs every voice sample. The same canonical-reference rule used for images applies to audio references.

---

## 2. Acting DNA and expression primitives

Expression references should not be confused with identity references.

Use a shared **Expression / Acting Primitive Library** for reusable performance patterns, and let each character define preferred intensity/range.

Example global primitives:

```text
suppressed_laughter
quiet_deadpan
sleepy_to_alert
small_surprise
embarrassed_smile
delayed_realization
```

Each primitive should be temporal rather than a static emotion label.

Recommended grammar:

```text
initial
→ onset
→ development
→ reaction / peak
→ settle
```

Example:

```text
suppressed_laughter
neutral
→ lips press together
→ cheeks rise
→ eyes narrow slightly
→ mouth corners struggle not to lift
→ one small involuntary breath break
→ brief release
→ settle
```

Where useful, describe performance across multiple channels:

```text
face
gaze
head
hands
posture
breathing
voice
timing
```

A character-specific Acting DNA should define how strongly that character uses these primitives rather than duplicating a complete expression sheet for every character.

---

## 3. Identity Master + Look Pack + Scene Packet

Do not create one giant all-purpose character sheet containing every outfit, hairstyle, prop, mood, and expression.

Use three levels.

### 3.1 Identity Master

Mostly stable across the series:

```text
FACE_MASTER
BODY_MASTER_FRONT
BODY_MASTER_BACK
VOICE_MASTER
ACTING_PROFILE
```

The visual identity master should remain neutral and objective where possible.

### 3.2 Look Pack

Represents a character's appearance state for one part of a day, episode, or activity.

Examples:

```text
LOOK_HOME
LOOK_SLEEP
LOOK_POOL
LOOK_WORK_UNIFORM
LOOK_BEACH_WALK
```

A Look Pack can include:

```yaml
wardrobe: work_uniform
hair_state: tied_clean
footwear: sneakers
accessories:
  - canonical_bracelets
```

Hair should be modeled as state, not necessarily identity drift.

Example hair states:

```text
HAIR_HOME_DOWN
HAIR_POOL_WET_BUN
HAIR_WORK_TIED
HAIR_SLEEP_MESSY
```

### 3.3 Scene Packet

The actual renderer-facing combination for one shot.

Example:

```text
Scene: pool morning
├─ FACE_MASTER
├─ BODY_MASTER
├─ LOOK_POOL
├─ HAIR_POOL_WET_BUN
├─ POOL_ENV_MASTER
├─ optional prop references
├─ optional VOICE_MASTER
└─ shot prompt / motion plan
```

The same identity stays fixed while Look Packs and scene context change.

---

## 4. Wardrobe changes should usually create a new scene packet

A recurring vlog often changes appearance several times in one day.

Example:

```text
wake up
→ pool
→ change clothes
→ work
→ after-work walk
```

Do not automatically send both the pool outfit and work uniform to every generation.

Preferred rule:

```text
pool shot
→ LOOK_POOL only

work shot
→ LOOK_WORK_UNIFORM only
```

Use multiple Look references together only when the transformation itself matters inside the shot or transition.

This reduces ambiguity and makes failure diagnosis easier.

---

## 5. Shot length is a strategy decision, not a fixed constant

There is a real trade-off:

### Short independent shots

Advantages:

- faster generation;
- smaller retry unit;
- easier failure isolation;
- simpler wardrobe/location changes;
- lower cost when a shot fails.

Disadvantages:

- more edit points;
- greater risk of visible continuity breaks;
- can make the result feel like a montage of unrelated AI clips.

### Long continuous shots

Advantages:

- stronger identity continuity within the shot;
- better behavioral continuity;
- more natural gaze, breath, voice, and expression flow;
- fewer artificial cuts.

Disadvantages:

- higher generation cost/time;
- one failure can invalidate a larger section;
- more opportunities for hands, props, identity, or space to drift over time.

### Continued / sliding-window shots

Potential middle ground:

```text
shorter generation unit
+ continuation context
+ overlap / carried motion
→ longer apparent continuous scene
```

This may preserve more continuity than independent clips while keeping retry units smaller than one very long generation.

Whether this is actually superior must be determined empirically for the active H3/WanGP workflow.

---

## 6. Default shot boundary principle: action continuity unit

Do not define a universal `6-second shot` or `15-second shot` rule.

Prefer the smallest unit that preserves the intended behavioral/emotional continuity.

Example:

```text
wake up → sit on bed → look outside
```

may remain one shot.

But:

```text
pool scene
→ clothing change
→ convenience-store work scene
```

should normally be separate shots because location and wardrobe state both change.

### Practical decision policy

```text
if location changes:
    prefer new shot

if wardrobe changes:
    prefer new shot

if hairstyle/state changes materially:
    usually new scene packet

if identity risk is high:
    prefer shorter unit

if emotional/dialogue continuity is important:
    prefer longer unit

if acting/gaze/breath continuity is important:
    prefer longer unit

if retry cost is high:
    prefer shorter unit

if one continuous action exceeds a comfortable generation span:
    consider continuation/sliding-window strategy
```

The decision should be model- and project-aware, not hard-coded forever.

---

## 7. Story agents should write production-aware stories

ChatGPT, Hermes, or another director/story agent should not output only prose story text.

Given:

- Character DNA;
- Voice DNA;
- Acting DNA;
- available Look Packs;
- available environments;
- target runtime/model;
- desired total runtime;

it should produce a production-aware plan.

Suggested output hierarchy:

```text
Episode
├─ Sequence
│  ├─ Story purpose
│  ├─ emotional beat
│  └─ continuity state
│
└─ Shot
   ├─ action unit
   ├─ dialogue
   ├─ recommended duration
   ├─ shot strategy
   │  ├─ independent_short
   │  ├─ long_take
   │  └─ continued_window
   ├─ character/look state
   ├─ hair state
   ├─ environment
   ├─ props
   ├─ voice requirement
   ├─ acting primitive
   └─ reference requirements
```

The agent should design the story with production cost and continuity in mind, rather than finishing a purely literary script and only later discovering that the required references do not exist.

---

## 8. Reference Planner / Asset Manifest

After the story plan is approved, compile an Asset Manifest.

Example:

```yaml
shot_03:
  character: lia
  identity:
    - FACE_MASTER
    - BODY_MASTER
  look:
    - LOOK_POOL
  hair:
    - HAIR_POOL_WET_BUN
  environment:
    - POOL_ENV_MASTER
  props:
    - TOWEL_MASTER
  voice:
    - VOICE_MASTER
  acting:
    - small_surprise
```

The planner should then check:

```text
required asset
↓
exists?
├─ yes → reuse
└─ no  → generate candidate
          ↓
        review
          ↓
       promote / reject
```

This prevents expensive video generation from starting before required appearance, location, or prop references exist.

---

## 9. WanGP should be treated as renderer/runtime, not story logic

The upstream system should decide:

- what the shot is;
- which references are authoritative;
- which Look Pack is active;
- which acting primitive applies;
- whether the shot is short/long/continued;
- what continuity constraints matter.

WanGP/H3 should receive a compiled job.

Conceptually:

```text
STORY / DIRECTOR AGENT
        ↓
SHOT PLAN
        ↓
REFERENCE PACK BUILDER
        ↓
MODEL ADAPTER
        ↓
WanGP JOB MANIFEST
        ↓
H3 RENDERER
```

Example conceptual job:

```yaml
shot_id: lia_pool_03
renderer: h3
mode: reference_generation
strategy: long_take
duration: 10
references:
  - FACE_MASTER
  - BODY_MASTER
  - LOOK_POOL
  - POOL_ENV_MASTER
  - VOICE_MASTER
prompt: <compiled shot prompt>
```

Exact field names belong to the WanGP/H3 adapter, not the canonical story schema.

---

## 10. Review and retry should operate at the smallest useful unit

After generation:

```text
render
↓
review
├─ accepted → lock / timeline
└─ failed
    ├─ identity failure
    ├─ body/wardrobe failure
    ├─ environment failure
    ├─ action failure
    ├─ gaze/reaction failure
    ├─ voice failure
    └─ temporal continuity failure
```

If only one shot fails, regenerate that shot rather than reopening the whole episode.

If a long shot repeatedly fails because only one subsection is unstable, consider splitting the shot.

If independent clips repeatedly lose continuity, consider merging the action into a longer shot or using continuation/sliding-window generation.

The shot strategy should evolve from observed failure patterns.

---

## 11. First experiment to determine shot policy

Do not guess the optimal shot strategy purely from theory.

Use the same approximately 10–12 second behavioral scene and generate it three ways:

```text
A. two independent short shots
B. one continuous long generation
C. continuation / sliding-window version
```

Evaluate:

```text
face identity
body consistency
wardrobe consistency
hair consistency
background stability
motion continuity
gaze continuity
acting continuity
voice continuity
editability
generation time
retry cost
failure frequency
```

The result should inform future default policy.

Do not promote a fixed rule before this test.

---

## 12. Recommended vlog operating loop

For a prompt such as:

```text
"Lia wakes up, goes swimming, then works at a convenience store."
```

The future production agent should ideally perform:

```text
1. Read Character / Voice / Acting DNA
2. Draft episode structure
3. Break into action-continuity units
4. Choose shot strategy per unit
5. Resolve Look Pack / Hair State per shot
6. Resolve environments / props
7. Build Asset Manifest
8. Generate missing reference assets
9. Human review / promote references
10. Compile WanGP/H3 jobs
11. Render
12. Review each shot
13. Retry only failed units
14. Assemble timeline
15. Record successful patterns and recurring failures
```

The user's high-value decisions should increasingly become:

```text
story approval
→ reference approval
→ result curation
```

while agent/runtime plumbing becomes automatic.

---

## 13. Agent-specific comments

### ChatGPT / Director Agent

- produce production-aware story structure rather than literary prose only;
- preserve character behavior and voice identity;
- choose shot strategy based on continuity, cost, and failure risk;
- explicitly identify required reference assets;
- do not force unnecessary camera complexity into simple vlog scenes.

### Hermes

- act as production planner and job assembler;
- read canonical DNA and approved asset registry before writing generation jobs;
- create/validate Asset Manifests;
- never silently replace canonical identity with the newest generated image;
- classify failures so repeated problems can later become system rules;
- when shot strategy is uncertain, preserve the uncertainty in metadata rather than inventing a permanent default.

### Codex / Claude Code

- keep story schema renderer-independent;
- isolate WanGP/H3 syntax in adapters;
- support Identity Master + Look Pack + Scene Packet composition;
- support Voice DNA and voice-reference metadata without assuming TTS/lip-sync is always downstream;
- preserve asset lineage and canonical authority;
- avoid building a complex shot-strategy engine until the A/B/C production experiment provides evidence.

---

## 14. Architecture summary

```text
Character DNA
├─ Face / Body
├─ Voice DNA
└─ Acting DNA
        │
        ├──────── Look Pack Library
        │           ├─ wardrobe
        │           └─ hair state
        │
        ├──────── Environment / Prop Library
        │
        ▼
Story / Director Agent
        │
        ▼
Sequence + Shot Plan
        │
        ▼
Shot Strategy
├─ independent short
├─ long continuous
└─ continuation/sliding window
        │
        ▼
Reference / Asset Manifest
        │
        ▼
Scene Packet
        │
        ▼
WanGP / H3 Adapter
        │
        ▼
Render
        │
        ▼
Review / Retry / Timeline
        │
        ▼
Production evidence → future rule refinement
```

## Core takeaway

The production system should not begin by deciding a fixed shot duration or a fixed character-sheet format.

It should preserve stable identity, voice, and acting knowledge; represent wardrobe/hair as replaceable Look Packs; let the story agent choose shot boundaries based on continuity and retry economics; then compile the exact reference packet required by each shot.

The correct default shot strategy should be learned from repeated H3/WanGP production evidence, not assumed in advance.