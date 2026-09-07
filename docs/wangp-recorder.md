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
  --status running
```

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

Rules:

- Write it **before** submitting the first job, and run the same command again with `--status completed` (or
  `failed`) when the session ends. Re-running is safe: it merges, keeps `created_at`, and preserves any extra keys
  you added yourself.
- It never rewrites `handoff.json`, `batch.yaml` or `prompt-trace.json`. Keep your own session file if you have one.
- Requester resolution for each submission: `--requested-by` → `XAI_REQUESTED_BY` → the session record
  (`session-provenance.json` → `handoff.json` → `batch.yaml` `session.created_by` → `prompt-trace.json`
  `invoked_by`) → `null`. Nothing is ever invented.
- Say who asked, not what ran: `requested_by` is the agent or person; `executor` is the runner; `engine` is WanGP;
  `model` is the checkpoint. The Control Tower shows all four separately.
- For character stills the scene pipeline already does this for you: `character_scene.py --actor <agent>` records
  `created_by` in `batch.yaml` and forwards it to every run.

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

The command returns immediately with a run directory and worker PID. The worker
continues independently of a browser. Check it later with:

```powershell
python tools/local_wangp.py status --run-dir projects/my-film/runs/RUN_ID
```

Only one XAI local worker may hold the GPU lock at a time. This lock does not
control a manually launched WanGP Web UI, so close the Web UI before using the
background runner.
