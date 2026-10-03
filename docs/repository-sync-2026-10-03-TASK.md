# Repository reconciliation and remote synchronization

- Date: 2026-10-03
- Active editor: Codex
- Status: ACTIVE

## Goal

Merge the upstream Muse failure-history work, reconstruct and verify the remaining documented local work, commit only reviewable public-repository changes in coherent packages, and synchronize local `main` with `origin/main`.

## Scope

- Upstream commits currently in `origin/main` but absent from local `main`.
- Tracked and source/document/test files named by existing task records in this repository.
- A final public-repository staged-content check before push.
- This task record.

## Constraints / Must Preserve

- Preserve all production outputs, failed runs, temporary review material, and existing uncommitted work; no deletion or destructive cleanup.
- Keep active-editor attribution and existing task histories intact.
- Treat the public repository boundary as strict: do not commit generated media, runtime state, private character material, local paths containing private data, secrets, or unreviewed bulk artifacts.
- Use existing task records and deterministic tests to reconstruct ownership and completion state.
- Keep commits separated by coherent subsystem where practical.

## Must NOT Do

- No media generation, GPU execution, service restart, Gallery mutation, character promotion, schema widening beyond existing changes, history rewrite, force push, or deletion.
- Do not claim the whole working tree is clean when retained production artifacts remain intentionally untracked.
- Do not publish any staged content until `check-public --staged` passes and the diff is reviewed.

## Plan

1. Merge `origin/main` without discarding the local vlog commit or dirty work.
2. Inventory every tracked modification and source-like untracked file against its owning task record.
3. Verify each coherent package with the narrowest deterministic checks, then broader relevant regression checks.
4. Commit verified public-safe packages; retain generated/runtime artifacts outside Git.
5. Run staged public checks, push local commits, fetch again, and confirm local/remote commit identity.

## Contract impact

This coordination task introduces no contract by itself. Contract impacts remain documented in the existing subsystem task records and must be reviewed before their changes are committed.

## Progress

- Governance initialized; repository classified public and dirty.
- Fetched `origin/main`: seven upstream documentation commits found, including `docs/failure-db.md` with 20 production failure cases and six revisions to the Rooftop 5AM scenario.
- Local `main` is one commit ahead and seven commits behind before reconciliation.

## Verification

Pending per package. Final gates: relevant tests, `git diff --check`, public staged-content validation, push, fetch, and zero ahead/behind.

## Rollback

Each new local package will be a separate commit. Revert the affected commit; do not rewrite shared history or delete production evidence.

## Next

Merge upstream, then classify and verify local packages.
