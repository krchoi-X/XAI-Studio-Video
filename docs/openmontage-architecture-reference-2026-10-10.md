# OpenMontage architecture reference and XAI Studio applicability

- Date: 2026-10-10
- Status: ARCHITECTURE REFERENCE / METHODOLOGY INPUT
- External source: https://github.com/calesthio/OpenMontage
- Scope: record the OpenMontage architecture, compare it with XAI-Studio-Video, and preserve recommendations for selective adoption.
- This note does not change canonical contracts, schemas, queues, or production ownership by itself.

Related XAI Studio documents:
- `docs/creative-treatment-production-storyboard-role-split-PROPOSAL.md`
- `docs/hermes-autonomous-pipeline-TASK.md`
- `docs/director-memory/autonomous-video-quality-guide.md`
- `docs/external-reference-and-h3-long-video-notes-2026-10-08.md`
- `docs/idea-to-production-contracts.md`

---

## 1. What OpenMontage is

OpenMontage describes itself as an open-source agentic video production system.

The central architecture is **agent-first and instruction-driven**:

```text
User request
-> agent reads pipeline manifest
-> agent reads stage-director skill
-> agent calls tools
-> agent writes checkpoint/artifacts
-> agent self-reviews
-> optional human approval gate
-> next stage
-> final render
```

A key architectural point in its documentation is:

- there is no central Python orchestrator deciding creative workflow;
- the AI coding agent is the control plane;
- Python provides tools, persistence, schemas, checkpointing, media operations, and provider adapters;
- pipeline manifests and skills contain the operational knowledge.

Its common stage progression is:

```text
research
-> proposal
-> script
-> scene_plan
-> assets
-> edit
-> compose
-> publish
```

OpenMontage also has specialized pipelines for cinematic work, animation, character animation, hybrid source/generated production, talking heads, localization, short-form extraction, and other tasks.

---

## 2. OpenMontage components worth studying

### 2.1 Pipeline manifests

Each pipeline is declared in YAML.

A manifest specifies things such as:

- stage order;
- stage-director skill;
- tools available in that stage;
- artifacts produced;
- review focus;
- success criteria;
- whether human approval is required;
- checkpoint policy;
- budget rules.

This gives each stage an explicit production contract without hard-coding the creative logic in Python.

### 2.2 Stage-director skills

Each stage has a Markdown skill that teaches the agent how to do that stage.

This separates:

```text
what tools exist
from
how the production system should use them
```

That distinction is directly relevant to XAI Studio's Hermes design.

### 2.3 Canonical artifacts

OpenMontage persists explicit artifacts rather than allowing important production state to live only in chat context.

Examples include:

- brief;
- script;
- scene_plan;
- asset_manifest;
- edit_decisions;
- render_report;
- review;
- cost_log.

The exact artifact set is not necessarily appropriate for XAI Studio, but the principle is highly relevant.

### 2.4 Checkpoints

Pipeline state is persisted after stages.

This supports:

- resume;
- audit;
- stage status;
- approval gates;
- artifact versioning;
- failure recovery.

### 2.5 Decision log

The agent guide treats consequential production decisions as explicit records.

Important decisions include:

- provider;
- model;
- render path;
- composition runtime;
- voice;
- other major production choices.

The documented rule is append-only history: when a decision changes, a new entry is appended rather than silently rewriting the old reasoning.

### 2.6 Tool registry and selector pattern

OpenMontage separates:

```text
capability
from
provider
```

For example a video-generation capability can route to several providers. The agent can inspect available tools and choose based on task fit, quality, cost, reliability, latency, and user preference.

This is relevant to XAI Studio's need to switch between H3, LTX, Wan, Qwen/Krea-style image paths, and future engines without rewriting the creative methodology.

### 2.7 Backlot — living storyboard

OpenMontage includes a local production board called Backlot.

It derives its display from files already written by the pipeline and can show:

- current stages;
- script;
- scene-plan filmstrip;
- asset-generation progress;
- approvals;
- decisions;
- spend;
- generated takes;
- renders;
- replay of the run history.

It is read-only with respect to production state and derives the board from durable artifacts, checkpoints, event logs, and output files.

### 2.8 Reference-video workflow

Reference video is treated as a first-class production entry point.

The documented workflow analyzes items such as:

- transcript;
- pacing;
- structure;
- scenes;
- keyframes;
- style.

It then proposes differentiated concepts rather than copying the reference literally.

This aligns closely with XAI Studio's existing Muse/Somni reference-state analysis direction and the rule to take reference grammar rather than content.

---

## 3. Direct comparison with the current XAI Studio direction

### OpenMontage default

```text
User
-> one strong coding agent
   -> research
   -> proposal
   -> script
   -> scene planning
   -> asset generation
   -> edit
   -> composition
   -> review
```

The same frontier coding agent remains the main production intelligence.

### XAI Studio target

The current proposed target is intentionally different:

```text
User
-> Frontier Creative Director
   (ChatGPT / Claude / Grok)
-> Creative Treatment
-> Hermes LLM
-> Production Storyboard
-> Hermes LLM
-> engine-specific prompts
-> Hermes Runtime
-> Local Engines
-> Hermes first-line review
-> frontier escalation only when needed
```

The important distinction is **creative responsibility is split across layers**.

Frontier models are used where broad synthesis and long-context reasoning are valuable.

Hermes owns local production direction and runtime prompt authorship.

Local image/video models own media generation.

---

## 4. Recommendation: do not replace the XAI Studio role split

OpenMontage is strong evidence that an instruction-driven agent can operate a production system from manifests, skills, tools, checkpoints, and artifacts.

It is **not** evidence that XAI Studio should collapse back into one frontier-agent-as-everything architecture.

The XAI Studio role split should remain:

> **Frontier models shape the story; Hermes directs the production; local engines render it.**

Reasons:

1. XAI Studio wants routine production to remain local-first.
2. Hermes needs ownership of the actual production storyboard and runtime prompts.
3. Frontier models are most valuable for idea development, treatment, difficult synthesis, and escalation.
4. Local production should not require a frontier model in the normal loop.
5. The user explicitly wants production-level mature/adult styling decisions to remain in the local production layer when appropriate to clearly adult fictional characters and the local environment.
6. Local model replacement should remain possible without replacing the entire creative front end.

Therefore the recommendation is:

```text
adopt OpenMontage's orchestration patterns
without adopting OpenMontage's single-agent ownership model
```

---

## 5. High-value patterns to consider adopting

### 5.1 Explicit pipeline manifest

XAI Studio already has contracts, skills, tools, and task documents.

A useful next step would be a compact manifest that clearly names, for every stage:

```yaml
stage:
primary_actor:
inputs:
skill:
tools:
produces:
review:
approval_gate:
next:
```

Example conceptually:

```yaml
- stage: creative_treatment
  primary_actor: frontier_creative_director
  produces: creative_treatment

- stage: production_storyboard
  primary_actor: hermes_llm
  consumes: creative_treatment
  produces: production_storyboard

- stage: runtime_prompt
  primary_actor: hermes_llm
  consumes: production_storyboard
  produces: prompt_packet

- stage: generation
  primary_actor: hermes_runtime
  renderer: local_engine

- stage: first_review
  primary_actor: hermes_llm
```

The value is not YAML itself. The value is **making the subject of each stage impossible to misunderstand**.

This directly addresses the user's recent concern: "who makes the storyboard, who makes the prompt, who submits it?"

### 5.2 Canonical artifact lineage

The following lineage would be useful:

```text
idea
-> creative_treatment
-> production_storyboard
-> prompt_packet
-> render_job
-> render_result
-> review_report
```

Each artifact should record provenance where practical:

```yaml
author:
model:
created_at:
input_artifact_ids:
engine_target:
revision:
```

This would make it much easier to diagnose:

- who changed the idea;
- who changed the shot;
- who wrote the prompt;
- which renderer produced the output;
- which review justified the repair.

### 5.3 Append-only production decision log

This is one of the highest-value OpenMontage ideas for XAI Studio.

Useful decision categories could include:

- treatment_author;
- storyboard_author;
- prompt_author;
- image_engine;
- video_engine;
- continuity_strategy;
- reference_role;
- aspect_ratio;
- scene_split;
- render_mode;
- repair_strategy.

When a choice changes, preserve the earlier choice and append the revised decision.

Do not silently overwrite history.

### 5.4 Living production board

Backlot is a strong UI reference.

XAI Studio already has Studio / Gallery / Control Tower concepts. Rather than clone Backlot, consider a production view that can show:

```text
Idea
Treatment
Storyboard
Prompt
Reference set
Continuity strategy
Current render state
Generated takes
Review findings
Accepted / rejected clips
Next repair
```

The user should be able to look at one production and understand immediately:

- what Hermes is doing;
- what it already decided;
- where it is waiting;
- which prompt created each clip;
- what failed;
- what is being regenerated.

This could solve a practical problem more important than another methodology rewrite: production state is currently spread across documents, queues, sessions, and agent reports.

### 5.5 Tool capability registry

A capability registry deserves further study.

Conceptually:

```text
image_generation
  -> Krea-compatible path
  -> Qwen Image 2.1
  -> Z-Image
  -> future image model

video_generation
  -> MiniMax H3
  -> LTX
  -> Wan
  -> future video model
```

Hermes should reason about capability first, provider second.

This reduces hard coupling between storyboard logic and a specific model.

### 5.6 Reference analysis as a first-class workflow

XAI Studio already has much of this through Muse/Somni and the reference corpus.

OpenMontage reinforces the value of formalizing:

```text
reference
-> transcript / frame / scene / pacing analysis
-> reusable grammar
-> differentiated creative treatment
```

This should continue to feed evidence and treatment, not become literal copying.

---

## 6. Patterns to avoid copying directly

### 6.1 One agent owns all creative stages

Do not adopt this as the XAI Studio default.

It conflicts with the intended Frontier Treatment / Hermes Production Director separation.

### 6.2 Excessive human approval at every decision

OpenMontage exposes many explicit approval gates because it is a general-purpose production framework.

XAI Studio's goal is more autonomous local production.

Keep user approval for high-value gates such as:

- treatment choice when needed;
- production-storyboard approval;
- expensive or long batch GO;
- final acceptance;
- major model/path changes.

Do not make the user approve routine mechanical decisions.

### 6.3 Copying its artifact taxonomy wholesale

XAI Studio has different production needs, especially:

- Character DNA;
- identity reference lineage;
- continuity state;
- first/last keyframes;
- local GPU queues;
- overnight generation;
- local adult-oriented production details for clearly adult fictional characters;
- clip-level repair.

Reuse the artifact principle, not necessarily the artifact names.

### 6.4 Replacing existing Hermes Runtime with a frontier coding agent

The current local-runtime direction should remain.

OpenMontage is a reference for **how instructions can drive tools**, not a reason to move the renderer queue back under Claude/Codex.

---

## 7. My architecture opinion

### Strong recommendation

Treat OpenMontage as a **primary architecture reference** for XAI Studio.

Among the external projects reviewed so far, it is unusually relevant because it addresses the same higher-level problem:

> how to turn an AI agent plus many media tools into a repeatable production studio rather than a pile of prompts.

The highest-value ideas are not its provider integrations or individual pipelines.

They are:

1. explicit pipeline manifests;
2. stage-director skills;
3. canonical durable artifacts;
4. checkpoints;
5. append-only decision history;
6. a capability-oriented tool registry;
7. a living production board;
8. reference video as a formal workflow.

### Most important near-term improvement

The first thing to borrow should **not** be more generation code.

It should be clearer production observability.

The current XAI Studio methodology has increasingly good reasoning about:

- treatment;
- production storyboard;
- continuity;
- prompts;
- renderer choice;
- failure memory.

But if the user cannot easily see "who made what and where the production currently is", the system will still feel opaque.

Therefore the most useful OpenMontage-inspired improvement is likely:

```text
one production
-> one visible lineage
-> one current state
-> one decision history
```

### Second improvement

Add an explicit role-bearing pipeline manifest.

This would operationalize the recently agreed role split and stop future drift such as:

```text
Claude happened to compile prompts in a test
-> later readers assume Claude is the normal prompt author
```

A stage manifest can make the normal owner explicit even when an experiment temporarily deviates.

### Third improvement

Introduce append-only decision lineage before building more autonomous behavior.

Autonomy without traceability will make failures harder to diagnose.

A small decision log is higher ROI than another large agent-memory layer.

---

## 8. Proposed review questions for Codex / Claude

Before implementing anything, compare OpenMontage patterns against existing XAI Studio components.

### Pipeline manifest
- Is there already one authoritative artifact that names every production stage and owner?
- If not, can one be added without duplicating existing skills/contracts?

### Artifact lineage
- Which current artifacts already correspond to:
  - creative treatment;
  - production storyboard;
  - prompt packet;
  - render job;
  - result;
  - review?
- Which are missing or only implicit in chat/task files?

### Decision history
- Is provider/model/continuity choice currently durably recorded?
- Can append-only decision records be added without changing existing persisted contracts?

### Production UI
- Can the current Productions view evolve toward a living production board?
- Which state can already be derived from existing sessions and artifacts without adding another database?

### Tool registry
- Can local engines be represented by capability + provider + runtime + stability + resource profile?
- Can Hermes query that inventory before compiling prompts?

### Reference workflow
- Can Muse/Somni reference grammar be attached directly to a Creative Treatment without bloating the prompt or canonical DB?

---

## 9. Suggested priority

```text
P0/P1:
- preserve this repo as an architecture reference
- compare OpenMontage pipeline/artifact/decision patterns with current XAI Studio

P1:
- formalize stage ownership
- add artifact lineage where missing
- design append-only decision history

P1/P2:
- evolve Productions view toward a living production board

P2:
- capability-oriented engine registry / selector
- deeper provider abstraction

Not now:
- port OpenMontage wholesale
- replace Hermes Runtime
- copy all 12 pipelines
- copy all skills
- redesign the full methodology again
```

The guiding rule remains:

> **Borrow the operating-system ideas, not the whole operating system.**

OpenMontage is most valuable as evidence that the architecture XAI Studio is converging on — skills + tools + artifacts + checkpoints + agent judgment — is a viable and increasingly important production pattern.
