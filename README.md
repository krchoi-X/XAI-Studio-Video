# XAI-Studio-Video

Version: **0.2.0-draft**

A reusable skillset and production-design framework for AI video generation.

XAI-Studio-Video treats a video prompt not as a long block of prose, but as a structured production specification that can be compiled into model-specific runtime prompts.

## Core principle

**Preserve invariants, describe transformations, control motion, and leave freedom where variation helps.**

The framework separates what must remain stable from what is allowed to change over time, and also separates hard constraints from useful generative freedom.

- **Character DNA** — identity invariants
- **Director Intent** — what the final video should feel like
- **Reference State** — evidence-first extraction from source images/video
- **Visual DNA** — light, color, texture, optics, composition
- **Control Levels** — Hard Lock / Soft Guidance / Creative Freedom
- **Action Skeleton** — causal action sequence before exact pose choreography
- **Action Grammar** — connected movement and multi-agent interaction logic for dense action
- **Physics Lock** — causal rules for extraordinary speed, force, or stylized effects
- **Reaction Evidence** — environmental consequences that make force readable
- **Shot Graph** — entry states, events, consequences, exit states, and transitions
- **Camera DNA** — framing, movement, and motivated imperfection
- **Motion DNA** — macro movement and movement grammar
- **Motion Budget** — total allowed motion and where it is allocated
- **Micro Motion** — breathing, blink, gaze, subtle head/expression motion
- **Ambient Motion Field** — wind, plants, fabric, hair, light, atmosphere
- **Audio DNA** — ambience, music, timing, emotional mix
- **Constraints** — identity, anatomy, temporal and aesthetic protections
- **Model Adapters** — conversion from master specification to runtime prompt
- **Series Master → Variant** — controlled expansion from unusually successful outputs

## Priority order

1. Character identity preservation
2. Temporal consistency
3. Natural physical motion
4. Shot intent and emotional beat
5. Aesthetic enhancement

When these conflict, higher priorities win.

## Repository layout

```text
XAI-Studio-Video/
├── README.md
├── SKILL.md
├── CHANGELOG.md
├── docs/
│   ├── architecture.md
│   ├── reference-extraction.md
│   └── action-design.md
├── templates/
│   └── master-creative-spec.md
├── primitives/
│   ├── stillness/
│   │   └── quiet-eye-contact-hold.md
│   └── dynamic/
│       └── occlusion-roll-reveal.md
├── examples/
│   └── Summer_Garden_EyeContact_v1.md
└── adapters/
    └── README.md
```

## Master Spec vs Runtime Prompt

The **Master Creative Spec** is the source of truth. It may be long, descriptive and model-agnostic.

The **Runtime Prompt** is compiled from the Master Spec for a specific engine. It should contain only the information that particular model needs.

```text
Master Creative Spec
        ↓
   Model Adapter
        ↓
 Runtime Prompt
```

Do not assume one universal prompt format is optimal for MiniMax, Kling, Veo, Runway, Seedance, or future models.

## Controlled creativity

The studio does not try to eliminate randomness.

Instead it divides requirements into:

```text
Hard Lock
→ must remain stable

Soft Guidance
→ preferred direction or range

Creative Freedom
→ low-risk details the model may decide
```

The objective is bounded generative freedom around a stable identity, story state, and creative direction.

## Action Skeleton before pose micromanagement

When exact joint placement is not story-critical, describe the causal action sequence first.

Example:

```text
notices object → reaches → picks it up → hesitates → looks toward camera → settles
```

Only add exact pose geometry when contact, silhouette, anatomy, or repeated model failure requires it.

## Dense action: grammar, physics, reaction, camera

For combat, chase, sports, panic, dance confrontation, or other fast scenes, use four additional controls when needed:

```text
Action Grammar
→ how movements and actors causally connect

Physics Lock
→ what creates stylized effects and what is forbidden

Reaction Evidence
→ how dust, fabric, props, light, and the environment prove force

Camera Imperfection
→ motivated lag, overshoot, reacquisition, or impact response
```

A good action prompt should make force readable through causes and consequences rather than rely on adjectives or arbitrary spectacle.

Example pattern:

```text
physical movement
→ contact / redirection
→ local effect
→ environmental reaction
→ camera reaction if motivated
→ settling / next state
```

See `docs/action-design.md`.

## Evidence-first reference analysis

Reference reverse-engineering should reconstruct visible effects, not speculate about hidden production details.

Extract:
- pose and gaze
- framing and perspective character
- spatial blocking
- lighting behavior
- material/texture cues
- foreground/background relationships
- movable environmental elements

Avoid unsupported claims about exact lenses, camera bodies, hidden lighting equipment, identity, or context outside the frame.

See `docs/reference-extraction.md`.

## Motion philosophy

AI video often fails because it adds motion simply because the output is a video. XAI-Studio-Video uses a stricter rule:

> A subject does not need to keep moving.

A natural rhythm is often:

```text
stillness → small event → stillness
```

Motion should have a reason, amplitude, duration, and settling behavior.

## Motion primitive families

### Dynamic primitives

For impact, transition, reveal and camera transformation.

Examples:
- lens occlusion transition
- leg/cloth/hair sweep reveal
- camera-roll reveal
- whip transition
- splash-cover transition
- reactive pursuit with camera lag/reacquisition

### Stillness primitives

For realism, intimacy and emotional retention.

Examples:
- quiet eye-contact hold
- observational portrait hold
- subtle breath portrait
- micro-smile settle
- found-moment hold

## Series Master → Variant

A generation that captures a strong character, visual identity, or interaction pattern should be evaluated as a reusable Series Master.

```text
strong result
→ preserve robust anchors
→ vary only selected axes
→ test stability and novelty
→ promote repeated successes into DNA / primitives
```

This supports recurring characters, vlogs, shorts, and systematic asset expansion without freezing every incidental detail.

## Status

This is an evolving draft. The goal is to accumulate tested prompting patterns, model-specific adapters, failure cases, reusable temporal primitives, and production knowledge rather than freeze a single 'perfect prompt'.

External methodologies may inspire candidate rules, but rules are promoted only when they survive practical generation tests.