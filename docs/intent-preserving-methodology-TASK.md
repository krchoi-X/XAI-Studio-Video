# Intent-preserving video methodology migration

- Date: 2026-10-03
- Active editor: Codex / GPT-6 Astra
- Status: COMPLETE — canonical guide, shared skill routing and deterministic pre-submit checker ready

## Goal

Preserve the current video methodology as an immutable Git-backed baseline, publish one canonical intent-preserving storyboard-to-video guide, and make future storyboard-derived video work use a portable, enforceable Intent Contract across Codex, Claude, Grok, Muse/Somni and Hermes/Meromero.

## Scope

- methodology backup manifest and local Git baseline tag;
- canonical runtime methodology and contract guide;
- shared `video-intent-contract` skill and references in `XAI-Studio-Private`;
- routing updates in shared storyboard/video skills and runtime agent entrypoints;
- artifact gates and deterministic validation guidance;
- focused validation of skill structure, catalog resolution, links and existing tests affected by edited guidance.

## Constraints / Must Preserve

- Preserve all existing user, character, production, review, storage and publication approvals.
- Preserve the useful camera, motion, continuity, model-adapter and failure-memory knowledge already present.
- Keep existing v1/v2 persisted records readable; do not silently widen a frozen schema.
- Do not modify or absorb Claude's active productions/Drive/Catch Me work or unrelated character changes.
- The contract must be usable without the originating conversation and must include bounded background and rationale.
- Narrative meaning is deny-by-default after approval; only an explicit creative-envelope allow-list may change.

## Must NOT Do

- No render, GPU job, paid API, service restart, media/database change, publication or push.
- No per-agent methodology fork and no duplicated agent-specific canonical policy.
- No claim that documentation alone is a deployed renderer gate.
- No destructive cleanup of prior guidance or history.

## Plan

1. Record immutable baseline commits and hashes for the current runtime guidance and shared skills.
2. Add a stable canonical methodology document with cross-agent background, Intent Contract lifecycle, enforcement levels, override rules and migration map.
3. Add a focused shared `video-intent-contract` skill; route existing director, cutboard, continuity and adaptive-production skills through it without duplicating their responsibilities.
4. Update runtime agent entrypoints and production artifact gates so future storyboard-derived video work must create, acknowledge and validate the contract before renderer handoff.
5. Validate skill metadata, catalog resolution, Markdown references, diffs and relevant deterministic tests.

## Contract impact

Producer: the director/storyboard stage creates the Intent Contract beside the approved Storyboard Spec. Consumers: cinematographer pass, model compiler, semantic checker, shot planner, renderer submission boundary, human review and Clypra segment selection. This change first establishes the canonical source, portable artifact requirements and mandatory gates in skills/guidance. Existing schemas and jobs remain valid. A later implementation of a persisted schema or hard runtime submission gate must use a new version or compatible sidecar, name every producer/consumer, include old-version fixtures and define rollback. Rollback of this documentation/skill migration restores the recorded baseline tag and removes the new catalog entry without touching production assets.

## Progress

- Task recorded before runtime/shared-skill edits.
- Claude's review and the user requirement for cross-agent background plus enforceable constraints were incorporated in the Private migration source.
- Preserved the runtime and shared-skill baselines with local annotated tags and a file-hash recovery manifest.
- Added the canonical runtime methodology and contract guide, closed v1 contract/compiler-IR schemas, and `tools/video_intent_contract.py`.
- Added and registered the canonical shared `video-intent-contract` skill; connected director, cutboard, continuity and adaptive-production stages without replacing their responsibilities.
- Updated common agent routing and the root video workflow. New storyboard-derived video work must produce the contract, acknowledgement, compiler IR and passing hash-bound check before submission.
- Added a native local WanGP gate for sessions registered with `--methodology intent-preserving-v1`. Submission now requires the exact storyboard, contract, compiler IR and prior semantic-check record, recomputes the check before run creation/GPU start, and stores verified evidence in `run.json`.
- Verification: 40 focused tests passed; five affected shared skills passed `quick_validate.py`; the catalog contains 13 unique definitions and resolves the new skill; Python compile and scoped diff checks passed.
- No render, GPU work, service restart, media/database change, publication or push occurred.

## Next

Request an independent Claude review after the Codex commits are preserved. Other renderer backends may later implement the same native boundary; local WanGP now enforces it directly while the maintained pre-submit checker remains the portable fallback.
