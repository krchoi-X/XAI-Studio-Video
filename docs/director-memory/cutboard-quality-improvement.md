# Cutboard Quality Improvement Notes

## Status

Reference and implementation guidance for the Director / Storyboard pipeline.

This document exists because the current workflow already follows a **storyboard-first** rule, but recent storyboard results have not consistently met the user's expectations. The problem is therefore **not the absence of a storyboard step**. The problem is the quality of the planning that happens *before* the grid is generated, and how reliably that grid can be translated into executable video shots.

This note uses a KAWANE-style ryokan brand-film example as a practical reference pattern. The useful lesson is the workflow structure and shot-planning discipline, not the literal visual style, shot order, nine-panel format, or brand-advertising aesthetic.

---

## Diagnosis

Recent storyboard/cutboard generation can still fail in several ways even when a grid is produced:

- visually pleasing panels without a clear shot function;
- panels that look like a collection of attractive stills rather than a video plan;
- weak emotional or temporal progression;
- candidate A/B differing only cosmetically;
- overloaded panels that ask one shot to perform several actions;
- generic face-first openings or repeated default compositions;
- panels that are difficult for the selected video renderer to execute;
- continuity that looks plausible in the grid but does not provide enough motion/transition logic for video reconstruction;
- optimizing for image-model beauty instead of motion-model usability.

The pipeline should therefore upgrade from **"make a storyboard first"** to **"plan shot functions first, then visualize them as a cutboard."**

---

## Core upgrade: cut-function allocation before grid generation

Before any storyboard grid image is generated, assign a primary purpose to every panel.

Typical functions include:

- `establish_space`
- `reveal_character`
- `introduce_object_or_service`
- `tactile_or_sensory_detail`
- `character_action`
- `emotional_release`
- `time_transition`
- `meal_or_ritual`
- `environment_pause`
- `closing_image`
- `brand_or_title_endcard`

A panel may support secondary purposes, but it should have **one dominant function**.

The system should be able to answer:

> Why does this shot exist, and what would be lost if it were removed?

If there is no good answer, the panel is probably decorative rather than structurally useful.

---

## Recommended planning flow

```text
Episode Brief / Scenario
        ↓
Visual Language Translator
        ↓
Directing Mode + Skill / Technique Routing
        ↓
Cut Function Allocation
        ↓
Panel Planning State
        ↓
Storyboard / Cutboard Grid Generation
        ↓
Human Review
        ↓
Video Reconstruction Prompt Compiler
        ↓
Renderer-specific feasibility adaptation
        ↓
Video Generation
        ↓
Result Review / Director Memory Update
```

The storyboard image is a **visualization of a planned shot structure**. It must not become the mechanism that invents the shot structure by itself.

---

## Minimum panel planning state

The image model should receive a board prompt compiled from structured planning state such as:

```yaml
panel_id: P01
shot_function: establish_space
subject: character approaching the destination
location: exterior entrance
continuity_unit: ryokan_afternoon_arrival
time_of_day: afternoon
framing: wide
camera_angle: eye_level
camera_distance: environmental_wide
dominant_action: character walks toward entrance
continuity_anchor: wardrobe + bag + architecture + autumn landscape
mood: restrained anticipation
reason_for_existence: establish destination, geography, and tone before intimate details
video_feasibility: easy
```

Do not require every field in every production implementation immediately. The important conceptual additions are:

- `shot_function`
- `dominant_action`
- `reason_for_existence`
- `video_feasibility`

These are the fields most likely to improve board quality beyond "pretty stills."

---

## One shot = one dominant action or emotional beat

Use the following default rule:

> Each panel should contain one dominant action or one emotional beat.

Examples:

Bad:

> The character enters the room, looks around, smiles, sits down, takes a cup, drinks, and relaxes.

Better:

> The character stops at the large window and looks toward the autumn valley.

Better next shot:

> Seated by the window, the character raises the cup and takes one sip.

This rule should be applied both to storyboard panels and to the video reconstruction timeline.

Decorative inserts are allowed when they serve pacing, sensory atmosphere, continuity, or a deliberate visual pause.

---

## Storyboard prompt and video prompt must be separate artifacts

### Storyboard / cutboard prompt

Optimize for:

- cut allocation;
- composition;
- character and wardrobe continuity;
- location / prop continuity;
- time-of-day progression;
- object / environment inserts;
- visual rhythm across panels;
- human review of the overall plan.

### Video reconstruction prompt

Optimize for:

- reconstructing each panel as a full-frame moving shot;
- one dominant action per shot;
- per-shot timing;
- camera motion where justified;
- edit transitions;
- sound and ambience;
- continuity handoff;
- renderer feasibility;
- explicit instruction that the storyboard grid itself must not appear in the output.

A useful reconstruction contract is conceptually:

```text
Use the approved storyboard as the reference for character identity,
wardrobe, location, props, visual tone, and composition baseline.
Reconstruct each panel as an independent full-frame live-action shot.
Do not display the storyboard grid, panel numbers, separators, or planning labels.
```

The renderer should **time and animate an approved visual plan**, not reinvent the directing structure from scratch.

---

## Candidate A/B diversity requirement

Candidate diversity must be structural.

Example:

```text
Candidate A
mode: observational / calm
opening: environment-first
base grammar: restrained static / slow movement
selected skills:
- environment-first opening
- continuity-first staging
selected techniques:
- frame-within-frame
- gentle push-in

Candidate B
mode: intimate / detail-led
opening: tactile detail-first
base grammar: inserts + closer subject scale
selected skills:
- object-first opening
- interaction-state handling
selected techniques:
- macro insert
- rack focus
```

Do not approve A/B as meaningfully different if they merely change lens wording, crop, or minor shot order while preserving the same visual grammar.

---

## Board-format presets

Do not treat nine panels as the universal storyboard format.

Useful initial presets:

```text
brand_9panel
- polished short brand / hospitality / product mood film

vlog_6panel
- short character vlog with environment, action, object, and character beats

drama_4to6panel
- emotion / blocking / continuity prioritized over montage density

travel_montage_8panel
- location / movement / food / object / character variation with rhythmic cuts
```

Presets should be **starting structures**, not hard templates.

A preset may suggest default functions, for example:

```text
brand_9panel
1 establish
2 character observation
3 tactile/service detail
4 character interaction
5 sensory/environment pause
6 emotional relaxation
7 product/meal/core-value detail
8 emotional peak
9 closure / brand image
```

The Director should be allowed to change or collapse these functions when the episode does not need them.

---

## Video-feasibility assessment before approval

A beautiful board can still be a poor video plan.

Before board approval, assess each shot with a lightweight rating such as:

```text
easy
- static object insert
- water surface
- seated one-step action
- food top shot

medium
- door opening
- short walk
- small camera push
- one clean hand-object interaction

risky
- long multi-step action chain
- complex handoff + body turn + dialogue in one shot
- difficult camera move with identity preservation
- precise text/logo transformation inside motion
```

Renderer-specific history should refine these ratings over time.

Do not globally ban a valid filmmaking idea because one renderer performs it poorly. Record the risk and fallback instead.

---

## Review checklist

A cutboard should not be approved merely because it looks attractive.

Before approval, check:

1. Does every panel have a clear shot function?
2. Can the emotional or informational progression be understood without reading the original prompt?
3. Is time progression coherent when time matters?
4. Are character identity, wardrobe, props, and location state consistent?
5. Does every panel translate into an executable video shot?
6. Is each panel dominated by one action or emotional beat?
7. Are character-free, object-led, or environment-led shots used when they improve rhythm or storytelling?
8. Is the opening deliberate rather than a generic face-first default?
9. Does the final panel provide closure, destination, or end-card space when appropriate?
10. Are Candidate A and Candidate B genuinely different in directing mode?
11. Are any panels present only because they look pretty?
12. Does any shot exceed the practical capabilities of the chosen renderer without a fallback?

Warnings should invite revision, not automatically hard-block all production.

---

## Important quality principle

> Do not optimize the storyboard only for aesthetic still-image quality.
> Optimize for shot function, emotional readability, continuity, video feasibility, and clean translation into renderer-friendly motion prompts.

A storyboard can be less visually spectacular as a still grid and still be superior if it produces a better moving sequence.

---

## What the KAWANE reference demonstrates

The reference example is useful because it separates two tasks clearly:

### Image stage

The image model is asked to decide / visualize:

- shot sequence;
- character and wardrobe continuity;
- location style;
- time progression;
- sensory inserts;
- closing composition;
- text-safe end-card space.

### Video stage

The video model is then asked to:

- treat the grid as the reference board;
- reconstruct panels as independent full-screen shots;
- animate a small action in each shot;
- preserve character / place / costume consistency;
- add timing, transitions, ambience, music, and voiceover;
- avoid morphing between shots;
- avoid showing the storyboard itself.

The useful transfer principle is therefore:

> **The image board establishes visual decisions; the video model temporalizes and animates those decisions.**

Do not copy the reference's ryokan style, nine-shot order, slow luxury mood, or brand-film look as a universal default.

---

## Codex implementation guidance

When this is implemented, keep the first change small.

Prefer:

```text
existing episode brief
→ structured cut-function plan
→ existing storyboard grid prompt path
→ board review artifact
→ selected board
→ separate video reconstruction prompt artifact
```

Do not respond to this guidance by creating a new orchestration platform, replacing the current gallery, or expanding the schema into a professional film-production database.

The highest-value implementation changes are likely:

1. add `shot_function`, `dominant_action`, `reason_for_existence`, and `video_feasibility` to the planning stage;
2. add a pre-grid cut-function allocation pass;
3. add real A/B directing-mode divergence;
4. keep storyboard prompt and video reconstruction prompt as separate artifacts;
5. add board-format presets without making them mandatory;
6. add a lightweight board-quality review pass before video generation.

Only automate additional complexity after real productions show repeated friction.

---

## User role

The user should not need professional directing knowledge.

The system should present enough information for simple judgments such as:

- Candidate A is better.
- Shot 1 feels generic.
- Shot 4 is unnecessary.
- The ending is weak.
- The board is visually attractive but does not feel like a good video.

The Director AI is responsible for translating that taste feedback into stronger shot planning and updating durable lessons when the evidence is meaningful.
