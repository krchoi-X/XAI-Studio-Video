# Productions view and Drive backup (character-independent content)

- Date opened: 2026-10-02
- Active editor: Codex for the 2026-10-03 hardening follow-up; Claude Code authored the completed implementation
- Status: COMPLETE — implementation and 2026-10-03 hardening are live and verified
- Relates to: [hermes-autonomous-pipeline-TASK.md](hermes-autonomous-pipeline-TASK.md) (the Rooftop 5AM test is the first content)

## Why

Studio's Gallery is keyed by character: the importer requires a registered `character_id` for every session. The
Rooftop 5AM production has no roster character, so it is invisible in Studio. The user asked for a read-only
"Productions" view for character-independent content (2026-10-02) and for those productions to be included in the
Google Drive backup that Codex built.

## Decisions (made by Claude within the user's request; the user may veto)

1. **Host: a new `/productions` page in Control Tower**, not a new Studio route. Control Tower is already a
   read-only tablet app on the tailnet (port 8790, autostart) that serves job outputs, and it is in Claude's
   scope. A Studio navigation destination or Gallery support for character-less sessions touches Studio's
   integration-owned router, API and importer, which belong to Codex. Folding this into Studio later is a
   separate Codex checkpoint; the read model below is reusable for it.
2. **Source of truth: the existing library session folders** under `D:\AI_Studio\library\videos\<session>` that have a
   `session-provenance.json`. No new store, no database, no copy of media.
3. **Drive backup: a separate exporter** (`tools/productions_drive_export.py`), not an edit of
   `tools/drive_media_export.py`. That file has uncommitted Codex changes and reads only the Gallery catalog, which
   cannot hold these productions. The new exporter reuses the same safety rules (never overwrite or delete, hash
   verification, ledger outside Drive) and is invoked as an additional, failure-isolated step by the existing runner
   `tools/run_drive_media_export.ps1`, so it rides the existing scheduled task.
4. **Backed-up set per production** (`G:\내 드라이브\XAI-Studio Media\Productions\<title [session-id]>\`):
   - `Videos\` final video, shot clips, experiment videos (outputs excluding `raw\` duplicates and `norm-*`
     intermediates);
   - `Images\` identity/reference stills under `refs\` (the chosen reference, not every candidate);
   - `Record\` small text needed to reproduce it: `session-provenance.json`, `shot-*.txt`, `*.settings.json`,
     driver and brief files. This extends the existing exporter's "media only" policy for productions only,
     because these files are tiny and make a video reproducible.

## Constraints / Must Preserve

- Read-only: the view and the scanner never write into the library, Gallery database, characters or night-batch
  directories. Existing Control Tower endpoints, config and the job database stay unchanged.
- Media is served only from inside a discovered production folder (no path traversal, symlink escape or absolute
  path from the request).
- Never overwrite or delete a Drive destination; adopt identical files; report conflicts. Ledger and logs live outside
  Drive at `D:\AI_Studio\workspace\productions-drive-export`.
- A successful filesystem copy is not proof that the cloud upload finished (same caveat as the existing exporter).
- The existing media exporter and its ledger are untouched; a failure of the new step must not fail the old one.

## Must NOT Do

- No Gallery database writes, no Studio frontend/backend changes, no Character DNA edits, no GPU work.
- No new scheduled task, tailnet publication or other system setting; the runner hook reuses the existing task.
- No edit of `tools/drive_media_export.py`, `tests/test_drive_media_export.py` or `docs/drive-media-export-TASK.md`
  (Codex working-tree changes).
- No review, approval or visibility controls in this version; it is a viewer.

## Contract impact

- New producer/consumer pair, both new: `control_tower/productions.py` (read model) is consumed by new routes in
  `control_tower/app.py`, the new page `control_tower/static/productions.html`, and `tools/productions_drive_export.py`.
- Existing persisted records: `session-provenance.json` (written by `wangp_recorder.py session`, unchanged,
  fields read-only: `session_id`, `title`, `requested_by`, `status`, `character_id`, `source_idea`,
  `user_request_verbatim`, `engine`, `model`, timestamps). A representative old-style session without optional
  fields must still list.
- Edited shared file: `tools/run_drive_media_export.ps1` (Codex-owned, clean in Git) gains one extra isolated call after
  the existing sync. Consumers: the existing scheduled task. Rollback: delete that block.
- Compatibility: additive routes only. Rollback: remove the new files and the one runner block; no data migration.

## Plan

1. Read model `control_tower/productions.py` plus tests (fixtures for new-style, minimal and malformed sessions,
   path-guard cases).
2. Routes in `control_tower/app.py` and the page `static/productions.html` (list, detail, inline video playback,
   tablet-first layout); link from the dashboard header.
3. Exporter `tools/productions_drive_export.py` plus tests (plan, copy, idempotence, conflict, no-delete); pilot
   copy of the Rooftop 5AM production; then the runner hook.
4. Restart Control Tower (its supervisor relaunches it) and verify live; report limits.

## Verification

Deterministic first: unit tests for the scanner, path guard, API and exporter; `git diff --check`; the live endpoints
on loopback; a pilot export compared by SHA-256 to the sources; a second export run must plan zero copies.

## Rollback

Remove the new files; delete the runner hook block; restart Control Tower. Drive copies already made remain valid
ledger-managed files and are never deleted by tooling.

## Progress

- 2026-10-02: Task opened; architecture decided after reading Studio (Gallery requires a character), the existing
  exporter (reads only the Gallery catalog; has an `Unassigned` bucket but nothing can register these assets) and
  Control Tower (read-only, serves job outputs).

- 2026-10-02: Done. `control_tower/productions.py` (read model + path guard), routes and `static/productions.html`,
  a header link on the dashboard, `Config.productions_root` (+`XAI_CT_PRODUCTIONS_ROOT`),
  `tools/productions_drive_export.py`, and one isolated block in `tools/run_drive_media_export.ps1`.
- Verification: `tests/test_control_tower_productions.py` (10, one skipped: symlinks not permitted here) and
  `tests/test_productions_drive_export.py` (11) pass; all `test_control_tower_*` pass (65, one skipped). Removing the
  path guard made two tests fail, so they are load-bearing. Live after a Control Tower restart: list, detail, video
  200 + byte-range 206, path traversal and the raw duplicate 404, existing `/api/overview` unchanged; the page
  renders the Rooftop 5AM production with the final video and six clips.
- Drive: pilot copied 50 files for Rooftop 5AM, all SHA-256 equal to the sources, a second plan is all `skip`.
  The existing runner was run once with `-MaxItems 1`; the media export completed and the productions step ran
  in the same invocation (0 pending). The productions log is written next to the media export logs as
  `productions-*.log` (UTF-16 as `Tee-Object` writes it under Windows PowerShell 5.1, like the existing logs).
- Defect found by the live check, not by the tests: a `` escape in the default root had turned it into a vertical
  tab. Fixed, and a config test now pins the default path.

## Known limits

- Viewer only: no approve/hold/reject. Not inside Studio's Gallery or navigation; that is a Codex integration step.
- Google Drive cloud-upload completion is not asserted. Files modified in the last 120 s are skipped until they settle.
- Tailnet reachability of this page follows Control Tower's existing publication; nothing new was published.

## Next

Open follow-ups for the user/Codex: fold productions into Studio (character-less sessions), and a decision whether
the `Productions` Drive folder should later move under the Gallery-driven exporter's tree.

## 2026-10-03 Codex hardening follow-up

User-authorized scope:

- reject symlinked files and any resolved path outside a production before listing or backup;
- freeze one Drive destination folder per session, including backward-compatible inference from the existing v1
  file ledger so a later title edit cannot split one production across folders;
- keep the original media export operationally independent, but return a non-zero scheduled-task result when the
  additional Productions export fails instead of leaving only a warning in a log; persist the last outcome and show
  it on the Productions page;
- add focused regression tests and re-run the live read-only checks. No media movement, deletion, upload, render,
  Gallery/Studio change, or scheduled-task reinstallation.

Contract impact: the Productions ledger gains an optional `sessions` map while remaining able to read the existing
`schema_version: 1` file-only ledger. Existing Drive files and file ledger keys are preserved. The runner continues
the old media export before the Productions step; a Productions failure changes only the wrapper exit status after
the old export has finished. `last-run.json` is a new replaceable status snapshot consumed read-only by Control Tower;
it contains no media or credentials. Rollback restores the implementation files and their tests; existing backup
copies remain untouched.

Hardening result:

- linked files and resolved paths outside the session are excluded before UI classification and backup manifest
  creation; the existing request-time containment check remains in place;
- the v2 ledger freezes one destination folder for each of the seven existing sessions. The live v1 ledger was
  inferred without copies or moves and now records 7 sessions / 176 files; all 176 destinations remain present;
- a Productions failure no longer leaves the scheduled task green: the old media export completes first, then the
  wrapper exits 2. Every Productions run atomically records `last-run.json`, and the read-only page/API displays its
  latest success or failure;
- focused tests: 23 passed, 1 skipped because this Windows host does not permit creating the symlink fixture;
  PowerShell parse and `git diff --check` passed (line-ending notices only);
- live after supervised restart: health and `/productions` 200, 7 productions, video range request 206. The
  2026-10-03 11:40 scheduled run returned 0 and the page reported backup `ok: true` at 11:40:58.
