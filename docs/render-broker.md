# Render Broker

## Purpose

The Render Broker routes one approved, durably recorded prompt to local WanGP, RunPod, Vast.ai, or a future self-hosted renderer without changing the canonical idea, Character DNA, or prompt lineage.

Hermes owns creative compilation and the pre-render record. The broker owns execution routing, provider lifecycle, progress, artifact recovery, and terminal status.

```text
User intent
  -> Hermes + XAI-Studio skill
  -> project / prompt / handoff records
  -> Render Broker
       -> local WanGP
       -> existing RunPod Pod
       -> existing Vast instance
       -> newly provisioned provider instance, when authorized
  -> durable run events and artifact storage
```

## Control plane vs execution plane

Keep the control plane outside disposable GPU instances.

The control plane stores project and prompt lineage, runtime-prompt SHA-256, routing decisions, provider identifiers, append-only run events, heartbeats, output checksums, cost/time limits, and cleanup state. The execution plane receives only the inputs needed for one run. A Pod or instance is replaceable compute, never the sole copy of creative history or final media.

Do not store provider API keys in Git, prompt files, images, container layers, or run records. Load them from the local secret store or process environment.

## Routing contract

Treat an explicit user destination as a Hard Lock.

```text
explicit local -> local only
explicit RunPod -> compatible RunPod only
explicit Vast -> compatible Vast only
auto -> broker may choose among allowed providers
```

For `auto`, evaluate candidates in this order:

1. healthy compatible instance already running
2. compatible reusable instance that can be started
3. new instance from an approved provider template, only when provisioning is authorized
4. local fallback, only when it satisfies the job and user preference
5. no route; report missing capacity instead of silently changing model, resolution, or provider

Compatibility includes renderer/model availability, GPU VRAM, CUDA/runtime version, attached storage, free disk, required input modes, expected duration, and configured cost/time limits.

Return available routes before submission when the user asks for a choice. Report provider, GPU, readiness, estimated hourly price when available, expected cold start, persistent-cache status, and material limitations. Price is advisory until the provider accepts the job.

## Provider registry

Maintain a local provider registry with non-secret identifiers and policy:

```text
provider and account alias
enabled / disabled
allowed GPU types
existing Pod or instance IDs
template or image ID
persistent volume ID and mount path
WanGP health/MCP endpoint method
maximum hourly price and run duration
idle shutdown policy
artifact destination
```

Discover current state from provider APIs at routing time. Do not assume a registered ID is still running or still has a GPU.

## Standard remote environment

Use one versioned OCI image or reproducible bootstrap manifest for both RunPod and Vast. Pin the WanGP commit, Python/CUDA runtime, model profile, bridge/recorder version, ffmpeg, metadata reader, health check, logging format, and mount paths.

Expose the same broker-facing operations everywhere:

```text
health
capabilities / model schema
submit
status
cancel
artifact manifest
shutdown-ready
```

Keep models on a RunPod persistent network volume as a cache when economical.
Vast uses disposable, empty-start workers by default: bootstrap the required
model profile for one session, export and verify all artifacts, then destroy the
instance. A Vast volume is allowed only as an explicit per-session override and
is never the canonical result archive.

## Durable run lifecycle

Create the run record locally before any provider call.

```text
planned -> queued -> provisioning -> starting -> running
        -> uploading -> succeeded -> verified -> cleaned
        -> failed | interrupted | timed_out | capacity_unavailable | unknown
```

Append every transition to `events.jsonl`. Never represent a missing heartbeat as success. On broker restart, reconcile non-terminal runs against the provider API, remote bridge, output storage, and local process state.

Minimum run identity includes `project_id`, `prompt_id`, `run_id`, runtime-prompt SHA-256, renderer/model/profile, requested and selected provider, provider job ID, Pod/instance ID, environment version, timestamps, and last heartbeat.

## Prompt and input transfer

Hermes saves the exact runtime prompt locally before submission. The broker sends it with the run ID, prompt hash, settings, and authenticated input references. Do not edit the prompt inside the remote adapter. If provider-specific compilation is required, persist it as a child prompt with its own hash.

Transfer reference media through authenticated object storage or a controlled copy operation. Verify size and checksum before starting the expensive render.

## Results and failure recovery

A remote worker must upload final media, a provider-neutral artifact manifest, effective settings, embedded renderer metadata when supported, an error/log summary, and output checksums before reporting success.

The broker downloads or registers the durable artifact, verifies its checksum and embedded prompt metadata, then marks the run `verified`. Only after verification may it stop or terminate ephemeral compute.

For failed runs, preserve last progress, error, remote log reference, provider state, and recoverable previews or partial artifacts. Never rely on a browser page or provider job retention as the only history.

## Storage policy

Use three storage classes:

1. Git for small canonical specs, prompt lineage, event metadata, and manifests.
2. Provider volumes for model/environment caches and temporary work files.
3. Durable artifact storage for final media and large references, preferably through one provider-neutral S3-compatible interface or an explicitly configured local archive.

Store artifact URIs and checksums in Git, not large videos. Verify that the control plane can read an uploaded object before releasing compute.

## Provider notes

### RunPod

Use the REST API to list/create/manage Pods and attach an existing network volume during Pod creation. Treat `/workspace` or the configured volume mount as cache/workspace, and export critical results before termination. Network-volume location constrains compatible Pod capacity.

### Vast.ai

Use the API or CLI to search offers, create/start/stop/destroy instances, attach an existing volume, and copy artifacts. Marketplace host variation makes template validation, disk/network checks, and post-start health checks mandatory.

The default Vast lifecycle is `create -> bootstrap -> render -> export ->
verify -> destroy`. Do not keep stopped Vast instances as caches: stopped
instance storage remains billable and restart availability is not guaranteed.
Every bootstrap must work against an empty workspace from the pinned image and
model manifest. Follow `docs/vast-ephemeral-runbook.md` for the operator gate
and mandatory teardown checks.

## Cost and cleanup guardrails

- Never create billable compute unless the user requested rendering or enabled an explicit auto-provision policy.
- Record the accepted offer or Pod price and start time.
- Enforce maximum hourly price, provisioning timeout, render timeout, and idle timeout.
- Upload and verify artifacts before stopping or destroying compute.
- Stop or terminate according to cache policy; report resources intentionally left billable.
- Do not automatically delete persistent volumes.
- For Vast, destroy the instance after verified export. A stopped instance is
  only a temporary recovery state and must include a recorded blocker and daily
  storage cost.

## Initial implementation boundary

Implement in this order:

1. local provider registry and durable run/event schema
2. local WanGP adapter
3. one already-running remote WanGP bridge
4. RunPod discovery and lifecycle adapter
5. Vast discovery and lifecycle adapter
6. standardized image/bootstrap and persistent model cache
7. automatic provisioning and cleanup after routing and recovery tests pass

Do not begin by rebuilding both cloud environments independently. Prove the broker contract with one remote instance, then reuse the same image and health protocol across providers.

The provider-neutral worker and dry-run-first provisioning skeleton live in
`infra/gpu-worker/`. Use that skeleton for the standardized environment step;
do not create a separate, drifting WanGP installation recipe per provider.

Use `tools/wangp_recorder.py` for the local durable run journal and artifact
verification described above. Its command contract is documented in
`docs/wangp-recorder.md`.
