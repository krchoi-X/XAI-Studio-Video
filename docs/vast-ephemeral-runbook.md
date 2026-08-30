# Vast.ai Ephemeral Worker Runbook

## Policy

Vast.ai is a disposable execution target for one production session. Every
session starts from a reproducible image or bootstrap manifest, exports all
valuable artifacts, and ends by destroying the instance. A stopped Vast
instance is not a cache and must not be kept for later work.

RunPod may use a persistent network volume under its own policy. Do not copy
that assumption to Vast.

## Required local inputs

Before renting a GPU, keep these outside Vast:

- exact container image tag or bootstrap version;
- pinned WanGP commit and worker environment version;
- model manifest with source URI, filename, size, and checksum when available;
- exact runtime prompt and settings;
- source-reference files and their checksums;
- local run record with project, prompt, and run IDs;
- durable artifact destination with enough free space.

Provider credentials stay in the local secret store or process environment.
Never bake them into the image or upload them with a run record.

## First-boot checklist

1. Search only verified offers satisfying the configured GPU, VRAM,
   reliability, disk, network, CUDA, and hourly-price limits.
2. Record the accepted offer ID, price, machine ID, instance ID, and start time.
3. Create the instance from the pinned worker image. Treat the instance disk as
   temporary. Do not attach a Vast volume unless the user explicitly overrides
   this runbook for a named session.
4. Verify GPU and runtime:

   ```text
   nvidia-smi
   Python and CUDA versions
   free disk space
   network reachability
   /workspace ownership and write access
   ```

5. Run the versioned bootstrap. It must be safe on an empty `/workspace` and
   create the complete directory layout without relying on an earlier instance:

   ```text
   /workspace/models
   /workspace/inputs
   /workspace/runs/<run-id>
   /workspace/outputs/<run-id>
   /workspace/logs/<run-id>
   ```

6. Download only the model profile required for the current job. Verify file
   sizes and checksums. Do not manually accumulate unrelated checkpoints.
7. Start exactly one WanGP service mode and verify:

   ```text
   GET :8080/healthz
   WanGP capability/model schema
   expected model and input modes
   writable output path
   ```

8. Transfer inputs and verify their checksums before generation.
9. Run one cheap smoke test before the production render.

If any step fails, preserve the failure log locally and destroy the instance.
Do not repair the host into a unique, undocumented snowflake.

## Production checklist

1. Submit the exact saved prompt and settings; do not edit the canonical prompt
   only inside the remote UI.
2. Record provider job ID, start time, progress, effective settings, seed, and
   output paths.
3. Keep outputs under the run-specific directory.
4. On failure, export the useful log and any recoverable preview before cleanup.

## Export and verification gate

Before stopping or destroying the instance, export:

- final media and selected previews;
- exact prompt and effective settings;
- seed and renderer/model versions;
- run log or concise failure log;
- artifact manifest containing size and SHA-256 for every retained file.

Download or register the artifacts in durable local/object storage, then verify
that they can be opened outside Vast and that their computed checksums match the
manifest. A browser thumbnail or a provider file listing is not verification.

## Mandatory teardown

After verification:

1. Confirm no upload or copy is still running.
2. Record final cost/time and cleanup status.
3. Destroy the Vast instance; do not merely stop it.
4. Confirm the instance no longer appears in the active instance list.
5. Confirm no Vast volume or other billable storage was left behind.
6. Mark the local run `cleaned` only after both compute and storage checks pass.

If export cannot be verified, do not destroy automatically. Stop the instance
only as a temporary safety measure, record the storage charge and blocker, and
ask the user whether to recover or discard the remaining data.

## Definition of done

A Vast session is complete only when all of the following are true:

```text
artifact exported
checksum verified outside Vast
prompt/settings/log preserved
instance destroyed
no Vast storage remains billable
local run marked cleaned
```

