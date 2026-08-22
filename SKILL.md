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

### 20. Use Action Grammar for fast or multi-agent motion

For combat, chase, sports, panic, dance confrontation, or other dense action, do not rely on adjectives such as "fast" or "intense" alone.

Define a connected verb chain:

```text
evade → parry → redirect → counter → sweep → recover
```

For multi-agent scenes, state the interaction logic explicitly when it matters:
- actors may attack or move simultaneously rather than taking turns
- physical contact changes later positions and momentum
- the main subject must physically travel through space rather than teleport
- background actors remain spatially accountable
- avoid repeated reset poses between actions

See `docs/action-design.md`.

### 21. Add a Physics Lock when spectacle could become arbitrary magic

When a scene contains extraordinary acceleration, stylized discharge, large impacts, unusual particles, or other effects that could become visually ungrounded, define:

```text
Source
Allowed manifestation
Forbidden manifestation
World reaction
```

Effects must emerge from readable causes whenever realism is desired.

Example:

```text
friction/contact
→ brief local static discharge
→ no beams / aura / teleportation
→ dust, hair, fabric, and loose objects react to force
```

### 22. Prove force through environmental Reaction Evidence

Do not communicate action intensity only through the actor or VFX.

Use physically motivated consequences in the world:
- dust wakes
- loose paper/debris displacement
- fabric compression or flutter
- hair response
- nearby object motion
- motivated light/electrical response
- lens shake, contamination, or flare only when the event reaches the camera

Use the causal sequence:

```text
physical event → local effect → secondary reaction → settling
```

### 23. Allow motivated Camera Imperfection

A reactive camera does not need to anticipate every movement perfectly.

Controlled realism may include:
- slight tracking lag
- brief overshoot
- delayed whip-pan reacquisition
- short focus recovery
- impact shake tied to a physical event

Do not confuse this with random handheld chaos. Action readability remains the priority.

Useful pattern:

```text
subject accelerates
→ camera briefly loses ideal framing
→ camera reacts / reacquires
→ framing settles
```

### 24. Preserve emotional continuity through action

Fast motion must not erase the character's emotional state.

Track an emotional chain alongside the action chain, for example:

```text
fear → involuntary competence → shock → renewed pressure → uncertain resolve
```

Avoid automatic triumphant hero posing unless that is the intended character beat.

### 25. Compile one coherent subject, body, and camera state

Do not create a runtime prompt by concatenating independently complete prompts. A character master written as a portrait and a separate full-body shot prompt can be interpreted as two simultaneous image concepts, producing a close-up face with a miniature or duplicated body layered over it.

At runtime, assemble one prompt from responsibility layers and remove competing declarations:

```text
one subject / one anatomically coherent body
→ one framing and camera-distance state
→ one pose or action state
→ only the identity features needed to preserve the character
→ wardrobe
→ environment, light, and finish
```

Apply these rules to both image and video prompts:

- Declare the intended shot type once. Do not retain `portrait`, `close-up`, or headshot language when compiling a true full-body shot.
- Put composition-critical framing early, especially for head-to-toe, wide, distant, or multi-subject shots.
- Compress Character DNA into identity features; do not paste a complete master portrait prompt unchanged into every shot prompt.
- Describe a single subject and a single continuous body when prior tests show duplication, miniature-body, collage, or body-overlay failures.
- Remove mutually exclusive instructions. For example, `all ten toes visible` conflicts with closed shoes; use `the soles of both shoes remain inside the frame` when the character is shod.
- Do not repeat the subject as though introducing a second rendering task. Merge face, body, pose, wardrobe, and framing into one camera-visible state.
- For video, distinguish the starting visual state from temporal change. Character DNA preserves identity; the Shot Graph and Motion DNA change that same body through time rather than describing another version of the person.
- Keep runtime prompts within the target model's useful instruction capacity. Prefer a shorter coherent prompt over a long prompt containing competing high-priority concepts.

Before rendering, run a prompt-collision check:

1. Is there exactly one intended subject count and one body state?
2. Is there exactly one active shot scale and camera distance at each time state?
3. Do pose, crop, wardrobe, and anatomy descriptions agree?
4. Did compilation accidentally preserve a complete prompt for a different shot type?
5. For video, are changes ordered in time instead of layered into one frame?

Known production failure:

```text
complete photorealistic portrait prompt
+ complete head-to-toe fashion prompt
→ giant close-up face with a small full body composited over it
```

Mitigation: remove portrait-shot language, declare one coherent adult body, place full-length framing first, merge only the necessary identity features, and eliminate wardrobe/anatomy contradictions.

### 26. Separate emotional expression from eye coordination

Do not rely on vague mood words to control the eyes. Terms such as `drowsy`, `relaxed eyelids`, `absent-minded`, or `subtle facial asymmetry` can combine into divergent pupils, mismatched eyelids, or an unintended crossed/wall-eyed gaze when the prompt does not define a shared visual target.

Treat these as separate responsibilities:

```text
eye anatomy and coordination
→ both eyes belong to the same face and track the same target

gaze direction
→ one explicit camera-relative or scene-relative target

emotional expression
→ brow, facial muscle tension, mouth, breath, and posture
```

For identity-sensitive image and video prompts:

- Give both eyes one shared target whenever the gaze must be readable: directly toward the camera, slightly camera-left, toward a named object, or another unambiguous point.
- Keep both irises and pupils consistently aligned toward that target, with coherent catchlights from the same light source.
- Express sleepiness, languor, sadness, distraction, or intoxication primarily through the brow, mouth, facial tension, breathing, head angle, and posture unless asymmetric eyelid behavior is intentionally required.
- If natural facial asymmetry is part of Character DNA, localize it to safe features such as cheeks, jawline, or mouth corners when eye coordination is important. Do not let general asymmetry silently authorize conflicting gaze directions.
- Avoid stacking several eye-relaxation phrases without a gaze lock. `Slightly drowsy + relaxed eyelids + absent-minded` is not a complete eye-direction specification.
- For video, preserve the same coordinated binocular target through blinks and gaze transitions. Move both eyes together to the next target before or with the head according to Motion DNA.
- Do not expect an upscaler to repair incorrect eye anatomy or gaze. Reject, rerender, or inpaint the source image before upscaling. When inpainting, repair both eyes and their surrounding eyelids together rather than independently.

Before accepting a face, verify:

1. Do both eyes focus on the same plausible point?
2. Are iris direction, pupil position, eyelid shape, and catchlights mutually coherent?
3. Is the intended emotion carried without sacrificing binocular coordination?
4. Does facial asymmetry preserve identity without becoming an eye-direction error?
5. For video, do blinks and gaze shifts remain coordinated over time?

Known production failure:

```text
subtle natural facial asymmetry
+ slightly drowsy
+ relaxed eyelids
+ absent-minded softness
+ no shared gaze target
→ each eye looks in a different direction
```

Mitigation: state one shared gaze target, explicitly coordinate both eyes, and carry the languid mood through relaxed brow, softened mouth, facial muscles, breathing, and body posture.

## Output workflow

When creating a new video prompt:

1. Write Director Intent.
2. Determine identity requirements.
3. Identify reference evidence and assign reference roles.
4. Separate Hard Locks, Soft Guidance, and Creative Freedom.
5. Assign Motion Budget.
6. Build the Action Skeleton.
7. For dense action, add Action Grammar, multi-agent interaction rules, and Physics Lock where needed.
8. Build the Shot Graph from entry states, events, consequences, and exit states.
9. Define camera behavior, including any deliberately motivated lag/overshoot.
10. Define subject macro motion.
11. Define Micro Motion.
12. Define Ambient Motion Field and Reaction Evidence.
13. Define visual/light/color behavior.
14. Define Audio DNA if applicable.
15. Add hard constraints and known failures.
16. Compile to the target model through an adapter.
17. Run the prompt-collision check on subject count, body state, framing, pose, wardrobe, and temporal ordering.
18. For visible faces, verify one shared gaze target and coherent iris, pupil, eyelid, and catchlight behavior.
19. Keep the Master Creative Spec separately from the Runtime Prompt.
20. After generation, preserve accepted work and revise only the failed responsibility layer when possible.
21. If the result is unusually strong, evaluate it as a Series Master for controlled variants.

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
- multi-agent action avoids artificial turn-taking when simultaneous pressure is intended
- stylized effects obey their Physics Lock
- environmental reactions provide believable evidence of force
- camera imperfection feels motivated rather than random
- character emotion remains continuous through spectacle
- the runtime prompt describes one coherent subject/body/camera state rather than concatenated competing shots
- both eyes maintain a coherent shared target and emotion wording does not destabilize eye anatomy

## Guiding maxim

**Preserve what matters, specify what changes, and leave freedom where variation can help.**
