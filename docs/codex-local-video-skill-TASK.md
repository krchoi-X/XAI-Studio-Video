# TASK — Build Local Video Director / Prompt Compiler Skill

Owner: Codex  
Status: ready for local implementation  
Updated: 2026-09-30

## Goal

Create a local reusable skill that lets Codex/Hermes/local LLM agents apply the
video knowledge base automatically when generating or revising AI-video prompts.

The skill must not become another independent knowledge database.
It must read the repository authorities and compile them into working guidance.

## Source authorities

Read these from the local clone of `XAI-Studio-Video`:

1. `docs/reference-state-analyses.md`
2. `docs/directing-technique-db.md`
3. `docs/prompt-craft-db.md`
4. `docs/knowledge-promotion-architecture.md`

Read these from the local clone of `XAI-Studio-Private`:

`XAI-Studio/personal-prompt-studio/library/video-motion/`

especially:
- `index.yaml`
- `camera-motion.yaml`
- `transition-motion.yaml`
- `timing.yaml`
- `physical-response.yaml`
- `AGENT_PROMPTING_GUIDE.md`

## Skill role

The local skill is a **director + compiler**, not a renderer and not a database editor.

Given a scene request, it should:

```text
1. infer the scene's directing problem
2. choose relevant T-techniques
3. choose relevant P-rules
4. load only needed motion primitives
5. inspect continuity state
6. inspect target-model capability profile
7. compile a renderer-specific prompt
8. return the final prompt plus concise internal rationale metadata
```

Do not force the human user to choose motion terms manually.

## Required decision order

### Step 1 — Define the visible objective

Identify:
- what must be visibly understood
- what must remain continuous
- what transition/state change occurs
- what the camera must communicate
- what can safely remain implied

### Step 2 — Renderability boundary decision

For each difficult intermediate state classify:

- DIRECT
- PARTIAL
- HIDE
- CONSEQUENCE_ONLY

Before adding more prompt detail, check whether a directing workaround is superior.

### Step 3 — Directing technique selection

Search `directing-technique-db.md` by problem, not by technique name.

Examples:
- unreliable door crossing → T-04/T-05/T-37
- weak action velocity → T-26/T-13/T-21
- spatial continuity → T-06/T-07/T-09
- difficult visible state transition → T-01/T-04/T-10/T-37

Do not apply every related technique. Use the smallest sufficient combination.

### Step 4 — Continuity/state collection

Build or read structured state for:
- character identity
- outfit
- location anchors
- gaze relationships
- props
- injuries/damage
- wet/dry/dirt state
- environment damage
- shot direction

P-29/P-30 are not merely prompt phrases. Treat them as persistent state input.

Recommended local representation:

```yaml
shot_state:
  character:
    identity_ref: ...
    outfit_state: ...
  props:
    bag:
      holder: left_hand
      contents: []
  physical_state:
    wetness: dry
    injuries: []
  spatial:
    screen_direction: left_to_right
    location_anchor: ...
```

### Step 5 — Prompt craft compilation

Apply P-rules as compiler behavior.

High-priority defaults:
- P-06 Trace-first: observable motion over abstract force words
- P-07 State Transition Chain
- P-13 Capability-calibrated language
- P-14 Positive Locks
- P-15 Reference Role Separation
- P-20 final logic consistency rule
- P-26 Model Adapter

Conditional:
- P-04 headcount for multi-character shots
- P-09 boundary lock for contact
- P-18 quantity economy when counts matter
- P-29/P-30 for persistent state

### Step 6 — Motion primitive expansion

Select semantic primitives from private `video-motion/*.yaml`.

Never send a jargon-only term when the model may misread it.

Example internal selection:
```text
camera_motion.dolly
timing.ease-out
physical_response.hair-inertia
```

Renderer output should expand them into observable physical language.

### Step 7 — Model capability profile

Create a local profile layer, not hard-coded prose scattered through the skill.

Suggested path:

```text
<local-skill>/model-profiles/
  minimax-h3.yaml
  ltx.yaml
  seedance.yaml
  veo.yaml
  default.yaml
```

Minimum fields:

```yaml
model: example
updated: YYYY-MM-DD
evidence:
  ordered_beats: HIGH|MEDIUM|LOW|UNKNOWN
  absolute_seconds: HIGH|MEDIUM|LOW|UNKNOWN
  percentage_phases: HIGH|MEDIUM|LOW|UNKNOWN
  camera_vocabulary: HIGH|MEDIUM|LOW|UNKNOWN
  multi_character_continuity: HIGH|MEDIUM|LOW|UNKNOWN
  contact_renderability: HIGH|MEDIUM|LOW|UNKNOWN
adapter_notes: []
source_refs: []
```

Do not guess unsupported capability values. Use UNKNOWN until tested.

### Step 8 — Final output

Default user-facing output:
- final renderer-ready prompt
- only essential caveats
- no taxonomy dump unless requested

Internal/debug output may include:
- selected T IDs
- selected P IDs
- selected primitives
- state locks
- adapter/profile used

## Local skill packaging

Use the skill system already used by the local agent environment.
Do not invent a new global plugin framework.

Suggested logical layout:

```text
video-director/
  SKILL.md
  references/
    authorities.md
  model-profiles/
    default.yaml
    minimax-h3.yaml
    ltx.yaml
    seedance.yaml
    veo.yaml
  templates/
    shot-state.yaml
    prompt-output.md
```

Avoid copying the full 68-reference corpus into the skill.
The skill should know where to read it from the repo.

## Cache policy

A compact derived cache is allowed only if:
- it records source file + commit SHA
- it can be regenerated
- it is not edited manually as a new authority
- stale cache detection is automatic

## Update workflow

When Git changes:

1. pull both repositories
2. detect changed authority files
3. invalidate derived cache
4. rebuild indexes if needed
5. do not rewrite T/P IDs automatically
6. report schema conflicts before changing canonical data

## Validation tests

Create small tests covering at least:

1. Dolly vs Zoom
2. Pan vs Truck
3. difficult door crossing → conceal/cut strategy
4. prop handoff across 3 shots
5. two-person eyeline continuity
6. action impact with anticipation/contact/consequence
7. same master scene compiled for H3 and one other renderer
8. unknown model capability → conservative observable description

## Non-goals

Do not:
- duplicate all docs into the skill
- create a second T/P database
- assume one universal prompt works across models
- promote every Muse observation automatically
- hard-code current model weaknesses as permanent truths

## Completion criteria

The task is complete when a local agent can receive:

```text
"미라가 카페를 나와 택시를 잡는 10초 컷. H3용."
```

and automatically:
- chooses scene/directing techniques,
- applies continuity state,
- selects/expands motion primitives,
- adapts to H3,
- emits a useful final prompt,

without requiring the user to remember T/P IDs or cinematography vocabulary.
