# Reference-Driven Production Pipeline

Updated: 2026-09-06

## Purpose

This document records production lessons from a FrameWire creator's Seedance 2.5 sitcom workflow and converts them into model-independent design rules for XAI-Studio-Video.

The important idea is not a specific Seedance prompt recipe. It is **information separation, reference authority, and scene-level assembly**.

The studio should preserve rich reusable knowledge in Character DNA and asset libraries, but provide each renderer only the smallest coherent reference packet needed for the current scene.

> **Agent note — Codex / Claude Code / Hermes**
>
> Treat this document as a design reference, not as an instruction to interrupt current P0 work. `docs/current-priorities.md` remains authoritative for execution priority. Do not turn every rule below into a new subsystem immediately. Promote these ideas into code/schema only when they solve an observed production failure or are needed by an active content workflow.

---

## 1. Production flow: plan before generating

Recommended high-level flow:

```text
Idea
↓
Mood / Keywords
↓
Reference Board
↓
Story Structure
↓
Sequence Breakdown
↓
Asset Manifest
↓
Character / Environment / Prop masters
↓
Scene Blocking / Diagram / Optional Previz
↓
Generation Packet
↓
Video generation + immediate timeline edit
↓
Selective repair
↓
Music / sound / final finishing
```

For dialogue-heavy sitcom/short-drama work, camera movement does not need to be fully designed in the first script draft. Story, dialogue, sequence role, and dramatic intensity should be stabilized first. Camera details can be refined after test generations.

For music-video, action, transition-heavy, or choreography-heavy work, camera and motion planning may need to move earlier.

### Planning rule

Do not build Sequence 1, generate its assets, then invent Sequence 2 from scratch unless deliberate improvisation is the project format.

First determine:

- the overall story shape;
- the role of each sequence;
- the primary hook/payoff points;
- where intensity rises, rests, and peaks;
- the full asset inventory implied by the script.

This reduces asset rework when the story changes later.

---

## 2. Character DNA is not the same thing as a Character Sheet

XAI-Studio should make a strong distinction between the canonical identity system and a renderer-facing reference packet.

### Character DNA

The long-lived source of truth may contain:

- face invariants;
- body invariants;
- hair rules;
- wardrobe rules;
- accessories;
- expression tendencies;
- behavior/personality notes;
- approved image pool;
- edge cases and forbidden drift;
- model-specific observations.

### Character Sheet

A Character Sheet is a **compiled visual reference artifact for one generation task or renderer family**.

It should contain only coherent, useful identity information.

A practical default for modern reference-aware video models is:

```text
LEFT PANEL
- one clean frontal face close-up
- neutral lighting
- neutral expression or canonical expression

RIGHT PANEL
- full-body front
- full-body back
- neutral studio lighting
- neutral gray background
```

The full-body faces may be masked or visually de-emphasized if they conflict with the authoritative face reference.

Additional 3/4, profile, expression, hair, or accessory references remain valuable in DNA/library storage, but should be supplied only when the target model or scene benefits from them.

### Design principle

```text
Character DNA = rich source of truth
Character Sheet = minimal coherent projection of that truth
```

More reference images are not automatically better. Slightly inconsistent identity images can cause averaging, blending, or identity drift.

---

## 3. Introduce Canonical / Master Asset authority

The asset system should distinguish **authority** from simple approval.

Suggested concepts:

```text
FACE_MASTER_001
BODY_MASTER_FRONT_001
BODY_MASTER_BACK_001
ENVIRONMENT_MASTER_001
PROP_MASTER_001
```

Possible metadata:

```yaml
canonical: true
reference_priority: 100
asset_role: face_master
identity_confidence: high
approved_for_video: true
derived_from: null
```

Alternative images can remain approved without being canonical.

Example:

```yaml
canonical: false
reference_priority: 60
asset_role: face_alt_3q
identity_confidence: medium-high
derived_from: FACE_MASTER_001
```

### Agent implementation note

Do not hard-code the exact field names above until they fit the existing Character Manager schema. Preserve the semantic requirement:

1. there must be a way to identify the authoritative reference;
2. there must be a way to distinguish alternates from masters;
3. renderer packet assembly should prefer canonical references;
4. the system should avoid indiscriminately sending every approved image.

---

## 4. No recursive reference degradation

Avoid repeatedly using an AI-generated derivative as the new identity source.

Bad pattern:

```text
MASTER
  ↓
A
  ↓
B
  ↓
C
```

Preferred pattern:

```text
             → A
MASTER       → B
             → C
             → D
```

The same rule applies to:

- face identity;
- body proportions;
- wardrobe structure;
- products/props;
- locations;
- textures and materials.

Repeated derivative-to-derivative generation can accumulate small changes in face geometry, skin texture, garment details, object dimensions, and scene layout.

### Proposed invariant

Call this rule **No Recursive Derivation**.

When feasible, new variants should derive directly from a canonical master or from a deliberately promoted new master, not from an arbitrary recent output.

A promoted new master should be an explicit human/agent decision, not an implicit consequence of generation order.

---

## 5. Separate reference roles

Do not overload one image with unrelated responsibilities.

```text
Character reference
≠ Body reference
≠ Wardrobe reference
≠ Prop / product reference
≠ Environment reference
≠ Mood reference
≠ Blocking reference
≠ Camera / previz reference
```

The Generation Packet should compose the references needed for the scene.

Example:

```text
Scene 07 packet
├─ FACE_MASTER_001
├─ BODY_MASTER_FRONT_001
├─ SUMMER_DRESS_003
├─ HOUSE_VERANDA_MASTER_001
├─ CAT_MASTER_001
└─ BLOCKING_DIAGRAM_007
```

This is preferable to one giant character sheet containing the person, props, products, backgrounds, color grade, and multiple poses.

### Why

Role separation makes failure diagnosis possible.

If the product shape is wrong, modify the product reference or adapter instructions without disturbing character identity. If blocking is wrong, change the diagram rather than rebuilding the character sheet.

This extends the repository's existing responsibility-layer architecture.

---

## 6. Environment Master before many conflicting views

For a recurring location, first create a wide master view that communicates the major spatial structure.

Example:

```text
LIA HOUSE — ENVIRONMENT MASTER

kitchen        living room
    │              │
    └──── veranda ─┘
            │
          garden
```

Independently generated views should not automatically be treated as mutually consistent views of the same physical space.

Several reference images are useful only when their spatial information does not conflict.

### Environment workflow

```text
Environment concept
↓
wide spatial master
↓
approve major layout
↓
derive secondary views where possible
↓
validate important anchors
↓
register approved views as children of the same environment master
```

Mood should also begin in environment assets when possible. If a project requires a clear summer youth-drama feel, the background references should already express compatible light, season, air, and material response instead of asking the final video prompt to transform a contradictory base image.

---

## 7. Add lightweight spatial specification: blocking diagrams

Multi-character scenes need more than identity references.

The production system should be able to provide:

- actor positions;
- actor facing/orientation;
- movement path;
- gaze target;
- important props;
- camera position/direction;
- relevant spatial anchors.

A minimal diagram can be more useful than a verbose paragraph.

Example:

```text
┌─────────────────────────────┐
│ sofa                        │
│ [B: phone/chips]            │
│                             │
│          [A]                │
│           ↓ gaze            │
│                             │
│                  [C: grill] │
│                             │
│         CAMERA ↑            │
└─────────────────────────────┘
```

### FrameWire/XAI-Studio direction

A canvas should not be treated only as an image moodboard or curation surface.

A high-value future use is a **lightweight previsualization layer** that allows the user to place references on a canvas and annotate:

- character labels;
- arrows;
- gaze;
- camera;
- movement;
- continuity-critical objects.

The result can be stored as a blocking asset and attached to a scene packet.

### Priority warning

This is not a reason to build a Blender replacement. Start with static 2D annotation. Add 3D/animated previz only if repeated real projects show clear credit/time savings.

---

## 8. Natural acting: action continuity + reaction + gaze

Dialogue should not automatically cause all characters to stop what they are doing and stare at each other.

Natural multi-character acting often comes from three interacting layers:

```text
ongoing activity
+
reaction to events/dialogue
+
gaze behavior
```

Example:

```text
Character A talks while brushing a cat.
She mostly looks at the cat rather than the listener.
The cat shifts position.
Her hand pauses briefly.
She gives a small smile and continues brushing.
```

This should be represented structurally where useful.

Candidate scene/action fields:

```yaml
primary_action: brushing_cat
secondary_action: removing_hair_from_brush
gaze_target: cat
reaction_trigger: cat_moves
reaction: brief_pause_then_small_smile
dialogue: "오늘은 얌전하네."
```

### Agent note

Do not immediately expand every schema with these exact fields. First test whether the current Shot Graph / Motion DNA / Micro Motion structures can express them cleanly. The invariant is more important than the syntax:

**preserve ongoing behavior while dialogue and reactions occur.**

This extends `Action Grammar` from physical interaction toward conversational acting grammar.

---

## 9. Native audiovisual performance before automatic lip-sync repair

For models that natively generate dialogue, voice, facial expression, mouth movement, breathing, and body acting together, prefer the native performance when it is acceptable.

Do not assume the production pipeline must always be:

```text
video → TTS → lip-sync
```

Prefer:

```text
native audiovisual generation
↓
review performance
├─ acceptable → keep
├─ voice problem → selective audio repair
├─ mouth mismatch → selective lip-sync repair
└─ acting failure → regenerate / edit shot
```

The reason is temporal coupling: replacing speech later may weaken alignment among facial expression, breath, gesture, timing, and mouth motion.

This rule is model-dependent. For renderers without useful native dialogue/voice, external voice and lip-sync remain valid adapters.

---

## 10. Character sheets should be neutral, not cinematic

A canonical Character Sheet should prioritize identity measurement over final-look aesthetics.

Recommended baseline:

- neutral studio light;
- gray or simple neutral background;
- natural white balance;
- minimal dramatic shadow;
- no strong color grade;
- clearly visible clothing/material colors;
- clearly visible identity markers.

Film look, seasonal grade, dramatic light, and scene mood should normally live in:

- environment/reference mood assets;
- Visual DNA;
- scene specification;
- renderer adapter/runtime prompt.

This prevents the identity reference from baking scene-specific color/light distortion into the character source of truth.

---

## 11. Asset Manifest before expensive generation

Once the story/sequence structure is stable enough, compile the required assets before video generation.

Example:

```yaml
sequence_02:
  characters:
    - yuna
    - jiyeon
    - female_friend
  location:
    - bbq_garden
  props:
    - phone
    - chips
    - grill
  spatial_reference:
    - blocking_diagram_seq02
```

This can be generated automatically from the approved storyboard/script and then reviewed.

The objective is to find missing dependencies before credits are spent on final video generation.

---

## 12. Generate and edit concurrently

For short-form work, do not necessarily generate every final clip first and edit only at the end.

A practical loop is:

```text
Generate shot
↓
Place immediately on timeline
↓
Evaluate pacing / continuity / actual duration
↓
Adjust next shot or regenerate weak shot
```

This lets real generated timing inform later decisions.

The story structure should still be planned globally; concurrent editing is not permission to improvise the entire narrative sequence after every shot.

---

## 13. Dramatic intensity is a budget

Not every beat should be maximally expressive.

Before generation, mark where the viewer should react most strongly.

```text
setup → information → small reaction → release → hook/payoff
```

Concentrate expression, camera, sound, motion, and edit emphasis at the intended payoff rather than making every shot equally intense.

This is compatible with the existing Motion Budget concept and should eventually connect to Storyboard/Narrative Tempo planning rather than becoming a separate redundant system.

---

## 14. Suggested future data model

This is conceptual, not an immediate migration request.

```text
PROJECT
│
├─ STORY / STORYBOARD
│
├─ ASSET REGISTRY
│   ├─ Character DNA
│   │   ├─ Face Master
│   │   ├─ Body Master
│   │   └─ Approved Alternates
│   ├─ Environment Master
│   ├─ Prop/Product Master
│   └─ Wardrobe Master
│
├─ SCENE
│   ├─ cast
│   ├─ environment
│   ├─ props
│   ├─ blocking
│   ├─ action / gaze / reaction
│   └─ camera intent
│
├─ GENERATION PACKET
│   └─ selected coherent references only
│
└─ MODEL ADAPTER
    └─ renderer-specific prompt/reference compilation
```

A Generation Packet is disposable and task-specific, analogous to the existing Runtime Prompt. Asset masters and Character DNA remain canonical.

---

## 15. Failure diagnosis rules

When a generated scene fails, identify the responsibility first.

```text
wrong face
→ identity/master reference issue

wrong body silhouette
→ body reference issue

wrong product
→ prop/product reference issue

room layout drift
→ environment/blocking issue

actors swap positions
→ blocking/spatial packet issue

actors feel stiff
→ action continuity / gaze / reaction issue

wrong mood
→ environment / Visual DNA / renderer prompt issue

bad lips only
→ audiovisual/lip repair issue
```

Avoid rebuilding unrelated accepted assets.

This is the reference-pipeline equivalent of the existing `Preserve accepted work` architecture rule.

---

## 16. Agent comments: how to use this document

### Codex

When editing schemas, UI, or asset-management code:

1. preserve a canonical/master concept even if the exact implementation differs;
2. avoid APIs/UI that implicitly treat every approved image as an equal reference;
3. avoid recursive derivation as a default workflow;
4. prefer a scene-level packet assembler over giant monolithic prompt/reference blobs;
5. keep model-specific limits and syntax in adapters;
6. reuse existing Shot Graph, Motion DNA, Micro Motion, Storyboard, and Character Manager structures before inventing overlapping abstractions;
7. do not promote this document into P0 unless `current-priorities.md` is intentionally changed.

### Claude Code

When proposing architecture:

- optimize for traceability of `master → derived asset → scene packet → generation`;
- prefer small composable reference roles;
- treat a canvas/diagram as structured scene information, not merely presentation;
- challenge schema additions that duplicate concepts already present elsewhere;
- document migrations before changing durable Character DNA formats.

### Hermes / production agents

When assembling a generation job:

- start from the canonical references;
- select only references required by the scene;
- avoid chaining from the last generated output unless explicitly authorized;
- preserve approved identity/location/prop masters;
- record which source assets were used;
- record failures by responsibility category so Codex can later identify recurring system-level issues.

---

## 17. Adoption strategy

These rules should enter the system in stages.

### Stage A — use immediately as human/agent operating rules

- canonical reference preference;
- no recursive derivation;
- separate character/prop/environment references;
- plan full asset inventory before final generation;
- preserve ongoing action + gaze + reaction in acting descriptions.

### Stage B — add when current tools need them

- master/reference-priority metadata;
- automatic Generation Packet assembly;
- lineage tracking;
- blocking-diagram attachment;
- environment hierarchy.

### Stage C — only after repeated production evidence

- sophisticated 2D diagram editor;
- 3D/animated previz;
- automatic spatial consistency validation;
- renderer-specific reference optimization policies learned from generation history.

The project should continue to favor **production evidence over architecture accumulation**.

---

## Core takeaway

The system should not try to give an AI model the maximum amount of information.

It should preserve maximum useful knowledge internally, then compile the **minimum coherent set of authoritative information** required for a particular generation.

```text
rich canonical knowledge
        ↓
role-separated assets
        ↓
scene-specific selection
        ↓
coherent Generation Packet
        ↓
model adapter
        ↓
runtime generation
```

This principle is expected to remain useful even as Seedance, Kling, H3, and future video models change.