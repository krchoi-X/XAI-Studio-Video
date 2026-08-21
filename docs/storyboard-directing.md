# Director Storyboard & Tempo Guidance

## Purpose

A storyboard in XAI-Studio-Video is not merely a panel sequence showing what happens. It is a **directing document** that must preserve shot order, duration, emotional weight, camera behavior, and pacing.

The storyboard should answer two different questions:

1. **What happens?** — beat, action, spatial state, continuity.
2. **How long and how intensely does the viewer experience it?** — tempo, hold length, shot scale, camera energy, emotional emphasis.

A good storyboard is therefore closer to a film director's continuity board than to a comic strip.

---

## Core workflow

```text
User idea
→ interpret dramatic intent
→ draft Beat Sheet
→ assign Tempo Map
→ create Director's Annotated Storyboard draft
→ review with the user
→ revise timing / shot emphasis / emotion
→ only then compile references and runtime video prompt
```

Do **not** jump directly from a loose idea to a final storyboard or video prompt when timing and emotional emphasis are important.

The first storyboard is explicitly a **draft for collaborative revision**.

---

## 1. Interpret the idea before drawing panels

Translate the user's idea into a small set of dramatic beats.

Example idea:

> She makes coffee, but we stay on her face longer. She is trying not to cry. She forces a smile while drawing the latte art.

The storyboard should not reduce this to:

```text
make espresso → steam milk → pour milk → finish latte art
```

It should preserve the emotional structure:

```text
routine
→ emotional crack becomes visible
→ she suppresses it and continues working
→ routine becomes a coping mechanism
→ forced smile / quiet payoff
```

When procedural action and emotional action conflict, the storyboard must allocate enough time to the emotional beat.

---

## 2. Build a Beat Sheet

A beat is a meaningful change in action, information, emotion, or viewer attention.

Each beat should specify:

- beat ID
- narrative purpose
- entry state
- action or change
- exit state
- emotional state
- key visual evidence
- continuity carried forward

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
```

---

## 3. Add a Tempo Map

Panels are not assumed to have equal duration or equal importance.

For each beat define:

- `duration_sec`
- `tempo_role`
- `shot_weight`
- `motion_density`
- `camera_energy`
- `emotional_weight`
- `transition_pressure`

Suggested values:

### tempo_role

- observe
- establish
- linger
- accelerate
- transition
- recover
- reveal
- payoff
- release

### shot_weight

- LOW
- MEDIUM
- HIGH

### motion_density

- still
- subtle
- moderate
- active

### camera_energy

- locked
- static observational
- slow drift
- slow push-in
- active tracking
- reactive

### transition_pressure

- soft
- neutral
- sharp

Example:

```text
B1  1.2s  observe  MEDIUM  subtle  static observational  MEDIUM  soft
B2  2.4s  linger   HIGH    still   slow push-in          HIGH    soft
B3  1.3s  transition MEDIUM subtle locked                MEDIUM  neutral
B4  1.8s  recover  MEDIUM  subtle  slight drift          MEDIUM  neutral
B5  1.5s  reveal   MEDIUM  subtle  locked close-up       MEDIUM  soft
B6  2.0s  payoff   HIGH    still   hold                   HIGH    soft
```

The exact numbers are planning estimates, not frame-accurate guarantees.

---

## 4. Use shot duration as meaning

A shot's duration changes its narrative function.

The same close-up can mean different things:

```text
0.7s close-up  → reaction insert
2.5s close-up  → emotional linger
4.0s close-up  → confrontation / discomfort / intimacy
```

Therefore the storyboard should visibly distinguish:

- quick inserts
- normal coverage
- emotional holds
- slow-motion emphasis
- long observational shots

Do not let equal-sized panels imply equal time when the intended rhythm is unequal.

---

## 5. Director's Annotated Storyboard

Each panel should include or be accompanied by:

- shot number
- approximate duration
- shot size: WS / MS / MCU / CU / ECU / Insert / Top / OTS / other
- camera behavior
- subject action
- emotional note
- shot purpose
- transition note
- important continuity state

Useful annotations:

```text
2.4s
CU
HOLD
slow push-in
holding back tears
pause before cut
```

A storyboard image may use larger panels for longer or emotionally heavier beats and smaller panels for fast inserts.

Arrows and simple director marks may show:

- camera push / pull
- pan / tilt
- eye-line
- subject path
- rack focus
- hold
- slow motion
- whip transition

---

## 6. Long shots and slow motion

### Long / lingering shot

Use when the viewer must remain with an emotion, uncertainty, intimacy, or observational detail.

Specify:

- why the shot holds
- what subtle motion is permitted during the hold
- what would break the mood
- how the shot exits

### Slow motion

Slow motion is an emphasis tool, not decoration.

Specify:

- trigger event
- approximate real-time / slow-motion relationship if important
- what detail the viewer should read during the slowdown
- exact return-to-normal beat

Example:

```text
real-time pour
→ milk pattern begins to resolve
→ brief 0.5s perceptual slow-down emphasizing trembling hand and eye reflection
→ return to real time before the forced smile
```

---

## 7. Emotional Tempo

Track emotional timing separately from physical action.

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

A character may continue moving while the emotional tempo slows.

Example:

```text
hands continue steaming milk
while
face / breath enter a lingering emotional beat
```

This separation is essential for quiet drama, slice-of-life, romance, grief, suspense, and character vlogs.

---

## 8. Storyboard reference roles for video models

When the target model accepts reference images, declare the storyboard's job explicitly.

Example:

```text
Character Reference:
controls identity, face, hair, body, wardrobe.

Storyboard Reference:
controls sequential shot order, approximate framing, subject placement, camera viewpoint, emotional emphasis, and relative shot duration.
```

Do not assume the model will infer reference roles automatically.

For MiniMax H3 Ref2VA, treat the storyboard as one multimodal reference among others and state what it controls. H3's multimodal context system is designed to interpret relationships among text, images, video, and audio, but the studio should still make those relationships explicit.

---

## 9. Draft-first collaboration rule

The first storyboard is not final.

Default workflow:

```text
Draft 0
→ user reviews beat order, duration, shot emphasis, and emotional truth
→ revise
→ Draft 1
→ user reviews framing and continuity
→ revise
→ Approved Storyboard
```

When the user changes one beat, preserve accepted beats unless the change creates a real continuity dependency.

Do not regenerate the whole storyboard merely because one emotional or temporal decision changes.

---

## 10. Storyboard quality checks

Before generating storyboard images, verify:

- Is the emotional peak visible in the beat structure?
- Are long and short shots intentionally different?
- Does the Tempo Map explain why the scene feels fast, slow, tense, calm, or intimate?
- Are procedural actions subordinate to story purpose rather than mechanically exhaustive?
- Does each panel have a shot purpose?
- Are identity and continuity anchors carried between panels?
- Is slow motion used only where it improves readability or emotion?
- Is the final beat a meaningful payoff, release, or unresolved question?
- Can the storyboard be revised one beat at a time?

---

## Guiding principle

**A storyboard is not a list of pictures. It is a visible model of time, attention, and emotion.**