# Storyboard Director Skill

## Purpose

Convert a rough story or scene idea into a **director-style Storyboard Spec draft** that preserves story intent, beat order, emotional weight, continuity, composition, and narrative tempo before expensive image or video rendering.

This skill is not a renderer. It is a directing and previsualization skill.

It should behave like a director preparing a continuity board for discussion, not like an image model that immediately freezes every visual decision.

The first output is always a **draft for collaborative revision**.

---

## Trigger

Use this skill when the user wants to:

- turn an idea into a storyboard or visual sequence
- plan a short film, vlog, scene, music-video beat, action scene, emotional sequence, graphic novel, comic, or illustration sequence
- decide beat/panel/shot order before expensive generation
- express tempo, long holds, inserts, slow motion, visual pauses, reveals, or emotional pacing
- prepare a storyboard reference for MiniMax H3 or another multimodal model
- create low-cost visual planning that can later feed a high-quality image renderer

Read `docs/storyboard-directing.md` before finalizing a storyboard plan.

---

## Core behavior

### 1. Interpret intent, do not merely literalize the request

Extract:

- dramatic premise
- emotional movement
- viewer attention path
- procedural or physical action
- relationship change
- reveal / payoff
- final impression

If the user says:

> She makes coffee, stays on her face longer, tries not to cry, then forces a smile while drawing latte art.

Do not produce only:

```text
espresso → steam → pour → latte art
```

Preserve the emotional structure:

```text
routine → crack in composure → suppression → continuation → fragile recovery → forced smile
```

### 2. Draft a Beat Sheet

For each beat specify:

- beat ID
- narrative purpose
- entry state
- action/change
- exit state
- emotional state
- key visual evidence
- continuity carried forward
- importance / survival priority

Use the minimum number of beats needed to express the scene clearly.

### 3. Assign a Narrative Tempo Map

For every beat estimate:

- tempo role
- relative weight
- attention hold: brief / normal / extended / dominant
- motion density
- camera/view energy
- emotional weight
- transition pressure
- optional video duration hint

Do not assume equal-duration or equal-size panels.

Tempo is medium-neutral. Do not reduce it to seconds unless the target medium needs seconds.

### 4. Choose visual language to serve the beat

For video-oriented planning, use shot language such as:

- WS / long shot for spatial relation, isolation, context
- MS / MCU for action plus emotion
- CU / ECU for emotional linger, detail, hesitation
- Insert for procedural or symbolic detail
- OTS for relational tension

For graphic-novel/comic planning, translate the same intent into:

- panel scale
- silent panel
- panel density
- page-turn reveal
- dialogue density
- negative space
- reading rhythm

Do not add unusual camera angles or panel tricks merely for visual variety.

### 5. Represent emotional holds explicitly

When a beat should linger:

- increase relative weight / attention hold
- reduce unnecessary motion or visual information
- state what subtle change remains
- explain why the audience should stay there

For video, this may become HOLD / slow push-in / static observational camera.
For sequential art, this may become a large silent panel, repeated close-up, or more negative space.

### 6. Use slow motion only when target medium is video

Specify:

- trigger
- what becomes readable during the slowdown
- approximate duration if needed
- return-to-real-time point

For static media, translate the same emphasis into panel scale, repetition, fragmentation, or another medium-appropriate device.

### 7. Preserve emotional continuity

Track emotion alongside action.

Physical action can continue while emotional tempo slows.

Example:

```text
hands continue steaming milk
while
face and breath enter a restrained emotional linger
```

### 8. Produce the Storyboard Spec before image generation

Each panel/shot specification should include:

- panel/shot number
- beat ID
- narrative purpose
- relative weight
- optional duration hint
- scale / framing
- composition
- camera/view behavior
- subject action
- emotional note
- transition
- continuity state
- relevant reference roles

The **Storyboard Spec**, not the rendered storyboard image, is the source of truth.

### 9. Render only after the plan exists

A rough storyboard image is a disposable previsualization artifact.

The storyboard renderer should optimize for:

1. composition
2. blocking
3. character recognizability enough for planning
4. expression readability
5. continuity
6. speed and cost

Do not require final-image polish.

Use `docs/storyboard-rendering.md` when compiling the spec for an image renderer.

### 10. Keep renderer/model choice replaceable

The approved Storyboard Spec should be usable by:

```text
cloud image model
local image model
5090-pod image model
future image model
video model adapter
graphic-novel panel renderer
```

Do not encode provider-specific safety rules, syntax, or aesthetics into the canonical Storyboard Spec.

### 11. Stop at draft and revise collaboratively

Label the first result `Storyboard Draft 0`.

Do not silently lock:

- final beat count
- final duration
- final panel count
- final camera/view style
- final emotional intensity
- final target renderer

Make assumptions visible so the user can revise them.

When the user changes one beat, preserve accepted beats unless continuity requires propagation.

The user is the final director.

---

## Default output structure

```text
# Storyboard Draft 0

## Director Intent

## Target Medium

## Emotional / Narrative Arc

## Beat Sheet

## Narrative Tempo Map

## Annotated Panel / Shot Plan

## Rough Storyboard Rendering Prompt

## Assumptions / Open Creative Decisions

## Review State
```

---

## Target-medium branching

### Video

Compile:

```text
Storyboard Spec
→ shot durations / cut rhythm / motion / camera / audio
→ video model adapter
```

### Graphic novel / comic

Compile:

```text
Storyboard Spec
→ panel size / page layout / silent beats / dialogue density / page-turn reveals
→ high-quality panel renderer
```

### Illustration sequence

Compile:

```text
Storyboard Spec
→ selected hero frames / ordering / visual pauses
→ high-quality image renderer
```

---

## MiniMax H3 handoff

When preparing H3 reference generation, separate roles explicitly:

```text
Character Reference
→ identity, hair, body, wardrobe

Storyboard Reference
→ beat order, framing, blocking, relative emphasis

Text Storyboard Spec / Runtime Prompt
→ dialogue, timing, emotional tempo, role assignment, continuity, details not reliably visible in the board
```

Do not rely on a storyboard image alone to communicate timing nuance.

MiniMax's official H3 documentation describes H3 as an omni-modal system and its H3-Context-IR as performing instruction parsing, cross-modal association, temporal understanding, and complex logical reasoning. Use that strength by clearly defining what each reference controls.

---

## Evaluation

A storyboard draft is good when:

- the user's story and emotional idea survive the translation into panels/shots
- the most important beat receives enough attention
- narrative tempo is visible even before final rendering
- visual framing serves attention rather than decoration
- procedural actions do not crowd out emotion
- continuity is clear between beats
- the storyboard can be revised one beat at a time
- the same approved spec can feed video, graphic novel, or illustration workflows
- rough storyboard quality can remain low without losing production information
- final image/video model choice remains replaceable

## Guiding maxim

**Direct the audience's story, time, and attention first; render it beautifully later.**