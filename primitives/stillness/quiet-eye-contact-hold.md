# Primitive: Quiet Eye-Contact Hold

**Family:** Stillness

**Status:** draft / reference primitive

## Intent

Create a realistic, intimate portrait moment in which the subject is mostly still, gradually notices the camera, makes brief direct eye contact, then releases the moment.

The goal is not 'animate the image.' The goal is to make a still composition feel briefly alive.

## Ideal use

- portrait I2V
- garden / beach / window / street observation
- memory-like short clips
- identity-sensitive generation
- scenes where emotional retention matters more than spectacle

## Motion Budget

**LOW**

- body: near-zero
- head: very low
- eyes: low-to-medium
- expression: very low
- hair: low
- clothing: very low
- environment: low
- camera: very low

## Core temporal grammar

```text
look away
→ eyes notice camera first
→ tiny head correction
→ optional single blink
→ quiet direct eye contact
→ near-imperceptible micro-smile
→ stillness
→ gaze gently releases
```

## Micro Motion rules

- natural breathing only
- about one blink in a ~10 s clip unless the model needs otherwise
- eyes lead gaze change
- head follows minimally
- torso stays stable
- expression changes by only a few perceptual degrees
- hair movement affects only a few strands
- clothing moves only if wind/body motion physically justifies it

## Camera

Preferred:
- observational framing
- subtle off-center composition
- minimal handheld breathing
- at most one slow push-in
- camera settles at eye-contact peak

Avoid adding camera movement solely to make the clip feel more cinematic.

## Ambient Motion Field

Use low-amplitude environmental motion to prevent the scene from feeling frozen:
- leaves / flowers move gently in one coherent breeze
- a few hair strands react to the same breeze
- fabric reacts slightly
- dappled light may shift only if leaves are moving
- foreground objects may drift partly across frame

## Emotional peak

During direct eye contact:
- reduce camera motion
- reduce subject motion
- allow the frame to breathe
- if audio exists, optionally lower music slightly and foreground ambience

## Identity risk

Low-to-medium if macro motion is kept small.

Risk rises sharply when:
- smile becomes large
- head rotates far
- camera pushes too close too fast
- wind animates the whole hairstyle
- the model invents continuous facial motion

## Positive constraints

Prefer wording such as:

```text
stable facial identity throughout
minimal subject motion
one natural blink
subtle gaze shift led by the eyes
near-still head and torso
very gentle breeze moving only a few strands of hair
camera becomes still during direct eye contact
```

## Common failures

### Floating face
Cause: continuous low-amplitude motion everywhere.
Correction: explicitly add settling phases and near-zero head motion.

### Beauty-ad smile
Cause: 'smile' interpreted too strongly.
Correction: use 'almost imperceptible softening at the corners of the mouth' or equivalent.

### Mechanical gaze
Cause: head turns as one rigid unit.
Correction: eyes first, tiny head correction second.

### Frozen environment
Cause: only subject motion specified.
Correction: add coherent low-amplitude ambient motion with a physical cause.

## Canonical rhythm

```text
stillness → awareness → connection → stillness → release
```