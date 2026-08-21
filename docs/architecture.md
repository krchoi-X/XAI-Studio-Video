# Architecture

XAI-Studio-Video is organized around one core distinction:

- **DNA layers define invariants and reusable aesthetic/identity rules.**
- **Graph and motion layers define transformations through time.**
- **Control levels define how strongly each requirement should constrain generation.**
- **Reference extraction must be evidence-first.**

## Layer model

```text
VIDEO PROJECT
│
├─ 1. CHARACTER DNA
│    ├ face identity
│    ├ body identity
│    ├ hair
│    └ wardrobe
│
├─ 2. DIRECTOR INTENT
│    └ emotional and experiential goal
│
├─ 3. VISUAL DNA
│    ├ light
│    ├ color
│    ├ optics
│    ├ texture
│    └ composition
│
├─ 4. SHOT GRAPH
│    ├ entry states
│    ├ events
│    ├ consequences
│    ├ exit states
│    ├ transitions
│    └ key emotional beats
│
├─ 5. CAMERA DNA
│    ├ framing
│    ├ focal behavior
│    ├ movement
│    ├ handheld amplitude
│    └ motivated imperfection
│
├─ 6. MOTION DNA
│    ├ action skeleton
│    ├ action grammar
│    ├ macro subject motion
│    ├ multi-agent interaction logic
│    ├ motion grammar
│    └ settling behavior
│
├─ 7. MOTION BUDGET
│    └ LOW / MEDIUM / HIGH plus allocation
│
├─ 8. MICRO MOTION
│    ├ breathing
│    ├ blink
│    ├ gaze
│    ├ head correction
│    └ micro-expression
│
├─ 9. AMBIENT MOTION FIELD
│    ├ wind
│    ├ plants
│    ├ hair
│    ├ fabric
│    ├ shadows / light
│    ├ atmosphere
│    └ reaction evidence
│
├─ 10. PHYSICS LOCK
│    ├ source / cause
│    ├ allowed manifestation
│    ├ forbidden manifestation
│    └ world reaction
│
├─ 11. AUDIO DNA
│    ├ ambience
│    ├ BGM
│    ├ timing
│    └ emotional mix
│
├─ 12. CONSTRAINTS & CONTROL LEVELS
│    ├ Hard Lock
│    ├ Soft Guidance
│    └ Creative Freedom
│
└─ 13. MODEL ADAPTER
     └ Master Spec → Runtime Prompt
```

## Why this separation matters

A long prose prompt often mixes fixed character attributes, changing motion, camera behavior, mood, audio, and negative constraints in one undifferentiated block. That makes revision difficult and obscures which requirement caused a failure.

With XAI-Studio-Video, each class of information has a home and a visual responsibility.

Example:

- Face shape belongs in Character DNA.
- 'Eyes move toward camera first' belongs in Micro Motion.
- 'Camera rolls 90 degrees behind full occlusion' belongs in Shot Graph + Camera DNA.
- 'Soft cyan shadows and lifted blacks' belongs in Visual DNA.
- 'BGM ducks during eye contact' belongs in Audio DNA.
- 'Static discharge only emerges from friction/contact' belongs in Physics Lock.

When a result fails, first identify which responsibility layer failed. Do not rewrite unrelated layers that are already working.

## Master Creative Spec

The Master Creative Spec is the canonical source document. It should remain readable by humans and agents and should not depend on one generation engine.

It may be detailed.

## Runtime Prompt

The Runtime Prompt is disposable and model-specific.

It should be recompiled whenever:
- target model changes
- model version changes materially
- reference input mode changes
- keyframe support changes
- audio support changes
- negative prompt behavior changes

## Visual responsibility model

Each prompt component should have a primary responsibility.

```text
Character DNA       identity
Director Intent     emotional goal
Visual DNA          visual appearance
Shot Graph          state transition through time
Camera DNA          viewpoint and camera behavior
Motion DNA          subject action grammar
Motion Budget       total motion allocation
Micro Motion        subtle realism
Ambient Motion      causal environmental life
Physics Lock        physical rules for stylized/high-risk effects
Audio DNA           temporal sound direction
Constraints         protection and bounds
Model Adapter       engine-specific compilation
```

Redundancy is allowed only when it intentionally reinforces a high-risk invariant.

## Action Skeleton

Before writing precise pose choreography, define the minimum causal action sequence needed for the scene.

Example:

```text
notices cup → reaches → lifts → drinks → notices camera → settles
```

The Action Skeleton answers **what changes and in what causal order** without forcing every joint and frame.

Exact pose detail should be added only when:
- anatomy is story-critical
- contact geometry matters
- a specific silhouette is essential
- model failure repeatedly shows that a looser description is insufficient

This keeps prompts readable and preserves natural variation.

## Action Grammar

Dense action needs more than a list of verbs. It needs connected interaction logic.

Example:

```text
evade → parry → redirect → counter → sweep → recover
```

For multi-agent scenes, explicitly state when:
- actions overlap instead of occurring one at a time
- contact changes later blocking or momentum
- the subject must physically travel through space
- actors must remain spatially accountable
- reset poses should be avoided

The Action Grammar is especially useful for combat, chase, sports, panic, dance confrontation, and other fast multi-body scenes.

See `docs/action-design.md`.

## Physics Lock

Stylized effects become believable when they obey a simple visible rule set.

A Physics Lock defines:

```text
Source
Allowed manifestation
Forbidden manifestation
World reaction
```

Example:

```text
friction / contact
→ local static discharge
→ no projectile / aura / teleportation
→ dust, hair, fabric, and loose objects respond to velocity and impact
```

The objective is not scientific simulation. The objective is causal readability.

Use Physics Lock when spectacle could otherwise drift into arbitrary magic, detached VFX, or physically impossible displacement.

## Reaction Evidence

Action intensity should be visible in consequences, not just in the actor or effect layer.

Useful Reaction Evidence:
- dust wakes
- loose paper/debris displacement
- fabric compression/flutter
- hair response
- nearby objects rolling or shifting
- motivated electrical/light response
- camera shake or lens contamination only when the event physically reaches the camera system

Preferred causal sequence:

```text
physical event → local effect → secondary reaction → settling
```

Reaction Evidence extends the Ambient Motion Field from passive environmental life to event-driven physical response.

## Camera Imperfection

A camera can feel more live-action when it reacts rather than predicts perfectly.

Motivated imperfections may include:
- slight tracking lag
- brief overshoot
- delayed whip-pan reacquisition
- short focus recovery
- impact shake tied to a real physical event

This must remain controlled. Random shake or continuous focus hunting is not realism.

Action readability outranks camera spectacle.

## Emotional continuity through spectacle

A fast scene still has a character state.

Track an emotional chain alongside the action chain:

```text
fear → involuntary competence → shock → renewed pressure → uncertain resolve
```

This prevents action from automatically turning the subject into a generic triumphant hero.

## Control levels

Not every requirement deserves equal rigidity.

### Hard Lock

Must remain stable. Breaking it makes the result unusable.

Examples:
- face identity
- story-critical prop ownership/state
- required spatial relationship
- wardrobe continuity when continuity matters
- entry/exit state required for the next shot

### Soft Guidance

Defines preferred direction while allowing small interpretation.

Examples:
- restrained handheld camera
- slight head correction
- warm late-afternoon light
- modest reaction intensity

### Creative Freedom

Deliberately left to the model within safe bounds.

Examples:
- exact blink timing
- tiny hand adjustments
- minor hair movement
- incidental background motion
- micro-expression timing

The objective is **bounded generative freedom**, not maximum constraint density.

## Controlled randomness

Randomness is useful when it creates natural variation without damaging the scene's anchors.

The studio should explicitly decide:
- what must be repeated
- what may vary
- what variation would make the result more interesting

A good production system does not try to freeze every visible detail. It locks the creative direction and identity while leaving low-risk degrees of freedom open.

## Evidence-first reference extraction

Reference analysis must separate observation from inference.

Extract only what the source visibly supports:
- subject pose and orientation
- gaze
- framing and crop
- foreground/background relationships
- light direction and character
- visible materials and texture
- spatial blocking
- movable environmental elements
- obvious camera perspective characteristics

Do not invent:
- exact camera or lens model
- hidden lighting equipment
- brand names not visibly supported
- identity or biography
- context outside the frame

The output should be a reusable **Reference State**, not speculative metadata.

See `docs/reference-extraction.md`.

## Series Master → Variant

An unusually successful image or clip should be treated as a possible **Series Master**.

A Series Master contains anchors worth preserving across future variants:
- character identity
- world/scene identity
- visual tone
- reliable framing pattern
- successful motion behavior
- reusable interaction pattern

Variants should deliberately change only selected axes:

```text
Series Master
→ keep anchors
→ change one or a few axes
→ evaluate stability and novelty
→ promote robust properties into DNA / primitives
```

This supports character vlogs, recurring short-form series, and systematic anchor expansion.

## Primitive library

A primitive is a tested temporal pattern that can be reused across characters, locations, and styles.

A primitive should specify:
- intent
- precondition
- temporal states
- motion envelope
- camera behavior
- identity risk
- common failures
- adaptation notes

### Dynamic primitive examples

```text
foot-cover → full occlusion → camera roll → face reveal
hair sweep → hidden cut → new composition
water splash → lens cover → scene reveal
reactive pursuit → tracking lag → whip-pan reacquire → settle
```

### Stillness primitive examples

```text
look away → eyes notice camera → one blink → quiet eye contact → micro-smile → release
```

## Motion Budget

Motion Budget is a planning abstraction, not necessarily a parameter sent to the model.

Example LOW-motion allocation:

```text
body       very low
head       very low
eyes       low-to-medium
expression very low
hair       low
fabric     very low
plants     low
camera     very low
lighting   very low
```

The purpose is to stop the prompt author or agent from adding movement to every available element.

## Ambient Motion Field

A scene should contain enough causal micro-motion to feel filmed, but not so much that temporal stability breaks.

Good ambient motion is:
- low amplitude
- spatially coherent
- caused by wind, body movement, light, camera breathing, or another physical source
- allowed to settle

Bad ambient motion is:
- continuous floating
- unrelated elements moving independently
- hair motion inconsistent with leaves/fabric
- changing light with no moving occluder or exposure cause

## Identity-first fallback rule

When generation fails, simplify in this order:

1. reduce camera transformation
2. reduce subject macro motion
3. reduce expression change
4. reduce environmental motion
5. shorten the number of distinct temporal events

Do not solve identity drift by adding more aesthetic description.

## Preserve accepted work

When a generation is partially successful, keep the accepted layers stable.

Example:

```text
identity accepted
composition accepted
camera accepted
motion failed
```

The next attempt should change motion-related instructions first, not regenerate the entire creative specification.

This applies the same principle as single-variable debugging: change the smallest plausible cause before disturbing working layers.

## Evolution strategy

This architecture is intentionally provisional. New concepts should be promoted into the schema only when they recur across multiple successful experiments or explain repeated failure modes better than the existing layers.

External prompting methodologies may inspire candidate concepts, but XAI-Studio-Video should absorb only principles that survive practical generation tests.