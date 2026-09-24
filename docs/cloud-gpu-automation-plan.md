# Cloud GPU Automation Plan — Ephemeral Pod Lifecycle and Durable Model Storage

Updated: 2026-09-18

Status: `IN PROGRESS — RunPod audit/readiness/verified termination implemented; Vast teardown,
model-schema readiness, and later phases remain`

Scope: `infra/gpu-worker/**`, one new RunPod operator runbook, one cost log.
Related: [render broker](render-broker.md), [Vast runbook](vast-ephemeral-runbook.md),
[async/ephemeral design reference](design-reference-async-production-and-ephemeral-gpu.md).

This plan makes cloud GPU rental repeatable and cheap for this project. It does not
introduce a new provider abstraction, a scheduler, or a second gallery. It completes the
lifecycle that `infra/gpu-worker/provision.py` already started.

---

## 1. What already exists

| Asset | State | Gap |
|---|---|---|
| `infra/gpu-worker/Dockerfile` | Pins WanGP `01a67f0a`, CUDA 13.0, torch 2.10.0; symlinks `ckpts`/`outputs` into `/workspace` | Never built or published; image tag is still `ghcr.io/YOUR_ACCOUNT/...` |
| `infra/gpu-worker/entrypoint.sh` | Selects one WanGP service mode, writes `worker-state.json`, starts health server | Does not fetch models; assumes `/workspace/models` is already populated |
| `infra/gpu-worker/health_server.py` | Port 8080 process-level health | Reports process state only, not model readiness |
| `infra/gpu-worker/provision.py` | `validate`, `runpod-create`, `vast-search`, `vast-create`; dry-run by default; price ceiling on Vast | **Create-only.** No status, no readiness wait, no stop, no destroy, no active-resource listing |
| `infra/gpu-worker/config.example.json` | GPU/price/disk policy, `network_volume_id` field | `network_volume_id` is empty; no volume creation, inspection, or content policy |
| `docs/vast-ephemeral-runbook.md` | Full operator gate with mandatory teardown | Vast only; no RunPod equivalent despite RunPod being the account the user already has |
| `tools/wangp_recorder.py` | Durable run journal (`prepare`/`session`/`state`/`attach`/`fail`) | No provider cost, no rented-resource identity, no teardown confirmation |
| Model manifest | **Does not exist** | Both runbooks require "source URI, filename, size, checksum"; nothing machine-readable provides it |

The asymmetry matters: this repository can currently **start** billable compute and cannot
**stop** it from code. Adding more automatic creation on top of that increases cost risk.

---

## 2. Structural challenge to the stated cost assumption

**[Premise re-examination]** The working assumption is that keeping checkpoints on network
storage reduces cost. For compute that is true — an idle pod is pure waste. For storage it is
usually false, because **network volumes bill 24/7 while pods bill only while running.**

Breakeven, per month:

```text
volume_monthly  =  volume_gb x storage_rate_per_gb_month
redownload_cost =  sessions_per_month x (bytes / throughput) x pod_hourly_rate

network volume is cheaper only when:
    volume_monthly  <  redownload_cost
```

Plugging in plausible numbers for a 200 GB profile [inference — rates must be measured, see §8]:

```text
volume:      200 GB x ~$0.07/GB/mo            ~= $14 / month, always
redownload:  200 GB at ~150 MB/s = ~22 min
             0.37 h x ~$0.80/h                ~= $0.30 / session
breakeven:   ~45 sessions / month
```

At a realistic few sessions per month, a 200 GB network volume costs several times more than
re-downloading. If the volume is kept purely for public checkpoints, it is a cost **increase**
disguised as a saving.

That does not make network storage wrong. It makes the justification different:

1. **Irreplaceable assets** — self-trained LoRAs, character reference sets, curated
   checkpoints. Re-download is not merely slow, it is impossible. These must be durable
   regardless of price, and they are small.
2. **Determinism** — an upstream weight that is re-uploaded, re-quantized, or withdrawn
   silently changes output. A checksummed local copy is the only defense.
3. **Session latency** — 20+ minutes of boot before the first frame is worse than the money.

So the correct rule is not "put checkpoints on network storage". It is **tier the storage and
size the volume to the active profile, not to the catalog.**

---

## 3. Storage tiering

```text
Tier A — network volume, mandatory, small
  self-trained LoRAs, character reference sets, custom/merged checkpoints,
  pinned runtime config, settings profiles
  -> irreplaceable; sized in single-digit to low-tens of GB

Tier B — network volume, optional, measured
  public checkpoints for the CURRENTLY ACTIVE model profile only
  -> re-acquirable; kept only while §8 measurement shows it pays or the
     latency is worth it; evicted when the profile goes inactive

Tier C — never on the volume
  final media, previews, run logs
  -> exported and checksum-verified to durable local/object storage,
     then the compute and its scratch disk are destroyed
```

Container image holds the runtime (WanGP, torch, CUDA) and no weights. That split already
exists in the Dockerfile and must be preserved.

### Provider asymmetry is intentional

RunPod keeps a network volume; Vast does not. This is already project policy and the reason
should stay recorded:

- A RunPod network volume is bound to one data center. That is acceptable for a single
  account with one region preference, but it **constrains which pods can be created** — if the
  volume's DC has no 5090 capacity, the run cannot start there.
- Vast is a marketplace of independent hosts. A Vast volume binds the session to one host,
  stopped-instance storage stays billable, and restart availability is not guaranteed. Vast
  therefore stays empty-start and destroy-always, per `docs/vast-ephemeral-runbook.md`.

Automation must surface "no capacity in the volume's data center" as an explicit failure. It
must never silently relocate, downgrade the GPU, or switch provider — `docs/render-broker.md`
already forbids that.

---

## 4. Target lifecycle

```text
preflight            manifest valid, destination writable, API key present,
                     NO pre-existing billable resource from this project
  -> record          local run record created BEFORE any provider call
  -> capacity        volume DC has the requested GPU, or stop with a named reason
  -> create          price ceiling enforced; accepted price + IDs recorded
  -> wait-ready      health + WanGP model schema polled; timeout -> teardown
  -> ensure-models   volume diffed against manifest; missing files only; checksums
  -> smoke           one cheap job before the expensive batch
  -> render          batch submitted; progress and effective settings recorded
  -> export          artifacts + manifest downloaded, checksums verified OUTSIDE the pod
  -> teardown        destroy; confirm resource no longer listed as billable
  -> account         runtime, accepted rate, total cost written to the cost log
```

**Every failure path terminates at `teardown`.** A crashed orchestrator must not leave a rented
GPU running, which is why §5 Phase 1 lands before any orchestration.

---

## 5. Phases

Implementation order is deliberately the reverse of the intuitive one: stop before start.

### Phase 0 — Unblock (user action, not automatable here)

Nothing downstream can run while the image is a placeholder.

1. Build and push the worker image to a registry both providers can pull (GHCR public is fine):
   `docker build -t ghcr.io/<account>/xai-wangp-h3:0.1.0 infra/gpu-worker && docker push ...`
2. Record the real image digest in `config.local.json` (git-ignored) and the environment
   version string.
3. Export `RUNPOD_API_KEY` / `VAST_API_KEY` in the shell profile only. Never in the JSON.

Acceptance: `python infra/gpu-worker/provision.py validate --config infra/gpu-worker/config.local.json` passes.

Note the image will be large (CUDA devel + torch + WanGP deps). If cold-pull time proves
significant, the follow-up is a slimmer `runtime` CUDA base — not moving the venv onto the
volume, which would break reproducibility.

### Phase 1 — Lifecycle and cost safety (highest priority)

New `provision.py` subcommands, all dry-run by default, all `--execute` to act:

```text
list-active   [--provider runpod|vast|all]
    every billable pod, instance and volume for the configured account,
    with hourly rate and elapsed runtime. The "am I leaking money?" command.

runpod-status   --pod-id ID
vast-status     --instance-id ID
    normalized: provider_state, public endpoints, uptime, accepted rate

wait-ready      --provider P --id ID [--timeout-seconds N] [--teardown-on-timeout]
    polls :8080/healthz then the WanGP model schema; distinguishes
    "process up" from "renderer able to accept this model"

runpod-terminate --pod-id ID
vast-destroy     --instance-id ID
    post-condition CHECK: re-list and assert the resource is gone.
    Exit non-zero if it still appears.

orphan-check
    reads local infra/gpu-worker/active-resources.json (written at create,
    cleared at verified teardown) and reconciles it against both provider APIs.
```

`active-resources.json` is the crash-safety net: if the orchestrator dies mid-session, the next
invocation — or a manual `orphan-check` — still finds the rented GPU.

Acceptance: unit tests extend `test_provision.py` with payload/parse tests using recorded
fixtures; no billable call in tests. One real paid smoke: create → status → terminate →
`list-active` shows empty.

### Phase 2 — Model manifest and volume management

```text
infra/gpu-worker/models.manifest.json
{
  "profiles": {
    "h3-video-v1": {
      "tier": "B",
      "files": [
        {"uri": "...", "filename": "...", "target": "models/...",
         "size_bytes": 0, "sha256": "..."}
      ]
    },
    "character-assets": { "tier": "A", "files": [...] }
  }
}
```

```text
ensure-models --profile NAME [--volume-mount /workspace]
    diff manifest vs. what is on the volume; download only missing files;
    verify size + sha256; never delete anything

volume-report
    per-profile occupancy, total used vs. provisioned GB, files present but
    absent from the manifest, files unused for N days.
    Reports eviction CANDIDATES. Deletion stays manual — render-broker.md
    forbids automatic volume deletion.
```

Tier A entries are the durable ones and must also exist in the local/durable archive, so the
volume is a cache for them too, not the only copy.

Acceptance: `ensure-models` on an already-complete volume performs zero downloads and exits 0;
a corrupted file is detected by checksum and re-fetched; `volume-report` matches `du`.

### Phase 3 — Session orchestrator

`infra/gpu-worker/session.py`, driven by one batch manifest — the small YAML shape already
sketched in `design-reference-async-production-and-ephemeral-gpu.md` §Night Batch.

```text
session run --config C --manifest M [--max-runtime-minutes N] --execute
session status --session-id S
session abort  --session-id S     # always tears down
```

Runs §4 end to end inside `try/finally`, where `finally` performs teardown and writes the cost
record. `--max-runtime-minutes` is a hard watchdog, independent of job progress.

Delegates rather than reimplements: `tools/wangp_recorder.py` for the durable run journal,
existing importer/Gallery contracts for results. No parallel output hierarchy.

Acceptance: a fake-provider integration test drives every failure branch (create fails,
readiness times out, render fails, export checksum mismatch) and asserts teardown ran in all of
them; export-verification failure must NOT auto-destroy — it stops the instance and raises, per
the Vast runbook.

### Phase 4 — RunPod operator runbook

`docs/runpod-ephemeral-runbook.md`, symmetric to the Vast one, differing where policy differs:
network volume retained, terminate-vs-stop decision rule, DC/capacity coupling, and the exact
manual fallback for every Phase 1–3 command. The archived P0 asked for exactly this and it
remains valid: automation should follow a runbook that a human can already execute.

### Phase 5 — Cost log and decision review

`infra/gpu-worker/cost-log.jsonl`, one record per session:

```text
session_id, provider, resource_id, gpu, accepted_hourly_rate,
started_at, ended_at, runtime_minutes, compute_cost,
volume_gb, volume_monthly_cost_share,
model_download_seconds, teardown_verified, notes
```

After ~5 real sessions this answers §2 empirically: keep the volume, shrink it to Tier A only,
or drop it. Until then the volume size stays at the minimum that holds Tier A plus one active
Tier B profile.

---

## 6. Contract impact

- **Producer:** `infra/gpu-worker/provision.py` gains subcommands; `models.manifest.json`,
  `active-resources.json`, `cost-log.jsonl` are new files.
- **Consumers:** operators via the runbooks; the future Render Broker adapter layer;
  `tools/wangp_recorder.py` (read-only relationship — the orchestrator calls it, the recorder
  schema is not changed in Phases 1–3).
- **Existing persisted records:** none are rewritten. `config.example.json` gains optional keys
  with defaults, so an existing `config.local.json` keeps working.
- **Compatibility:** all new subcommands are additive; existing four subcommands keep their
  exact arguments and output shape.
- **Rollback:** delete the new subcommands and new files; the create-only CLI is unaffected.
- **Deterministic verification:** `infra/gpu-worker/test_provision.py` extended with recorded
  provider-response fixtures; no network and no billable call in the test suite.

---

## 7. Guardrails

1. Dry-run stays the default for every new subcommand.
2. No billable resource is created without `--execute` and a live price ceiling check.
3. Destroy commands verify the post-condition by re-listing, and fail loudly otherwise.
4. Volumes are never deleted automatically; only eviction candidates are reported.
5. Export must be checksum-verified outside the pod before compute is destroyed. If
   verification fails, stop — do not destroy — record the blocker and escalate.
6. Missing capacity is reported, never worked around by changing GPU, model or provider.
7. API keys come from the environment only.

## 8. Open measurements (blocking §2's conclusion, not §5's start)

**Measured 2026-09-18:** the existing RunPod network volume bills **~$1.6/day (~$48/month)**,
charged continuously through a month in which it was not used at all. That is far above the
$14/month the §2 example assumed, and it implies a several-hundred-GB volume — i.e. a cache of
re-downloadable public weights. It is the empirical confirmation of §2.

The [PC-less cloud studio plan](pc-less-cloud-studio-plan.md) removes the need for a provider
volume in every branch: weights, inputs and outputs all live in Google Drive, which is already
paid for. The volume is therefore to be deleted, not resized. A RunPod volume has no paused
state — deletion is the only thing that stops the charge — and it cannot be deleted while a pod
is attached, so pods terminate first.

Still unverified:

- current RunPod network-volume $/GB/month and its minimum billable granularity;
- current Vast volume pricing and stopped-instance storage charge;
- real 5090 on-demand hourly rate in the volume's data center;
- measured download throughput from the actual weight sources into a pod;
- cold-pull time for the published worker image;
- total bytes of the active model profile.

Record each in `cost-log.jsonl` or this section as it is measured. Do not restate the §2
example figures as facts — they are illustrative arithmetic, not observations.
