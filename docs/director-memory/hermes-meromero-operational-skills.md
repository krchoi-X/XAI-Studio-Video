# Hermes / Meromero Operational Skill Layer

## Purpose

This document defines how the detailed Director Memory and production guidance should be distilled into small, executable skills for Hermes using the local Meromero model.

The goal is **not** to make a smaller local model read and reconcile the entire directing knowledge base. The goal is to convert durable directing knowledge into narrow operational procedures that a smaller model can execute reliably.

This layer exists because strong frontier agents such as Codex or Claude can usually infer priority and resolve conflicts across long documents, while a smaller local model is more likely to degrade when given too many guides, examples, cinematic techniques, renderer constraints, and historical notes at once.

The intended architecture is:

```text
Detailed Director Knowledge
- Director Memory
- failure lessons
- cinematic techniques
- cutboard rules
- renderer notes
- prompt compiler guidance
        ↓
Codex / Claude distillation
        ↓
Small operational skills
        ↓
Hermes / Meromero execution
        ↓
Structured output
        ↓
Validation / repair
        ↓
Renderer-specific prompt / production
```

## Core principle: one skill = one bounded decision

Do not create one monolithic "AI movie director" skill for Meromero.

Prefer small skills with narrow responsibility and strongly constrained output.

Recommended initial skill set:

```text
video-director
storyboard-cutboard
cinematic-technique-selector
continuity-check
video-prompt-compiler
```

These are logical roles. Reuse existing project skill infrastructure where possible rather than creating a new skill engine.

## 1. video-director

Purpose: decide the directing strategy only.

Inputs should stay small, for example:

```yaml
episode:
character:
duration:
renderer:
```

Expected output:

```yaml
directing_mode: observational
construction: multi_cut
opening_strategy: environment_first
needed_skills:
  - storyboard-cutboard
  - cinematic-technique-selector
```

Do not ask this skill to also write the final renderer prompt.

## 2. storyboard-cutboard

Purpose: convert an already selected directing strategy into a structured cutboard.

Prefer fixed schema over prose.

Example:

```yaml
shots:
  - id: S01
    function: establish_space
    framing: wide
    action: character enters the inn
    continuity_anchor: wardrobe + bag + entrance
    duration_s: 1.5
    reason: establish destination and calm tone
    feasibility: easy
```

The skill should not improvise unrelated techniques or renderer syntax.

Each shot should follow the existing cutboard guidance:

- one primary shot function;
- one dominant action or emotional beat;
- clear continuity anchor;
- explicit reason for existence;
- rough video feasibility.

## 3. cinematic-technique-selector

Purpose: select only a few techniques that solve the scene's actual visual/narrative problem.

Do not load or expose hundreds of techniques to Meromero at once.

Use a curated subset and retrieve only a few candidates.

Expected output:

```yaml
selected:
  - frame_within_frame
  - rack_focus
why:
  - reinforce spatial depth
  - transfer attention from landscape to character
rejected:
  - whip_pan: conflicts with calm directing mode
```

Default behavior should be restrained:

- one coherent base visual grammar;
- one or two accent techniques;
- zero or one transition technique when justified.

Technique diversity should accumulate across episodes, not through overload inside one episode.

## 4. continuity-check

Purpose: review an existing cutboard. Do not generate new creative direction unless repair is requested.

Check only bounded items such as:

- character identity consistency;
- wardrobe continuity;
- prop presence and hand/object state;
- spatial position;
- time progression;
- one dominant action per shot;
- shot-to-shot handoff readability.

Expected output:

```yaml
status: revise
issues:
  - shot: S03
    rule: prop_state
    message: cup appears before the handoff
  - shot: S05
    rule: wardrobe_continuity
    message: wardrobe differs from the active continuity unit
```

Keep this skill diagnostic. It should not rewrite the whole storyboard automatically.

## 5. video-prompt-compiler

Purpose: compile an approved storyboard into a renderer-specific prompt.

Input should be limited to:

```text
approved storyboard
+ selected techniques
+ renderer profile
+ relevant references
```

Output should be renderer-ready text or structured prompt data.

Do not ask Meromero to reinterpret the episode from scratch at this stage.

## Progressive disclosure

Operational skills should be small.

Recommended layout when compatible with the current project skill system:

```text
.agents/skills/storyboard-cutboard/
├── SKILL.md
└── references/
    ├── vlog.md
    ├── brand.md
    ├── drama.md
    └── examples.md
```

`SKILL.md` should contain only:

- purpose;
- required inputs;
- decision procedure;
- output schema;
- validation rules;
- conditions for loading optional references.

Load a specific reference only when relevant to the current task.

Do not make Meromero read the entire Director Memory directory for every storyboard.

## Distillation rule

The detailed documentation remains the source of knowledge for stronger agents and human review.

Operational skills should contain only the minimum executable procedure.

Use this transformation:

```text
long directing guidance
→ recurring decision pattern
→ explicit decision procedure
→ narrow skill
→ fixed schema
```

For example, a large external cinematic-technique reference should be distilled as:

```text
large catalogue
→ current high-value subset
→ function-indexed entries
→ retrieve a few candidates
→ select one or two
```

Do not copy large reference catalogues into a local skill.

## Small-model guidance

For Meromero, prefer:

1. one skill = one bounded decision;
2. YAML/JSON schema over long prose;
3. short decision trees over long rule lists;
4. one good example and one bad example rather than many examples;
5. separate generation from review;
6. repair only the failed part when possible.

Example decision tree:

```text
Does the scene need spatial orientation?
YES → consider environment-first.
NO ↓

Is an object narratively important?
YES → consider object-first.
NO ↓

Is emotional intimacy the priority?
YES → consider character/detail-first.
```

The purpose is to reduce hidden reasoning burden, not to make the model memorize film theory.

## Generate → validate → repair → compile

Do not expect one-pass correctness from a small local model.

Recommended loop:

```text
Meromero Director
→ storyboard.yaml

Deterministic validator + Meromero semantic checker
→ validation result

If invalid:
    repair only failed shots/fields
Else:
    prompt compiler

→ WanGP / H3 / selected renderer
```

Example validation output:

```yaml
errors:
  - shot: S03
    rule: one_dominant_action
    message: drink + walk + dialogue are combined
```

Repair S03 rather than regenerating the entire cutboard.

## Deterministic validation vs LLM review

Do not use Meromero for checks that code can perform reliably.

Deterministic checks:

```text
shot count
duration total
required fields
unique shot_id
known skill_id
known renderer
allowed enum values
selected technique count limit
```

LLM semantic review:

```text
is the opening generic?
is the emotional progression readable?
are shot functions redundant?
does a technique serve the directing intent?
is a shot overloaded despite schema validity?
```

Use both layers.

## Shared skill location

Where compatible with the actual Hermes/runtime configuration, prefer a project-local shared skill location such as `.agents/skills/` so the same operational skill can be consumed by multiple agents without duplicating policy.

Before implementation, Codex must inspect the installed Hermes/Meromero version and verify the supported project skill paths rather than assuming documentation from another version is authoritative.

Do not create parallel skill copies under multiple directories unless the active runtime requires it.

## Relationship to existing Director Memory

`docs/director-memory/` remains the durable knowledge layer.

The operational skill layer is not a replacement for Director Memory.

Think of the separation as:

```text
docs/director-memory/
= human + strong-agent knowledge layer

project operational skills
= compressed execution layer for Hermes/Meromero and other agents

renderer profiles
= H3 / WanGP / other engine-specific execution constraints
```

Changes to the detailed knowledge layer should not automatically expand local skill prompts. Promote only stable, repeatedly useful procedures.

## First implementation milestone

Do not implement all five skills at once.

Start with only:

1. `storyboard-cutboard`
2. `continuity-check`

Acceptance criteria:

- both use small, fixed schemas;
- Meromero can create one structured cutboard from a simple episode brief;
- deterministic validation catches structural errors;
- semantic continuity review catches at least one intentionally introduced narrative/continuity error;
- failed shots can be repaired without regenerating the full storyboard;
- the output can be consumed by another agent/session without original chat context.

Only after this works should the project add:

3. `cinematic-technique-selector`
4. `video-prompt-compiler`
5. a fuller `video-director` router if it is still needed.

## Scope guard

Do not turn this into a new orchestration project.

Do not:

- build a new vector database just for skills;
- copy all Director Memory into each skill;
- copy all cinematic-technique references into Meromero context;
- create a large universal system prompt;
- require Meromero to perform planning, validation, compilation, and execution in one pass;
- duplicate canonical project policy already owned by shared resources;
- resume broad repository restructuring to support this feature.

The objective is simple:

> Make a smaller local model reliable by reducing each task until it can follow a clear procedure and produce a machine-checkable artifact.

## Recommended Codex interpretation

When Codex later integrates this, treat the work as **Director Knowledge → Operational Skill Distillation**.

The implementation should optimize for:

- bounded context;
- deterministic interfaces;
- selective retrieval;
- repairability;
- shared artifacts across agents;
- low frontier-model dependency;
- compatibility with the existing XAI-Studio-Video production path.
