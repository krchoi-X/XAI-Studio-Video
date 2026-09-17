# Google Drive media-only export

Active editor: Codex
Status: IN PROGRESS — Gallery video backfill
Date: 2026-09-16

## Goal

Create a one-way, resumable exporter that reads the existing Gallery catalog and copies only registered original image/video assets into a human-browsable Google Drive streaming tree organized by character, media kind, and month.

## Scope

- `tools/drive_media_export.py`
- `tests/test_drive_media_export.py`
- `docs/drive-media-export.md`
- `tools/run_drive_media_export.ps1`
- `tools/install_drive_media_export_task.ps1`
- This task record
- Runtime state only under `D:\AI_Studio\workspace\drive-media-export`
- Pilot output only under `G:\내 드라이브\XAI-Studio Media`

## Constraints / Must Preserve

- Keep all Library originals, session folders, Gallery rows, review state, visibility, provenance, IDs, and hashes unchanged.
- Read the Studio SQLite catalog read-only; never write its database.
- Export only Gallery-registered original `image/*` and `video/*` assets, not previews, inputs, prompt/settings files, logs, or temporary frames.
- Use stable character IDs plus display names; organize as `Characters/<name [id]>/<Images|Videos>/YYYY-MM/`.
- Put multi-character, project-only, and unassigned assets in explicit non-character buckets rather than guessing ownership.
- Keep the export ledger outside Google Drive. Never infer Drive cloud-sync completion merely from a successful filesystem copy.
- Preserve restricted content in the user's private Drive only; no publication or sharing changes.

## Must NOT Do

- No move, rename, deletion, deduplication, or migration of existing originals.
- No automatic deletion from Google Drive.
- No overwrite when an existing destination differs.
- No Gallery/database mutation, service restart, GPU work, push, or public upload.
- Do not disable the existing Google Drive backup until the pilot and a later full export are independently verified.

## Contract impact

Producer: new read-only CLI projects existing Studio `assets`, `asset_roots`, `session_assets`, `generation_sessions`, and `characters` records into copied media files plus a local export ledger. Consumers: the operator and Google Drive for desktop; Gallery remains the only review/catalog surface. Existing DB records and Library paths are unchanged. Compatibility is additive and rollback consists of stopping the tool and removing its derived Drive tree/state after explicit operator approval. Deterministic tests use temporary SQLite databases and files. A live pilot copies only the five already completed Reika batch assets after a dry-run review.

Multi-character extension: producers may record the complete cast in `settings_json.session.character_ids` (preferred) or top-level `settings_json.character_ids`. The exporter unions those explicit IDs with the legacy primary `generation_sessions.character_id`; it does not infer cast from prompt text. Legacy rows remain compatible but cannot be retrospectively classified as multi-character without explicit metadata. New character rows are resolved dynamically with no exporter configuration.

## Plan

1. Confirm the Gallery schema and physical-path resolution rules.
2. Implement `plan`, `sync`, and `status` commands with character/month naming, hash verification, collision protection, limits, and a local JSON ledger/event log.
3. Add fixtures for image/video, missing files, duplicate hashes, filename collisions, unassigned assets, and incremental reruns.
4. Run deterministic tests and a dry-run against the live catalog.
5. If the dry-run selects exactly the five intended Reika assets, copy that bounded pilot to the Drive streaming folder and verify file hashes locally.
6. Make repeated whole-catalog syncs advance past already-exported assets instead of getting stuck behind the batch limit.
7. Add a no-LLM PowerShell runner and a Windows Task Scheduler installer suitable for a streamed `G:` drive in the logged-in user session.
8. Inventory and backfill the remaining Gallery media, then verify a second incremental run is a no-op.
9. Read explicit `character_ids` from session settings, keep legacy single-character compatibility, create stable named multi-character buckets, and verify new characters require no exporter configuration.
10. After the Studio registers manifest-less legacy Library videos, back up all registered candidates without selection and verify incremental scheduled operation.

## Progress

- Governance resolved Library, Gallery data, workspace, and export roots.
- Confirmed Studio SQLite records asset root + relative path and joins assets to sessions/characters.
- Confirmed `G:\내 드라이브` is the Google Drive streaming root.
- Implemented read-only `plan`, bounded `sync`, and `status` commands with character/media/month organization, collision protection, temporary-copy plus hash/size verification, and an external ledger/event log.
- Added deterministic coverage for organization, incremental reruns, adoption, conflicts, unassigned video, missing originals, selection safety, and unknown asset IDs. `8 passed` on 2026-09-16.
- Live dry-run selected exactly the five intended Reika Krea2 JPEG assets.
- Pilot copied and verified all five files under `G:\내 드라이브\XAI-Studio Media\Characters\Mizuki Reika [ch-mizuki-reika]\Images\2026-09`.
- A second identical sync returned `skip: 5`; status reported five recorded and present destinations with none missing.
- Updated whole-catalog batching so prior exports do not consume the per-run limit; deterministic coverage is now `10 passed`.
- Backfilled the complete Gallery catalog: 761 registered originals across 12 characters, approximately 390 MB. Final status reports 761 destinations present and none missing; a subsequent run processed zero items.
- Added a no-LLM PowerShell runner with persistent logs and a transient Windows ledger-lock retry.
- Installed the current-user `XAI Studio Media Export` scheduled task at a 30-minute interval with a 100-new-file cap. A real Task Scheduler execution completed with result code `0`.
- Added explicit multi-character cast parsing and stable named group folders, including 3+ cast support through sorted IDs and a group hash. New Gallery characters are resolved dynamically. Deterministic coverage is now `12 passed`.
- Live compatibility check returned `skip: 761`; the scheduled task still completed with result code `0`, so no existing media was duplicated.

## Next

Manually confirm Google Drive reports cloud synchronization complete before disabling the old raw-library backup. Periodically inspect the task result or the logs under `D:\AI_Studio\workspace\drive-media-export\logs`.

## Blockers / uncertainties

- A completed write to `G:` proves the local streaming filesystem accepted the bytes, not that Google Drive has finished uploading them. Cloud completion remains a manual Drive status check unless a supported status API is added later.
