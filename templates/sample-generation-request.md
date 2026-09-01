# Sample Generation Request Template — `renderer-job-request-v1`, `stage: "sample"`

Use after the user has explicitly chosen one storyboard candidate. The sample is a cheap correctness check on composition, identity, wardrobe, and continuity — not a quality target.

Related: `skills/idea-to-production/SKILL.md`, `skills/idea-to-production/references/prompt-trace.md`.

---

## 1. Preconditions

- [ ] The user chose a candidate explicitly. An inferred or defaulted choice does not count.
- [ ] Every `character_ids` and `reference_asset_ids` entry was resolved by the approved adapter.
- [ ] Constraint reconciliation produced no `constraint_conflict_unresolvable`.
- [ ] The queue minted a durable `job_id` **before** submission.

If the last box is unchecked, do not submit. Contract rule 5 has no exception for a quick test render.

## 2. Build

Start from the chosen shot's `sample_request` and add exactly two fields:

```text
renderer job = sample_request + { job_id, prompt_trace }
```

Change nothing else. If the shot needs different content, that is a revision of the storyboard, not an edit at submission time.

## 3. Fields

| Field | Sample-stage rule |
|---|---|
| `schema_version` | `1` |
| `job_id` | From the queue. Pattern `job_[A-Za-z0-9_-]+`. Never generated locally at submission. |
| `request_id` | Same value the whole run uses, from the original request. |
| `storyboard_id` | The chosen `sb_...`. `null` only when there is no storyboard at all. |
| `shot_id` | The shot being sampled. |
| `stage` | `"sample"` |
| `character_ids` | Non-empty, unique. |
| `reference_asset_ids` | Opaque IDs only. Never a path. May be empty. |
| `prompt_strategy` | The request's `mode`, carried unchanged. |
| `raw_user_prompt` | The user's text verbatim. |
| `scene_spec` | Keys from `scene-spec-v1` so it stays comparable with `tools/character_scene.py` output. |
| `immutable_constraints` | The request's `constraints`, flat scalars only. |
| `engines` | Sample default `["z-image"]`. One engine. |
| `count` | Sample default `2`. Keep it low; range is 1–10. |
| `prompt_trace` | Required and complete. See below. |

## 4. Prompt Trace

Required: `raw_user_prompt`, `after_character_dna_merge`, `after_constraint_validation`, `final_prompt_sent_to_image_engine`.

```json
{
  "raw_user_prompt": "",
  "structured_scene_spec": {},
  "after_character_dna_merge": "",
  "after_constraint_validation": {
    "ok": true,
    "precedence": ["explicit_user_constraints", "stable_character_dna", "scene_requirements", "style_enrichment", "optional_creative_detail"],
    "applied_constraints": [],
    "conflicts": [],
    "dropped_enrichment": [],
    "errors": []
  },
  "after_scene_style_expansion": null,
  "final_prompt_sent_to_hermes": null,
  "final_prompt_sent_to_image_engine": "",
  "suppressed_stable_dna_fields": []
}
```

Mode checks:

- `exact` — `after_character_dna_merge` and `final_prompt_sent_to_image_engine` both equal `raw_user_prompt`; `after_scene_style_expansion` is `null`.
- `strict_translation` — `after_scene_style_expansion` is `null`.
- `creative_expansion` — `after_scene_style_expansion` is a non-null string.

`final_prompt_sent_to_hermes` stays `null` unless a Hermes agent handoff actually happened.

## 5. Deliverable

```json
{
  "schema_version": 1,
  "job_id": "job_",
  "request_id": "req_",
  "storyboard_id": "sb_",
  "shot_id": "shot_01",
  "stage": "sample",
  "character_ids": [],
  "reference_asset_ids": [],
  "prompt_strategy": "creative_expansion",
  "raw_user_prompt": "",
  "scene_spec": {},
  "immutable_constraints": {},
  "engines": ["z-image"],
  "count": 2,
  "prompt_trace": {}
}
```

Validate against `schemas/renderer-job-request-v1.schema.json` before submitting. The object is closed — no extra keys.

## 6. Result

Track as `production-job-result-v1`. `status` moves `queued` → `running` → `completed` / `failed` / `interrupted`.

- `result_session_id` is the Gallery handoff key, not a directory path.
- `progress.total` equals `count × len(engines)`.
- On failure or interruption keep `job_id`, real progress counts, and any partial `asset_ids`. See `references/failure-modes.md`.

## 7. Stop

Present sample results per shot and stop. The user keeps, regenerates, or revises before anything reaches `templates/final-generation-request.md`.
