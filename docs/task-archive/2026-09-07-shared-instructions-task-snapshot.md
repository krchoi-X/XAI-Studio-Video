# Current Task — Shared agent and artifact instructions

Updated: 2026-09-07 (Asia/Tokyo)
Active editor: Codex
Status: COMPLETE — repository documentation aligned; deployment/runtime gaps recorded

## Goal

Unify instructions for Codex, Claude Code, Grok Bot, and models running inside Hermes; align handoffs, artifact storage, and Gallery/Production navigation with existing contracts.

## Constraints / Must Preserve

Preserve existing edits, IDs, media, review state, and runtime behavior. Previous Control Tower task is archived in `docs/task-archive/2026-09-07-control-tower-task-snapshot.md`. Grok's scoped work remains in `external_media_import/TASK.md`.

## Must NOT Do

No generation, media migration, deployment, installed-agent configuration changes, API/CLI changes, new UI tabs, or commits of other agents' work.

## Plan / Scope

1. Reconcile shared startup, priority, ownership, routing, persistence, and verification docs.
2. Link thin agent entrypoints and Studio instructions to shared artifact policy.
3. Check links, code references, and diff; document implementation gaps.

## Progress

- Read both repositories' instructions, actual importer, routes and CLI; archived previous root task/priorities.
- Updated shared policy, all four agent entrypoints, role/handoff instructions, video and character skills.
- Added shared agent workflow, artifact/review contract and scoped verification guide; linked Studio instructions without changing its active implementation records.
- Preserved Grok assignment and existing uncommitted edits. Updated original handoff status from its scoped task evidence.

## Verification

- 39 relative Markdown links in the changed entrypoints/docs resolve.
- Documented test-selection files exist; actor enum and Studio routes/importer behavior cross-checked with source.
- Documentation diff whitespace check passed after removing one trailing-space issue.
- No runtime code changed; no renderer/full application tests or installed-agent deployment claimed.

## Contract impact

Producers: agents following instructions. Consumers: other agents, Studio importer/Gallery and Control Tower. Documentation only: existing batch/session formats, paths and IDs remain valid. No migration. Rollback only this task's documentation changes; archives preserve prior notes. Verify relative links, code/command references and whitespace. Installation and live UI behavior require separate verification.

## Next

Use the shared entrypoints for subsequent work. Installation adoption, direct Claude/Grok actor support and pending live video review remain explicit follow-ups in shared docs/current priorities; do not automatically start them or resume archived P0 work.

## Blockers / Uncertainties

- CLI actor currently accepts only codex/hermes/web.
- Grok's scoped task still lists live desktop/tablet playback checks as pending.

---

Scoped active task (Claude Code, 2026-09-07): explicit requester provenance on the WanGP submit path — see `control_tower/TASK.md`.
