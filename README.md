# XAI-Studio-Video

Version: **0.3.0-draft**

A reusable skillset and production-design framework for AI visual storytelling, with video as the first production target.

XAI-Studio-Video treats generation prompts as compiled outputs of a structured creative system rather than as the source of truth.

## Core principle

**Preserve invariants, describe transformations, direct attention, control motion, and leave freedom where variation helps.**

The framework separates story/directing decisions from renderer-specific execution.

Key components:

- **Director Intent** — what the audience should experience
- **Storyboard Spec** — medium-neutral story, beat, tempo, composition, emotion, and continuity plan
- **Narrative Tempo Map** — relative attention and pacing before medium-specific timing/layout
- **Character DNA** — identity invariants
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
- **Model / Renderer Adapters** — conversion from canonical specs to disposable runtime instructions
- **Series Master → Variant** — controlled expansion from unusually successful outputs

## Priority order

1. Story / character intent
2. Character identity preservation
3. Temporal / spatial consistency
4. Natural physical motion or readable static sequencing
5. Emotional beat and attention control
6. Aesthetic enhancement

When these conflict, higher priorities win.

## Storyboard-first workflow

The studio now treats storyboarding as a reusable intermediate representation rather than a video-only preproduction artifact.

```text
Idea
↓
Director Interpretation
↓
Beat Sheet
↓
Narrative Tempo Map
↓
Storyboard Spec Draft 0
↓
User Review / Revision
↓
Approved Storyboard Spec
      │
      ├─ Video
      │   └─ H3 / Seedance / Kling / Veo / ...
      │
      ├─ Graphic Novel / Comic
      │   └─ page/panel adaptation → high-quality image rendering
      │
      └─ Illustration Sequence
          └─ selected hero frames → high-quality image rendering
```

The **Storyboard Spec is canonical**. A rough storyboard image is a disposable, low-cost visualization used to inspect composition, blocking, expression, continuity, and tempo.

This lets the studio use cheap storyboards to decide which expensive images or videos are worth rendering.

See:

- `skills/storyboard-director/SKILL.md`
- `docs/storyboard-directing.md`
- `docs/storyboard-rendering.md`
- `templates/storyboard-draft.md`

## Renderer independence

The studio does not require one image or video provider.

```text
Approved Storyboard Spec
        ↓
Renderer / Model Adapter
        ├─ cloud image model
        ├─ local open-weight image model
        ├─ ephemeral 5090-pod model
        ├─ video model
        └─ future renderer
```

Provider-specific syntax, safety behavior, prompt conventions, and aesthetics belong in adapters rather than in the canonical creative spec.

For graphic novels or illustration sequences, final images can be generated **one panel at a time** from the approved panel spec plus character/location/prop references. The rough board does not need final-quality faces, skin, lighting, or anatomy.

## Repository layout

```text
XAI-Studio-Video/
├── README.md
├── SKILL.md
├── CHANGELOG.md
├── docs/
│   ├── architecture.md
│   ├── reference-extraction.md
│   ├── action-design.md
│   ├── storyboard-directing.md
│   └── storyboard-rendering.md
├── skills/
│   ├── README.md
│   └── storyboard-director/
│       └── SKILL.md
├── templates/
│   ├── master-creative-spec.md
│   └── storyboard-draft.md
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

The **Master Creative Spec** and **Storyboard Spec** are reusable sources of truth.

The **Runtime Prompt** is disposable and model-specific.

```text
Storyboard Spec / Master Creative Spec
              ↓
         Model Adapter
              ↓
        Runtime Prompt
```

Do not assume one universal prompt format is optimal for MiniMax, Kling, Veo, Runway, Seedance, image models, or future engines.

## Controlled creativity

The studio does not try to eliminate randomness.

```text
Hard Lock
→ must remain stable

Soft Guidance
→ preferred direction or range

Creative Freedom
→ low-risk details the model may decide
```

The objective is bounded generative freedom around stable story, identity, continuity, and creative direction.

## Action and physical realism

For fast or multi-agent scenes, use:

```text
Action Grammar
→ connected actor/motion logic

Physics Lock
→ what creates stylized effects and what is forbidden

Reaction Evidence
→ how the world proves force

Camera Imperfection
→ motivated lag, overshoot, reacquisition, or impact response
```

See `docs/action-design.md`.

## Evidence-first reference analysis

Reference reverse-engineering should reconstruct visible effects, not speculate about hidden production details.

See `docs/reference-extraction.md`.

## Motion philosophy

A natural rhythm is often:

```text
stillness → meaningful event → stillness
```

Motion should have a reason, amplitude, duration, and settling behavior.

## Series Master → Variant

A generation that captures a strong character, visual identity, or interaction pattern should be evaluated as a reusable Series Master.

```text
strong result
→ preserve robust anchors
→ vary selected axes
→ test stability and novelty
→ promote repeated successes into DNA / primitives
```

## Status

This is an evolving draft. The current goal is not to build a giant fixed schema, but to accumulate tested storyboarding, prompting, rendering, model-adapter, recovery, and evaluation patterns that remain useful as models change.

External methodologies may inspire candidate rules, but rules are promoted only when they survive practical production tests.