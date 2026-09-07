# Artifact and review contract

Accepted user direction: 2026-09-07. All agents use the same existing artifact hierarchy and review surfaces. This document standardizes operating instructions; it does not migrate data, introduce fields, or claim new UI features.

## Roots and identities

Resolve the checkout from actual Git/files, not an old app working directory. Current operator defaults are below; another host must verify or explicitly configure equivalent roots. Existing manifests remain authoritative for already registered assets.

| Purpose | Current location / rule |
|---|---|
| Implementation and generation records | `D:\codex\XAI-studio` |
| Private web-app source | `D:\codex\personal-prompt-studio\personal-prompt-studio` |
| Character identity | `<repo>/characters/<character-id>/character.json` |
| Character session records | `<repo>/characters/<character-id>/02_generations/<session-id>/` |
| Character originals | `D:\AI_Studio\library\characters/<character-id>/generations/<session-id>/outputs/<engine>/` |
| Standalone video prompt project, new work | `D:\AI_Studio\outputs\video-prompts\projects/<project-id>/` |
| Development decision/report | Relevant `docs/` file; historical task snapshots in `docs/task-archive/` |
| Runtime queue/cache/database | Existing owning service's configured workspace/cache; not a second media library |

Use canonical character IDs, tool-created session IDs and existing asset/job IDs across records, handoffs and UI. Human-readable titles may change independently. Never rename an existing session/path merely for visual uniformity: the importer derives asset identity from root and relative path, so moves can break reviews and create duplicates. Reuse the existing session on resume. New IDs come from the owning tool; do not impose a new naming algorithm in prose.

Originals are organized by character/session/engine, not by Codex/Claude/Grok/Hermes. Record executor and provider as metadata. `output/` scratch work is not final Gallery delivery. Do not move existing scratch or legacy assets as part of reading this policy. Preserve originals, hashes, visibility, favorites and human review decisions. Private records must follow repository publication policy; permission to save locally is not permission to push.

## Route by requested result and engine

| Request | Existing route |
|---|---|
| Existing-character still, supported local engine | Character Manager skill → `tools/character_scene.py prepare` or `produce` |
| Explicit external image/video engine | Use that engine's available authorized tool; import originals through `external_media_import` and existing Studio sync |
| Video prompt / rendering | Root `SKILL.md`; existing recorder/broker workflow, explicit destination preserved |
| Idea requiring storyboard/sample decisions | `skills/idea-to-production/SKILL.md` and its existing approval states |
| Night batch for supported local engines | Character Manager night-batch workflow; sequential durable queue |

An explicit engine overrides defaults in every row, including night batches. If unavailable, report the missing capability; do not silently switch engine or pretend the local CLI supports it. Exact requests and per-item runtime prompts remain durable. Canonical DNA edits and human reference approval require their existing explicit workflows.

## Record, import, sync, review

Character records retain `batch.yaml`, `prompt.txt` and the producing tool's run/trace/manifest/provenance files. `session.asset_root` points to actual originals. Engine directories must agree with manifest output directories because the importer reads the first relative path component as engine.

For external imports, inspect `python -m external_media_import --help` and the package README. Use dry-run to validate the intended manifest, then the authorized apply workflow. It copies originals and publishes discoverable `batch.yaml` last. Do not write directly to the Studio database. Different per-item prompts must remain accurate: use the importer's existing per-item/session support and provenance; never present a batch summary as the exact prompt for every image. Do not claim provenance fields are visible in the UI until verified.

Generation completion, import completion, Gallery sync, and human review are separate states. Preserve each service's actual status vocabulary; do not rewrite stored enums to match a display phrase. A completed render does not mean synced or approved. If sync fails, retry sync using existing records; do not regenerate. Verify expected IDs/counts, preview access and, for video, supported playback/Range and seeking before claiming web verification. New imports remain needs_review according to the existing importer contract.

## Consistent places to inspect results

| User intent | Existing surface |
|---|---|
| Browse or review completed images/videos | Studio Gallery: Library / Review, same character and session |
| Create or follow production requests | Studio Production: Create / Batch / Jobs |
| Inspect GPU/process execution | Control Tower; observability with output links, no duplicate review database |
| Read a development report | Linked repository document in the current host's file viewer |
| Inspect prompt-only standalone work | Project record and prompt file; Gallery availability is not automatic |

Current Studio shell includes `/review`, `/library/characters/<character-id>` and `/production/create`, `/production/jobs`. Verify the deployed base URL and supported route/query before giving a clickable deep link. Do not invent `/gallery/<id>` or new session query parameters. If precise selection is unsupported, give the existing route plus character/session title and ID. Keep one logical destination per purpose; use engine/executor as metadata or existing filters rather than new top-level tabs or copied folders. Preserve selection/return context when existing navigation supports it.

For UI implementation, the Studio `DESIGN.md`, navigation plan and private/public architecture remain authoritative. Agent entrypoints must link this contract; they do not independently redefine tab labels or layout. This policy does not authorize public publication or claim installation/runtime verification.

## Standalone video project persistence

Resolve `project_root` once: explicit user-selected root; otherwise an existing project's recorded location when resuming; otherwise the default above. Under it retain `project.md`, `prompts/<prompt-id>.md`, exact `prompts/<prompt-id>.txt`, `handoff.json` and unique recorder run directories. Legacy `<repo>/projects/<project-id>/` remains readable in place. Never create both roots for one project or migrate it implicitly. Character pipelines retain their established session root instead of creating a second standalone project copy. Recorder/tool path arguments must point at the resolved root; bundled executables resolve from the verified checkout/skill bundle.

## Known adoption gaps

Installed agent copies have not been updated by this document. Direct Claude/Grok local CLI actor support remains limited; see [shared workflow](shared-agent-workflow.md). External video integration is recorded as implemented in its scoped task, with live desktop/tablet checks pending. Standalone prompt projects are not automatically indexed by Gallery. These are explicit follow-ups, not grounds to claim end-to-end consistency already deployed.
