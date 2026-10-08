# Gallery Character Compiler — isolated worktree checkpoint

Recorded: 2026-10-07

Purpose: preserve the exact pre-task repository state and isolate contract work. No stash, reset, clean, media move or overwrite was performed.

## Original XAI worktree

- Path: `D:/codex/XAI-studio`
- Base: `2791df509c23aae2de5ddc177ea1f161d7cd0c67`
- Branch at capture: `main`, ahead of `origin/main`; remote-behind count was zero after the earlier merge.
- Modified and left untouched:
  - `TASK.md`
  - `tests/test_hermes_night_batch.py`
  - `tools/character_manager.py`
  - `tools/hermes_night_batch.py`
- Untracked and left untouched:
  - `_ct_q.py`
  - `characters/ch-hana/`
  - `docs/TASK-20261006-jjigae-v4v5-char2-hermes.md`
  - `docs/continuous-production-batch-TASK.md`
  - `docs/experiments-jjigae-v4v5-and-char2-hermes-20261006.md`
  - `docs/reference-review/2026-10-04-55hawks-facetime-cockroach.md`
  - `docs/storyboard-reika-onsen-maple.md`
  - `output/hana-gpt-closeups-20261004/`
  - `output/hana-gpt-swimwear-fullbody-20261004/`
  - `output/hana-xpade-closeup03-20261004/`
  - `output/reika-continuous-production-20261005.json`
- Isolated branch: `codex/gallery-character-compiler-contract-xai`
- Isolated base: the same `2791df5` commit; uncommitted original files were deliberately not copied.

## Original Studio worktree

- Repository root: `D:/codex/personal-prompt-studio`
- Base: `500384f0e67d3db5ae9ced9c8c30ec9a792f2654`
- Branch at capture: `master`, ahead of `origin/master`.
- Modified and left untouched:
  - `personal-prompt-studio/DESIGN.md`
  - `personal-prompt-studio/backend/app/database.py`
  - `personal-prompt-studio/backend/app/importer.py`
  - `personal-prompt-studio/backend/app/main.py`
  - `personal-prompt-studio/backend/app/schemas.py`
  - `personal-prompt-studio/backend/tests/test_api.py`
  - `personal-prompt-studio/backend/tests/test_identity_reference.py`
  - `personal-prompt-studio/backend/tests/test_sync_jobs.py`
  - `personal-prompt-studio/docs/studio-performance-pagination-TASK.md`
  - `personal-prompt-studio/frontend/src/App.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/BatchPanel.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/JobCard.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/JobsPanel.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/ProductionApp.test.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/ProductionApp.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/handlers.ts`
  - `personal-prompt-studio/frontend/src/apps/production/interactions.test.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/model.test.tsx`
  - `personal-prompt-studio/frontend/src/apps/production/model.ts`
  - `personal-prompt-studio/frontend/src/shared/api.ts`
  - `personal-prompt-studio/frontend/src/shared/production.ts`
  - `personal-prompt-studio/frontend/src/shared/types.ts`
- Untracked and left untouched:
  - `personal-prompt-studio/backend/tests/test_continuous_batch.py`
  - `personal-prompt-studio/backend/tests/test_incremental_reconciliation.py`
  - `personal-prompt-studio/docs/native-face-sculptor-TASK.md`
- Isolated branch: `codex/gallery-character-compiler-contract`
- Isolated base: the same `500384f` commit; uncommitted original files were deliberately not copied.

## Shared authority

- Repository: `D:/codex/XAI-Studio-Private`
- Base: `bdb30a7a81ebcc3c14bc0ca8e0dc398754b7ddd8`
- Status at capture: clean `main`, aligned with `origin/main`.
- No canonical character, shared skill or policy file was changed by steps 1-2.

## Contract checkpoints created from the isolated bases

- XAI: `618df72` — additive schemas, Master Face writer, fixtures and tests.
- Studio: `4799184` — pure presentation contract/fixture/test; `f607c91` records completion evidence.

These checkpoints are not merged into the original dirty worktrees and are not pushed. Downstream work must inspect their diffs and use the isolated branches or an explicit later integration operation.
