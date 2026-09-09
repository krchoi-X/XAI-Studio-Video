# Current task — Automatic character reference resolution for WanGP video

Active editor: Codex
Status: COMPLETE — default reference resolution committed
Date: 2026-09-10

## Goal
Make a Ref2VA video submission resolve the character's durable default identity reference automatically, so Hermes and other agents do not need to repeat an absolute image path and do not lose it with conversation context.

## Constraints / Must Preserve
Preserve explicit `image_refs` unchanged. Do not mark an image approved without a human review decision. Existing sessions and settings continue to work; no GPU job is launched for verification.

## Must NOT Do
No media deletion, automatic reference selection from arbitrary newest files, GPU generation, runtime restart, push, or publication.

## Plan
Add an explicit default-reference record for Jun based on the known base close-up; resolve it for Ref2VA only when settings supply no references; persist evidence in the run record; add deterministic tests and update Hermes instructions.

## Progress
Confirmed the latest corrected Hermes run uses valid H3 resolution/frame fields but has `image_refs: []`, producing WanGP's "You must provide at least one Reference Image" validation failure. The Jun close-up import provenance identifies `jun-closeup-01.png` as the base image for the four dependent portraits.

## Contract impact
Producer: `character.json` optional `reference_defaults.identity` record containing a path and provenance. Consumer: `tools/local_wangp.py submit` for `*_ref2va*` models. Explicit `image_refs` override it; no default remains a clear pre-launch error. Old character records stay valid. Rollback removes the optional record and resolver. Verify with a fake WanGP worker plus a missing-reference test.

## Next
Hermes may submit the corrected Jun shot with empty `image_refs`; inspect the new run record for `reference_inputs[0].basis: character-default` before expanding the batch. Add durable defaults for other characters only when a user-selected base reference is known.

## Verification
- `tools/test_local_wangp.py`: 8 passed, including default injection, explicit-reference override and missing-default rejection.
- `tools/test_requester_provenance.py`: 17 passed.
- WanGP Python compiled the changed modules. A direct non-GPU resolution against the real Jun correction session injected `jun-closeup-01.png` and verified its recorded SHA-256.
- No GPU worker, runtime restart, media modification or external request was performed.

## Review results
- Corrected real YAML batch requester inheritance (including BOM/malformed-file fallback) and obsolete actor restrictions in shared instructions.
- Reviewed Claude commits 87ce3a2/d8366f4, pending importer/Gallery code, production metadata and curation diffs. Preserved historical record values; did not relabel old runs.
- XAI explicit regression selection from docs/verification.md plus tools/test_requester_provenance.py: 131 passed, one environment failure; that fixture subprocess test passed separately after supplying inherited PYTHONPATH. Total 132 selected tests passed across these runs.
- Interpreter: D:/codex/personal-prompt-studio/personal-prompt-studio/backend/.venv/Scripts/python.exe. jsonschema supplied from existing Hermes site-packages (appended after Studio packages); no dependency install. CWD: D:/codex/XAI-studio. Writable pytest base: C:/Users/krcho/Documents/ChatGPT/XAI-Studio/pytest-review-xai-sep7. Follow-up fixture command: python -m pytest tests/test_idea_to_production_fixtures.py -q with inherited PYTHONPATH.
- Studio: backend tests 24 passed; frontend npm test 495 passed; npm run build passed after fixing optional media-type union narrowing. npm run lint blocked because repository has no eslint.config.* (pre-existing configuration gap).
- Pending JSON syntax: 183 XAI records and 3 Studio curation files valid. Generated output media and pytest caches excluded; small media test fixtures retained. Git diff whitespace check passed.
- No live GPU render, live tablet playback, deployment or push performed. Existing running services were not restarted.
