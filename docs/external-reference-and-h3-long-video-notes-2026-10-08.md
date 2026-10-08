# External reference sources and MiniMax H3 long-video orchestration notes

- Date: 2026-10-08
- Status: RESEARCH NOTE / INPUT TO METHODOLOGY REVIEW
- Scope: record two external references discussed with the user and the resulting recommendations.
- Related:
  - `docs/creative-treatment-production-storyboard-role-split-PROPOSAL.md`
  - `docs/hermes-autonomous-pipeline-TASK.md`
  - `docs/director-memory/autonomous-video-quality-guide.md`
  - `docs/reference-state-analyses.md`
  - `docs/directing-technique-db.md`
  - `docs/prompt-craft-db.md`

This note does not change a schema, queue, renderer, or canonical methodology by itself.

---

## 1. CheerSelfAI resource library

Source:
- https://cheerselfai.com/en/resources

### What the source currently provides

The resource library presents itself as a curated, source-aware collection rather than an unlimited link dump. Its stated curation standards include:

- used in practice or verified against the source;
- states who the item is for and what problem it solves;
- prefers official documentation and first-hand sources.

Relevant sections for XAI Studio include:

- MiniMax H3 Video Prompt Library;
- MiniMax H3 Video Gallery;
- Seedance 2.5 Video Prompt Library;
- Seedance 2.5 Video Gallery;
- Blender + Seedance workflow examples;
- agent/product comparison experiments;
- public model use-case collections with original-source attribution and evidence limits.

As of 2026-10-08 the site reports a Seedance 2.5 gallery with more than 11,000 public video references and preserves creator/source metadata.

### Why it is useful here

This is a good **external reference source**, not a database to mirror wholesale.

It can feed three different internal lanes:

```text
Prompt examples
  -> candidate prompt-craft lessons

Video examples
  -> reference-state analysis / directing-technique candidates

Workflow / agent examples
  -> methodology and role-architecture candidates
```

### Recommended ingestion rule

Do not promote an external example directly into a canonical rule.

For each imported item, preserve:

```yaml
source:
creator:
model_and_version:
task:
original_prompt_if_available:
output_reference:
what_worked:
what_failed_or_is_unknown:
reusable_hypothesis:
evidence_level:
```

Promotion path:

```text
external source
-> evidence note
-> repeated observation
-> candidate lesson
-> validated production result
-> technique / prompt-craft / methodology promotion
```

### Recommendation

Use CheerSelfAI as one of the high-value discovery sources for Muse/Somni and manual research.

Priority areas:

1. MiniMax H3 prompt/gallery cases;
2. Seedance 2.5 prompt/gallery cases;
3. Blender + Seedance previs workflows;
4. agent/workflow cases that expose role split, tool ownership, and failure modes.

Do not scrape or clone the entire site into this repository by default. Preserve source URLs and evidence instead.

---

## 2. Ripcurlsurf/Mini-Max-Long-Videos-unlimited-scenes

Source:
- https://github.com/Ripcurlsurf/Mini-Max-Long-Videos-unlimited-scenes

Repository description:
- community project;
- single-file offline HTML workflow generator;
- creates ComfyUI workflows for long, multi-scene MiniMax H3 productions.

### Verified features from the repository README

The tool supports:

- arbitrary numbers of scenes;
- per-scene prompt, duration, seed, and optional first/last frame;
- MiniMax H3 ImageToVideo and ReferenceToVideo paths;
- optional Qwen Image 2.1 reference-image generation;
- consistency-bible text injected into every scene;
- dialogue/sound fields and optional external TTS;
- scene-range rendering;
- ffmpeg assembly outside the ComfyUI graph;
- strict scene ordering;
- ComfyUI subgraph packing;
- an AI-fillable JSON template workflow.

### Continuity modes

The repository explicitly separates three continuity mechanisms:

#### A. Last-frame chaining

```text
scene N last frame
-> scene N+1 first frame
```

Advantage:
- simple and smooth for a directly continuous action.

Risk:
- errors and drift accumulate across scenes.

#### B. First + last keyframes

Each scene is anchored between planned endpoint frames.

Advantage:
- explicit endpoint control;
- less accumulated drift;
- scenes can be regenerated independently.

Cost:
- N scenes need approximately N+1 planned keyframes;
- keyframe quality becomes a production dependency.

#### C. Reference-to-video

Character/location/style references are supplied to each scene through H3 semantic reference inputs.

Advantage:
- useful for identity, location, and style persistence;
- avoids relying on chained pixels alone.

Limitation:
- reference conditioning is not the same thing as temporal-state continuity;
- this mode does not use FIRST/LAST inputs in the cited tool.

### Important design lesson

Continuity should not be treated as one prompt-writing problem.

It is useful to separate continuity by responsibility:

```text
identity continuity
-> identity reference / Character DNA

location continuity
-> location reference / plate

temporal-state continuity
-> previous last frame or explicit boundary frame

planned endpoint continuity
-> first + last keyframes

dialogue / voice continuity
-> external TTS or dedicated audio pipeline when needed

story / causal continuity
-> Hermes Production Storyboard
```

This is directly relevant to the current XAI Studio failures where text-only continuity was insufficient.

---

## 3. Broader H3 long-video ecosystem signal

The Ripcurlsurf repository should not be treated as a unique proof that one implementation has solved long-form generation.

Current public work shows several parallel approaches:

- H3-LongVideos: shot-by-shot generation with last-frame continuation;
- LongMedia Director: timeline authoring with semantic REF / FIRST / LAST roles;
- experimental long-reference samplers with latent continuation and segment rerolling;
- H3-LongTake: clip-by-clip resumable generation and rerender of individual clips;
- AutoContext / Endless-Sampler style projects: segmented inference and latent anchoring.

The shared architectural pattern is more important than any single repository:

```text
long-form authoring
-> model-sized segments
-> explicit continuity carrier
-> disk-backed checkpoints
-> selective rerender
-> final assembly
```

This supports the direction already emerging in XAI Studio: long video is primarily an **orchestration problem around a short-video model**, not a single-prompt / single-render problem.

---

## 4. Recommended integration into XAI Studio

### 4.1 Add a continuity-strategy decision to Hermes planning

Do not force one global continuity method.

Hermes should decide per scene boundary, using a small vocabulary such as:

```text
HARD_CUT
REFERENCE_ONLY
LAST_FRAME
FIRST_LAST_KEYFRAME
LOCATION_PLATE
DELIBERATE_MONTAGE
```

A production-plan representation could conceptually carry:

```yaml
continuity:
  identity: reference
  location: reference
  temporal: last_frame
  endpoint: none
  audio: external_tts
```

Exact schema design remains a Codex/integration decision. Do not introduce a new schema solely for this note.

### 4.2 Prefer scene logic over fixed duration

Keep the newer methodology rule:

- cut because place, time, viewpoint, or dramatic function changes;
- do not split every production into identical five-second chunks merely because H3 is clip-oriented.

Use H3 scene boundaries as an execution constraint, not as the story grammar.

### 4.3 Use chunked rendering for long productions

For large productions:

```text
Production Storyboard
-> chunk 01 (e.g. scenes 1-15)
-> chunk 02
-> chunk 03
-> ...
-> ffmpeg / assembly step
```

Benefits:

- bounded failure domain;
- easier overnight batching;
- selective repair;
- lower RAM pressure;
- resumable production.

Chunk size should be benchmark-driven, not copied blindly from an external repository.

### 4.4 Preserve independent scene generation where possible

Default to independent scenes plus stable references when the story permits.

Use LAST_FRAME or FIRST_LAST_KEYFRAME only where temporal continuity actually adds value.

Reason:

- chaining transfers good state;
- chaining also transfers bad state.

A bad hand, bad pose, wrong prop, or camera error can become the next scene's starting truth.

### 4.5 Keep story continuity under Hermes

No continuity mechanism replaces production reasoning.

Even perfect pixel-level handoff does not answer:

- why the character moved;
- where the bag went;
- which direction the bus travels;
- whether it is the same location;
- why the radio was fixed;
- whether the next scene occurs later.

Those remain Hermes Production Storyboard responsibilities under the role-split proposal.

---

## 5. Relation to the Creative Treatment / Hermes role split

The external references strengthen, rather than replace, the proposed role model:

```text
User
-> Frontier Creative Treatment
-> Hermes Production Storyboard
-> Hermes engine-specific prompts
-> Hermes Runtime
-> local image/video engines
-> Hermes first-line review
-> frontier escalation when needed
```

The long-video references mainly improve the **Hermes Production Storyboard -> Runtime** boundary:

- Hermes chooses continuity strategy;
- Hermes writes the prompt;
- Hermes Runtime wires the correct reference/frame mechanism;
- the local H3/ComfyUI engine performs generation.

They do not argue for moving storyboard authorship back into Claude/ChatGPT.

---

## 6. Licensing / reuse caution

The Ripcurlsurf repository has a licensing inconsistency worth preserving as a warning.

At repository metadata level GitHub currently reports GPL-3.0, while the README text states personal/non-commercial/educational use only and prohibits commercial incorporation without permission.

Therefore:

- treat the repository as an architectural reference;
- do not copy source code into XAI Studio until the license is clarified;
- independently implement useful concepts where needed;
- preserve provenance if any code is ever evaluated for reuse.

This is not legal advice; it is a repository-risk note.

---

## 7. My recommendation

### Strong recommendation

Adopt the **concepts**, not the external implementation.

The two highest-value additions are:

1. explicit per-boundary `continuity_strategy`;
2. chunked, resumable long-video rendering with selective rerender and final assembly.

### Do not do yet

- do not replace the current methodology;
- do not add another large canonical schema without a demonstrated gap;
- do not make last-frame chaining the default for every scene;
- do not treat a long-video node as a solution to causal/story continuity;
- do not copy the external repository code while its license remains ambiguous.

### Suggested experiment

Use one short story with a genuine continuous action and compare:

```text
A. independent scenes + identity/location references
B. last-frame chaining
C. planned first/last keyframes
```

Hold the story, character, and engine settings as constant as practical.

Judge:

- identity;
- place;
- pose/state continuity;
- accumulated visual drift;
- editability after one failed scene;
- total render/rework time.

That experiment is more valuable than choosing a continuity mechanism from documentation alone.

---

## 8. Priority assessment

This research does **not** justify another methodology reset.

Priority:

- P1: preserve as implementation/reference input for Hermes long-video orchestration;
- P1: incorporate continuity-strategy vocabulary into the next production-plan review;
- P2: test 2-3 continuity methods on one controlled story;
- P2: use CheerSelfAI selectively as an external evidence source;
- Later: evaluate code-motion / long-media tooling only if a real production requires it.

The current highest-level architectural rule remains:

> **Frontier models shape the story; Hermes directs the production; local engines render it.**

Long-video tooling belongs underneath that rule.
