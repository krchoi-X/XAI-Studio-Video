# Master Creative Spec Template

Use this as the canonical, model-agnostic source document for a video generation task.

---

## Project

**Name:**

**Version:**

**Duration:**

**Aspect Ratio:**

**Generation Mode:** T2V / I2V / first-last frame / keyframe / reference video / other

**Reference Assets:**

---

## 1. Director Intent

Describe what the clip should feel like as an experienced moment, not merely what objects it contains.

- emotional tone:
- viewer relationship to subject:
- staged vs observed:
- most important moment:
- final memory / impression:

---

## 2. Character DNA

### Identity priority

P0 / P1 / P2

### Immutable identity features

- face:
- eyes:
- nose:
- mouth:
- skin tone:
- hair style / length:
- body proportions:
- wardrobe:
- accessories:

### Identity source

- source image(s):
- face anchor:
- body anchor:
- wardrobe anchor:

---

## 3. Reference State & Evidence

Describe only what is visibly supported by the reference. Separate observation from inference.

### Reference roles

- identity reference:
- wardrobe reference:
- prop reference:
- location reference:
- composition reference:
- spatial blocking reference:
- motion reference:
- audio / voice reference:

### Observable state

- subject pose:
- gaze:
- face orientation:
- body orientation:
- framing / crop:
- camera height / perspective character:
- foreground relationships:
- background relationships:
- visible props:
- movable environmental elements:
- light direction / hardness:
- visible material / texture cues:

### Unsupported inference to avoid

List assumptions that should not be promoted into the prompt unless independently verified.

---

## 4. Visual DNA

### Scene

- environment:
- season / time:
- atmosphere:

### Lighting

- source:
- direction:
- hardness:
- dynamic behavior:

### Color

- skin:
- highlights:
- shadows:
- saturation:
- black level:

### Optical / texture character

- depth of field:
- focus behavior:
- bloom:
- halation:
- flare:
- grain / scan texture:
- digital vs analog character:

---

## 5. Control Levels

### Hard Locks

Requirements that must remain stable for the result to be usable.

- identity:
- wardrobe / prop state:
- spatial relationship:
- story-critical continuity:
- required entry / exit state:

### Soft Guidance

Preferred direction or range.

- camera:
- expression intensity:
- motion amplitude:
- lighting character:
- pacing:

### Creative Freedom

Low-risk details the model may decide within bounds.

- micro gesture:
- blink timing:
- minor hair / fabric motion:
- incidental background motion:
- micro-expression timing:

---

## 6. Action Skeleton

Write the essential causal sequence before exact pose choreography.

Example:

```text
notices object → reaches → picks it up → hesitates → looks toward camera → settles
```

- required action chain:
- contact geometry that must be explicit:
- pose details that are actually story-critical:
- details intentionally left open:

---

## 7. Shot Graph

Represent the clip as entry states, events, and exit states.

```text
S0 [entry state / time]

E1 [event / time range]

S1 [exit state / next entry state]

E2 [event / time range]

S2 [exit state]
```

For every important state, record the story-critical invariants that must survive into the next beat.

### Emotional structure

Examples:

```text
observe → notice → suspend → connect → release
```

or

```text
impact → transition → reward
```

---

## 8. Camera DNA

- framing:
- focal character:
- camera height:
- camera distance:
- camera movement:
- handheld amplitude:
- push/pull:
- pan/tilt:
- roll:
- orbit:
- foreground occlusion:
- settling behavior:
- permitted imperfection / lag / overshoot:

---

## 9. Motion DNA

### Macro subject motion

- torso:
- arms:
- legs:
- head:

### Motion grammar

Describe causal sequence, e.g.:

```text
eyes shift → head follows slightly → motion settles
```

### Settling rule

Every movement should specify whether and how it settles.

---

## 10. Motion Budget

**Overall:** LOW / MEDIUM / HIGH

Suggested allocation:

- body:
- head:
- eyes:
- expression:
- hair:
- clothing:
- environment:
- camera:
- lighting:

### Forbidden additions

List motions the agent should not invent.

---

## 11. Micro Motion

- breathing:
- blink count / cadence:
- gaze behavior:
- head correction:
- expression change:
- hair strands:
- fabric response:

Default rhythm:

```text
stillness → subtle motion → stillness
```

---

## 12. Ambient Motion Field

- wind:
- plants:
- water:
- curtains / objects:
- hair:
- fabric:
- moving shadow:
- reflected light:
- haze / dust / humidity:
- camera breathing:

State the physical cause of each environmental motion.

---

## 13. Audio DNA

### Ambience

- foreground:
- background:

### Music

- genre / instrumentation:
- BPM:
- entry time:
- emotional peak behavior:
- ending:

### Mix events

```text
[time] ambience foregrounded
[time] music fades in
[time] music ducks
[time] reverb / fade-out
```

---

## 14. Constraints

### Hard identity constraints

- stable facial identity
- stable hair
- stable wardrobe
- stable body proportions

### Anatomy constraints

- hands:
- limbs:
- posture:

### Temporal constraints

- no flicker:
- no background morphing:
- stable lighting logic:
- stable object permanence:

### Aesthetic constraints

- avoid excessive beauty filtering:
- avoid excessive HDR/sharpening:
- avoid excessive flare/bloom:
- avoid commercial posing unless intended:

---

## 15. Known Failure Modes

Record failures observed in previous generations.

- failure:
- likely responsibility layer:
- likely cause:
- accepted work to preserve:
- single-variable correction:

---

## 16. Model Adapter Notes

### Target model

### Input mode

### What the reference already provides

### What must be emphasized in text

### Negative prompting behavior

### Keyframe / start-end frame support

### Audio support

### Adapter maturity

L0 / L1 / L2 / L3 / L4

---

## 17. Runtime Prompt

Compiled output for this specific model goes here.

Do not treat this section as the source of truth; revise the Master Spec first when creative intent changes.

---

## 18. Series Master / Variant Plan

If this result is unusually strong, decide whether it should become a Series Master.

### Anchors to preserve

- identity:
- world / location:
- visual tone:
- framing pattern:
- motion behavior:
- interaction pattern:

### Candidate variant axes

- scene:
- action:
- framing:
- wardrobe:
- mood:
- time / weather:

### Maximum simultaneous changes

Prefer one or a few intentional variation axes rather than uncontrolled full-scene mutation.

---

## 19. Result Log

- model/version:
- settings:
- seed:
- result rating:
- identity rating:
- motion realism rating:
- temporal stability rating:
- approved clip grade: A / B / C / F
- successful primitive(s):
- accepted layers:
- failed layer(s):
- failures:
- next single-variable change:
- Series Master candidate: yes / no
