# Rough 3D Blocking Reference Tools for Storyboard Production

## Status

Reference/design note for Codex and other agents. This is **not** an instruction to replace the current storyboard pipeline or to start another large tool-integration project immediately.

The current priority remains: finish the in-progress Noa video, compare its result against Hermes/Grok alternatives, then improve the pipeline based on observed quality and cost.

## Why this note exists

Recent storyboard work shows that some failures are not fundamentally language-model problems. Camera placement, body orientation, frame occupancy, hand position, spatial relation, and perspective can be difficult to specify reliably with text alone.

A lightweight 3D blocking stage may reduce these failures by fixing spatial facts before photoreal image/video generation.

The intended pattern is:

```text
Episode / scene intent
→ Director chooses shot function
→ rough 3D blocking fixes camera / pose / spatial layout
→ export reference frame
→ photoreal storyboard renderer
→ approved storyboard
→ video prompt compiler
→ WanGP / H3 / other renderer
```

The 3D tool should not become the creative director. It should act as a deterministic spatial helper.

## Reference source

HAELE 3D publisher page:
https://store.steampowered.com/publisher/haele3d

The HAELE family is useful as a conceptual reference because it provides controllable human posing, camera, lighting, and artist-reference workflows.

For this project, however, free/open or lightweight alternatives are more attractive when they fit the shot-blocking problem.

## Candidate tools

### 1. Wonder Unit Storyboarder / Shot Generator — strongest first candidate

Primary reason to study:
- purpose-built for storyboard shot construction rather than anatomy-only posing;
- 3D characters, props, camera, and lighting can be placed to design a shot;
- free / open-source heritage;
- conceptually close to the project's storyboard-first workflow;
- potentially scriptable or automatable later if a narrow integration proves useful.

Project fit:

```text
shot schema
→ rough 3D camera/blocking
→ PNG/reference export
→ photoreal storyboard generation
```

Recommended first experiment:
- reproduce one simple Noa shot only;
- example: room visible, fixed placed-camera angle, Noa enters or settles into frame;
- evaluate whether rough 3D reference materially improves framing/body orientation compared with text-only prompting.

Do **not** integrate the full app into XAI-Studio before this test.

### 2. PoseMy.Art — quick pose / ControlNet-oriented reference

Useful characteristics:
- browser-based and low-friction;
- IK posing, camera and lighting controls;
- useful pose/reference exports;
- OpenPose / depth / edge-style reference outputs can be useful for image-model guidance.

Best fit:
- exact body orientation;
- 30° / 60° / 90° view control;
- full-body composition;
- low/high camera placement;
- hand/arm position guidance;
- quick reference without building a full scene.

This is likely better as a **quick pose/reference utility** than as the canonical storyboard system.

### 3. MPFB2 + Blender — powerful backend candidate, not first UI

MPFB2 is an open-source human generator for Blender.

Advantages:
- full control over rig, camera, focal setup, lights, spatial layout;
- scriptable;
- potentially suitable for agent-driven automatic rough blocking later.

Disadvantages:
- much more complex than the user's preferred workflow;
- high risk of becoming another infrastructure project;
- poor fit for frequent manual use unless hidden behind automation.

Treat Blender/MPFB as a future backend option if automatic shot blocking becomes valuable. Do not make it the first experiment.

### 4. Magic Poser — simple manual reference option

Potential use:
- lightweight human pose and camera reference;
- easier manual use than Blender.

Lower priority because it offers less obvious automation/storyboard-pipeline leverage than Storyboarder or PoseMy.Art.

### 5. Cascadeur — motion/action reference, later

Potential value:
- body mechanics;
- weight transfer;
- walking / sitting / dynamic pose transitions;
- motion-state references.

This is overkill for the present still-shot blocking problem. Revisit only when dynamic motion planning becomes a demonstrated bottleneck.

## Structural lesson

### Do not make the LLM solve deterministic geometry unnecessarily

Current failure mode:

```text
LLM prompt
→ image/video model must infer camera + perspective + body pose + spatial layout simultaneously
```

Preferred split:

```text
Director / LLM
→ choose narrative intent and shot function

3D blocking tool
→ resolve camera, pose, frame occupancy, spatial relation

Image model
→ realism, character appearance, wardrobe, material, lighting style

Video model
→ motion, timing, temporal continuity
```

This reduces the amount of geometric reasoning demanded from the generative models.

## What 3D blocking should control

Good candidates for deterministic control:
- camera position and height;
- camera yaw/pitch / approximate angle;
- framing and subject scale;
- character orientation;
- approximate pose;
- prop position;
- spatial relation between character and environment;
- rough eyeline;
- blocking of entrances / exits.

Do not try to encode all cinematography or realism in the 3D stage.

## What should remain generative

Prefer image/video models for:
- facial identity;
- believable skin / hair / clothing;
- photoreal materials;
- nuanced lighting;
- atmosphere;
- emotion;
- subtle natural motion;
- final visual polish.

## Relationship to Director Memory

3D blocking is downstream of directing intent.

It must not decide:
- whether an opening is environment-first or character-first;
- emotional rhythm;
- shot function;
- narrative reveal order;
- whether a cinematic technique is appropriate.

Those remain Director / Skill Router decisions.

3D blocking only makes a selected shot spatially explicit.

## Suggested future schema extension

Do not add these fields until a real prototype needs them, but a rough-blocking adapter may eventually accept something like:

```yaml
shot_id: S01
framing: medium_wide
camera_height: 1.1m
camera_position: shelf_north_wall
camera_yaw: 20deg
character_position: near_sofa_left
character_facing: 30deg_camera_right
pose: standing_entering_frame
prop_positions:
  action_camera: shelf_north_wall
  bag: right_hand
```

These values should be treated as approximate spatial constraints, not cinematic truth.

## Minimal experiment before any integration

Run one A/B test only:

### A — text-only storyboard reference
Generate a storyboard panel from the normal prompt.

### B — rough-blocked reference
Create the same intended shot in Storyboarder or PoseMy.Art, export a simple reference, then generate the photoreal panel from that reference.

Compare:
- camera correctness;
- full-body / framing correctness;
- body direction;
- environment readability;
- hand / prop placement;
- character identity preservation;
- extra user effort;
- whether the reference over-constrains aesthetics.

Stop after one shot unless the result clearly helps.

## Important scope guard

Do **not**:
- install and integrate several 3D tools at once;
- build a Blender automation stack before a manual A/B test;
- replace the existing storyboard-first design;
- create a new asset format just for this experiment;
- build a generalized 3D scene editor inside XAI-Studio;
- spend Codex credit automating a tool before confirming that its exported blocking reference improves actual generated results.

Follow:

```text
manual test
→ compare result
→ repeat only if useful
→ standardize minimal interface
→ automate repeated friction
```

## Current recommendation

Priority order for evaluation:

1. Wonder Unit Storyboarder / Shot Generator
2. PoseMy.Art
3. Blender + MPFB2 only if automation value becomes clear
4. Magic Poser as optional manual reference
5. Cascadeur only for future motion-blocking needs

The immediate goal is not to adopt a new tool. The goal is to determine whether **rough 3D blocking meaningfully improves the specific storyboard failures currently seen in Noa/Lia production**.

## Implication for Codex

When Codex later improves the storyboard pipeline, treat 3D blocking as an optional adapter:

```text
structured shot
→ optional rough-blocking adapter
→ exported reference image
→ existing storyboard/image generation route
```

Do not hard-wire the entire pipeline to one external application.

If the A/B test proves useful, the first automation target should be only:

```text
shot schema
→ rough 3D blocking
→ PNG export
```

Nothing beyond that should be implemented until this path is used in a real episode.
