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

## 3. Visual DNA

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

## 4. Shot Graph

Represent the clip as states (S) and events (E).

```text
S0 [time]

E1 [time range]

S1 [time]

E2 [time range]

S2 [time]
```

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

## 5. Camera DNA

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

---

## 6. Motion DNA

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

## 7. Motion Budget

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

## 8. Micro Motion

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

## 9. Ambient Motion Field

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

## 10. Audio DNA

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

## 11. Constraints

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

## 12. Known Failure Modes

Record failures observed in previous generations.

- failure:
- likely cause:
- correction:

---

## 13. Model Adapter Notes

### Target model

### Input mode

### What the reference already provides

### What must be emphasized in text

### Negative prompting behavior

### Keyframe / start-end frame support

### Audio support

---

## 14. Runtime Prompt

Compiled output for this specific model goes here.

Do not treat this section as the source of truth; revise the Master Spec first when creative intent changes.

---

## 15. Result Log

- model/version:
- settings:
- seed:
- result rating:
- identity rating:
- motion realism rating:
- temporal stability rating:
- successful primitive(s):
- failures:
- next change:
