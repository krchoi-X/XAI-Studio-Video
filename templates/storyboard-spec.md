# Storyboard Spec Template — `storyboard-candidates-v1`

Fill this in when producing storyboard candidates from an `idea-production-request-v1`.
This template is the human-readable working form. The **JSON at the bottom is the deliverable**; the prose above it must not contradict it.

Related: `skills/idea-to-production/SKILL.md`, `templates/storyboard-draft.md` (medium-neutral directing draft, upstream of this file).

---

## 1. Request echo

Copy from the request; do not re-derive.

- `request_id`:
- `idea` (verbatim):
- `character_ids`:
- `candidate_count`: 2 / 3
- `mode`: `strict_translation` / `creative_expansion` / `exact`
- `constraints`:
- `reference_asset_ids`:
- `output_intent`: `image` / `video` / `mixed`

## 2. Adapter resolution

Every ID must be confirmed by the approved adapter before any candidate is written.

| ID | Kind | Adapter result | Notes |
|---|---|---|---|
| | character / asset | resolved / not found / access denied | |

If any row is not `resolved`, stop. Emit `status: "failed"` with the matching code from `skills/idea-to-production/references/failure-modes.md` and leave `storyboards` empty. Do not fill in the rest of this template.

## 3. Constraint reconciliation

| Constraint | Level | Outranks | Resolution | Suppressed DNA field |
|---|---|---|---|---|
| | 1 | `stable_dna.<field>` | constraint_wins | |

Two level-1 constraints in conflict → `constraint_conflict_unresolvable`, `status: "failed"`, stop here.

Dropped enrichment (levels 4–5 removed to satisfy a higher level):

-

## 4. Candidates

Each candidate is a distinct directing approach to the same idea — different attention path, tempo, or emotional emphasis — not a rewording of the same shot list.

In `exact` mode there is exactly one candidate with one shot whose description is the `idea` string verbatim.

### Candidate A — `sb_<slug>`

- title:
- summary (what makes this reading different):
- shot count:

#### Shot `shot_01`

- purpose (why this shot exists in this candidate):
- description (what is in frame):
- continuity carried in:
- continuity carried out:
- sample stage: engines / count

Repeat per shot, then per candidate.

## 5. Continuity object

Free-form per the schema. Use stable keys across all shots of a run so the reviewer can diff them:

```json
{
  "carries_from": "shot_01",
  "location": "seafront promenade",
  "time_of_day": "late afternoon",
  "wardrobe": "navy wool coat",
  "hair_state": "A",
  "props": "single-scoop ice cream cone",
  "emotional_state": "settling after a long shift"
}
```

`carries_from` is `null` on the first shot of a candidate.

## 6. `sample_request` object

Per shot. It is the renderer job body **minus the two fields the queue mints**:

```text
sample_request = renderer-job-request-v1 fields  -  { job_id, prompt_trace }
```

so it carries `schema_version`, `request_id`, `storyboard_id`, `shot_id`, `stage: "sample"`, `character_ids`, `reference_asset_ids`, `prompt_strategy`, `raw_user_prompt`, `scene_spec`, `immutable_constraints`, `engines`, `count`.

Sample defaults for this repository: `engines: ["z-image"]`, `count: 2`.

Never put `job_id` or `prompt_trace` here. The queue owns both.

## 7. Deliverable

```json
{
  "schema_version": 1,
  "request_id": "req_",
  "status": "needs_user_choice",
  "storyboards": [
    {
      "id": "sb_",
      "title": "",
      "summary": "",
      "shots": [
        {
          "id": "shot_01",
          "purpose": "",
          "description": "",
          "continuity": {},
          "sample_request": {}
        }
      ]
    }
  ],
  "errors": []
}
```

`status` is `needs_user_choice` or `failed` — there is no third value.

Validate against `schemas/storyboard-candidates-v1.schema.json` before returning. `storyboard`, `shot`, and `error` are closed objects: an extra key fails the document.

## 8. Stop

Present the candidates and stop. Do not pre-select, do not rank, and do not start a sample render before the user chooses.
