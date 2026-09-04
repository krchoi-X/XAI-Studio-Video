# Current Task

Status: READY — begin with the RunPod inventory and runbook; no cloud spend is authorized by this file.

## Goal

Make one RunPod 5090 workflow repeatable from provisioning through verified local recovery and compute termination. Produce a short operator runbook first, then use one deliberately small content job to validate it with the user.

## Constraints / Must Preserve

- Use RunPod first; Vast remains deferred until the RunPod loop is routine.
- Treat every cloud worker as ephemeral: download, verify, register locally, then terminate compute.
- Preserve prompts, settings, provenance, and the durable local asset location.
- Keep generated media out of ordinary Git. Store it under `D:\AI_Studio\library` and back it up separately.
- Reuse existing Render Broker, worker, and character-session conventions where useful without making automation a prerequisite.
- Do not spend cloud money or terminate a live Pod without the user's explicit instruction for that operation.

## Must NOT Do

- Do not implement multi-provider orchestration, a new model router, or full auto-provisioning.
- Do not require finished Character DNA, LoRA training, or new UI work before the pilot.
- Do not push private character prompts or generation history to the public upstream.
- Avoid unrelated renderer, schema, or application refactors.

## Expected Scope

- Likely files/directories: existing RunPod/worker docs and scripts, `docs/`, this file.
- Expected change radius: small.
- Mechanically verifiable: partial; commands and file checks are deterministic, billing/availability and the creative result require human confirmation.
- Expected deliverable: one concise runbook plus one recorded pilot result/failure report.

## Work Allocation

- **Codex:** inventory existing assets, reconcile architecture, write/integrate the runbook, inspect pilot evidence, and make repo-wide changes if a proven gap requires them.
- **Claude Code:** only a bounded documentation, checklist, or isolated module package with explicit owned files and acceptance criteria. Do not ask Claude to rediscover repository-wide state.
- **Hermes/local LLM:** prepare prompt variants and execute repeatable content batches after the workflow and constraints are approved.
- **Deterministic tools:** readiness checks, checksums, file manifests, tests, and process/billing cleanup evidence before any second-LLM review.

## Plan

1. Inventory existing RunPod templates, worker scripts, model paths, storage conventions, and prior run notes.
2. Write a manual operator checklist covering provision, attach storage, readiness, one minimal job, download/register, checksum verification, and termination/billing confirmation.
3. Review the checklist with the user before starting billable compute.
4. Run one small pilot and save its prompt/settings/result manifest outside the Pod.
5. Record only repeated or material friction; automate the smallest proven pain point afterward.
6. After the loop is repeatable, return to automatic first-pass curation and tablet batch controls.

## Progress

- [x] Pulled the credit-aware handoff protocol from public upstream.
- [x] Recovered and committed three Lia scene-variation metadata sessions locally.
- [x] Confirmed those sessions contain compact metadata only, not generated media or credentials.
- [ ] Inventory the existing RunPod path.
- [ ] Draft and verify the operator runbook.
- [ ] Run the user-approved pilot.

## Verification

- Repository sync: public upstream incorporated through `5f26199`.
- Lia metadata: no media files, no files over 20 MB, and no credential-pattern matches before commit `d9b02f3`.
- Tests: not required for the metadata-only checkpoint; run relevant deterministic checks for any implementation change.

## Next

Search the repository for existing RunPod templates, endpoints, worker commands, storage paths, and cleanup notes. Produce an evidence-based inventory before editing or provisioning anything.

## Blockers / Uncertainties

- Current RunPod template ID, network-volume mount layout, and model readiness must be discovered from repository/local evidence or confirmed by the user.
- The Lia metadata commit is intentionally local/private and must not be pushed to the public `XAI-Studio-Video` upstream.

## Relevant Files

- `AGENTS.md`
- `docs/current-priorities.md`
- `docs/agent-handoff-protocol.md`
- `docs/repository-backup-policy.md`
- Existing RunPod/worker documentation and scripts found during inventory

## Recovery Rule

If this file is stale, trust evidence in this order: code and working tree, Git history/diff, deterministic verification, this file, prior agent prose. After two materially similar failures, stop and change strategy.
