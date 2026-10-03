# WanGP Prompt / Result Recorder

WanGP embeds effective generation settings, including the prompt, in successful
MP4 metadata. That is useful but insufficient by itself: failed jobs have no
MP4, and a browser refresh can erase the visible queue. The recorder therefore
creates the durable local run before WanGP submission and attaches the artifact
after completion.

## Record lifecycle

```text
exact prompt.txt
  -> prepare run.json + events.jsonl (queued)
  -> submit to WanGP and save provider/WanGP job ID
  -> append running progress
  -> success: hash MP4 + inspect embedded prompt + artifact-manifest.json
  -> failure: preserve error and last progress without requiring an MP4
```

The exact UTF-8 bytes of the submitted prompt are the primary matching key.
A normalized newline/outer-whitespace hash is recorded only as diagnostic
evidence; it never silently overrides an exact mismatch.

## Requester provenance (required for new callers)

Every submission should say **who asked for it**. The run record keeps four different facts apart:

```text
requested_by  grok | claude | codex | hermes | web | user     who asked
executor      local-wangp-worker | render-broker | ...        what ran it
renderer      WanGP                                            the engine
model         settings.value.model_type                        the model
```

Pass `--requested-by` on `local_wangp.py submit` (or `wangp_recorder.py prepare`), or export
`XAI_REQUESTED_BY` once in the calling environment. Grok Bot, Claude Code, Codex and Hermes each pass their own
name. When neither is given the field is recorded as `null` — it is never guessed, and the Control Tower falls back
to observing the worker process. Records written before this field existed keep working unchanged.

```powershell
python tools/local_wangp.py submit `
  --runs-root <session>/runs --prompt-file <session>/shot-01.txt `
  --settings-file <session>/shot-01.settings.json `
  --project-id <session-id> --prompt-id shot-01 `
  --output-dir <library>/videos/<session-id> `
  --requested-by grok
```

The value is written to `run.json` (`requested_by`, `executor`), echoed in the `queued` event and in the JSON that
`submit` and `status` print, and passed to the detached worker's command line. The Control Tower then shows the job
as `grok (from record)` instead of inferring the requester from process telemetry.

## Recording a production session

Record the session **once, before the first render**, then every submission into it inherits the requester. This is
the rule for real production work, not only for tests:

```powershell
python tools/wangp_recorder.py session `
  --session-dir characters/ch-lia/02_generations/VIDEO-20260907-181254-lia-sundress-shift-cat `
  --requested-by grok `
  --engine WanGP --model minimax_h3_ref2va_pruned `
  --character-id ch-lia --title "Lia micro-vlog: sundress to shift to cat" `
  --user-request "<the operator's request, verbatim>" `
  --production-plan <session>/shot-production-plan-v2.json `
  --status running
```

`--production-plan` is the opt-in safety contract for new character-video and multi-pack work. It accepts only an
approved schema-v2 plan. The session stores the plan path and SHA-256, and a later submission fails before a run
directory or GPU worker is created if the plan file changed. Sessions without this option retain the legacy v1
behavior.

That writes `<session>/session-provenance.json`:

```json
{
  "schema_version": 1,
  "session_id": "VIDEO-20260907-181254-lia-sundress-shift-cat",
  "requested_by": "grok",
  "executor": "local-wangp-worker",
  "engine": "WanGP",
  "model": "minimax_h3_ref2va_pruned",
  "character_id": "ch-lia",
  "title": "Lia micro-vlog: sundress to shift to cat",
  "user_request_verbatim": "…",
  "status": "running",
  "created_at": "…",
  "updated_at": "…"
}
```

### Where the runs directory must be

Pass `--runs-root <session>/runs`. The Control Tower names a job from its session, so a run whose parent is not a
session directory can only be listed by its `project_id` and is not grouped with the character, prompts or outputs.
Passing the repository root, as in `--runs-root D:\codex\XAI-studio\runs`, produces exactly that.

```text
characters/<character-id>/02_generations/<SESSION-ID>/
    session-provenance.json        written by `wangp_recorder.py session`
    <shot>.txt, <shot>.settings.json
    runs/<run-id>/                 written by `local_wangp.py submit --runs-root <session>/runs`
```

The Control Tower also scans `runs/` and `examples/` at the repository root, so records already written there stay
visible — but they appear without a session, character or grouping.

Rules:

- Write it **before** submitting the first job, and run the same command again with `--status completed` (or
  `failed`) when the session ends. Re-running is safe: it merges, keeps `created_at`, and preserves any extra keys
  you added yourself.
- It never rewrites `handoff.json`, `batch.yaml` or `prompt-trace.json`. Keep your own session file if you have one.
- Requester resolution for each submission: `--requested-by` → `XAI_REQUESTED_BY` → the session record
  (`session-provenance.json` → `handoff.json` → `batch.yaml` `session.created_by` → `prompt-trace.json`
  `invoked_by`) → `null`. Nothing is ever invented.
- `settings.model_type` must be an id from [WanGP model types](wangp-models.md); check it with
  `python tools/wangp_models.py --check <model_type>` rather than guessing.
- Say who asked, not what ran: `requested_by` is the agent or person; `executor` is the runner; `engine` is WanGP;
  `model` is the checkpoint. The Control Tower shows all four separately.
- For character stills the scene pipeline already does this for you: `character_scene.py --actor <agent>` records
  `created_by` in `batch.yaml` and forwards it to every run.
- For a `*_ref2va*` character video, `local_wangp.py submit` fills empty `image_refs` from the session character's
  durable `character.json.reference_defaults.identity` record. It records the path, hash, byte count and
  `character-default` basis in `run.json`. A non-empty settings value remains authoritative; the tool never selects a
  newest file or treats an unreviewed image as approved.
- When a schema-v2 production plan is registered, its stricter rules take precedence: every `image_refs` value must
  exactly match the ordered references for that `prompt_id`. The final prompt must contain every frozen mandatory
  identity term; the current character record path/version/Stable-DNA hash must still match; file hashes, declared
  laterality, native-landscape roles, forbidden state tags and required pack/shot boundary frames must pass. This
  check runs before the recorder creates the run. The accepted contract is copied to `run.json.production_contract`.
- The laterality declaration is a review record, not computer vision. `verified_by` must name the reviewer who
  inspected the pixels. Width/height is checked from the file, but semantic left/right and visual padding still need
  human review.

## Commands

Create the run before clicking Generate or calling `wangp_generate`:

```powershell
python tools/wangp_recorder.py prepare `
  --runs-root projects/my-film/runs `
  --prompt-file projects/my-film/prompts/shot-01.txt `
  --project-id my-film --prompt-id shot-01 --target vast `
  --settings-file projects/my-film/prompts/shot-01.settings.json `
  --requested-by hermes
```

Persist the returned WanGP or provider job ID and progress:

```powershell
python tools/wangp_recorder.py state --run-dir projects/my-film/runs/RUN_ID `
  --state running --provider-job-id WANGP_JOB_ID --message "denoising 4/20"
```

Attach and verify a successful artifact:

```powershell
python tools/wangp_recorder.py attach --run-dir projects/my-film/runs/RUN_ID `
  --artifact D:/AI/WanGP/outputs/videos/result.mp4
```

Record failure even when no video exists:

```powershell
python tools/wangp_recorder.py fail --run-dir projects/my-film/runs/RUN_ID `
  --message "CUDA out of memory" --last-progress "denoising 4/20"
```

## Automation ownership

Hermes creates the prompt and calls `prepare` with `--requested-by hermes`. The Render Broker calls `state`,
submits/polls WanGP, then calls `attach` or `fail`. Manual Web UI submission is
supported only if the exact pasted prompt is recorded with `prepare` first.
The intended default is MCP submission, because the returned WanGP job ID gives
an unambiguous link that filename/time matching cannot provide.

## Local background runner

`tools/local_wangp.py` completes the local-PC path without a browser. It creates
the recorder run first, writes effective settings, starts the inspected WanGP
Python environment as a detached worker, streams durable events, and attaches
or fails the run when WanGP terminates.

Check the installed local environment without generating:

```powershell
python tools/local_wangp.py doctor
```

Submit a prepared prompt and settings file:

```powershell
python tools/local_wangp.py submit `
  --runs-root projects/my-film/runs `
  --prompt-file projects/my-film/prompts/shot-01.txt `
  --settings-file projects/my-film/prompts/shot-01.settings.json `
  --project-id my-film --prompt-id shot-01 --requested-by hermes
```

When Hermes is the caller, add `--wait`. A Hermes-attributed worker automatically unloads models resident in both
the Hermes llama.cpp router and Ollama, verifies free VRAM before WanGP initialization, and keeps Windows awake while
the renderer is alive. Blocking is part of the safety contract: it prevents Hermes from beginning another inference
turn and reloading the planning model while the renderer owns the GPU.

For an enrolled schema-v2 session, `--prompt-id` must equal exactly one chunk's `prompt_id`; the plan is inherited
from `session-provenance.json`. `--production-plan <same-plan-path>` may be supplied explicitly as an additional
match check. Because the approved reference packet is exact, do not leave `image_refs` empty and rely on the legacy
character-default injection for these sessions.

Without `--wait`, the command returns immediately with a run directory and worker PID. The worker
continues independently of a browser. Check it later with:

```powershell
python tools/local_wangp.py status --run-dir projects/my-film/runs/RUN_ID
```

Only one XAI local worker may hold the GPU lock at a time. This lock does not
control a manually launched WanGP Web UI, so close the Web UI before using the
background runner.
