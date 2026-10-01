# Public remote synchronization

Active editor: Codex
Status: ready to publish
Date: 2026-10-01

## Goal

Publish the already-created local merge of `origin/main` only after removing the 17 publication-policy findings introduced relative to the remote baseline.

## Constraints / Must Preserve

- Preserve the merge commit and all unrelated committed behavior.
- Preserve the 19 tracked and all untracked working-tree changes without staging them.
- Limit edits to the eight newly flagged files and this task record.
- Compare the staged result against the current `origin/main` policy baseline before pushing.

## Must NOT Do

- Do not alter the publication policy or suppress findings.
- Do not clean, stash, commit, or delete unrelated working-tree files or production artifacts.
- Do not rewrite published history or force-push.

## Plan

1. Locate each newly introduced match and replace private identifiers or machine-specific paths with public-safe placeholders.
2. Stage only the scoped files and confirm the staged tree adds no findings relative to `origin/main`.
3. Commit the sanitization, push `main`, fetch, and verify local/remote convergence.

## Contract impact

Documentation examples and test fixtures retain their public interfaces while using portable placeholders. No runtime schema, API, persisted record, or production storage contract changes.

## Progress

The remote was merged locally without conflicts as commit `d181d89`. Baseline comparison found 17 new publication-policy findings across eight files. Machine-specific paths now use portable root variables; private character, asset, repository and identity-field examples use public-safe placeholders. Direct matching against every configured publication pattern finds no scoped matches. The full staged tree has 3,158 findings, equal to the existing `origin/main` baseline, with one additional scanned task file. `tests/test_hermes_night_batch.py` passes: 15 tests.

## Next

Commit the nine scoped files, push `main`, fetch, and verify convergence.
