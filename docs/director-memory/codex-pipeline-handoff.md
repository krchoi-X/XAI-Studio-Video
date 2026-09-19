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
5. `docs/director-memory/continuity-as-story-language.md`
6. `docs/director-memory/principles.md`
7. `docs/director-memory/opening-patterns.md`
8. `docs/director-memory/failures.md`
9. `docs/director-memory/capabilities.md`
10. `docs/director-memory/candidate-template.md`
11. `docs/director-memory/prompt-compiler-principles.md`
12. `docs/director-memory/cinematic-technique-library.md`
13. existing `skills/idea-to-production/` shared-resource adapter and its actual shared source
14. current architecture/artifact contracts relevant to storyboard and production routing

Do not duplicate or fork project policy already owned by shared resources.

## Architectural intent

The desired logical pipeline is:

```text
Episode idea / scenario
        ↓
Visual Language Translator
        ↓
Director Core / Skill Router
        ↓
Selected directing + production skills
        ↓
Technique need detection / selective technique retrieval
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

This is a **logical architecture**, not a demand to create twelve new services/classes.

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

Owns scenario → visual-directing interpretation.

Before choosing camera technique, it should determine:

- scene / continuity-unit goal;
- narrative beat sequence;
- information release order;
- emotional progression;
- shot functions;
- physical continuity requirements;
- reveal order;
- visual focus;
- action vs dialogue;
- camera role/viewpoint;
- `long_take` / `multi_cut` / `hybrid` choice;
- feasible creative alternatives.

Treat continuity as three related layers when relevant:

- physical continuity;
- informational continuity;
- emotional continuity.

The planner should not produce a sequence of individually attractive but narratively disconnected shots.

It should normally produce a small search space rather than one deterministic answer.

### Director Core / Skill Router

The Director/Planning AI should **not** load every directing guide, prompt example, or renderer note for every episode.

Its job is to:

1. interpret the episode's visual and emotional needs;
2. choose one or two coherent directing modes/grammars;
3. identify relevant prior failures/preferences;
4. inspect currently available production capabilities;
5. select only the skills/references needed for this episode/candidate;
6. identify whether a cinematic technique is actually needed and, if so, retrieve only a small technique subset;
7. generate candidates from those selected skill/technique sets.

This is intentionally a **router + specialist skill** design.

The always-loaded Director Core should remain small. Large guides, example libraries, and cinematic-technique catalogues belong in selectively retrieved skills/references.

Do **not** average all available references into every prompt. Prefer one coherent visual grammar over combining many individually good ideas.

Suggested directing modes include, but are not limited to:

- observational;
- intimate;
- rhythmic;
- object-led;
- environment-led;
- graphic;
- restrained cinematic;
- self-recorded / placed-camera vlog.

These are routing aids, not fixed genres.

### Skill metadata contract

Each directing or production skill/reference should eventually expose lightweight routing metadata such as:

```yaml
skill_id: object_first_opening
when_to_use:
  - episode has a meaningful object or prop that can carry the opening beat
when_not_to_use:
  - object has no narrative/visual importance
inputs:
  - episode brief
  - continuity unit
outputs:
  - opening beat options
conflicts:
  - character_first_only
what_to_extract:
  - reveal logic
  - object-to-character transition
  - continuity requirements
do_not_copy:
  - literal shot order from reference examples
  - reference-specific wardrobe/location/style
```

The first implementation does not need a complex registry service. A small manifest/YAML/Markdown metadata convention is enough if it works with existing shared-resource mechanisms.

### Cinematic technique routing

Use `docs/director-memory/cinematic-technique-library.md` as the current project interpretation of external cinematic-technique references such as Melies.

Do not treat the technique catalogue as an always-loaded skill or as a checklist that every episode must satisfy.

The desired behavior is:

```text
scene intent
→ detect visual/narrative problem
→ choose relevant technique category
→ retrieve a few candidate techniques
→ select only techniques that serve the scene
→ check renderer feasibility
→ compile into storyboard/prompt
```

Default short-form guidance:

- one coherent base visual grammar;
- one or two accent techniques;
- zero or one distinctive transition when justified;
- variety should accumulate across episodes, not through technique overload inside one episode.

A technique should carry at least:

```yaml
technique_id: rack_focus
category: focus_optics
narrative_function:
  - redirect viewer attention inside one shot
when_to_use:
  - two stable depth planes matter to the scene
when_not_to_use:
  - renderer cannot maintain the focus relationship reliably
renderer_risk:
  h3: unknown_until_tested
fallback:
  - cut to closer framing
```

Keep `directing_fit` and `renderer_feasibility` conceptually separate. A technique that is valid filmmaking may still be unreliable in a particular generative renderer.

Do not ban a directing technique globally because one model failed to execute it. Record renderer risk and fallback instead.

For the first implementation, do **not** scrape/index the entire Melies catalogue or build a vector service. Start with roughly 30–50 hand-curated, high-value entries relevant to current vlog/short production and expand only from real production needs.

### Selective retrieval policy

Default behavior:

- load Director Core every time;
- retrieve only the most relevant 2–4 pattern/skill references;
- retrieve only 1–3 concrete examples when useful;
- retrieve only a small number of cinematic-technique entries when a technique need is detected;
- retrieve relevant renderer capability notes only for the selected production route;
- retrieve relevant failure entries, not the full failure archive.

Reference-library size may grow over time, but **per-episode prompt context should stay intentionally small**.

### Candidate diversity through skill selection

Candidate A and Candidate B should not merely paraphrase one another.

When practical, route them through different skill subsets and, where justified, different technique subsets.

Example:

```text
Candidate A
mode: observational
skills:
- environment-first opening
- long-take continuity
- restrained action blocking
techniques:
- frame-within-frame
- match on action

Candidate B
mode: rhythmic / object-led
skills:
- object-first opening
- interaction-state handling
- multi-cut transition grammar
techniques:
- rack focus
- selective whip pan
```

This preserves shared lessons while avoiding style collapse.

When multiple LLMs are used, keep their fresh candidate generation independent before cross-comparison.

### Storyboard Prompt Compiler

Owns chosen text storyboard → image-model-ready storyboard representation.

It should preserve scene/continuity state and panel intent without asking each model to invent prompt grammar from scratch.

### Renderer-specific layer

Owns actual H3/WanGP/image-model syntax and execution.

Do not let renderer-specific prompts become the canonical storyboard representation.

## Minimum storyboard schema

Do not start with a large cinematic schema.

A shot/beat should remain lightweight, but add one explicit narrative field:

```yaml
shot_id: S01
shot_function: establish space and self-recording setup
framing: medium_wide
camera: fixed shelf-mounted observer angle
action: character enters frame and checks framing
continuity_anchor:
  physical: room layout + wardrobe + action camera position
  informational: establishes who is filming and from where
  emotional: casual preparation before speaking
duration_s: 3.0
production_route: canonical still -> H3/WanGP I2V
```

The continuity subfields may collapse back to a single compact note for trivial shots. Do not force professional-film metadata where it adds no value.

Candidate-level metadata should include at least:

```yaml
candidate_id: A
construction: long_take   # long_take | multi_cut | hybrid
creative_intent: observational and natural
risk_level: low
selected_skills:
  - environment_first_opening
  - long_take_continuity
selected_techniques:
  - frame_within_frame
```

Technique metadata can remain optional until a real technique is selected. Do not inflate every shot schema with filmmaking vocabulary just because the library exists.

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
- restrained rhythm vs stronger graphic editing;
- restrained technique set vs one justified distinctive technique.

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
- adjacent cuts that do not preserve or intentionally transform informational continuity;
- reaction/reveal ordering that creates unintended emotional meaning;
- shots with no clear function beyond looking visually attractive;
- accidental repetition of identical shot scale;
- generic opening fallback when no such style was deliberately selected;
- redundant visual information;
- too many sequential actions inside one generated clip;
- unsupported/unreliable camera behavior for the selected renderer;
- unavailable references/tools required by the proposed production route;
- accidental loading of irrelevant/contradictory skills;
- candidates using effectively the same skill subset without deliberate reason;
- technique overload or multiple techniques serving no clear narrative function;
- selected technique has high renderer risk but no fallback.

These should surface warnings. Do not turn all warnings into hard blocks.

## First implementation milestone

The first useful milestone should be deliberately small.

Suggested acceptance flow:

```text
1. Input one episode brief + character ID.
2. Resolve canonical character context.
3. Run Director Core to identify directing mode(s), relevant failures, and required capabilities.
4. Route/select a small skill subset for Candidate A and a distinct subset for Candidate B where appropriate.
5. If needed, retrieve a small cinematic-technique subset by narrative function and renderer feasibility.
6. Ask one configured LLM to return two storyboard candidates in structured form.
7. Validate the six-field shot schema and selected-skill/technique metadata.
8. Export human-readable Markdown/JSON.
9. Compile the selected candidate into one scene-grid storyboard prompt.
10. Stop before automatic video rendering if integration would expand scope materially.
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
- optionally allow a second independent LLM to generate an alternate candidate set;
- improve routing metadata only from observed misroutes or missing skill coverage;
- accumulate renderer-specific technique reliability only from actual tests/results.

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
- load all directing guides/examples into every episode prompt;
- load the entire cinematic-technique catalogue into every candidate;
- merge many references into an averaged default style;
- maximize technique count as a quality metric;
- create a new parallel gallery/artifact store;
- fork renderer integration unnecessarily;
- force commercial-film-level metadata;
- add vector DB / workflow engine / event platform solely for this feature;
- scrape/index hundreds of external techniques before a real production need exists;
- vendor external projects such as Hypit, MoneyPrinterTurbo, Buzz, or Melies content just because their architecture/reference material was studied;
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

### From prompt/reference study

Good examples should be decomposed into:

- transferable principle;
- example-specific stylistic choice.

Only the transferable principle should be promoted into core/directing memory. Example-specific choices should remain optional references.

A useful pattern observed in strong prompts is:

> keep global continuity strong while allowing shot grammar to vary.

This does **not** mean every episode should copy the same camera language.

### From cinematic-technique study

A large technique catalogue is valuable as vocabulary, but loading or using many techniques at once is not the goal.

The system should select techniques based on:

- narrative function;
- visual problem being solved;
- coherence with the chosen directing mode;
- renderer feasibility;
- fallback availability.

Variety should emerge across episodes and characters, while each individual episode remains visually coherent.

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
- one lightweight skill-routing convention/manifest exists;
- one small technique-routing convention/manifest exists or reuses the same routing mechanism;
- one command/function/path can produce two structured candidates from an episode brief using a configured LLM;
- each candidate records which skills/references were selected;
- selected techniques, if any, record narrative purpose and renderer risk/fallback;
- relevant Director Memory/capability context is injected without copying the entire repository into the prompt;
- only a bounded, relevant skill/reference/technique subset is loaded per candidate;
- output validates deterministically;
- selected candidate can be exported/compiled into a scene-grid storyboard prompt artifact;
- no existing character/gallery/renderer contract is broken;
- tests cover schema validation, routing metadata, and at least one fixture showing distinct candidate skill subsets;
- docs explain how Claude/Grok/Hermes/Codex can consume the same durable output;
- implementation remains scoped and does not resume paused repository cleanup.

After this point, use the feature on one real vlog before expanding it.
