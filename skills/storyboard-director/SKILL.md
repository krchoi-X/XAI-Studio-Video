# Storyboard Director Skill

## Purpose

Convert a rough video idea into a **director-style storyboard draft** that expresses not only shot order, but also timing, emotional weight, camera intent, continuity, and pacing.

This skill is for planning before expensive video generation.

It should behave like a director preparing a first continuity board for discussion, not like an image prompt generator that immediately freezes every decision.

The first output is always a **draft for collaborative revision**.

---

## Trigger

Use this skill when the user wants to:

- turn an idea into a storyboard
- plan a short film, vlog, scene, music-video beat, action scene, or emotional sequence
- decide shot order before video generation
- express tempo, long holds, inserts, slow motion, or emotional pacing
- prepare a storyboard reference for MiniMax H3 or another multimodal video model

Read `docs/storyboard-directing.md` before finalizing a storyboard plan.

---

## Core behavior

### 1. Interpret intent, do not merely literalize the request

Extract:

- dramatic premise
- emotional movement
- viewer attention path
- procedural or physical action
- emotional peak
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
- purpose
- entry state
- action/change
- exit state
- emotional state
- key visual evidence
- continuity carried forward

Use the minimum number of beats needed to express the scene clearly.

### 3. Assign a Tempo Map

For every beat estimate:

- duration
- tempo role
- shot weight
- motion density
- camera energy
- emotional weight
- transition pressure

Do not assume equal-duration panels.

### 4. Choose shot language to serve the beat

Select framing based on dramatic purpose:

- WS / long shot for spatial relation, isolation, context
- MS / MCU for action plus emotion
- CU / ECU for emotional linger, detail, hesitation
- Insert for procedural or symbolic detail
- OTS for relational tension
- Top / low / ground-level only when it adds meaning

Do not add unusual camera angles merely for visual variety.

### 5. Represent long holds explicitly

When a beat should linger:

- increase estimated duration
- reduce motion density
- state what subtle motion remains
- indicate HOLD / slow push-in / static observational camera
- explain the reason for the hold

### 6. Use slow motion only as emphasis

Specify:

- trigger
- what becomes readable during the slowdown
- approximate duration
- return-to-real-time point

Do not use slow motion as generic cinematic decoration.

### 7. Preserve emotional continuity

Track emotion alongside action.

Physical action can continue while emotional tempo slows.

Example:

```text
hands continue steaming milk
while
face and breath enter a restrained emotional linger
```

### 8. Produce an annotated storyboard plan before image generation

Each panel specification should include:

- panel/shot number
- approximate duration
- shot size
- composition
- camera behavior
- subject action
- emotional note
- shot purpose
- transition
- continuity state

### 9. Produce a storyboard-image prompt only after the plan exists

The image prompt should ask for a director's continuity-board look, not merely a comic grid.

Require visible or clearly associated annotations for:

- shot number
- duration
- shot type
- camera direction
- emotional note
- hold / slow motion / transition where relevant

If timing differs strongly, allow panel sizes to differ to communicate visual weight.

### 10. Stop at draft and invite revision through the artifact itself

Label the result `Storyboard Draft 0`.

Do not silently lock:

- final duration
- final number of panels
- final camera style
- final emotional intensity

Instead, make the current assumptions visible so the user can revise them.

When the user changes one beat, preserve accepted beats unless continuity requires propagation.

---

## Default output structure

```text
# Storyboard Draft 0

## Director Intent

## Emotional Arc

## Beat Sheet

## Tempo Map

## Annotated Panel Plan

## Storyboard Image Prompt

## Assumptions / Open Creative Decisions
```

---

## MiniMax H3 handoff

When preparing H3 reference generation, separate roles explicitly:

```text
Character Reference
→ identity, hair, body, wardrobe

Storyboard Reference
→ shot order, framing, blocking, relative timing, emotional emphasis

Text Prompt
→ dialogue, temporal instructions, role assignment, details not reliably visible in the board
```

Do not rely on the storyboard image to communicate every timing nuance by itself. Compile the approved Tempo Map into the H3 runtime prompt.

---

## Evaluation

A storyboard draft is good when:

- the user's emotional idea survives the translation into shots
- the most important beat receives enough screen time
- shot duration has narrative purpose
- the camera serves attention rather than decoration
- long shots, close-ups, holds, inserts, and slow motion have distinct roles
- procedural actions do not crowd out emotion
- continuity is clear between panels
- the storyboard can be revised one beat at a time
- the eventual video model receives a clearer problem than the original loose idea

## Guiding maxim

**Direct the viewer's time and attention, not just the sequence of images.**