# XAI-Studio-Video Skill

## Purpose

Use this skill to design, critique, reverse-engineer, or adapt prompts for AI-generated video.

The skill is not a collection of decorative prompt phrases. Its job is to convert a creative goal into a structured temporal specification that preserves identity, controls motion, and can be adapted to different video engines.

## Operating rules

### 1. Start from Director Intent

Before optimizing camera terms or model syntax, state what the final clip should feel like in one short paragraph.

Director Intent answers:
- What kind of moment is this?
- Is it observed, staged, cinematic, documentary, commercial, dreamlike, social-video, found-footage, etc.?
- Where is the emotional peak?
- What must the viewer remember?

### 2. Separate invariants from transformations

**Invariants** belong in Character DNA / Visual DNA / Constraints.

Examples:
- face identity
- hair length
- wardrobe design
- body proportions
- core color palette

**Transformations** belong in Shot Graph / Motion DNA.

Examples:
- gaze shifts toward camera
- foot approaches lens
- camera rolls during occlusion
- flower crosses foreground

Do not mix these layers unnecessarily.

### 3. Identity preservation outranks spectacle

Default priority:

```text
P0 Character identity
P1 Temporal consistency
P2 Natural motion
P3 Shot/emotional intent
P4 Aesthetic enhancement
```

If an elaborate motion threatens identity consistency, simplify the motion.

### 4. Build a Shot Graph

Represent the clip as temporal states plus events.

Example:

```text
S0: subject watches flower
E1: eyes notice camera
S1: quiet awareness
E2: breeze moves environment
S2: direct eye contact
E3: gaze releases
S3: ending occlusion / fade
```

For short social clips, also identify the retention structure when relevant:

```text
impact → transition → reward
```

or

```text
observe → notice → suspend → connect → release
```

### 5. Declare a Motion Budget

Classify the clip as LOW, MEDIUM, or HIGH motion.

LOW motion means:
- no unnecessary walking or gesturing
- near-zero torso movement
- small head movement
- controlled hair/fabric/environment motion
- camera movement kept minimal unless essential

Motion should be allocated intentionally across subject, camera, hair, fabric, environment, light, and atmosphere.

### 6. Use Micro Motion deliberately

For realistic portrait-oriented video, prefer small causal motion:
- natural breathing
- one or few natural blinks
- gaze moves before head when appropriate
- nearly invisible head correction
- micro-expression rather than large facial acting
- a few strands of hair moving, not the whole hairstyle
- fabric responding slightly to wind or body motion

Default rhythm:

```text
stillness → subtle motion → stillness
```

### 7. Model the Ambient Motion Field

A realistic scene should not look like a moving subject pasted onto a frozen image.

Consider low-amplitude motion in:
- leaves
- flowers
- grass
- curtains
- hair
- clothing
- shadows
- reflected light
- particles / haze
- camera breathing

All environmental motion must have a plausible cause.

### 8. Use occlusion to hide difficult transitions

When a large visual transformation is required, prefer a motivated full-frame or near-full-frame occlusion.

Reusable occluders:
- hand
- foot/leg
- fabric
- hair
- water splash
- foreground object
- darkness / doorway

Pattern:

```text
Scene A
→ occluder fills frame
→ hidden transition / camera transformation
→ occluder clears
→ Scene B reveal
```

This is especially useful for identity-sensitive or large camera-state changes.

### 9. Design sound around attention

Audio is part of temporal direction.

Use:
- ambience before music when the scene should feel discovered rather than staged
- gradual BGM entry
- selective BGM ducking at emotional peaks
- environmental sound emphasis during eye contact or important stillness
- natural reverb/fade at the end

Do not add strong beats merely because the clip is short-form.

### 10. Keep the Master Creative Spec model-agnostic

The master specification may contain:
- Director Intent
- Character DNA
- Visual DNA
- Shot Graph
- Camera DNA
- Motion DNA
- Motion Budget
- Micro Motion
- Ambient Motion Field
- Audio DNA
- Constraints

Do not force model-specific syntax into this layer.

### 11. Compile through a Model Adapter

A runtime prompt should be generated from the Master Creative Spec according to model behavior.

Examples:
- If the model already receives a strong I2V reference, omit redundant visual description and focus on motion.
- If the model does not respond well to negative wording, convert prohibitions into positive stable-state instructions.
- If the model supports explicit negative prompts, preserve relevant failure constraints there.
- If the model supports first/last frames or keyframes, convert the Shot Graph into explicit control states.
- If the model supports synchronized audio, compile Audio DNA; otherwise keep audio as a separate production spec.

### 12. Prefer observable visual behavior over speculative gear trivia

Lens and camera references are useful when they clearly influence geometry, depth of field, motion, or optical character.

Prefer:
- extreme ground-level ultra-wide perspective
- shallow depth of field with foreground flowers blurred
- restrained handheld breathing

Over unsupported assumptions about exact real-world hardware.

### 13. Make negative constraints actionable

Store failures in the Master Spec, but convert them when needed.

Instead of only:

```text
no identity drift
no excessive blinking
no strong wind
```

also express desired state:

```text
stable facial identity throughout
one natural blink
very gentle breeze affecting only a few hair strands
```

### 14. Preserve successful generations as reusable assets

A successful result should produce more than a finished clip.

Record:
- source image/reference
- master spec
- runtime prompt
- model and version
- settings
- seed if available
- successful motion primitive
- observed failure modes
- what changed in rerolls

Successful motion patterns should be promoted into the primitive library.

## Output workflow

When creating a new video prompt:

1. Write Director Intent.
2. Determine identity requirements.
3. Assign Motion Budget.
4. Build Shot Graph.
5. Define camera behavior.
6. Define subject macro motion.
7. Define Micro Motion.
8. Define Ambient Motion Field.
9. Define visual/light/color behavior.
10. Define Audio DNA if applicable.
11. Add hard constraints and known failures.
12. Compile to the target model through an adapter.
13. Keep the Master Creative Spec separately from the Runtime Prompt.

## Evaluation checklist

A result is successful when:
- the same character remains recognizable throughout
- movement has clear physical causes
- motion settles naturally instead of continuously floating
- face and body do not morph during low-motion intervals
- environment is alive without becoming chaotic
- camera motion supports the emotional beat
- the most important moment is temporally emphasized
- the clip feels filmed rather than merely animated
- aesthetic effects do not overpower identity or motion realism

## Guiding maxim

**Do not ask how to make everything move. Ask what must remain still, what deserves to move, and why.**