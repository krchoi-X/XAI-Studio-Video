# Noa Codex Production Postmortem and Next Operating Rule

## Status

Decision record / production lesson. This document is **not** an instruction to stop the current Noa production attempt.

The immediate priority is to **finish the Noa vlog currently being produced with Codex** and evaluate the actual result before making another large architectural change.

## Why this record exists

The first serious Codex-driven attempt to produce a Noa vlog from storyboard through video consumed roughly one 5-hour Codex credit window and still did not reach a completed result.

Some inefficiency is expected because this was an early end-to-end attempt and the workflow is still immature. However, failure to complete inside a full credit window is a strong signal that the current production boundary is too large and that Codex is being asked to perform too many roles in one long-running loop.

Do not explain this away solely as a first-run cost. Treat it as evidence for redesigning the **work boundary**, not merely writing more instructions.

## Immediate rule: finish before redesign

Before changing the pipeline again:

1. Finish the current Noa production attempt.
2. Preserve the resulting storyboard, prompts, intermediate artifacts, failed attempts, render outputs, and final video.
3. Compare the completed Codex result against outputs made from the same or comparable Noa brief by Hermes/Meromero and Grok.
4. Judge the result primarily by the user's taste and production usefulness, not by implementation sophistication.

The point of this comparison is to answer:

> Does the extra Codex cost and complexity produce a materially better storyboard/video result for the user?

Do not assume the answer is yes.

## Comparison criteria

For the current Noa experiment, record at least:

```yaml
producer: codex | hermes_meromero | grok
brief_id: noa_<episode>
storyboard_quality:
  opening_originality:
  spatial_readability:
  character_consistency:
  shot_function_clarity:
  visual_variety:
video_quality:
  identity_consistency:
  motion_naturalness:
  continuity:
  directing_fit:
  overall_user_preference:
production_cost:
  human_interventions:
  elapsed_time:
  premium_agent_credit:
  failed_shots:
  full_regenerations:
notes:
```

The values do not need to become a complicated scoring system. A short comparative production note is enough.

## Working diagnosis

The current Codex production path effectively asks one agent to perform many jobs:

```text
story interpretation
→ directing decisions
→ shot decomposition
→ storyboard prompting
→ image/storyboard generation management
→ storyboard review
→ video prompt compilation
→ renderer operation
→ failure diagnosis
→ retries
→ artifact organization
→ final assembly
```

This is too broad for an expensive coding agent to own as one continuous production task.

The likely failure mode is not only model quality. It is also **context growth, repeated re-reasoning, renderer waiting/retry loops, and failure propagation from early creative decisions into later production steps**.

## Core operating principle

> Codex should primarily build, repair, and improve the production pipeline. It should not remain the expensive worker that personally shepherds every episode from idea to final render.

Target long-term role split:

```text
Codex
= pipeline builder / maintainer / difficult debugging / schema and deterministic automation

Claude
= selective implementation / difficult review / UI or architecture work when justified

Hermes + Meromero
= repeated storyboard generation / prompt compilation / semantic QA where local execution is sufficient

Grok
= independent creative candidate / field research / alternate storyboard source

Python + WanGP + local tools
= deterministic execution / render queue / retries / artifact handling

Human
= taste, A/B selection, veto, approval, final preference
```

This is a target direction, not a requirement to replace the current attempt before it finishes.

## Future production boundary after the current comparison

If the comparison confirms that the current Codex end-to-end path is too costly, future episodes should be checkpointed:

```text
Task 1: episode brief → storyboard candidates → STOP
Task 2: selected candidate → storyboard grid prompt/artifact → STOP
Task 3: human storyboard approval → STOP
Task 4: approved board → per-shot video prompts → STOP
Task 5: render queue; retry only failed shots → STOP
Task 6: assemble/edit/finalize
```

Every stage should persist durable artifacts so later stages do not reconstruct prior reasoning from chat context.

Suggested durable outputs:

```text
episode.yaml
storyboard-A.yaml
storyboard-B.yaml
approved-storyboard.yaml
storyboard-grid.*
shot-prompts/
renders/
render-manifest.json
final.*
```

## Retry rule

A failed shot should normally cause a **shot-local retry**, not a full storyboard redesign or full-video regeneration.

When a render fails:

```text
identify failed shot
→ classify failure
→ adjust only necessary prompt/reference/renderer setting
→ regenerate shot
→ preserve all unaffected approved shots
```

Full regeneration is justified only when the underlying directing plan or continuity state is wrong.

## Credit-efficiency principle

Premium-agent credit should be spent on work that benefits from premium reasoning:

- architecture and pipeline improvement;
- difficult production failure diagnosis;
- skill/schema design;
- automation code;
- renderer integration debugging;
- comparison and synthesis of genuinely ambiguous alternatives.

Do not spend premium-agent time repeatedly performing:

- render polling;
- deterministic file moves;
- simple retries;
- manifest updates;
- repeated prompt formatting that can be handled by a stable compiler/skill;
- ordinary storyboard generation once Hermes/Meromero can perform it reliably.

## Decision gate after Noa completion

After the current Noa output is complete, compare it with Hermes/Meromero and Grok outputs.

Use the result to choose the next direction:

### Case A — Codex result is clearly preferred

Preserve the directing/prompt behavior that made it better, then **distill that behavior into shared schemas and operational skills** so Hermes/Meromero can reproduce as much of it as possible without repeating Codex cost per episode.

### Case B — Codex result is only slightly better

Do not keep Codex in the full production loop. Use it to improve the shared skills/compiler and let cheaper/local agents do routine episode production.

### Case C — Hermes or Grok result is equally good or better

Treat this as evidence that Codex should not be the default creative production agent. Reassign Codex to pipeline engineering and use the better low-cost creative path for routine production.

## Important constraint

Do **not** start another broad repository redesign, orchestration project, or cleanup effort because of this failure.

First obtain the finished Noa artifact and comparative evidence.

The correct sequence is:

```text
finish current attempt
→ compare actual outputs
→ identify recurring production friction
→ change only the proven bottleneck
→ test one more real episode
```

This follows the project operating rule:

> Manual / real use → Measure → Standardize → Automate.

## Definition of useful improvement

A production-pipeline change is useful only if it improves one or more of:

- user's preference for the final video;
- time to first acceptable storyboard;
- time to finished video;
- number of failed/repeated shots;
- premium-agent credit usage;
- ease of resuming work across sessions/agents;
- ability for Hermes/Meromero to execute the same workflow locally.

Architecture elegance alone is not a success metric.

## Codex instruction

When this document is consulted later:

1. Do not discard or restart the current Noa work if a usable production state already exists.
2. Reuse existing artifacts and finish the closest viable path first.
3. Do not assume that more Codex autonomy is the answer to a failed long production run.
4. Prefer explicit checkpoints and persisted artifacts.
5. Push repeated low-complexity work downward to deterministic scripts or Hermes/Meromero.
6. Preserve enough provenance to compare Codex, Hermes/Meromero, and Grok fairly.
7. Improve the pipeline only after the completed Noa comparison identifies the actual bottleneck.
