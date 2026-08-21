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

### Emotional continuity

For action-heavy scenes, record the emotional state that must survive choreography.

- entry emotion:
- emotional transition:
- exit emotion:
- emotional behavior to avoid:

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

### Dense-action grammar

For combat, chase, sports, dance confrontation, panic, or other fast scenes:

```text
evade → parry → redirect → counter → sweep → recover
```

- connected verb chain:
- reset poses allowed? yes / no
- simultaneous actions allowed / required:
- momentum / redirection logic:
- required physical travel through space:

### Multi-agent interaction logic

- actor roles:
- who can act simultaneously:
- spatial blocking constraints:
- contact consequences:
- positions that must persist into the next beat:

---

## 7. Shot Graph

Represent the clip as entry states, events, consequences, and exit states.

```text
S0 [entry state / time]

E1 [event / time range]

C1 [physical / environmental consequence]

S1 [exit state / next entry state]

E2 [event / time range]

C2 [consequence]

S2 [exit state]
```

For every important state, record the story-critical invariants that must survive into the next beat.

### Emotional structure

Examples:

```text
observe → notice → suspend → connect → release
```

```text
impact → transition → reward
```

```text
fear → involuntary competence → shock → renewed pressure → uncertain resolve
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
- reacquisition behavior after fast action:
- focus recovery behavior:
- impact shake cause:

### Camera rule for action

State why the camera moves. Action readability should outrank camera spectacle.

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

### Micro-slow-motion emphasis

If used:

- trigger event:
- approximate duration:
- return-to-real-time behavior:
- reason this moment deserves emphasis:

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

### Reaction Evidence

For impacts, acceleration, or stylized force, describe world consequences that prove the event happened.

- dust / debris:
- paper / loose objects:
- clothing / fabric:
- hair:
- nearby props:
- floor / structural response:
- lighting / electrical response:
- lens / camera response:
- settling behavior:

Preferred causal sequence:

```text
physical event → local effect → secondary reaction → settling
```

---

## 13. Physics Lock

Use when the scene contains extraordinary speed, stylized energy, unusual impact effects, or any spectacle that could become arbitrary or magical.

### Source / cause

What physically creates the effect?

### Allowed manifestation

How may the effect appear?

### Forbidden manifestation

What visually similar but incorrect behavior must not occur?

### World reaction

How do nearby materials, objects, light, dust, hair, fabric, or camera react?

Example:

```text
Source: friction / physical contact
Allowed: brief branching static at contact points
Forbidden: beams, aura, projectiles, teleportation
World reaction: dust, loose paper, hair, and clothing respond to force and velocity
```

---

## 14. Audio DNA

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

## 15. Constraints

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
- no teleport-like displacement when physical travel is required:
- no artificial turn-taking when simultaneous pressure is intended:
- no repeated reset poses when continuous chaining is intended:

### Aesthetic constraints

- avoid excessive beauty filtering:
- avoid excessive HDR/sharpening:
- avoid excessive flare/bloom:
- avoid commercial posing unless intended:

---

## 16. Known Failure Modes

Record failures observed in previous generations.

- failure:
- likely responsibility layer:
- likely cause:
- accepted work to preserve:
- single-variable correction:

---

## 17. Model Adapter Notes

### Target model

### Input mode

### What the reference already provides

### What must be emphasized in text

### Negative prompting behavior

### Keyframe / start-end frame support

### Audio support

### Action / multi-agent behavior

- does the model follow timestamp blocks well?
- does it handle simultaneous actors reliably?
- does it benefit from compressed Action Grammar?
- how much camera complexity is safe?
- how does it interpret stylized physical effects?

### Adapter maturity

L0 / L1 / L2 / L3 / L4

---

## 18. Runtime Prompt

Compiled output for this specific model goes here.

Do not treat this section as the source of truth; revise the Master Spec first when creative intent changes.

---

## 19. Series Master / Variant Plan

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

## 20. Result Log

- model/version:
- settings:
- seed:
- result rating:
- identity rating:
- motion realism rating:
- temporal stability rating:
- action readability rating:
- multi-agent coherence rating:
- physics-lock adherence rating:
- reaction-evidence rating:
- approved clip grade: A / B / C / F
- successful primitive(s):
- accepted layers:
- failed layer(s):
- failures:
- next single-variable change:
- Series Master candidate: yes / no
