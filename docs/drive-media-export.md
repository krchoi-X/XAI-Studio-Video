# Google Drive media-only export

`tools/drive_media_export.py` creates a one-way, human-browsable copy of Gallery-registered original images and videos. It does not move Library originals, write the Gallery database, export previews/logs/settings, or delete Drive files.

Default destination:

```text
G:\내 드라이브\XAI-Studio Media\
  Characters\<Romanized Name [ch-id]>\Images\YYYY-MM\...
  Characters\<Romanized Name [ch-id]>\Videos\YYYY-MM\...
  Multi-Character\Group <stable hash> - <Name [id] + Name [id]>\<Images|Videos>\YYYY-MM\...
  Unassigned\<Images|Videos>\YYYY-MM\...
```

The local ledger is kept outside Drive at `D:\AI_Studio\workspace\drive-media-export`. A successful copy means the Drive streaming filesystem accepted and hash-verified the file; it does not prove the cloud upload has completed.

New characters require no exporter configuration: once the Gallery contains the character record and a session references its ID, the next scheduled run creates the character folder. Multi-character sessions must explicitly record the complete cast as `settings_json.session.character_ids` (or top-level `settings_json.character_ids`). The legacy singular `generation_sessions.character_id` remains the primary-character fallback. The exporter never guesses cast membership from prompt prose. Explicit multi-character assets go to one stable `Multi-Character` group folder rather than being duplicated into every individual character folder.

## Safe workflow

Always inspect a plan before copying:

```powershell
python tools/drive_media_export.py plan --character-id ch-mizuki-reika --since 2026-09-16
```

Copy the same bounded selection:

```powershell
python tools/drive_media_export.py sync --character-id ch-mizuki-reika --since 2026-09-16
```

Inspect the ledger:

```powershell
python tools/drive_media_export.py status
```

## Automatic incremental sync

The automatic runner uses no LLM and consumes no AI credits. It asks the same exporter for only not-yet-exported Gallery media, copies at most 100 new files per run, and writes execution logs outside Drive:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/run_drive_media_export.ps1
```

Install or refresh a current-user Windows task that runs every 30 minutes while that user is logged in (the streamed `G:` drive is normally available only in that session):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/install_drive_media_export_task.ps1
```

The defaults can be changed with `-IntervalMinutes` and `-MaxItems`. Re-running the installer updates the same `XAI Studio Media Export` task rather than creating duplicates. If `G:` is unavailable, the runner stops without changing the export ledger; Task Scheduler can try again at the next interval.

Use repeated `--asset-id` or `--session-id` flags for a precise pilot. `sync` refuses an unfiltered run unless `--all` is explicit. For `sync --all`, already-exported files do not consume the default 100-new-file batch limit, so repeated scheduled runs continue advancing through a backlog. Existing destinations are never overwritten. Matching existing files are adopted; differing files are reported as conflicts. No command deletes a destination.

Keep the existing raw-library Google Drive backup enabled until the pilot, a bounded backfill, and a manual Drive cloud-status check all succeed. Disabling that backup is an operator action outside this tool.
