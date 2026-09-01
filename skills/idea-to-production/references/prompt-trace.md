# Prompt Trace Requirements

Reference for `skills/idea-to-production/SKILL.md`. Schema: `prompt_trace` in `schemas/renderer-job-request-v1.schema.json` (closed object — no extra properties).

Purpose: a reader who has only the renderer job must be able to reconstruct **why the final prompt says what it says**, without re-running the compiler and without access to the conversation.

## Fields

| Field | Required | Type | Rule |
|---|---|---|---|
| `raw_user_prompt` | yes | string | The user's text verbatim. Never normalized, translated, or trimmed of meaning. Empty string only if the user genuinely supplied none. |
| `structured_scene_spec` | no | object | The Scene Spec used for this shot. Keys must be `scene-spec-v1` field names so `character_scene.py` semantics stay comparable. |
| `after_character_dna_merge` | yes | string | The prompt after identity merge and after suppression is applied. Suppressed DNA text must already be absent here, not merely marked. |
| `after_constraint_validation` | yes | object | Structured validation result. See below. |
| `after_scene_style_expansion` | no | string \| null | Enriched prompt in `creative_expansion`. `null` in `strict_translation` and `exact`. |
| `final_prompt_sent_to_hermes` | no | string \| null | Set only when a Hermes agent handoff actually occurred. `null` otherwise — do not fill it with the engine prompt. |
| `final_prompt_sent_to_image_engine` | yes | string | Byte-for-byte what the adapter receives. If this does not match what was sent, the trace is wrong. |
| `suppressed_stable_dna_fields` | no | string[] | Stable DNA field names omitted for this run. Sorted, unique, no prose. |

## `after_constraint_validation`

The schema leaves this a free object. Use this shape so results stay comparable across runs and across the two stages:

```json
{
  "ok": true,
  "precedence": [
    "explicit_user_constraints",
    "stable_character_dna",
    "scene_requirements",
    "style_enrichment",
    "optional_creative_detail"
  ],
  "applied_constraints": ["wardrobe", "coverage"],
  "conflicts": [
    {
      "constraint": "hair",
      "outranked": "stable_dna.hair",
      "resolution": "constraint_wins"
    }
  ],
  "dropped_enrichment": ["loose hair moving in the wind"],
  "errors": []
}
```

- `ok` is `false` only when the job should not be submitted.
- `conflicts` records every level-1-over-level-2 resolution. An empty array means no DNA field was displaced, and `suppressed_stable_dna_fields` must then be empty or absent too.
- `dropped_enrichment` records level 4/5 material removed to satisfy a higher level. Silently discarding enrichment defeats the point of the trace.
- `errors` mirrors the structured error objects from `references/failure-modes.md`. Non-empty implies `ok: false`.

## Per-mode expectations

| | `exact` | `strict_translation` | `creative_expansion` |
|---|---|---|---|
| `after_character_dna_merge` | `== raw_user_prompt` | differs (merge + structure) | differs |
| `after_scene_style_expansion` | `null` | `null` | non-null string |
| `final_prompt_sent_to_image_engine` | `== raw_user_prompt` | derived from merge | derived from expansion |
| `suppressed_stable_dna_fields` | allowed | allowed | allowed |

The `exact` equalities are the machine-checkable form of "exact mode cannot creatively rewrite the supplied prompt". `tests/fixtures/idea-to-production/validate_fixtures.py` asserts them.

## Stage rules

- Sample and final are separate jobs with separate `job_id` values and separate traces. Never reuse the sample trace on the final job.
- Both traces carry the same `raw_user_prompt` unless the user revised the shot during review. If they revised it, the final trace carries the revised text as `raw_user_prompt` and the earlier job remains on record.
- A retry after a renderer failure gets a fresh `job_id` and a fresh trace. The trace content may be identical to the failed attempt; the identity is not.

## Do not

- Do not backfill a trace after the render. It is part of the submission, not of the result.
- Do not put the trace in `production-job-result-v1`. That schema is closed and has no place for it.
- Do not compress the trace by dropping intermediate stages when they happen to be equal — equality is itself the evidence in `exact` mode.
