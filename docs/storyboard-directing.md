# Director Storyboard & Tempo Guidance

## Purpose

A storyboard in XAI-Studio is not merely a panel sequence showing what happens. It is a **medium-neutral directing document** that preserves story intent, shot/panel order, emotional weight, spatial relationships, continuity, and narrative tempo before expensive rendering.

The storyboard should answer three questions:

1. **What happens?** — beat, action, information, spatial state, continuity.
2. **How does the audience experience it?** — attention, emphasis, emotional linger, reveal, rhythm.
3. **How should that intent later be expressed in a target medium?** — video timing and motion, graphic-novel panel weight, or illustration sequencing.

The rough storyboard image is disposable. The canonical asset is the **Storyboard Spec**: Beat Sheet + Tempo Map + Panel/Shot Specs + continuity state + approved creative decisions.

---

## Core workflow

```text
User idea
→ interpret dramatic intent
→ draft Beat Sheet
→ assign Narrative Tempo Map
→ create Storyboard Spec Draft 0
→ optionally render a low-cost rough storyboard
→ review with the user
→ revise beats / tempo / emotion / framing
→ Approved Storyboard Spec
→ branch to target-medium adapter
```

Do **not** jump directly from a loose idea to a final image or video prompt when story, tempo, or emotional emphasis matters.

The first storyboard is explicitly a **draft for collaborative revision**.

---

## 1. Interpret the idea before drawing panels

Translate the user's idea into dramatic and visual beats rather than literal task steps.

Example idea:

> She makes coffee, but we stay on her face longer. She is trying not to cry. She forces a smile while drawing the latte art.

Do not reduce this to:

```text
make espresso → steam milk → pour milk → finish latte art
```

Preserve the emotional structure:

```text
routine
→ emotional crack becomes visible
→ she suppresses it and continues working
→ routine becomes a coping mechanism
→ forced smile / quiet payoff
```

When procedural action and emotional action compete for space, allocate attention to the emotional beat that carries the scene's meaning.

---

## 2. Build a Beat Sheet

A beat is a meaningful change in action, information, emotion, relationship, or viewer attention.

Each beat should specify:

- beat ID
- narrative purpose
- entry state
- action or change
- exit state
- emotional state
- key visual evidence
- continuity carried forward
- importance / survival priority

Example:

```text
B2 — Emotional Linger
Purpose: reveal that she is barely holding herself together
Entry: espresso routine is still normal
Action: she pauses; eyes lower; breath tightens
Exit: she regains enough control to continue
Emotion: restrained sadness, not open crying
Visual evidence: wet eyes, slight jaw tension, tiny inhale
Continuity: hands remain in work position; no melodramatic collapse
Importance: HIGH
```

Use the minimum number of beats required for the story to read clearly.

---

## 3. Narrative Tempo Map

Tempo is a story property before it becomes a video-duration property.

For each beat define:

- `tempo_role`
- `relative_weight`
- `attention_hold`
- `motion_density`
- `camera_or_view_energy`
- `emotional_weight`
- `transition_pressure`
- optional `video_duration_hint`

Suggested `tempo_role` values:

- establish
- observe
- linger
- accelerate
- transition
- recover
- reveal
- payoff
- release
- cliffhanger

Suggested `attention_hold` values:

- brief
- normal
- extended
- dominant

Suggested `motion_density` values:

- still
- subtle
- moderate
- active

Suggested `transition_pressure` values:

- soft
- neutral
- sharp

Example:

```text
B1 observe     MEDIUM  normal   subtle  MEDIUM  soft
B2 linger      HIGH    extended still   HIGH    soft
B3 transition  LOW     brief    subtle  MEDIUM  neutral
B4 recover     MEDIUM  normal   subtle  MEDIUM  neutral
B5 reveal      MEDIUM  normal   subtle  MEDIUM  soft
B6 payoff      HIGH    extended still   HIGH    soft
```

If the target is video, duration hints may be added. They are planning estimates, not frame-accurate guarantees.

---

## 4. Tempo adapts differently by medium

The same narrative tempo should survive even when the output medium changes.

### Video

Tempo may become:

- shot duration
- cut rhythm
- camera speed
- slow motion
- hold length
- silence / audio density

### Graphic novel / comic

Tempo may become:

- panel size
- panel density
- silent panel
- page-turn reveal
- close-up emphasis
- amount of dialogue
- gutter rhythm

### Illustration sequence

Tempo may become:

- image ordering
- focal hierarchy
- repeated motif
- hero-frame selection
- visual pause between high-information images

A long emotional video close-up may become one large silent comic panel. A quick insert may become a small narrow panel. Preserve the **narrative function**, not the literal video timing.

---

## 5. Storyboard Spec is the source of truth

Do not treat the rendered storyboard sheet as canonical.

The source of truth should be structured text or data that records:

```text
story intent
beat order
narrative tempo
shot/panel purpose
composition
character state
prop/location continuity
emotion
reference roles
accepted/rejected decisions
```

A rough storyboard image exists to help humans and multimodal models understand the spec visually. It may be low-quality and inexpensive.

This allows the same approved storyboard to feed:

```text
Video Adapter
Graphic-Novel Adapter
Illustration-Sequence Adapter
Storyboard Renderer
```

without rebuilding the story from scratch.

---

## 6. Director's Annotated Storyboard

Each panel should include or be accompanied by:

- panel / shot number
- beat ID
- narrative purpose
- relative weight
- optional duration hint
- shot / panel scale
- framing and composition
- camera/view behavior
- subject action
- emotional note
- transition note
- continuity state
- annotation marks

Useful annotations:

```text
EMOTIONAL HOLD
CU / ECU
slow push-in
silent beat
page-turn reveal
holding back tears
pause before transition
```

A storyboard renderer may use larger panels for emotionally heavier or longer beats and smaller panels for fast inserts.

Arrows and director marks may show:

- camera push / pull
- pan / tilt
- eye-line
- subject path
- rack focus
- hold
- slow motion
- whip transition
- reading direction

---

## 7. Long holds, slow motion, and visual pauses

### Emotional / observational hold

Use when the audience must remain with an emotion, uncertainty, intimacy, or detail.

Specify:

- why the beat holds
- what subtle change is allowed
- what would break the mood
- how the beat exits

### Slow motion

Slow motion is a target-video emphasis tool, not generic decoration.

Specify:

- trigger event
- what must become readable
- approximate slowdown if useful
- return-to-real-time cue

### Non-video equivalent

When adapting to a static narrative medium, translate the same intention into panel scale, silence, repetition, negative space, page structure, or another appropriate device.

---

## 8. Emotional Tempo is separate from physical action

Track emotional timing alongside physical action.

Example:

```text
routine calm
→ hesitation
→ suppressed sadness
→ self-control
→ fragile composure
→ forced smile
→ unresolved release
```

A character may continue moving while emotional tempo slows:

```text
hands continue steaming milk
while
face / breath enter an emotional linger
```

This separation is essential for quiet drama, slice-of-life, romance, grief, suspense, action-with-character, and character vlogs.

---

## 9. Reference roles

Do not ask one reference image to control everything.

Typical roles:

```text
Character Reference
→ identity, face, hair, body, wardrobe

Storyboard Reference
→ beat order, framing, blocking, viewpoint, relative emphasis

Location / Prop Reference
→ reusable world and object anchors

Text Storyboard Spec
→ tempo, emotion, timing, dialogue, continuity, role definitions
```

For MiniMax H3 Ref2VA, the storyboard can be one multimodal reference among others. H3 is explicitly designed to interpret relationships among text, images, video, and audio, but reference roles should still be stated in the text prompt. MiniMax's official H3 documentation describes H3-Context-IR as performing instruction parsing, cross-modal association, temporal understanding, and complex logical reasoning before generation.

---

## 10. Renderer independence

Storyboard generation and final rendering are separate responsibilities.

```text
Approved Storyboard Spec
        ↓
Storyboard Renderer Adapter
        ├─ cloud image model
        ├─ local image model
        ├─ 5090-pod image model
        └─ future model
```

The studio must not depend on one image provider's policy, aesthetics, availability, or model behavior.

The first rough board should optimize for:

1. character recognizability enough for planning
2. composition
3. blocking
4. expression readability
5. continuity
6. speed / cost

It does **not** need final-image skin, texture, lighting, or anatomy quality.

High-quality images are generated later, panel by panel, using whichever image model best fits the project.

See `docs/storyboard-rendering.md`.

---

## 11. Draft-first collaboration rule

Default workflow:

```text
Draft 0
→ user reviews story truth, beat order, tempo, emphasis
→ revise only affected beats
→ Draft 1
→ user reviews framing, continuity, and medium assumptions
→ Approved Storyboard Spec
```

When one beat changes, preserve accepted beats unless continuity genuinely requires propagation.

The AI proposes a directorial interpretation; the user remains the final director.

---

## 12. Storyboard quality checks

Before rendering a storyboard, verify:

- Does the story have a visible emotional or informational change?
- Is the emotional peak or reveal given enough relative weight?
- Are quick and lingering beats intentionally different?
- Does the Tempo Map explain why the sequence should feel fast, slow, tense, calm, awkward, intimate, or explosive?
- Are procedural actions subordinate to story purpose rather than mechanically exhaustive?
- Does each panel have a narrative purpose?
- Are character, wardrobe, prop, and location states carried between panels?
- Could the same Storyboard Spec be adapted to video or static sequential art without losing the story?
- Can one beat be revised without rebuilding the rest?
- Are final renderer/model choices still replaceable?

---

## Guiding principle

**A storyboard is not a list of pictures. It is a reusable model of story, time, attention, space, and emotion.**