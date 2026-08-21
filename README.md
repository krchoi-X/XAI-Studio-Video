# XAI-Studio-Video

Version: **0.1.0-draft**

A reusable skillset and prompt-design framework for AI video generation.

XAI-Studio-Video treats a video prompt not as a long block of prose, but as a structured production specification that can be compiled into model-specific runtime prompts.

## Core principle

**Preserve invariants, describe transformations, control motion.**

The framework separates what must remain stable from what is allowed to change over time.

- **Character DNA** — identity invariants
- **Director Intent** — what the final video should feel like
- **Visual DNA** — light, color, texture, optics, composition
- **Shot Graph** — temporal states and transitions
- **Camera DNA** — framing and camera behavior
- **Motion DNA** — macro movement and movement grammar
- **Motion Budget** — total allowed motion and where it is allocated
- **Micro Motion** — breathing, blink, gaze, subtle head/expression motion
- **Ambient Motion Field** — wind, plants, fabric, hair, light, atmosphere
- **Audio DNA** — ambience, music, timing, emotional mix
- **Constraints** — identity, anatomy, temporal and aesthetic protections
- **Model Adapters** — conversion from master specification to runtime prompt

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
│   └── architecture.md
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

Do not assume one universal prompt format is optimal for MiniMax, Kling, Veo, Runway, or future models.

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

### Stillness primitives

For realism, intimacy and emotional retention.

Examples:
- quiet eye-contact hold
- observational portrait hold
- subtle breath portrait
- micro-smile settle
- found-moment hold

## Status

This is an evolving draft. The goal is to accumulate tested prompting patterns, model-specific adapters, failure cases, and reusable temporal primitives rather than freeze a single 'perfect prompt'.