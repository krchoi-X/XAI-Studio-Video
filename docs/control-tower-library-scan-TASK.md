# Control Tower — shared Library run discovery

Active editor: Codex
Status: COMPLETE
Date: 2026-09-18

## Goal

Show current WanGP runs written under `D:\AI_Studio\library\characters` in Control Tower Recent Results.

## Constraints / Must Preserve

- Control Tower remains read-only.
- Preserve legacy repository scan roots and existing job IDs.
- Prefer the current shared Library record when the same run also exists in a legacy repository snapshot.
- Do not surface archived `historical-records` copies as live duplicate jobs.

## Must NOT Do

- Do not alter generated media, Gallery state, run manifests, or the night-batch queue.
- Do not change generation or storage producers.
- Do not refactor unrelated Control Tower behavior.

## Plan

1. Add the shared character Library to the default WanGP scan roots.
2. Exclude archival `historical-records` trees and deduplicate discovered jobs by canonical `job_id`.
3. Cover the new root and duplicate behavior with focused tests.
4. Restart the local read-only service and verify today's runs appear in `/api/overview` Recent Results.

## Contract impact

- Producer: existing WanGP run records in repository and shared Library session trees; unchanged.
- Consumer: Control Tower `WangpRunAdapter` and Recent Results view.
- Compatibility: old repository-only records remain visible. When identical `run_id` records exist in both locations, the shared Library copy wins by scan-root order.
- Rollback: remove the Library default root and deduplication/exclusion changes.
- Verification: focused Control Tower adapter/API tests, health endpoint, and live overview containing 2026-09-18 Library runs without duplicate job IDs.

## Progress

- Diagnosed: night batch is visible through the batch adapter, but individual runs are absent because the default WanGP roots exclude the shared Library.
- Diagnosed: adding the Library naively would duplicate many migrated and archived records.
- Added the shared Library as the first default scan root, excluded `historical-records`, and deduplicated by canonical `job_id` with first-root precedence.
- Extended character inference to recognize both legacy `02_generations` and current `generations` session layouts.
- Updated the operating documentation and restarted the read-only service.

## Next

- No implementation work remains. Refresh an already-open dashboard if its SSE connection did not reconnect automatically.

## Verification

- Interpreter: Hermes Python 3.11 from `PATH`; CWD `D:\codex\XAI-studio`.
- `python -X utf8 -m unittest discover -s tests -p "test_control_tower*.py"`: 55 passed.
- Live `/api/health`: `ok=true`, `monitor_alive=true`, `adapter_errors={}`, 536 jobs.
- Live `/api/overview`: all 10 runs from `NIGHT-20260918-052335-375a0c` occupy the newest Recent Results slots, each exposes two outputs and links to the night-batch parent.
- Live `/api/jobs`: zero duplicate `job_id` values.
