# Lightweight Visual-Language Production Pipeline

## Why this exists

The user is not trying to become a professional film director or reproduce a commercial feature-film production process. The target is practical: make character-driven vlogs and shorts that feel intentional, visually varied, spatially coherent, and producible with the available AI image/video tools.

A professional filmmaker's workflow is valuable as a source of reusable structure, but the human user should not be required to supply ten years of directing knowledge. Repetitive directing judgment should be delegated to AI, while the user retains taste, selection, revision, and final approval.

This document defines the minimum useful pipeline between scenario/episode intent and actual image/video generation.

## Core principle

Do not jump directly from prose such as "Noa records her first vlog" to a renderer prompt.

Use explicit intermediate representations:

```text
Episode idea / scenario
        ↓
Visual Language Translator
        ↓
Text storyboard candidates
        ↓
Director Memory + Capability check
        ↓
Storyboard Prompt Compiler
        ↓
Scene-grid storyboard images
        ↓
Human selection / revision
        ↓
Approved shot plan
        ↓
Renderer-specific compilation
        ↓
WanGP / H3 / image model / editor
        ↓
Result review
        ↓
Director Memory update
```

The intermediate layers exist to preserve directing intent across different LLMs and different chat sessions.

## User role vs AI role

### User owns

- story/episode intention;
- character and world canon;
- subjective taste;
- choosing between 2 strong alternatives;
- short revision notes such as "too cramped", "too ad-like", "show the room first", or "A is better";
- final approval and veto.

### AI owns

- translating scenario meaning into visual language;
- deciding whether information is best shown through space, action, object, expression, sound, or dialogue;
- proposing reveal order;
- choosing plausible shot scale and camera placement;
- comparing `long_take`, `multi_cut`, and `hybrid` construction;
- checking spatial continuity and prop/action continuity;
- avoiding previously recorded failure patterns;
- respecting current renderer capabilities and limits;
- compiling the approved storyboard into production prompts and artifacts.

The user should not need cinematography expertise to operate this system.

## Quality target

The pipeline is not designed to reach commercial feature-film precision. It should reliably achieve:

- a deliberate opening rather than an accidental model cliché;
- understandable spatial relationships;
- natural character action;
- sensible cut/beat transitions;
- visual-scale variation where appropriate;
- continuity of important objects, wardrobe, position, and state;
- a plan that the available AI tools can actually generate;
- enough visual distinction between episodes that the system does not feel templated.

Do not add professional film-production complexity unless repeated production failures justify it.

## Stage 1 — Episode brief / scenario

Input may be short and non-technical.

Example:

> Noa wakes late, makes coffee, and looks out the window before starting her day.

The user should not be forced to specify lens, coverage, blocking, edit rhythm, or shot list.

The episode brief should preserve only story intent, character state, relevant location, and any required event.

## Stage 2 — Visual Language Translator

This layer converts narrative meaning into visual choices before shot prompts are written.

Before choosing camera technique, it should first establish the scene's **dramatic goal, information flow, emotional progression, and shot functions**. Shot order controls information release, so individually attractive shots are not enough if their relationship is unclear.

Use three continuity layers when relevant:

- **Physical continuity** — position, hand/prop/contact state, wardrobe, layout, lighting/state.
- **Informational continuity** — what the audience knows, what is withheld, eyeline/reveal relationships, questions passed to the next cut.
- **Emotional continuity** — what feeling the current shot creates and what emotional state it hands to the next cut.

It should answer internally:

- What is the scene trying to make the viewer notice or feel?
- What information should be shown first, and what should be delayed?
- Should the episode begin with character, environment, object, action, sound, aftermath, or detail?
- Is dialogue necessary immediately, or can action precede speech?
- Should the camera behave as observer, placed self-recording camera, handheld participant, or another clear viewpoint?
- Would one continuous take strengthen the scene, or would cuts improve rhythm/clarity?
- What spatial or continuity facts must survive between beats?
- Which ideas are risky or expensive with the current video model?

The translator should not output a single universal answer. It should define a small creative search space.

## Stage 3 — Two storyboard candidates

Default output: **two meaningfully different candidates**.

Recommended bias:

- Candidate A: production-safe / continuity-first.
- Candidate B: visually distinctive / more exploratory.

The candidates should differ in directing logic, not merely wording.

Useful axes include:

- `long_take` vs `multi_cut`;
- character-first vs environment-first;
- object-first vs body/action-first;
- close-to-wide reveal vs wide-to-intimate progression;
- observer camera vs clearly placed self-recording camera;
- restrained rhythm vs graphic/rhythmic editing.

Do not force every episode to use the same opening family.

## Stage 4 — Director Memory check

Before finalizing candidates, read the relevant Director Memory:

- known failure patterns;
- approved storyboard examples;
- demonstrated user preferences;
- current capabilities and limitations.

Failure knowledge is a warning, not a permanent ban.

Example:

- Recorded failure: vague "vlog introduction" repeatedly defaulted to a generic face-filling selfie that hid body language and space.
- Wrong rule: never use close-up vlog openings.
- Correct use: consciously choose the opening strategy. A close-up is valid when it serves the episode, but should not appear merely as a statistical default.

## Stage 5 — Lightweight shot representation

Keep each shot/beat compact. Add **shot function** as the clearest expression of why the shot exists; do not choose a "cool" angle before deciding what information/emotion the shot must deliver.

Default required fields:

1. **Shot function** — establish / question / reveal / reaction / decision / payoff / transition, etc.
2. **Framing** — close / medium / knee-up / full / wide, etc.
3. **Camera** — position/support/viewpoint and only necessary movement.
4. **Action** — one readable action beat.
5. **Continuity anchor** — physical state plus, when relevant, informational/emotional handoff to adjacent shots.
6. **Duration** — approximate beat length.
7. **Production route** — still/reference/control needs and expected renderer path.

Optional fields may be added only when they solve a real production need.

Do not turn every vlog shot into a professional cinematography worksheet.

## Stage 6 — Scene continuity units

For storyboard-image generation, group panels by **visual continuity unit**, not as unrelated independent images.

A continuity unit normally shares:

- location;
- time / lighting condition;
- character state;
- wardrobe;
- relevant props;
- overall spatial layout.

This is similar to a conventional scene but should be defined pragmatically for AI production. The same physical room in morning and night may be separate continuity units.

Example:

```yaml
scene_id: noa_room_morning_01
location: noa_room
time: late_morning
wardrobe: homewear_A
lighting: soft_window_daylight
character_state: just_woke_up
persistent_props:
  - phone_on_bedside_table
  - coffee_mug_after_kitchen_beat
```

## Stage 7 — Storyboard Prompt Compiler

Do not ask each AI model to reinvent storyboard-image prompting from scratch.

Compile text storyboard beats into a stable prompt representation that can be adapted to the active image model.

The compiler should preserve:

- scene identity;
- panel/shot ID;
- subject scale;
- viewpoint/camera placement;
- character placement and orientation;
- action state;
- important foreground/midground/background relationships;
- persistent props;
- lighting baseline;
- continuity from previous panel;
- which details are identity-critical vs merely temporary styling/state.

The compiler should avoid unnecessary photographic jargon when a simpler description is more reliable.

## Stage 8 — Scene-grid storyboard generation

Generate storyboard images **per continuity unit as a grid/contact sheet when the image model supports it well**.

Example 6-panel grid:

```text
[wide establish] [medium action] [detail object]
[full body]      [OTS / POV]     [close reaction]
```

Why use grids:

- multiple views share the same scene context;
- room layout and lighting are less likely to drift;
- wardrobe and prop state can remain more coherent;
- the user can compare shot relationships quickly;
- the grid acts as a review artifact before expensive video generation.

The storyboard grid is a planning artifact, not necessarily the final production still. After approval, critical shots may be regenerated individually at higher fidelity with canonical references.

## Stage 9 — Human review

Show the user the small number of meaningful alternatives rather than raw internal reasoning.

Expected user feedback should be lightweight:

- choose A or B;
- reject both;
- one or two short changes;
- flag a shot as visually wrong or too generic.

The pipeline should then revise only what is necessary.

## Stage 10 — Production compilation

Once approved, compile the storyboard into the actual production route.

Examples:

- canonical/reference still → WanGP/H3 I2V;
- H3 reference mode for identity-sensitive shots;
- control/motion reference for specific body movement;
- separate clips for beats that are too complex for one generation;
- one continuous clip where continuity and natural observation matter more than edit rhythm;
- approved low/mid-resolution generation first, upscale only final masters.

Do not let the renderer decide shot order or directing intent that should already have been fixed upstream.

## Stage 11 — Automatic checks before generation

AI should check these without requiring the user to understand film grammar:

- Did character/object position jump implausibly between adjacent shots?
- Did an important prop disappear or switch hands?
- Does an action have a readable handoff into the next shot?
- Are all shots accidentally the same scale?
- Is the opening merely a generic model cliché?
- Is the same information being shown repeatedly?
- Is one generated clip being asked to perform too many sequential actions?
- Does the proposed camera movement exceed what the chosen model reliably handles?
- Is the shot actually producible with the available references/tools?

These are assistance checks, not absolute creative prohibitions.

## Stage 12 — Learning loop

After real production, record evidence in Director Memory.

Record:

- selected candidate;
- user revision reason;
- whether the shot was successfully produced;
- notable model/tool limitation;
- repeated failure worth remembering;
- successful directing principle worth reusing.

Do not store every temporary experiment. Promote only durable lessons.

## Multi-model use

Claude, Grok, Hermes/Meromero, ChatGPT, or another model may all use this pipeline.

They should share:

- Director Memory;
- character/world canon;
- current Capability Registry;
- output schema.

They should **not** be forced to produce identical ideas.

When multiple models ideate, prefer independent candidate generation before cross-reading each other's answers. This preserves diversity while still benefiting from shared production knowledge.

## Guardrails against overengineering

This pipeline should remain lightweight until real production proves more structure is needed.

Default limits:

- 2 storyboard candidates;
- roughly 3–6 shots/beats per short scene unless the episode demands otherwise;
- 6 core fields per shot;
- one scene grid per continuity unit;
- no mandatory professional lens package, coverage matrix, shot-reverse-shot doctrine, or complex continuity database;
- no new automation layer merely because a reference project contains one.

If the user can choose between two good visual plans and another agent can execute the selected plan without reconstructing intent from chat history, the pipeline is doing its job.


## Continuity as story language

See `continuity-as-story-language.md` for the detailed rationale. The key rule is that continuity is not only spatial/physical stability. The sequence must also preserve or intentionally transform **what the audience knows** and **what the audience feels**. A storyboard should therefore be evaluated as a chain of shot functions and handoffs, not as a gallery of individually strong frames.
