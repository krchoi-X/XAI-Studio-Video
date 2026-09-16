# Scoped task — historical artifact bundle readers

Active editor: Codex / Terra

Goal: provide read-only discovery and verified source-path resolution for final shared
standalone-run and report archive markers, plus an additive Studio listing route.

Constraints / Must Preserve: markers are immutable snapshot records; absent original
sources remain resolvable from the snapshot; no Gallery/database/importer/frontend,
copy, backup, Sync, generation, restart, or runtime activation work.  Existing staged
work and original source material stay untouched.

Must NOT Do: elect a latest bundle, accept partial folders, mutate a marker or bundled
file, create database rows, or inspect/live-process archived media.

Contract impact: Astra's archive copier publishes schema-1 `archive-bundle.json` last.
Consumers are `tools/artifact_bundles.py`, `tools/shared_resources.py --record-bundles`,
and Studio `GET /api/record-bundles`.  Old state without a marker remains invisible;
rollback removes only the readers/routes and retains snapshots.  Validation rejects
unsafe links/junctions, invalid paths/types/roles/IDs, duplicate normalized target or
source identities, missing members, and tampering on explicit resolution.  Deterministic
fixtures cover source absence, multiple snapshots, partial markers, malformed members,
tampering, a Windows junction, and an API no-write/409 boundary.

Expected scope: `tools/artifact_bundles.py`, `tools/shared_resources.py`,
`tests/test_artifact_bundles.py`, this task note; Studio `backend/app/character_authority.py`,
`backend/app/main.py`, `backend/tests/test_artifact_bundles.py`, and its append-only task note.

Plan: harden the scaffolded marker reader; add focused XAI and Studio fixtures; run the
two focused suites with the supplied Studio interpreter and pinned import paths; inspect
the diff and freeze the bounded result for integration.

Progress: complete and frozen for integration. The reader validates final schema-1
markers, exact `records/<bundle>/<snapshot>` nesting, canonical targets/sources,
case-insensitive duplicate identities, root marker/pending-marker reservations, missing
members and link/junction ancestors. Explicit resolution verifies byte count and SHA-256;
discovery intentionally does not hash members. Studio exposes the additive read-only
route and maps invalid authority to 409.

Verification: with the supplied Studio `.venv` and XAI `tools` on `PYTHONPATH`,
`pytest tests/test_artifact_bundles.py -q --basetemp .pytest_tmp/artifact-bundles-xai-final`
passed 13 tests, including an actual Windows junction fixture. From Studio `backend/`
with its own checkout first on `PYTHONPATH`, `pytest tests/test_artifact_bundles.py -q
--basetemp .pytest_tmp/artifact-bundles-studio-final` passed 2 tests; the import probe
resolved the intended Studio checkout's `backend/app/main.py`.
Both repository `git diff --check` runs passed. No live archive/source data, DB, Sync,
copy, generation or runtime process was touched.

Next: Astra may use this bounded reader patch for its separate archive-copy and
integration/adoption gates.
