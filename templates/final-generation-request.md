# Final Generation Request Template — `renderer-job-request-v1`, `stage: "final"`

Use only after the user has reviewed sample results for this shot. The final render is the expensive pass; everything it should prove was already proven at sample stage.

Related: `templates/sample-generation-request.md`, `skills/idea-to-production/SKILL.md`.

---

## 1. Preconditions

- [ ] A sample job for this shot reached a terminal state and its result was shown to the user.
- [ ] The user approved the shot, or revised it and the revision was re-sampled.
- [ ] A new durable `job_id` was minted. Never reuse the sample's `job_id`.
- [ ] `request_id` is unchanged, so the Gallery can group the whole run.

An `interrupted` or `failed` sample is not an approval. Retry the sample first — see `skills/idea-to-production/references/failure-modes.md`.

## 2. What changes from the sample

Only these:

| Field | Sample | Final |
|---|---|---|
| `job_id` | `job_..._sample` | new value from the queue |
| `stage` | `"sample"` | `"final"` |
| `engines` | `["z-image"]` | `["z-image", "krea2"]` |
| `count` | 2 | higher, within 1–10 |
| `prompt_trace` | sample trace | fresh trace |
| `raw_user_prompt` | original | revised text, only if the user revised it |

Everything else — `request_id`, `storyboard_id`, `shot_id`, `character_ids`, `reference_asset_ids`, `prompt_strategy`, `immutable_constraints` — is carried unchanged.

`prompt_strategy` in particular is carried, never re-decided. A different strategy is a new request.

## 3. Carrying review revisions

If the user revised the shot during review:

- the revised text becomes `raw_user_prompt` on the final job and drives the whole trace;
- `scene_spec` is updated to match, using `scene-spec-v1` keys;
- the sample job and its result stay on record unchanged;
- a revision that would change Stable DNA is not a revision. Stop and route it to `skills/character-manager/SKILL.md`.

Revisions that only reject an enrichment detail belong in `prompt_trace.after_constraint_validation.dropped_enrichment`, not in `immutable_constraints`. Promote a revision to `immutable_constraints` only when the user states it as a hard requirement.

## 4. Deliverable

```json
{
  "schema_version": 1,
  "job_id": "job_",
  "request_id": "req_",
  "storyboard_id": "sb_",
  "shot_id": "shot_01",
  "stage": "final",
  "character_ids": [],
  "reference_asset_ids": [],
  "prompt_strategy": "creative_expansion",
  "raw_user_prompt": "",
  "scene_spec": {},
  "immutable_constraints": {},
  "engines": ["z-image", "krea2"],
  "count": 4,
  "prompt_trace": {}
}
```

Validate against `schemas/renderer-job-request-v1.schema.json` before submitting. Closed object; `count` maximum is 10 per job. For a larger volume run use `tools/hermes_night_batch.py` rather than inflating `count`.

## 5. Result and handoff

`production-job-result-v1`, `status: "completed"` only when `progress.failed == 0` and the adapter said so.

- `progress.total` equals `count × len(engines)`.
- `asset_ids` lists every durably stored asset, unique.
- `result_session_id` is the Gallery handoff key. Hand this string to the frontend; do not hand it a path, and do not construct one from it.

Multi-shot candidates produce one final job per shot, all sharing `request_id`, each with its own `job_id` and `result_session_id`.

## 6. After delivery

- Stable DNA is unchanged. A production run never writes to `characters/*/character.json`.
- Curation, favorites, and review decisions happen in the Gallery, not here.
- If final results suggest a real identity change, that is a separate Character Manager decision with cited evidence, not a side effect of this run.
