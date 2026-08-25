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

## Commands

Create the run before clicking Generate or calling `wangp_generate`:

```powershell
python tools/wangp_recorder.py prepare `
  --runs-root projects/my-film/runs `
  --prompt-file projects/my-film/prompts/shot-01.txt `
  --project-id my-film --prompt-id shot-01 --target vast `
  --settings-file projects/my-film/prompts/shot-01.settings.json
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

Hermes creates the prompt and calls `prepare`. The Render Broker calls `state`,
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
  --project-id my-film --prompt-id shot-01
```

The command returns immediately with a run directory and worker PID. The worker
continues independently of a browser. Check it later with:

```powershell
python tools/local_wangp.py status --run-dir projects/my-film/runs/RUN_ID
```

Only one XAI local worker may hold the GPU lock at a time. This lock does not
control a manually launched WanGP Web UI, so close the Web UI before using the
background runner.
