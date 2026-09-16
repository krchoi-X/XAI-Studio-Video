# Noa historical record archive discovery
Active editor: Codex / Astra; bounded implementation completed by Terra.
Goal: read copied historical records beside shared originals without relying on the source checkout.
Scope: record_archives.py, shared_resources.py, tests/test_record_archives.py, this task; named Studio wrapper/API/tests/scoped task. Contract: Private NOA_RECORD_ARCHIVE_CONTRACT.md, read committed checkpoint.
Constraints: old files/IDs/encoded text/reviews unchanged; no live copy, backup, render, Sync, DB writes, restart or public commit by executor. Preserve staged prior changes.
Contract impact: new record-archive.json is a historical snapshot marker, never batch.yaml; exact listed source paths resolve to verified copied bytes; Gallery import behavior unchanged; old source may be absent. Rollback leaves copies and originals in place.
Plan: lightweight sibling-CM resolver; confinement/marker validation; read-only CLI/API; synthetic source-absent/tamper/duplicate/API no-write checks.
Progress: schema-2 nested historical snapshots implemented under the Private LEGACY_HISTORY_ARCHIVE_CONTRACT.md checkpoint dfed35b. Both schema versions preserve source-absent reads; schema-2 explicit null outputs remain unlinked. Nested raw batch.yaml is outside importer discovery. Fixtures cover multiple snapshots, invalid nesting/paths/hashes, partial invisibility and exact legacy import/review identity preservation. Integration owner runs final checks and copy/recovery gates; actual status is in Private legacy-history/ACCEPTANCE.md.
Next: add the contracted schema-2 null-output `recorded_artifacts` reader only. Preserve schema-1 and linked/null empty rows; validate archived run JSON and provide explicit artifact resolution without listing hashes. Synthetic fixtures and the existing Studio route must remain read-only. No live archive, source, database, Sync, process, or media work.

## Output association reader (2026-09-15)

Active editor: Codex / Terra. Scope: `tools/record_archives.py`,
`tests/test_record_archives.py`, this note, and the named Studio archive test/task
append. Contract impact: immutable schema-2 archive markers are unchanged; only null
`outputs_root` archive rows gain additive `recorded_artifacts` metadata. Consumers retain
the existing CLI/API route. The archive resolver validates listed run records first;
listing reports availability without hashing media and explicit resolution hashes only
the chosen, allowed byte target. Old schema-1/linked rows and historical null outputs
remain compatible. Rollback removes the additive field/resolver only.

Plan: record scope, implement strict archived-run parsing and safe target resolution,
add source-absent/tamper/blocked/missing/repeated-path/indexed fixtures and Studio
no-write/409 coverage, then run focused suites. Progress: implementation complete for
review. Schema-2 null-output rows derive records only from marker-listed,
hash-verified `runs/<id>/run.json`; listing never hashes media and reports
`integrity: not_checked`. Source-root paths use archived copies, same-character Library
targets are contained and size-checked, and unsafe/cross-character paths remain blocked.
The explicit resolver re-verifies the selected bytes and requires a checksum. Existing
schema-1 and linked schema-2 shapes remain unchanged.

Verification: focused XAI archive tests passed 28 with 2 expected link-capability
skips; Studio archive tests passed 4 using the pinned backend environment and copied
runtime helper. These include source-absent archived resolution, same-size altered-byte
resolver rejection, cross-character block, tampered archived run rejection, an indexed
resolver guard, and existing route no-write coverage. No live state or historical source
was read or changed beyond synthetic fixtures.

Next: Astra review and its separate bounded audit/commit gates. Risks: listing asserts
metadata/location only; actual content verification intentionally occurs solely through
`resolve_artifact_path`.
