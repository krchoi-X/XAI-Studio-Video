# Failure Modes and Error Vocabulary

Reference for `skills/idea-to-production/SKILL.md`.

Contract rule 7: missing references and renderer failures are structured errors, not guessed substitutions. Contract rule 5: every renderer submission has a durable job ID before execution and preserves failure or interruption state.

## Error object shape

Both error-carrying schemas require `code` and `message`.

- `storyboard-candidates-v1` errors also allow `field` (`string` or `null`).
- `production-job-result-v1` errors allow **only** `code` and `message`. Do not add `field` there; the object is closed and the document will fail validation.

`message` is written for the director, not for a log parser: name the offending ID or constraint and say what the user can do about it.

## Code vocabulary

The schemas accept any non-empty string. Use these so the frontend can branch on them; add a new code only when no existing one fits, and record it here.

### Request and planning — `storyboard-candidates-v1`

| Code | Meaning | `field` |
|---|---|---|
| `schema_validation_failed` | Request did not validate against `idea-production-request-v1` | offending pointer |
| `character_not_found` | A `character_ids` entry has no adapter record | `character_ids` |
| `reference_not_found` | A `reference_asset_ids` entry has no adapter record | `reference_asset_ids` |
| `reference_access_denied` | Asset exists but is restricted for this context | `reference_asset_ids` |
| `adapter_unavailable` | Approved adapter could not be reached at all | `null` |
| `constraint_conflict_unresolvable` | Two level-1 constraints contradict | offending constraint key |
| `constraint_unsupported` | Constraint key is not a scalar or is not expressible | offending constraint key |
| `stable_dna_change_required` | Request cannot be satisfied without editing Stable DNA | `character_ids` |

### Execution — `production-job-result-v1`

| Code | Meaning | Terminal status |
|---|---|---|
| `renderer_submission_failed` | Queue rejected the job before execution | `failed` |
| `renderer_failed` | Engine ran and errored | `failed` |
| `renderer_interrupted` | Host, GPU, or process died mid-run | `interrupted` |
| `engine_out_of_memory` | VRAM exhaustion; retry with lower count/resolution | `failed` |
| `engine_unavailable` | Named engine not installed or not reachable | `failed` |
| `asset_write_failed` | Image produced but not durably stored | `failed` |

## Missing reference

Stop the whole run. Do not partially plan, do not substitute a visually similar asset, and do not fall back to "the character's most recent image".

```json
{
  "schema_version": 1,
  "request_id": "req_...",
  "status": "failed",
  "storyboards": [],
  "errors": [{
    "code": "reference_not_found",
    "message": "Reference asset 'asset_ch-harim_deadbeef' was not resolved by the approved adapter. Choose an asset from the Gallery or remove it from the request.",
    "field": "reference_asset_ids"
  }]
}
```

Rules:

- `status` is `failed` and `storyboards` is `[]`. A partial candidate set is worse than none, because the user cannot tell which shots were planned without the reference.
- Report every unresolved ID in one response — one error object per ID — rather than surfacing them one round-trip at a time.
- Never derive a path from the ID to check the filesystem yourself. Absence of adapter confirmation is the answer.

## Renderer failure

The request survives the failure. That is the whole point of contract rule 5.

- `job_id` and `request_id` are unchanged and still present.
- `progress.completed`, `progress.failed`, `progress.total` hold the real counts. Do not zero them.
- `asset_ids` keeps whatever was durably written. A partial success is not discarded.
- `result_session_id` is populated when any asset landed, so the Gallery can still show the partial batch; `null` only when nothing was produced.
- `status` is `failed` for a definite engine error, `interrupted` for a lost host or process.

```json
{
  "schema_version": 1,
  "job_id": "job_...",
  "request_id": "req_...",
  "status": "failed",
  "progress": {"completed": 1, "failed": 1, "total": 2, "message": "z-image OOM on image 2 of 2"},
  "result_session_id": "sess_...",
  "asset_ids": ["asset_..."],
  "errors": [{"code": "engine_out_of_memory", "message": "..."}]
}
```

## Retry

A retry is a **new job under the same request**:

- new `job_id`;
- same `request_id`, `storyboard_id`, `shot_id`, `stage`, `prompt_strategy`;
- fresh `prompt_trace`;
- the failed job's result stays on record — never overwrite it.

Reduce `count` or drop an engine when the failure was resource exhaustion. Do not silently change the prompt on retry; a changed prompt makes the failure unreproducible and is a new creative decision the user has not made.

## `interrupted` versus `failed`

- `interrupted` means the outcome is unknown — the process stopped before reporting. Assume nothing about the missing images.
- `failed` means the engine reported an error.

Both are retryable and both keep partial `asset_ids`. Never convert an `interrupted` job to `completed` because the expected files happen to be on disk; only an adapter result may set `completed`.

## Never

- Never invent an asset ID to fill a gap.
- Never mark `status: "completed"` when `progress.failed > 0`.
- Never drop the errors array to make a run look clean.
- Never resolve a failure by editing Stable DNA.
