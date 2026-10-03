# Grok Bot project entrypoint

Explicitly load [AGENTS.md](AGENTS.md), [shared agent workflow](docs/shared-agent-workflow.md), and the applicable scoped TASK. This filename is a bootstrap pointer; automatic loading depends on the host configuration.

For XAI work, also read `D:/codex/XAI-Studio-Private/control/generated/grok.md` and `D:/codex/XAI-Studio-Private/control/agents/production-roles.md`; follow the mandatory rules and Grok responsibilities before production or skill maintenance.

For routine credit-sensitive character image/video work, follow the [Grok/Hermes production playbook](docs/grok-hermes-production-playbook.md), including its still-image DNA rule. “Transform this image” requires both the exact hash-bound source and canonical Stable DNA; wardrobe/pose text is a Scene Delta, never the identity definition. When a run exposes an identity, reference, continuity or recording problem that may need Codex/Claude review, create a durable report using the [production incident guide](docs/production-incident-and-agent-consultation.md) and its template before spending more credits.

## Production recording rules

Every render you produce must record who asked for it. Do this with the repository tools; do not invent a new file
layout. Full rules and the record shape: [WanGP recorder](docs/wangp-recorder.md#recording-a-production-session).

1. **Register the session once, before the first render.**

```powershell
python tools/wangp_recorder.py session --session-dir <session> --requested-by grok `
  --engine WanGP --model minimax_h3_ref2va_pruned --character-id ch-lia `
  --title "<short title>" --user-request "<operator request, verbatim>" --status running `
  --production-plan <session>/shot-production-plan-v2.json
```

For new character-video and multi-pack sessions, the approved schema-v2 plan is required by this operating guide.
Validate it before registration. It freezes Stable DNA and mandatory prompt anchors and makes pack-specific
references, laterality/composition review and boundary frames fail closed before GPU work. Historical sessions
without a plan keep their legacy behavior.

2. **Submit each shot.** The requester is inherited from the session record, so the flag is optional; pass it
   anyway when you submit outside a registered session.

```powershell
python tools/local_wangp.py submit --runs-root <session>/runs `
  --prompt-file <session>/<shot>.txt --settings-file <session>/<shot>.settings.json `
  --project-id <session-id> --prompt-id <shot> --output-dir <library>/videos/<session-id> `
  --requested-by grok
```

3. **Character stills go through the scene pipeline** with your own actor, never `codex`:

```powershell
python tools/character_scene.py produce --character ch-lia --request "<prompt>" `
  --engines krea2 --count 2 --strategy strict_translation --actor grok
```

4. **Close the session** when it finishes: rerun step 1 with `--status completed` (or `failed`). Re-running merges
   and keeps your extra keys.

Keep `requested_by` (you), `executor` (the local WanGP worker), `engine` (WanGP) and `model` (the checkpoint) as four
separate facts. Never label your own work as another agent, and never write a requester you did not verify. The
Control Tower then shows your renders as `grok (from record)` with live progress and ETA.

For the external image/video import assignment, read [handoff](docs/grok-bot-handoff.md) and [package task](external_media_import/TASK.md); inspect current code before treating the original assignment as unimplemented. For production, follow [artifact and review contract](docs/artifact-and-review-contract.md). Grok Bot is the executor, not necessarily the rendering engine. Preserve the requested provider, truthful provenance, existing Gallery IDs and review state. Do not run the handoff's Task B unless the user requested that trial.
