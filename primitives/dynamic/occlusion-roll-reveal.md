# Primitive: Occlusion Roll Reveal

**Family:** Dynamic

**Status:** draft / reference primitive

## Intent

Create a high-impact transition by using a foreground body/object sweep to cover the lens, hide a camera-state change, and reveal a new composition.

This is useful when a direct continuous transformation would be difficult for the model to render convincingly.

## Core temporal grammar

```text
impact approach
→ foreground object rapidly enlarges
→ full or near-full lens occlusion
→ hidden camera transformation
→ occlusion clears
→ reveal
→ motion decelerates
→ stable hold
```

## Canonical example

```text
extreme ground-level wide shot
→ subject steps toward lens
→ boot/leg dominates perspective
→ leg sweeps across lens
→ sole fully covers frame
→ camera rolls ~90° during full occlusion
→ occlusion clears into close facial reveal
→ movement settles into stable beauty hold
```

## Why it works

The occlusion acts as a visual bridge. Instead of forcing the generator to visibly interpolate every detail between two very different camera states, the difficult state change is hidden behind a motivated foreground obstruction.

## Shot Graph example

```text
S0 [0.0]
Ground-level ultra-wide view.

E1 [0.0–0.9]
Subject approaches; foreground limb rapidly enlarges.

E2 [0.9–1.6]
Sweep passes close to lens; perspective impact peaks.

E3 [1.6–1.9]
Full-frame occlusion with directional motion blur.

E4 [1.9–2.0]
Camera roll / hidden state transition.

S1 [2.0]
Close face reveal.

E5 [2.0+]
Motion decelerates and settles.
```

## Camera rules

- large camera-state change should happen during strongest occlusion
- preserve directional continuity across the hidden cut
- avoid stacking additional pan/orbit/zoom after reveal unless essential
- stabilize quickly after the reveal so the viewer can read the reward frame

## Occluder options

- foot / leg
- hand / palm
- fabric
- hair
- water splash
- foreground plant/object
- doorway / darkness

## Motion Budget

**MEDIUM to HIGH during transition, LOW after reveal.**

The contrast matters:

```text
high motion → occlusion → reveal → low motion
```

## Identity risk

Medium-to-high because the reveal can be interpreted as a new subject.

Mitigation:
- explicit identity lock
- use same reference identity across both states
- minimize expression change during reveal
- allow motion to settle immediately after transition
- use keyframes / first-last frame controls when available

## Common failures

### New face after reveal
Cause: hidden transition treated as scene replacement.
Correction: strengthen identity reference; reduce simultaneous style/wardrobe changes.

### Rubber leg / foot
Cause: excessive foreground deformation.
Correction: shorten peak deformation interval and describe the occlusion as a fast sweep rather than prolonged proximity.

### Transition visible through occluder
Cause: lens never becomes sufficiently covered.
Correction: request full-frame or near-full-frame occlusion before camera transformation.

### Chaotic second half
Cause: transition motion continues after reveal.
Correction: explicitly require rapid deceleration and a stable hold.

## Reusable structure

```text
ATTENTION HIT
→ MOTION BUILD
→ OCCLUSION
→ HIDDEN TRANSFORMATION
→ REVEAL
→ REWARD HOLD
```

This primitive should be adapted to model capability rather than copied literally.