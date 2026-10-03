# Current priorities

Updated: 2026-09-28 (Asia/Tokyo)

## P0 — Qwen Image 2.1 character-identity pilot

- Context: the approved face master drifts during Krea2 character-sheet edits and new-angle generation. The user selected a local Qwen Image 2.1 uncensored GGUF experiment before more video work.
- Priority rationale: stable approved character views are upstream of storyboards and video continuity; another video-layer expansion would not fix an unstable identity source.
- Status: HANDOFF READY — WanGP registration and text-to-image smoke passed; reference-bound integration and identity A/B remain.
- Owner: Claude Code for the user-assigned implementation; Codex authored the completed pilot record and handoff.
- Depends on: the verified local finetune `qwen_image_21_uncensored_q4_k_m`, existing companion files, one user-selected face master and preserved Krea2 evidence.
- Blocks: making Qwen a selectable Character Manager/Studio engine and deciding whether generated profiles are usable as reviewed angle masters.
- Next action: Claude Code follows the [Studio integration handoff](qwen-image-2.1-studio-integration-handoff.md), beginning with the common reference adapter and deterministic compatibility tests before the fixed identity gate.
- Not now: making Qwen the default, automatic canonical promotion, concurrent Krea2/Qwen GPU work, another model download/update, video generation or unrelated refactors.

## Completed — Consistent shared instructions and artifact review

- Context: the user requested one consistent workflow across Codex, Claude Code, Grok Bot and Hermes-hosted models, including folders and web-app surfaces.
- Priority rationale: conflicting agent rules and output locations cause avoidable handoff and review failures.
- Status: COMPLETE — documentation aligned; see [root task](../TASK.md).
- Owner: Codex for this documentation task; the resulting policy applies to every agent.
- Depends on: existing character/session records, Studio importer/Gallery and scoped task evidence.
- Blocks: reliable adoption of the same instructions by all executors.
- Next action: use the shared policy; select installation adoption or runtime verification only as the next assigned task. No new P0 is automatically active.
- Not now: media migration, UI restructuring, paid generation or unrelated infrastructure work.

## Tracked follow-ups — not additional P0 tasks

| Work | Evidence / status | Next action when assigned |
|---|---|---|
| External image/video import | [Scoped task](../external_media_import/TASK.md) records implementation; live playback checks remain | Verify desktop/tablet playback and integration; do not restart Task A or run Task B automatically |
| Control Tower v0.1 | [Archived task](task-archive/2026-09-07-control-tower-task-snapshot.md) records completion | Tablet review and optional autostart |
| Pending character records | Existing working-tree changes remain | Audit separately before any publication/push |
| Hermes night batches / curation | Existing operational lane | Refine when requested; no implicit new batch |
| RunPod 5090 practice | Previous P0, now parked by the current user objective | Resume the operator runbook only when selected |
| h3_intent / Vast expansion | Deferred | Reassess after a demonstrated production need |
| Video pattern-card expansion | Deferred by the Qwen character objective | Resume after the identity pilot decision |

The [previous priority snapshot](task-archive/2026-09-07-priorities-snapshot.md) preserves historical rationale. Keep at most one active main P0. On completion mark it complete and record the next assigned task; do not silently promote an old TODO. Package assignments may proceed within their already authorized scope without replacing the root main task.
