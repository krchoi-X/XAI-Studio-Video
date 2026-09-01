# Idea-to-Production Fixtures

Deterministic reference documents for the frozen v1 contracts. Owned by Claude package C3.

These are **fixtures, not test data for a running system**. Nothing here calls a renderer, resolves an asset, reads Character DNA, or writes to the repository. They pin down what a valid document looks like at each step of the flow so that the queue, adapter, and API work Codex does next has something concrete to match.

## Run

```bash
python tests/fixtures/idea-to-production/validate_fixtures.py
```

Requires `jsonschema`. Exit code 0 when every fixture is schema-valid and every semantic invariant holds; 1 otherwise, with one `FAIL` line per violation.

The script is intentionally not named `test_*.py`, so `pytest tests/` does not collect it and the existing suite is untouched. Codex can wire it into pytest later — see `skills/idea-to-production/references/codex-integration.md`.

## Cases

| Directory | What it pins down |
|---|---|
| `normal/` | Happy path: idea → 3 candidates → choice → cheap sample → final on both engines. No conflicts, no suppression, no errors. |
| `exact/` | `exact` mode: `candidate_count: 2` clamped to one storyboard, description byte-identical to `idea`, full Prompt Trace with equal stages. |
| `constraint-conflict/` | Resolvable (explicit `hair` outranks Stable DNA `hair`, suppressed for the run) and unresolvable (two level-1 constraints contradict → `failed`). |
| `missing-reference/` | Two unresolvable asset IDs → `failed`, zero storyboards, one structured error per ID, no substitution. |
| `renderer-failure/` | VRAM failure with one image kept → interrupted retry with nothing kept → second retry completes. Three job IDs, one request ID, one prompt. |

`manifest.json` maps every file to its schema and to the expectations the validator enforces. A fixture that is not listed in the manifest fails the run, so the two cannot drift apart.

## What the validator enforces

Beyond plain schema validation:

- **Opaque IDs.** No `character_ids`, `reference_asset_ids`, `asset_ids`, or `result_session_id` value may look like a filesystem path.
- **`sample_request` shape.** For every shot, `sample_request` carries no `job_id` and no `prompt_trace`, uses only `renderer-job-request-v1` property names, and becomes a valid renderer job once those two fields are added. Its `request_id`, `storyboard_id`, and `shot_id` must agree with the document around it.
- **Scene Spec conformance.** Every non-empty `scene_spec` validates against `scene-spec-v1` and its `mode` equals the job's `prompt_strategy`.
- **Prompt Trace mode invariants.** `exact` requires `after_character_dna_merge == raw_user_prompt == final_prompt_sent_to_image_engine` and a null `after_scene_style_expansion`; `strict_translation` requires a null expansion and a merge that actually changed something; `creative_expansion` requires a non-empty expansion.
- **Suppression matches conflicts.** A recorded conflict implies a suppressed Stable DNA field and vice versa, the suppressed list is sorted and unique, and every conflict resolves as `constraint_wins` against a `stable_dna.*` field.
- **Result consistency.** `completed` implies zero failures, no errors, and a non-null `result_session_id`; `failed`/`interrupted` imply at least one structured error; `completed + failed <= total`.
- **Durable job identity.** Job IDs are unique within a case, every result maps to a job, `progress.total == count × len(engines)`, a `final` job requires a completed `sample` for the same shot, and a retry keeps the prompt byte-identical.
- **Partial results survive failure.** A failed job retains exactly the assets it durably stored and keeps its Gallery handoff key when it stored anything.

The validator was checked against 22 deliberate mutations — enum widening, a renamed `sample_request` field, a smuggled `job_id`, `exact` mode rewriting the prompt, a dropped reference error, a discarded partial batch, a reused job ID, a silently changed retry prompt, an asset ID turned into a path — and rejected all 22.

## Extending

1. Add the JSON file under the relevant case directory.
2. Add it to `manifest.json` with its schema and expectations. Unlisted files fail the run.
3. Re-run the validator.

Two rules for anything added here:

- Never rename a schema field, add a property to a closed object, or widen an enum. The v1 schemas are owned by Codex and frozen.
- Keep values deterministic. No timestamps generated at read time, no random IDs, no machine-specific paths.
