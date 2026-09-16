# Codex Handoff — Director / Storyboard Pipeline

## Status

Design record only. Do **not** start implementation merely because this file exists.

The user intentionally paused broad repository/folder cleanup because it consumed too much coding-agent credit. Remaining cleanup is a long-term maintenance backlog. When Codex credit becomes available again, this document should be used as the starting point for a **small, scoped pipeline implementation**, not another repository-wide refactor.

## User objective

Build a lightweight pipeline that allows Claude, Grok, Hermes/Meromero, ChatGPT, Codex, or another model to propose and execute better character-driven vlog/short storyboards while sharing durable lessons across sessions.

The user does **not** want commercial feature-film complexity. The intended quality bar is:

- deliberate and varied openings;
- understandable space;
- natural character action;
- better cut/beat continuity;
- fewer repeated AI-video clichés;
- practical execution through existing image/video tools;
- durable reuse of failures, preferences, and successful patterns across models.

The user should provide story intent and taste decisions, not professional cinematography knowledge.

## Read before planning implementation

1. `AGENTS.md`
2. applicable root/scoped `TASK.md`
3. `docs/director-memory/README.md`
4. `docs/director-memory/visual-language-pipeline.md`
5. `docs/director-memory/principles.md`
6. `docs/director-memory/opening-patterns.md`
7. `docs/director-memory/failures.md`
8. `docs/director-memory/capabilities.md`
9. `docs/director-memory/candidate-template.md`
10. existing `skills/idea-to-production/` shared-resource adapter and its actual shared source
11. current architecture/artifact contracts relevant to storyboard and production routing

Do not duplicate or fork project policy already owned by shared resources.

## Architectural intent

The desired logical pipeline is:

```text
Episode idea / scenario
        ↓
Visual Language Translator
        ↓
2 storyboard candidates
        ↓
Director Memory + Capability check
        ↓
Storyboard Prompt Compiler
        ↓
Scene-grid storyboard artifact
        ↓
Human selection / revision
        ↓
Approved shot plan
        ↓
Renderer-specific compiler / existing production routing
        ↓
WanGP / H3 / image renderer / editor
        ↓
Result review
        ↓
Director Memory update
```

This is a **logical architecture**, not a demand to create eleven new services/classes.

Prefer the smallest implementation that fits existing project boundaries.

## Required conceptual boundaries

### Character DNA

Owns stable identity/canon.

Must not absorb:

- one-off shot order;
- temporary camera choice;
- episode-specific object placement;
- directing tricks;
- transient production failures.

### Director Memory

Owns reusable directing experience:

- known failure patterns;
- demonstrated user preferences;
- approved storyboard lessons;
- opening/shot grammar alternatives;
- relevant production capability constraints.

A failure lesson is not automatically a universal ban.

### Visual Language Translator

Owns scenario → visual-directing interpretation:

- reveal order;
- visual focus;
- action vs dialogue;
- camera role/viewpoint;
- `long_take` / `multi_cut` / `hybrid` choice;
- continuity needs;
- feasible creative alternatives.

It should normally produce a small search space rather than one deterministic answer.

### Storyboard Prompt Compiler

Owns chosen text storyboard → image-model-ready storyboard representation.

It should preserve scene/continuity state and panel intent without asking each model to invent prompt grammar from scratch.

### Renderer-specific layer

Owns actual H3/WanGP/image-model syntax and execution.

Do not let renderer-specific prompts become the canonical storyboard representation.

## Minimum storyboard schema

Do not start with a large cinematic schema.

A shot/beat only needs these six required fields initially:

```yaml
shot_id: S01
framing: medium_wide
camera: fixed shelf-mounted observer angle
action: character enters frame and checks framing
continuity_anchor: room layout + wardrobe + action camera position
duration_s: 3.0
production_route: canonical still -> H3/WanGP I2V
```

Candidate-level metadata should include at least:

```yaml
candidate_id: A
construction: long_take   # long_take | multi_cut | hybrid
creative_intent: observational and natural
risk_level: low
```

Add fields only when real production requires them.

## Scene continuity unit

Storyboard image generation should support grouping panels by a practical continuity unit sharing:

- location;
- time / lighting baseline;
- wardrobe;
- relevant character state;
- important props;
- spatial layout.

The same physical location may become a new continuity unit when time, lighting, wardrobe, or story state changes materially.

The pipeline should be able to generate or export one grid/contact-sheet prompt/artifact per continuity unit.

## Candidate generation rule

Default: two meaningfully different candidates.

Preferred bias:

- A = production-safe / continuity-first;
- B = visually distinctive / exploratory.

Difference must be structural, not cosmetic. Useful differences include:

- long take vs multi-cut;
- object-first vs environment-first;
- close-to-wide vs wide-to-intimate;
- observer camera vs placed self-recording camera;
- restrained rhythm vs stronger graphic editing.

When multiple LLMs are used, allow independent exploration before showing them each other's fresh candidates.

## Human interaction contract

The system should minimize the expertise required from the user.

Expected user actions:

- choose A/B;
- reject both;
- give one or two revision notes;
- mark an individual shot as wrong/generic;
- approve production.

Do not require the user to specify focal lengths, professional coverage strategy, axis rules, or technical cinematography terminology unless the user voluntarily does so.

## Automatic checks

Before renderer execution, add lightweight deterministic or LLM-assisted checks for:

- implausible spatial jumps;
- important prop disappearance or hand switching;
- unreadable action handoff between adjacent beats;
- accidental repetition of identical shot scale;
- generic opening fallback when no such style was deliberately selected;
- redundant visual information;
- too many sequential actions inside one generated clip;
- unsupported/unreliable camera behavior for the selected renderer;
- unavailable references/tools required by the proposed production route.

These should surface warnings. Do not turn all warnings into hard blocks.

## First implementation milestone

The first useful milestone should be deliberately small.

Suggested acceptance flow:

```text
1. Input one episode brief + character ID.
2. Resolve canonical character context.
3. Load relevant Director Memory and current capabilities.
4. Ask one configured LLM to return two storyboard candidates in structured form.
5. Validate the six-field shot schema.
6. Export human-readable Markdown/JSON.
7. Compile the selected candidate into one scene-grid storyboard prompt.
8. Stop before automatic video rendering if integration would expand scope materially.
```

Success is **not** "fully automatic film production".

Success is:

> Another model/session can understand the chosen visual plan and continue production without reconstructing the directing intent from the original chat.

## Second milestone, only after first is used successfully

After at least one real user selection/revision loop:

- connect approved storyboard to existing renderer routing;
- preserve generation/artifact provenance;
- write back selected/rejected lessons to Director Memory through an approval-aware path;
- support a storyboard scene-grid image artifact;
- optionally allow a second independent LLM to generate an alternate candidate set.

Do not build these preemptively if the first milestone already reveals a better boundary.

## Must preserve

- existing shared-resource authority;
- Character Manager authority for identity/canon;
- existing artifact/gallery contracts;
- real requesting actor / executor / model attribution;
- current renderer routing and WanGP recording rules;
- human approval before canon/memory promotion;
- backward compatibility for existing production records where applicable.

## Must NOT do

- repository-wide reorganization;
- another large folder cleanup;
- replace Character DNA with Director Memory;
- hard-code one "correct" vlog opening;
- require every episode to use the same storyboard template visually;
- create a new parallel gallery/artifact store;
- fork renderer integration unnecessarily;
- force commercial-film-level metadata;
- add vector DB / workflow engine / event platform solely for this feature;
- vendor external projects such as Hypit, MoneyPrinterTurbo, or Buzz just because their architecture was studied;
- make speculative capability entries authoritative without runtime verification.

## Reference insights to preserve

### From experienced film-production practice

Useful transferable structure:

```text
scenario
→ text storyboard / visual language
→ storyboard-image prompting
→ scene-wise storyboard grid
→ approved visual plan
→ video production
```

The user is not expected to perform the professional directing work manually. AI should internalize/generalize the reusable part of that expertise.

### From current user experience

A vague request such as "make Noa's vlog" often leads different LLMs toward the same generic face-filling selfie opening. Iterative corrections improve the current chat, but those lessons disappear when switching models/sessions. The new pipeline must make those lessons durable while preserving creative variation.

### From production constraints

The directing plan should be upstream of renderer syntax. WanGP/H3 should execute an approved visual plan rather than invent shot structure from an underspecified paragraph.

## Recommended implementation strategy

Use existing code and project contracts first.

Prefer:

```text
Manual/structured prototype
→ real use
→ measure recurring friction
→ standardize schema
→ automate only repeated steps
```

Do not begin with a new orchestration platform.

## Definition of done for the first scoped Codex task

The task can close when all are true:

- one documented schema exists for storyboard candidates and shots;
- one command/function/path can produce two structured candidates from an episode brief using a configured LLM;
- relevant Director Memory/capability context is injected without copying the entire repository into the prompt;
- output validates deterministically;
- selected candidate can be exported/compiled into a scene-grid storyboard prompt artifact;
- no existing character/gallery/renderer contract is broken;
- tests cover schema validation and at least one fixture;
- docs explain how Claude/Grok/Hermes/Codex can consume the same durable output;
- implementation remains scoped and does not resume paused repository cleanup.

After this point, use the feature on one real vlog before expanding it.
