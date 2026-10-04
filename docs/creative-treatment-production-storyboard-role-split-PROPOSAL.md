# Proposal — Creative Treatment / Production Storyboard Role Split

- Date: 2026-10-04
- Status: PROPOSAL — review for integration; no schema, contract, queue, renderer, or Studio change is authorised by this document.
- Scope: clarify **who owns each creative and production step** in the Hermes autonomous video pipeline.
- Intended reviewers: Codex / Claude Code / ChatGPT when maintaining the production methodology.
- Related documents:
  - `docs/hermes-autonomous-pipeline-TASK.md`
  - `docs/director-memory/autonomous-video-quality-guide.md`
  - `docs/idea-to-production-contracts.md`
  - `docs/hermes-pipeline-step1-findings.md`
  - `docs/director-memory/failures.md`

## Why this proposal exists

The current pipeline documents say that Hermes runs the whole chain, but some real production tests were executed with Claude compiling runtime prompts and selecting production details. That makes the **subject of each step** ambiguous.

The user wants the final system to preserve two things at once:

1. Use frontier models where long-context reasoning, reference synthesis, and failure-memory interpretation are valuable.
2. Keep the actual production storyboard, runtime prompts, and local generation under Hermes/local control so that the production system remains flexible, local-first, and not dependent on frontier-model intervention for routine work.

The proposed solution is to split the old single `idea -> storyboard` step into two creative layers:

```text
idea
-> Creative Treatment
-> Production Storyboard
-> engine-specific runtime prompts
-> local generation
```

The most important design rule is: **every stage has one clearly named primary author/operator.**

---

## Proposed role model

### 1. User — Idea Owner / Final Approver

The user supplies the idea, direction, constraints, or source material and remains the final authority for creative approval and GO gates.

Typical inputs:

- a one-line idea;
- an external prompt or reference;
- a desired mood or genre;
- an existing character;
- a request to imitate only the grammar of a successful reference;
- an approved/rejected production result.

The user does not need to write a production-ready storyboard.

---

### 2. Frontier Creative Director — ChatGPT / Claude / Grok

**Primary responsibility: turn the raw idea into a Creative Treatment.**

The frontier model should use the available long-context evidence:

- previous failures and production incidents;
- successful references and reference analyses;
- directing-technique DB;
- prompt-craft DB;
- approved/rejected examples;
- current Character / location constraints where relevant.

It answers:

- What is this piece actually about?
- What should the viewer understand?
- What should the viewer feel?
- What is the story arc?
- What are the important visual moments?
- What reference grammar is useful?
- Which known production failures should be avoided?
- Which parts should remain creatively open for Hermes?

It should **not normally write the final shot-by-shot production storyboard or renderer prompt**.

### Creative Treatment boundary

The treatment should stay above the shot-production layer.

Recommended content:

```yaml
concept:
viewer_should_understand:
viewer_should_feel:
story_arc:
key_visual_moments:
important_objects:
reference_grammar:
known_failure_risks:
production_risks:
creative_freedom:
```

Avoid prematurely locking:

- exact shot count;
- exact camera path;
- exact timing per action;
- renderer-specific syntax;
- final prompt wording;
- detailed per-frame state changes.

Those decisions belong to Hermes unless the user explicitly requests otherwise.

### Content-boundary note

The frontier treatment should remain usable as a self-contained general-audience creative brief. It should not encode hidden instructions intended to bypass another provider's policies.

For clearly adult fictional characters, mature styling or other adult-oriented production details may be decided later by the local Production Director where appropriate to the user's intent and the policies/rules governing that local production environment.

This separation is a responsibility boundary, not a policy-evasion mechanism.

---

### 3. Local Production Director — Hermes LLM

**Primary responsibility: turn the Creative Treatment into a production-ready storyboard.**

Hermes owns the actual production decisions:

- number of clips/shots;
- cut boundaries;
- shot purpose;
- camera and framing;
- character blocking;
- performance and gesture;
- wardrobe/styling choices;
- visible-world state;
- continuity and handoff;
- reference roles;
- renderability decisions;
- local-model-specific simplification or enrichment.

Hermes should use the current production environment, not an abstract ideal:

- active Character DNA;
- approved identity references;
- location/background references;
- available local image/video engines;
- aspect-ratio constraints;
- known engine capabilities and limitations;
- current failure memory;
- current render budget.

The production storyboard should answer:

```yaml
shot_id:
intent:
where:
camera:
screen_direction:
people_and_positions:
entry_state:
primary_action:
visible_cause:
exit_state:
handoff:
important_props:
references:
renderability:
engine_candidate:
```

The exact schema remains an integration decision. This proposal does **not** require a new schema if `shot-production-plan-v2` plus the existing visible-world packet can already carry the information.

---

### 4. Prompt Author — Hermes LLM

**Hermes also writes the actual image and video prompts.**

This is deliberate.

The same local production director that chose the shot should translate that decision into the engine-specific prompt, because it knows:

- why the shot exists;
- which details are hard invariants;
- which details can remain flexible;
- which engine is being used;
- which references are attached;
- which previous failures apply.

Example flow:

```text
Creative Treatment
  -> Hermes Production Storyboard
  -> Hermes Qwen/Krea/Z-Image image prompt
  -> Hermes H3/LTX/Wan video prompt
```

Frontier models may author prompt-writing **skills, guides, adapters, examples, validators, or consultation feedback**, but they are not the default runtime prompt author.

---

### 5. Hermes Runtime — Production Operator

**Primary responsibility: submit and manage jobs, not invent the creative content.**

Hermes Runtime:

- reads the approved production plan;
- resolves approved references;
- chooses the configured adapter/profile;
- submits image/video jobs;
- respects GPU queue ownership and locks;
- records job/session metadata;
- joins clips where required;
- stores artifacts and evidence;
- triggers review passes.

This preserves the existing principle that Hermes is the single normal submitter to the local generation queue.

---

### 6. Local Engines — Renderers

The local engines generate the actual media.

Typical roles:

```text
Local image engines:
  Krea / Qwen / Z-Image / future local image models

Local video engines:
  H3 / LTX / Wan / future local video models

Optional hybrid/code-motion layer:
  typography / UI / overlays / deterministic graphics / compositing
```

The local engine is an executor, not the author of the story structure.

---

### 7. Hermes Review — First-Line Critic

Hermes should perform the normal first review of its own production using an independent pass.

Review evidence should include, where applicable:

- contact sheet;
- critical-frame strip around important actions;
- first/last frames of clip boundaries;
- moving-video review;
- audio/dialogue review;
- continuity comparison;
- state/prop persistence.

The review should ask:

1. Does the story read without explanation?
2. Are place, screen direction, time, and causality coherent?
3. Do identity, wardrobe, carried objects, pose, and emotion persist?
4. Did the important visual moment survive the render?
5. Is the result natural and specific rather than merely compliant?

The authoring pass should not be the only review pass.

---

### 8. Frontier Models — Escalation Consultants

ChatGPT / Claude / Codex / Grok should be called back in only when their stronger reasoning or outside context is worth the cost.

Appropriate escalation cases include:

- two materially similar generation failures;
- unresolved continuity or causality defects;
- ambiguity between several plausible story repairs;
- conflict between production constraints;
- a new engine/model whose behavior is not represented in local guidance;
- a need to synthesize many reference analyses or failure records.

Routine intake, prompt compilation, queue management, and first-line review should remain local.

---

## Proposed end-to-end flow with explicit subjects

```text
[USER]
idea / direction / source material
        |
        v
[FRONTIER CREATIVE DIRECTOR: ChatGPT / Claude / Grok]
Creative Treatment
        |
        v
[HERMES LLM]
Production Storyboard
        |
        v
[HERMES LLM]
Image prompts + Video prompts
        |
        v
[HERMES RUNTIME]
Submit / queue / record / join
        |
        v
[LOCAL IMAGE + VIDEO ENGINES]
Generate media
        |
        v
[HERMES LLM, independent review pass]
Review evidence / repair narrowly
        |
        +--> PASS -> user review / final assembly
        |
        +--> repeated or ambiguous failure
                  |
                  v
        [FRONTIER CONSULTANT]
        diagnosis / recommendation
                  |
                  v
              Hermes repair
```

---

## Why split Creative Treatment from Production Storyboard

### Frontier-model advantage

Frontier models are better suited to the first layer when the job requires:

- synthesizing a large history of failures;
- comparing many successful references;
- reasoning across directing-technique and prompt-craft databases;
- identifying the core dramatic idea;
- producing several distinct creative approaches;
- noticing structural story problems before production detail obscures them.

The output is therefore a **creative direction artifact**, not a renderer prompt.

### Hermes advantage

Hermes is better placed to own the second layer because it sits next to:

- the current local model roster;
- the renderer constraints;
- Character DNA and references;
- the actual production queue;
- the current prompt adapters;
- the outputs and failure evidence.

It can therefore make shot decisions that are both creative and executable.

### Independence advantage

If Hermes or the local production LLM is replaced later, the Creative Treatment can remain the stable interface:

```text
Frontier Creative Treatment
  -> Hermes today
  -> Qwen/MiMo/GLM-based local director later
```

This reduces architectural dependence on any one local LLM.

---

## Relation to the 2026-10-04 Opus motion-design article

The article's useful lesson for this pipeline is not to adopt its `seek(t)` renderer as the main architecture.

The reusable lessons are:

1. **The harness matters more than a one-line prompt.**
2. **Reference material should be converted into grammar, not copied as content.**
3. **State and transitions should be made explicit before rendering.**
4. **Render -> observe -> critique -> repair is part of the method, not evidence of failure.**
5. **Code-motion / deterministic graphics are useful as an optional render strategy for typography, UI, overlays, and hybrid work.**

These lessons fit the existing XAI Studio direction and do not require replacing the current methodology.

### Reference Grammar Extraction

When a reference video or image set matters, a bounded analysis pass should extract reusable grammar such as:

```yaml
reference_grammar:
  pacing:
  framing_pattern:
  camera_language:
  motion_language:
  transition_language:
  environmental_motion:
  performance_style:
  temporal_density:
```

Rule: **take the grammar, not the content, identity, logos, or characters.**

The frontier Creative Director may use or request this analysis to form the treatment. Hermes may also use a production-specific reference grammar when constructing the storyboard.

---

## What should NOT change yet

This proposal does not justify another large methodology rewrite.

Keep:

- current Hermes queue ownership;
- Character DNA as read-only during production;
- current GO gates;
- current failure-memory approach;
- `shot-production-plan-v2` unless a proven field gap exists;
- the current quality guide's bounded passes;
- local-first runtime execution;
- narrow repair after failures.

Do not add a separate `canonical-state-spec-v1` merely because the Opus article uses explicit states. The existing visible-world packet and production plan should be strengthened first. Add a new schema only if repeated real productions prove that the current contracts cannot represent necessary information.

---

## Integration questions for Codex / Claude review

Before editing canonical methodology or contracts, review the following:

1. **Where should Creative Treatment live?**
   - new durable artifact/contract;
   - or an optional document consumed by the existing idea-production worker.

2. **Can the current `idea-production-request-v1` carry a Creative Treatment cleanly without semantic overload?**
   - If not, propose the smallest compatible extension.
   - Do not rename current v1 fields casually.

3. **Can `shot-production-plan-v2` already express the production storyboard responsibilities listed above?**
   - especially WHERE, screen direction, entry/exit state, causality, and handoff.

4. **How should a frontier treatment be requested?**
   - explicit user action;
   - default only for complex productions;
   - or automatically when long-context reference/failure synthesis is needed.

5. **How should multiple frontier treatments be handled?**
   - default: one treatment;
   - optional: ChatGPT/Claude/Grok alternatives only when the user requests exploration or the first treatment is weak.

6. **How do we prevent role drift?**
   - runtime logs should record `treatment_author`, `storyboard_author`, `prompt_author`, `submitter`, and `renderer` where practical.
   - historical tests where Claude compiled prompts must not be interpreted as the future default role model.

7. **How should Reference Grammar Extraction fit the current Muse/Somni corpus?**
   - production-specific grammar should not overwrite evidence corpora;
   - promotion into technique DBs should still require repeated evidence.

---

## Recommended default after review

Unless the integration review finds a contract blocker, use this default:

```text
User
  -> Frontier Creative Treatment
  -> Hermes Production Storyboard
  -> Hermes engine-specific prompts
  -> Hermes Runtime
  -> Local Engines
  -> Hermes Review
  -> Frontier escalation only when needed
```

For very simple productions, the frontier-treatment stage may be skipped and Hermes can start from the user's idea directly.

For complex, reference-heavy, continuity-sensitive, or story-driven productions, the frontier-treatment stage is preferred.

---

## Acceptance criteria for adopting this methodology

Do not declare the proposal adopted merely because the document exists.

Adopt it only after:

1. one complex production uses a frontier-authored Creative Treatment;
2. Hermes independently creates the production storyboard and prompts from it;
3. no frontier model rewrites the runtime prompts during the normal path;
4. local engines generate the media through Hermes Runtime;
5. Hermes performs the first review;
6. the user compares the result with the previous workflow;
7. role ownership and observed defects are recorded.

The decision should be evidence-based after one or two real productions, not another speculative architecture rewrite.

---

## Recommended wording for the top-level methodology

If adopted, keep the top-level rule short:

> **Frontier models shape the story; Hermes directs the production; local engines render it.**
>
> ChatGPT / Claude / Grok create the Creative Treatment when higher-level synthesis is useful. Hermes converts that treatment into the production storyboard and writes all normal runtime prompts. Hermes Runtime submits and records local jobs. Local image/video engines generate the media. Frontier models return only for escalation, methodology design, or explicit user-directed creative work.

This wording keeps the subject of every stage explicit and avoids future ambiguity.
