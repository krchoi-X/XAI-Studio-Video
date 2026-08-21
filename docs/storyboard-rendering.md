# Storyboard Rendering Guidance

## Purpose

Storyboard rendering is a **visualization step**, not the source of creative truth.

The canonical asset is the approved Storyboard Spec. A rough storyboard image exists to make composition, blocking, emotion, and tempo easier for humans and multimodal models to inspect.

The final high-quality image/video model may be chosen later.

---

## Core separation

```text
Storyboard Spec
        ↓
Rough Storyboard Renderer
        ↓
Human review / model reference
        ↓
Approved Storyboard Spec
        ↓
Target-medium renderer
```

The rough renderer and final renderer may be completely different models.

---

## Rough-board priorities

Optimize in this order:

1. panel/shot composition
2. spatial blocking
3. action readability
4. emotional expression readability
5. character recognizability sufficient for continuity
6. prop/location state
7. speed and cost
8. aesthetic polish

Do not spend expensive compute chasing final-quality skin, texture, lighting, anatomy, or finish in a disposable storyboard.

---

## Reference responsibility

Do not ask the rough storyboard itself to define final identity.

Prefer separate references:

```text
Character Reference
→ actual identity / body / hair / wardrobe

Storyboard Spec + Rough Board
→ composition / beat / blocking / emotion / tempo

Location / Prop Reference
→ reusable world and object anchors
```

This lets a crude board remain useful even if the drawing style or face quality is poor.

---

## Renderer Adapter principle

A storyboard renderer adapter converts the medium-neutral Storyboard Spec into model-specific instructions.

Possible backends include:

- cloud image services
- local open-weight models
- image models running on an ephemeral GPU pod
- future multimodal image/video models

Provider policy, syntax, safety behavior, and prompt conventions belong in the adapter, not in the Storyboard Spec.

This preserves creative work when providers change.

---

## Local vs pod vs cloud roles

### Local workstation

Best for:
- cheap repeated draft rendering
- quick composition experiments
- prompt/adapter testing
- low-resolution boards

### Ephemeral high-end GPU pod

Best for:
- larger open-weight image models
- higher-quality storyboard candidates
- final panel rendering
- character-reference expansion
- batch panel production

### Frontier cloud models

Best for:
- difficult interpretation
- high-value critique
- optional rendering when policy and subject matter fit

No backend should be mandatory.

---

## Final rendering after storyboard approval

For graphic novels or illustration sequences, generate final images **one panel at a time** when that improves control.

For each final panel combine:

```text
approved panel spec
+ Character DNA / references
+ location / prop references
+ target visual style
+ final image renderer adapter
```

Generate multiple candidates only for high-value panels or unresolved visual decisions.

Do not re-search the story at final-render cost.

---

## Video handoff

For video models that can understand storyboard images, use the rough board as a sequential visual reference while compiling the approved tempo and continuity information into text.

Do not assume the image alone communicates:

- exact duration
- emotional weight
- slow-motion trigger
- dialogue timing
- continuity priority
- reference roles

For MiniMax H3, the official system architecture explicitly includes multimodal relationship interpretation and temporal understanding through H3-Context-IR, so a storyboard can be valuable as one reference among character, location, video, and audio references. Reference roles should still be stated explicitly.

---

## Graphic novel handoff

Narrative tempo becomes page/panel grammar:

```text
extended emotional hold
→ larger or quieter panel

quick insert
→ small narrow panel

reveal
→ page turn / dominant panel

silence
→ reduced dialogue and stronger negative space
```

The same Storyboard Spec can therefore survive a change from video to graphic novel without rewriting the underlying story.

---

## Evaluation

A rough storyboard is successful when:

- the story reads despite low image quality
- the intended composition and blocking are visible
- emotional priority is obvious
- tempo differences are understandable
- continuity mistakes can be spotted cheaply
- the user can revise one beat/panel without rebuilding the entire sequence
- the board can guide multiple downstream renderers

## Guiding principle

**Use cheap images to decide expensive images. Use the Storyboard Spec to preserve the decisions.**