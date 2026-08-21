# XAI-Studio-Video Skill

## Purpose

Use this skill to design, critique, reverse-engineer, or adapt prompts for AI-generated video.

The skill is not a collection of decorative prompt phrases. Its job is to convert a creative goal into a structured temporal specification that preserves identity, controls motion, separates evidence from inference, and can be adapted to different video engines.

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

### 15. Give every prompt layer a visual responsibility

Do not let multiple sections compete to control the same thing unless redundancy is intentional.

Typical responsibilities:
- Character DNA controls identity.
- Visual DNA controls scene appearance, light, color, optics, and texture.
- Shot Graph controls temporal state changes.
- Camera DNA controls framing and camera behavior.
- Motion DNA controls subject motion grammar.
- Constraints protect invariants and known failure points.

When a generation fails, identify which responsibility layer failed before rewriting anything else.

### 16. Use an Action Skeleton before exact pose choreography

Describe the essential causal action sequence first, then add only the pose detail needed for clarity.

Example:

```text
notices object → reaches → picks it up → hesitates → looks toward camera → settles
```

Prefer an action skeleton when exact limb placement is not story-critical. Over-specifying every joint can reduce natural variation and make the prompt internally brittle.

### 17. Preserve controlled randomness

Do not eliminate useful generative variation.

Separate control strength into three levels:

```text
Hard Lock       must remain stable
Soft Guidance   preferred direction or range
Creative Freedom model may decide within bounds
```

Good candidates for Creative Freedom:
- tiny hand adjustments
- exact blink timing
- minor hair movement
- incidental background motion
- micro-expression timing

Good candidates for Hard Lock:
- identity
- story-critical prop state
- required spatial relationship
- entry/exit state needed for continuity

The goal is not maximum control. The goal is bounded freedom around a stable creative direction.

### 18. Reverse-engineer references from visible evidence only

When extracting a prompt or state description from an image/video reference:
- describe what is visibly supported
- separate observation from inference
- do not invent exact camera bodies, lens models, brands, identities, or hidden context without evidence
- extract reusable spatial, lighting, material, composition, and motion-relevant properties

Reference analysis should produce a usable state description, not unsupported trivia.

### 19. Expand successful results as Series Masters

When one generation captures a valuable character, scene, or visual identity, treat it as a reusable series master rather than an isolated success.

Pattern:

```text
Series Master
→ preserve identity / world / visual anchors
→ vary scene, action, framing, or mood selectively
→ evaluate which properties remain stable
→ promote robust properties into reusable DNA / primitives
```

Variants should change a small number of intentional axes while preserving the anchors that made the master successful.

## Output workflow

When creating a new video prompt:

1. Write Director Intent.
2. Determine identity requirements.
3. Identify reference evidence and assign reference roles.
4. Separate Hard Locks, Soft Guidance, and Creative Freedom.
5. Assign Motion Budget.
6. Build the Action Skeleton.
7. Build the Shot Graph from entry states, events, and exit states.
8. Define camera behavior.
9. Define subject macro motion.
10. Define Micro Motion.
11. Define Ambient Motion Field.
12. Define visual/light/color behavior.
13. Define Audio DNA if applicable.
14. Add hard constraints and known failures.
15. Compile to the target model through an adapter.
16. Keep the Master Creative Spec separately from the Runtime Prompt.
17. After generation, preserve accepted work and revise only the failed responsibility layer when possible.
18. If the result is unusually strong, evaluate it as a Series Master for controlled variants.

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
- action remains readable without unnecessary pose micromanagement
- model creativity appears inside permitted bounds rather than breaking invariants

## Guiding maxim

**Preserve what matters, specify what changes, and leave freedom where variation can help.**