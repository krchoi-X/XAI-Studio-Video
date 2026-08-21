# Architecture

XAI-Studio-Video is organized around one core distinction:

- **DNA layers define invariants and reusable aesthetic/identity rules.**
- **Graph and motion layers define transformations through time.**

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
│    ├ states
│    ├ events
│    ├ transitions
│    └ key emotional beats
│
├─ 5. CAMERA DNA
│    ├ framing
│    ├ focal behavior
│    ├ movement
│    └ handheld amplitude
│
├─ 6. MOTION DNA
│    ├ macro subject motion
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
│    └ atmosphere
│
├─ 10. AUDIO DNA
│    ├ ambience
│    ├ BGM
│    ├ timing
│    └ emotional mix
│
├─ 11. CONSTRAINTS
│    ├ identity
│    ├ anatomy
│    ├ temporal
│    └ aesthetic
│
└─ 12. MODEL ADAPTER
     └ Master Spec → Runtime Prompt
```

## Why this separation matters

A long prose prompt often mixes fixed character attributes, changing motion, camera behavior, mood, audio, and negative constraints in one undifferentiated block. That makes revision difficult and obscures which requirement caused a failure.

With XAI-Studio-Video, each class of information has a home.

Example:

- Face shape belongs in Character DNA.
- 'Eyes move toward camera first' belongs in Micro Motion.
- 'Camera rolls 90 degrees behind full occlusion' belongs in Shot Graph + Camera DNA.
- 'Soft cyan shadows and lifted blacks' belongs in Visual DNA.
- 'BGM ducks during eye contact' belongs in Audio DNA.

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

## Evolution strategy

This architecture is intentionally provisional. New concepts should be promoted into the schema only when they recur across multiple successful experiments or explain repeated failure modes better than the existing layers.