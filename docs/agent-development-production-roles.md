# Agent Development & Production Role Split

Status: **Draft operating architecture**  
Updated: 2026-09-01

## Goal

Keep expensive coding agents out of the repetitive content-production path.

The system is split into two planes:

```text
DEVELOPMENT PLANE
Codex / Claude Code
→ design and improve rules, skills, adapters, schemas, tests, and UI

PRODUCTION PLANE
Web UI
→ Hermes
→ local / cloud models and generation engines
→ images / text / storyboards / video
```

The user should normally interact only with the web application: enter an idea, choose among options, approve/regenerate results, and request final output.

## Roles

### User — Director

The user does not need to operate Hermes, ComfyUI, local model endpoints, or generation providers directly.

Primary actions:

- enter an idea
- choose a storyboard / concept
- approve or reject shots
- request regeneration
- choose among sample outputs
- trigger final generation

The UI should expose **creative decisions**, not infrastructure decisions.

### Codex — Repository / integration engineer

Primary role:

- repository-wide implementation
- integration between web UI, Hermes, storage, jobs, schemas, and generation services
- refactoring and tests
- API / queue / persistence work
- codebase-wide consistency
- creation and maintenance of Hermes-facing adapters where repository integration is involved

Codex is not part of the normal content-generation loop.

### Claude Code — Skill / workflow / UX co-developer

Primary role:

- design and improve Hermes instructions and reusable skills
- refine `SKILL.md` workflows
- create prompt templates and structured output contracts
- review creative workflow quality
- UI/UX implementation or polish where it performs better than the current Codex path
- independently own clearly bounded implementation tasks when useful

Claude Code should not simultaneously edit the same files as Codex. Prefer **serial ownership** of a task or file set.

### Hermes — Production execution agent

Hermes is the production worker.

It reads the approved skills, instructions, schemas, character/world knowledge, and model adapters created by Codex / Claude, then performs the actual content work.

Typical responsibilities:

- interpret user ideas
- produce storyboard candidates
- write or refine prompts
- create prose / scripts
- call image generation
- call video generation
- call local or cloud models
- invoke ComfyUI / H3 / Seedance / future renderers
- validate outputs
- return structured results to the web UI

Hermes should normally run without requiring Codex or Claude for every production job.

## Production flow

Preferred user-facing flow:

```text
1. IDEA
   user enters a simple concept

2. STORYBOARD
   Hermes produces several structured candidates

3. SAMPLE
   user selects one candidate
   Hermes generates low-cost sample images / clips

4. REVIEW
   user approves, rejects, edits, or regenerates selected shots

5. FINAL
   Hermes routes approved shots to final-quality renderers
```

Example:

```text
User:
"Lia finishes her convenience-store shift and walks by the sea eating ice cream."

        ↓

Hermes + storyboard skill

        ↓

A. quiet after-work version
B. cat-homecoming version
C. sunset cinematic version

        ↓
User selects B

        ↓

Hermes creates shot specs + samples

        ↓
User approves / regenerates

        ↓

Hermes performs final generation
```

## Development flow

The development plane improves the production plane itself.

```text
production failure / UX friction / repeated prompt weakness
        ↓
identify failing responsibility
        ↓
Codex or Claude updates:
- SKILL.md
- prompt template
- schema
- model adapter
- validation rule
- UI
- tests
        ↓
Hermes uses improved version on future jobs
```

Do not fix recurring production problems by manually rewriting prompts for every job if the underlying skill or adapter can be improved once.

## Canonical artifacts

Codex / Claude should primarily maintain reusable artifacts such as:

```text
skills/
  idea-to-storyboard/
  character-consistency/
  image-prompt/
  video-prompt/
  vlog-director/
  result-review/

templates/
  storyboard-spec.md
  image-generation-request.md
  video-generation-request.md

schemas/
  storyboard.json
  generation-job.json
  review-result.json

adapters/
  hermes/
  local-llm/
  comfyui-h3/
  seedance/
  image-models/
```

Actual names may evolve; the responsibility split matters more than the directory spelling.

## UI ↔ Hermes contract

Prefer structured contracts at system boundaries.

User input may be natural language, but the web application and Hermes should exchange explicit structured state wherever practical.

Example request:

```json
{
  "action": "create_storyboards",
  "idea": "Lia walks home after work and eats ice cream by the sea",
  "character_id": "lia",
  "candidate_count": 3
}
```

Example response:

```json
{
  "storyboards": [
    {
      "id": "sb-01",
      "title": "Quiet Walk",
      "shots": []
    }
  ]
}
```

This prevents the UI from depending on one model's conversational phrasing.

## Model / tool hiding

Normal UI:

```text
Text       Auto
Image      Auto
Video      Auto
```

Advanced UI may expose:

```text
Story planner → Hermes + local LLM
Image        → local / cloud provider
Video        → H3 / Seedance / other
Final render → local / Runpod / Vast / other
```

Infrastructure details should stay hidden unless the user explicitly needs to override routing.

## Cost strategy

Use expensive coding agents to improve reusable production capability, not to repeatedly create individual content.

Preferred:

```text
Codex / Claude
→ build or improve a skill once

Hermes + local / low-cost models
→ use that skill many times
```

Avoid:

```text
Every image / video / story
→ requires Codex or Claude interaction
```

That turns development-model credits into recurring production cost.

## Ownership rules

1. One agent owns a bounded change at a time.
2. Avoid Codex and Claude editing the same files concurrently.
3. Before handing off:
   - commit or clearly preserve the current state
   - state what changed
   - state what remains
   - state acceptance criteria
4. Prefer small, testable changes.
5. Production jobs must not modify canonical skills unless explicitly running a development workflow.

## Escalation logic

Suggested ownership:

```text
Hermes
→ normal content production

Claude Code
→ skill/prompt/workflow refinement
→ bounded UI implementation/polish

Codex
→ repository-wide integration
→ persistence, jobs, APIs, architecture implementation

Codex + Claude review
→ only for hard cross-cutting changes when the added cost is justified
```

The precise model used inside each tool may change; the role boundary should remain stable.

## Architectural principle

**The user directs content. Hermes produces content. Codex and Claude improve the production system.**

This allows model and provider changes without forcing the user to learn a new production workflow.

```text
User
  ↓
Creative Web UI
  ↓
Hermes
  ↓
Skills / Knowledge / Adapters
  ↓
Local LLM / Image / Video / GPU services

          ▲
          │ improve
Codex / Claude Code
```

## Next implementation milestones

1. Define the web UI's five canonical states:
   - Idea
   - Storyboard
   - Sample
   - Review
   - Final
2. Define the JSON contract for Idea → Storyboard.
3. Create the first Hermes `idea-to-storyboard` skill.
4. Add structured generation-job state.
5. Connect one low-cost sample image/video path.
6. Add per-shot approve / regenerate.
7. Keep model/provider selection behind an advanced settings layer.
