# Character Eye Realism — Experimental Notes

## Status

**Experimental / candidate knowledge.**

Do not treat this as a permanent Character DNA rule until it improves repeated generations across more than one renderer and scene.

The immediate purpose is to test whether more physically coherent eye rendering makes a character feel more like a real person without pushing the image into forensic macro-detail or artificial hyperrealism.

---

## Why eyes matter

A portrait can have convincing skin, hair, and facial proportions and still feel synthetic when the eyes are visually inconsistent.

Common failure signals include:

- flat or painted-looking irises
- overly large or doll-like irises
- unnaturally white sclera
- catchlights that do not match the actual scene lighting
- eyes that look glossy but have no believable corneal reflection structure
- eyelids that appear disconnected from the eyeball
- excessive or uniform eyelashes
- identical eye rendering across unrelated lighting environments

The goal is **natural cinematic eye realism**, not maximum microscopic detail.

---

## Candidate Eye DNA

Character-stable properties may include:

- iris color
- approximate iris size
- eye shape
- limbal-ring strength
- eyelash character
- characteristic eyelid shape

Example compact block:

```text
natural dark-brown eyes, realistic iris size, subtle radial iris fibers, weak natural limbal ring, clean centered pupils, natural off-white sclera with extremely faint veins, subtle lower tear film, soft upper-eyelid shadow over the iris, individual natural eyelashes, no enlarged doll-like irises, no glassy artificial eyes
```

This block should remain concise. Do not keep adding microscopic descriptors unless a repeated generation failure proves they are useful.

---

## Scene-dependent eye rendering

Some eye properties should **not** be frozen into Character DNA because they are consequences of the current environment.

Scene-dependent properties include:

- catchlight shape
- catchlight direction
- corneal reflection intensity
- sclera brightness
- pupil dilation
- tear-film visibility
- eyelid shadow strength

These should be compiled from scene lighting / Visual DNA rather than treated as immutable character traits.

### Window light example

```text
soft rectangular window catchlight reflected naturally across both corneas, consistent in direction and intensity with the window light
```

### Overcast daylight example

```text
broad dim catchlight from an overcast sky, low-contrast corneal reflection
```

### Dim evening interior example

```text
small warm practical-light reflection mixed with faint ambient window reflection
```

---

## Core realism principle

**Catchlight is lighting evidence, not eye decoration.**

The eye should inherit the logic of the scene:

```text
scene light source
→ corneal reflection
→ eyelid / iris shading
→ believable eye appearance
```

Do not add generic "beautiful catchlights" when the reflection geometry contradicts the environment.

---

## Restraint rule

Avoid turning realistic eyes into exaggerated macro-photography artifacts.

Use cautiously:

- highly visible blood vessels
- extreme iris microstructure
- excessive wetness
- hard sparkling highlights
- very dark limbal rings
- excessive eyelash density

For grounded character work, prefer subtle evidence of anatomy and optics rather than aggressive detail.

---

## Validation protocol

Before promoting Eye DNA into the core character schema, run a simple A/B test.

Keep as many variables fixed as possible:

```text
A — current character prompt
B — same prompt + compact Eye DNA block
```

Evaluate:

- same-person recognizability
- natural iris appearance
- sclera realism
- lighting-consistent catchlights
- eyelid / eyeball integration
- absence of doll-eye or glass-eye appearance
- whether the eyes still fit the character's overall understated realism

Repeat under at least three lighting conditions:

1. soft indoor daylight
2. window-side directional light
3. dim evening interior

If the block improves results consistently, promote only the stable parts into Character DNA. Keep light-dependent parts in Visual DNA / renderer compilation.

---

## Design rule

Do not expand the Character DNA schema merely because a descriptor sounds useful.

Use this progression:

```text
observed failure
→ minimal candidate fix
→ A/B test
→ repeated improvement
→ promote to reusable Character DNA / adapter knowledge
```

This document records the candidate knowledge so it can be tested without prematurely turning it into a permanent studio rule.
