# Current task — Integration review and full local commits

Active editor: Codex
Status: COMPLETE — reviewed integration checkpoint
Date: 2026-09-07

## Goal
Review Claude requester/session recording and all pending changes in XAI-studio and personal-prompt-studio; commit the reviewed working trees as explicitly requested by the user.

## Constraints / Must Preserve
Preserve production records, media, existing agent edits and review state. Previous task: docs/task-archive/2026-09-07-shared-instructions-task-snapshot.md.

## Must NOT Do
No push, publication, GPU generation, runtime restart or media deletion. Exclude caches and generated media from Git; keep small test fixtures.

## Plan
Review diffs and provenance producer/reader contracts, correct stale actor instructions and confirmed defects, run Python and Studio checks, inspect staged files and commit both repositories.

## Progress
Claude commits 87ce3a2 and d8366f4 exist. Found stale actor restrictions in shared docs and batch.yaml inheritance parsed as JSON only. Located Studio Python environment with pytest.

## Contract impact
Producers: existing JSON/YAML sessions and CLI submit. Consumers: requester resolver and Control Tower. Preserve old JSON batches; support genuine YAML batches with regression fixture. No required fields or migration. Rollback review fix independently; verify requester tests and existing suites.

## Next
Live tablet playback remains unverified. Restore the missing frontend ESLint configuration in a separate tooling task.

## Review results
- Corrected real YAML batch requester inheritance (including BOM/malformed-file fallback) and obsolete actor restrictions in shared instructions.
- Reviewed Claude commits 87ce3a2/d8366f4, pending importer/Gallery code, production metadata and curation diffs. Preserved historical record values; did not relabel old runs.
- XAI explicit regression selection from docs/verification.md plus tools/test_requester_provenance.py: 131 passed, one environment failure; that fixture subprocess test passed separately after supplying inherited PYTHONPATH. Total 132 selected tests passed across these runs.
- Interpreter: D:/codex/personal-prompt-studio/personal-prompt-studio/backend/.venv/Scripts/python.exe. jsonschema supplied from existing Hermes site-packages (appended after Studio packages); no dependency install. CWD: D:/codex/XAI-studio. Writable pytest base: C:/Users/krcho/Documents/ChatGPT/XAI-Studio/pytest-review-xai-sep7. Follow-up fixture command: python -m pytest tests/test_idea_to_production_fixtures.py -q with inherited PYTHONPATH.
- Studio: backend tests 24 passed; frontend npm test 495 passed; npm run build passed after fixing optional media-type union narrowing. npm run lint blocked because repository has no eslint.config.* (pre-existing configuration gap).
- Pending JSON syntax: 183 XAI records and 3 Studio curation files valid. Generated output media and pytest caches excluded; small media test fixtures retained. Git diff whitespace check passed.
- No live GPU render, live tablet playback, deployment or push performed. Existing running services were not restarted.
