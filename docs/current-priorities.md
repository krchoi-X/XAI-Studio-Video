# Current priorities

Updated: 2026-09-07 (Asia/Tokyo)

## P0 — Consistent shared instructions and artifact review

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

The [previous priority snapshot](task-archive/2026-09-07-priorities-snapshot.md) preserves historical rationale. Keep at most one active main P0. On completion mark it complete and record the next assigned task; do not silently promote an old TODO. Package assignments may proceed within their already authorized scope without replacing the root main task.
