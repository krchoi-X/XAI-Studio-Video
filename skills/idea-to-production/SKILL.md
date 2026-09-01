---
name: idea-to-production
description: Turn a natural-language production idea into 2-3 storyboard candidates, then an explicit user choice, a low-cost sample render, and a final render, using the frozen idea-to-production v1 JSON contracts. Use when the user describes what they want made. Do not use for character identity edits or for re-sending a single already-compiled prompt.
---

# Idea to Production

Convert one natural-language idea into a durable, schema-valid production run that a human director reviews at exactly two points: candidate choice and sample review.

This skill plans and compiles. It does not render. Every asset, reference, and render outcome comes from an approved adapter result, never from inspection of the filesystem and never from assumption.

## Trigger

Load this skill when the user describes something to be **made** and the flow needs storyboard candidates before rendering:

- "Harim finishes her shift and walks by the sea eating ice cream — make it."
- "Give me 3 versions of this scene, then a cheap test before the real render."
- "Same idea as last time but keep the navy coat."

Do **not** load this skill for:

| Situation | Use instead |
|---|---|
| Create or revise Character DNA | `skills/character-manager/SKILL.md` |
| Story/beat/tempo design without a production request | `skills/storyboard-director/SKILL.md` |
| One already-approved prompt to re-render | `tools/character_scene.py produce` |
| Scheduled overnight volume batch | `tools/hermes_night_batch.py` |

`storyboard-director` designs the beats. This skill is the production wrapper that carries those beats through the v1 contracts to a finished render.

## Authoritative contracts

These are owned by Codex and frozen. Read them before emitting anything; never rename a field or widen an enum:

- `docs/idea-to-production-contracts.md`
- `schemas/idea-production-request-v1.schema.json`
- `schemas/storyboard-candidates-v1.schema.json`
- `schemas/renderer-job-request-v1.schema.json`
- `schemas/production-job-result-v1.schema.json`

Character identity rules stay in `HERMES.md` and `skills/character-manager/SKILL.md`. Stable DNA is read-only for the whole of this workflow.

## Inputs

The entry document is `idea-production-request-v1`:

```json
{
  "schema_version": 1,
  "request_id": "req_20260901_seawalk",
  "action": "create_storyboards",
  "idea": "Harim finishes her shift and walks by the sea eating ice cream.",
  "character_ids": ["ch-harim"],
  "candidate_count": 3,
  "mode": "creative_expansion",
  "constraints": {"wardrobe": "navy wool coat", "coverage": "clothed"},
  "reference_asset_ids": ["asset_ch-harim_0f2c9a41"],
  "output_intent": "image"
}
```

Field notes that are easy to get wrong:

- `candidate_count` accepts only `2` or `3`.
- `mode` is optional and defaults to `creative_expansion`. It becomes `prompt_strategy` on the renderer job — the same three values under a different field name.
- `constraints` values are flat scalars only (`string`, `number`, `boolean`, `null`). No nested objects. The same shape reappears as `immutable_constraints` on the renderer job.
- `reference_asset_ids` are **opaque**. Resolve them only through an approved adapter. Never infer, construct, or glob a filesystem path, and never map an ID to a file by matching names under `characters/`.
- `output_intent` defaults to `image`.

## Ordered workflow

### 1. Accept and validate the request

Validate against `idea-production-request-v1` before doing any creative work. On failure emit `storyboard-candidates-v1` with `status: "failed"` and a `schema_validation_failed` error. Do not repair the caller's document.

### 2. Resolve references through the adapter

Ask the approved adapter to resolve every entry in `character_ids` and `reference_asset_ids` in one pass. Any unresolved ID stops the run — see [references/failure-modes.md](references/failure-modes.md). Never substitute a similar asset, and never continue with a partial reference set.

### 3. Reconcile constraints against Stable DNA

Apply the precedence ladder in [references/precedence-and-modes.md](references/precedence-and-modes.md). A user constraint that contradicts Stable DNA wins and suppresses that DNA field for this run only; record it in `suppressed_stable_dna_fields`. Two explicit user constraints that contradict each other cannot be ranked and are a structured failure.

### 4. Produce storyboard candidates

Emit `storyboard-candidates-v1` with `status: "needs_user_choice"` and `candidate_count` storyboards (exactly one in `exact` mode — see the mode table). Each storyboard is a genuinely different directing approach to the same idea, not a rewording.

Each shot carries a `sample_request`, which is the renderer job body this skill would submit for that shot **minus the two fields the queue mints at submission**:

```text
sample_request = renderer-job-request-v1 fields  -  { job_id, prompt_trace }
```

with `stage: "sample"`. Codex adds `job_id` and `prompt_trace` when it enqueues. Keeping the shape identical is what makes the handoff mechanical rather than a translation step.

Then **stop and ask the user to choose.** This is a hard stop condition.

### 5. Submit the sample

After the explicit choice, build a full `renderer-job-request-v1` with `stage: "sample"`: take the chosen shot's `sample_request`, add the `job_id` from the queue, and add a complete Prompt Trace per [references/prompt-trace.md](references/prompt-trace.md).

Sample stage is deliberately cheap: one engine, low count. Defaults that match this repository are `engines: ["z-image"]`, `count: 2`.

The job ID exists **before** execution. Track outcome as `production-job-result-v1`.

### 6. Review, then submit the final

Present sample results per shot. The user keeps, regenerates, or revises each shot. Only after that, emit `stage: "final"` renderer jobs — same `request_id`, new `job_id`, `engines: ["z-image", "krea2"]`, higher `count`.

This is the second and last hard stop. Everything between the two stops runs without Claude or Codex intervention.

## Precedence

```text
1  explicit user constraints        (request.constraints / immutable_constraints)
2  stable Character DNA             (read-only)
3  scene requirements               (what the shot must show to work)
4  style enrichment                 (mood, lens, grade)
5  optional creative detail         (droppable)
```

Lower levels never overwrite a higher one. When a level is dropped to satisfy a higher one, say so in the Prompt Trace rather than silently discarding it. Full rules and worked conflicts: [references/precedence-and-modes.md](references/precedence-and-modes.md).

## Modes

`mode` on the request becomes `prompt_strategy` on the renderer job, unchanged.

| Mode | Rewrites user text | Storyboards emitted | Typical use |
|---|---|---|---|
| `exact` | Never | 1 | User supplies a finished prompt |
| `strict_translation` | Structure only, no new content | `candidate_count` | Identity, wardrobe, continuity work |
| `creative_expansion` | Adds non-conflicting enrichment | `candidate_count` | Default; open-ended ideas |

`exact` is the constrained one. It never adds, removes, reorders, softens, or translates the user's words, and it therefore cannot produce creative variants — `candidate_count` is clamped to one storyboard with one shot whose `description` is the `idea` string verbatim. It still produces a durable request and a full Prompt Trace; that is required by contract, not optional. In `exact` mode `raw_user_prompt`, `after_character_dna_merge`, and `final_prompt_sent_to_image_engine` are all identical, and `after_scene_style_expansion` is `null`.

## Prompt Trace

Every renderer job carries `prompt_trace`. Required: `raw_user_prompt`, `after_character_dna_merge`, `after_constraint_validation`, `final_prompt_sent_to_image_engine`. The trace must let a reader reconstruct why the final prompt says what it says, including which DNA fields were suppressed and by which constraint. Field-by-field rules: [references/prompt-trace.md](references/prompt-trace.md).

## Validation gate

Nothing leaves this skill unvalidated. Before returning any document, validate it against its schema. A document that does not validate is replaced by a structured failure in the schema the caller expects — never by a partial or repaired document, and never by prose.

The deterministic fixtures under `tests/fixtures/idea-to-production/` are the reference for what a valid document of each kind looks like in each of the five situations. Validate them with:

```bash
python tests/fixtures/idea-to-production/validate_fixtures.py
```

## Failure behavior

Missing references and renderer failures are structured errors, never guessed substitutions. Every error is `{"code": ..., "message": ...}` with a code from the vocabulary in [references/failure-modes.md](references/failure-modes.md).

A renderer failure never loses the request. The `job_id` and `request_id` survive, `progress` keeps the real completed/failed/total counts, partial `asset_ids` are retained, and the state is `failed` or `interrupted` so it stays retryable. A retry is a new `job_id` under the same `request_id`.

## Stop conditions

Stop and hand control back to the user when:

1. storyboard candidates are ready — the user must choose (`needs_user_choice`);
2. sample results are ready — the user must approve, revise, or regenerate;
3. any reference fails to resolve;
4. two explicit user constraints contradict each other;
5. a render fails or is interrupted;
6. the request would require changing Stable DNA.

Case 6 is not something to work around. Route it to `skills/character-manager/SKILL.md` as an explicit identity decision.

## Never

- Never edit `characters/*/character.json` or any Stable DNA during production.
- Never claim an asset, reference, or render exists without an adapter result that says so.
- Never infer a filesystem path from an asset ID.
- Never rename a schema field, add a property to a closed object, or widen an enum.
- Never emit a renderer submission without a durable `job_id`.
- Never treat `result_session_id` as a directory. It is the Gallery handoff key.
- Never rewrite the user's text in `exact` mode, including "obvious" typo fixes.
- Never skip the user choice between candidates, or the review between sample and final.

## References

- [references/precedence-and-modes.md](references/precedence-and-modes.md) — the ladder, the three modes, worked conflicts
- [references/prompt-trace.md](references/prompt-trace.md) — Prompt Trace field rules per mode
- [references/failure-modes.md](references/failure-modes.md) — error code vocabulary and recovery
- [references/codex-integration.md](references/codex-integration.md) — what Codex still has to wire up
- `templates/storyboard-spec.md`, `templates/sample-generation-request.md`, `templates/final-generation-request.md`
