# Task — infra/gpu-worker (ephemeral cloud GPU lifecycle)

Owner / Active editor: Claude
Integration owner: Codex
Status: PHASE 1 STARTED — `list-active` account audit implemented
Started: 2026-09-18
Authority: direct user objective (automate RunPod/Vast pod lifecycle with cost control).
This overrides the parked "RunPod 5090 practice" line in `docs/current-priorities.md`
for this bounded package only.

Do **not** replace or rewrite root `TASK.md` (Codex, reference-resolution, COMPLETE).
This file is the durable state for `infra/gpu-worker/**` plus the new RunPod runbook.

Plan of record: [docs/cloud-gpu-automation-plan.md](../../docs/cloud-gpu-automation-plan.md).

## Goal

Make one cloud production session start, run, export and terminate from code without leaving
billable resources behind, and keep only irreplaceable assets on paid persistent storage.

## Constraints / Must Preserve

- Existing four `provision.py` subcommands keep their exact arguments and output shape.
- Dry-run remains the default; `--execute` remains the only path to a billable call.
- Vast stays empty-start / destroy-always (`docs/vast-ephemeral-runbook.md`). The network
  volume policy is RunPod-only and that asymmetry is intentional.
- `docs/render-broker.md` routing rules: missing capacity is reported, never worked around by
  changing GPU, model or provider.
- Durable run journalling stays in `tools/wangp_recorder.py`; results stay in the existing
  importer/Gallery contracts.
- Container image holds runtime only; weights live on the volume or are fetched per session.

## Must NOT Do

- No billable provider call from tests.
- No automatic volume deletion; report eviction candidates only.
- No destroy before export checksums verify outside the pod — stop and escalate instead.
- No API keys in config files, images, run records or Git.
- No new provider abstraction layer, scheduler, or parallel output hierarchy.
- No unrelated refactor of `tools/` or Studio while in this scope.

## Plan

Ordered stop-before-start, per the plan document:

0. **Unblock (user):** build and push the worker image; write `config.local.json`; export keys.
1. **Lifecycle/cost safety:** `list-active`, `runpod-status`, `vast-status`, `wait-ready`,
   `runpod-terminate`, `vast-destroy`, `orphan-check`, `active-resources.json`.
2. **Model manifest:** `models.manifest.json`, `ensure-models`, `volume-report`, A/B/C tiering.
3. **Session orchestrator:** `session.py` run/status/abort with `try/finally` teardown and a
   `--max-runtime-minutes` watchdog.
4. **RunPod runbook:** `docs/runpod-ephemeral-runbook.md`, symmetric to the Vast one.
5. **Cost log:** `cost-log.jsonl`; revisit the volume-size decision after ~5 real sessions.

## Progress

- 2026-09-18: implemented `provision.py list-active`, the first Phase 1 command. Read-only,
  dry-run by default, needs no config file (so it works before the worker image exists).
  Reports pods/instances/volumes with hourly rate, plus `hourly_burn` (running compute only)
  and `persistent_storage_gb` (billed continuously). Warns on the storage-with-no-compute case
  and on non-running compute. A failing endpoint lands in `notes` rather than aborting the audit.
  9 tests pass; no network call and no billable call in the suite.
- User reported real evidence for the plan's §2 challenge: after several unused weeks, storage
  was charged while compute was not. Volume cleanup therefore moves ahead of the rest of Phase 1.
- Inventoried existing assets. `provision.py` is create-only: it can start billable compute and
  cannot stop it from code. That asymmetry is the first thing to fix.
- No model manifest exists anywhere, although both runbooks require one.
- No cost or pricing figure is recorded anywhere in the repository.
- Recorded the storage-economics challenge: a network volume bills 24/7 while pods bill only
  while running, so a large volume of re-acquirable public checkpoints is likely a cost
  increase at this session frequency. Justification shifts to irreplaceable assets,
  determinism, and boot latency — which implies tiering, not a blanket cache.

## Contract impact

Producer: `provision.py` (additive subcommands), new `models.manifest.json`,
`active-resources.json`, `cost-log.jsonl`.
Consumers: operators via both runbooks; future Render Broker adapter; `wangp_recorder.py`
(called, not modified in Phases 1–3).
Old persisted examples: an existing `config.local.json` stays valid; new config keys are
optional with defaults. No existing record is rewritten.
Rollback: remove the new subcommands and files; the create-only CLI is unaffected.
Verification: `infra/gpu-worker/test_provision.py` extended with recorded provider-response
fixtures; no network and no billable call in the suite.

## Next

Run `list-active --execute` against the real account, confirm the reported volume size, data
center and 30-day billing match the RunPod console, and correct any null field accessor. Then
copy Tier A assets off the volume and shrink or delete it. Remaining Phase 1 commands
(`*-status`, `wait-ready`, terminate/destroy, `orphan-check`) follow.

Earlier note on phase order: Phase 0 is a user action (image build/push) and
blocks any real provider call, but Phases 1 and 2 are implementable and testable now against
recorded fixtures without it.

## Blockers / uncertainties

- **RunPod REST v1 (`rest.runpod.io/v1`) is deprecated and retires 2026-11-15.** `runpod-create`
  still targets it. The audit path already uses v2 (`api.runpod.io/v2`). Migrating the create
  path is dated work, not optional cleanup, and must land before that date.
- Field names in the v2 audit responses were not verified against a live account; `pick()`
  tolerates several spellings, but the first real `--execute` run should be checked against the
  RunPod console and the accessors corrected if anything reads as null.
- Worker image is unpublished; the image tag is still the `YOUR_ACCOUNT` placeholder.
- Current provider pricing, real 5090 hourly rate in the volume's data center, measured
  download throughput, and active-profile byte size are all unmeasured. The breakeven
  arithmetic in the plan is illustrative, not observed — see plan §8.
- Whether the existing RunPod network volume's data center reliably has 5090 capacity is
  unknown and is a real failure mode for automatic creation.
