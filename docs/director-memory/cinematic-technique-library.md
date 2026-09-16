# Cinematic Technique Library — Routing Reference

Source reference: https://melies.co/cinematic-techniques

## Purpose

Use the Melies cinematic-techniques catalogue as a **retrievable directing vocabulary**, not as a rulebook that is loaded into every episode.

The value of the source is not the sheer number of techniques. Its useful structure is that techniques are organized by areas such as camera movement, shot size, angle, lighting, composition, lenses, color, time/motion, optical effects, editing/transitions, weather, and genre look, and individual technique pages describe what the technique is and when/why it is useful.

For XAI-Studio, the Director/Planning AI should retrieve techniques only after it understands the episode intent and chosen visual grammar.

## Core principle

> Technique diversity is desirable across a body of work, not necessarily within every episode.

Do not maximize the number of techniques in one short. Prefer one coherent base visual grammar plus a small number of accent techniques that serve the scene.

Recommended default for short-form character work:

- one base camera/editing grammar;
- one or two accent techniques;
- zero or one distinctive transition technique when justified;
- renderer feasibility checked before final compilation.

## Routing model

```text
Episode Brief
  ↓
Visual Language Translator
  ↓
Director Core
  ↓
Technique need detection
  ↓
Retrieve only relevant cinematic-technique entries
  ↓
Select 1–3 techniques for each candidate
  ↓
Renderer feasibility / risk check
  ↓
Storyboard candidate
  ↓
Prompt Compiler
```

Do not send the entire technique catalogue into the model context.

## Technique metadata

A technique entry should be represented with lightweight metadata such as:

```yaml
technique_id: rack_focus
category: focus_optics
narrative_function:
  - redirect audience attention within one shot
  - reveal subject importance without cutting
when_to_use:
  - foreground/background relationship matters
  - reveal can happen through focus rather than framing change
when_not_to_use:
  - renderer cannot hold two stable depth planes
  - scene already contains excessive camera/focus activity
inputs:
  - shot intent
  - subject positions
  - focus start target
  - focus end target
renderer_risk:
  h3: unknown_until_tested
  wangp_route: model_dependent
fallback:
  - hard cut to closer framing
  - static deep-focus composition
source_reference: melies
```

Suggested fields:

- `technique_id`
- `category`
- `narrative_function`
- `when_to_use`
- `when_not_to_use`
- `visual_effect`
- `required_scene_conditions`
- `renderer_risk`
- `fallback`
- `source_reference`

## Priority categories for XAI-Studio

Do not index all techniques first. Start with a small high-value subset from these categories:

### Camera movement
- locked-off / static
- follow shot
- tracking
- push-in / pull-back
- arc/orbit
- handheld
- whip pan
- SnorriCam-type body-locked movement where appropriate

### Framing / shot function
- establishing shot
- full-body / medium / close-up variation
- insert
- cutaway
- reaction shot
- extreme close-up

### Composition
- negative space
- frame within frame
- foreground interest
- layered depth
- symmetry/asymmetry
- reflections

### Focus / optics
- rack focus
- deep focus
- shallow focus
- macro/detail emphasis

### Editing / transitions
- match on action
- match cut
- smash cut
- invisible cut
- J/L cut where audio workflow supports it

### Time / motion
- long take
- slow motion
- speed ramp

### Naturalistic lighting / look
- available light
- window light
- practical lighting
- golden hour
- blue hour

## User-facing diversity goal

The goal is not to make every episode visually maximal. The goal is for different episodes and characters to avoid collapsing into the same generic AI-video grammar.

Example:

```text
Lia — quiet seaside vlog
base grammar: observational handheld + environment-led framing
accent: frame-within-frame + rack focus
transition: match on action

Aoi — energetic urban vlog
base grammar: handheld tracking + quicker multi-cut rhythm
accent: whip pan + selective speed ramp
transition: smash cut when justified
```

The specific combinations are examples, not templates.

## Selection rule

Before choosing a technique, the Director AI should be able to state:

1. what narrative/visual problem the technique solves;
2. why the technique fits this specific episode;
3. whether the renderer can execute it reliably;
4. what fallback exists if execution fails.

Do not select techniques merely because they look cinematic or because they are present in the library.

## Renderer reality over film-theory purity

A technique can be valid in traditional cinematography but unreliable in a generative-video model.

Therefore keep two separate judgments:

- `directing_fit`: does this technique serve the scene?
- `renderer_feasibility`: can the selected model reliably produce it?

Observed failures in H3/WanGP or other renderers should update `renderer_risk`, not erase the technique from the directing vocabulary.

Example:

> Low-angle or worm's-eye framing may be a valid directing choice even if a specific renderer sometimes reverses the intended angle. Record the renderer reliability problem and fallback, rather than banning the technique globally.

## Technique variety without style collapse

Avoid these failure modes:

- loading dozens of techniques into one candidate;
- forcing a different gimmick into every shot;
- treating cinematic terminology as quality by itself;
- selecting techniques without narrative function;
- making Candidate A and Candidate B share the same technique set with only cosmetic changes;
- copying Melies examples literally into unrelated characters/locations.

Prefer:

- Candidate A: restrained/production-safe technique set;
- Candidate B: more distinctive but still coherent technique set;
- no more than a small subset retrieved for either candidate.

## Initial implementation recommendation

For the first Codex implementation, do **not** scrape/index all 424 techniques or create a dedicated vector service.

Start with roughly 30–50 hand-curated, high-value technique entries relevant to current character vlog/short production. Store them in simple Markdown/YAML compatible with the existing shared-resource/skill-routing structure.

After real production use:

- add techniques that would have solved a repeated visual problem;
- add renderer reliability notes;
- remove or deprioritize techniques that are rarely useful;
- expand only when real episodes reveal missing vocabulary.

## Source vs project interpretation

Source-derived idea:
- Melies provides a broad catalogue of cinematic techniques organized by filmmaking function and explains individual techniques in practical terms.

Project interpretation / recommendation:
- treat that catalogue as an external technique vocabulary;
- retrieve only relevant techniques;
- select techniques by narrative function;
- keep episode-level technique counts low;
- optimize diversity across multiple works rather than maximizing novelty inside one work;
- maintain renderer-specific risk/fallback metadata separately.
