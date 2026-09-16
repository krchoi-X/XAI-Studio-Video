# Shared resource authority transition

Active editor: Codex / Astra (integration and runtime); Studio assigned to Terra separately.
Status: shared authority active; exact local code patch checkpoint stored privately.
Date: 2026-09-14

## Goal
Read and author character records and reusable skill sources outside the application checkout through the configured shared workspace. Keep session/media roots intact.

## Constraints / Must Preserve
Stable IDs, all existing JSON values/unknown fields, exact prior bytes, DNA approval guard, review/reference decisions and runtime provenance. Preserve unrelated generated work. No live creative edits.

## Must NOT Do
No deletion, GPU jobs, service restart, DB Sync, push or publication. No silent fallback from a broken active shared authority.

## Scope and plan
Complete character_manager resolver/index/history, character_scene, local_wangp, face_discovery, dna_proposal_worker, hermes_night_batch, character_sheet, idea_production_worker; add a shared-resource resolver CLI and synthetic boundary fixtures. Replace three project skill definitions with shared-source adapters; preserve reference copies as legacy documented snapshots. Application executable dependencies remain local. Private contract: SHARED_AUTHORITY_CONTRACT.md at 870427b.

## Contract impact
Producers: existing promote/refresh; consumers: named runtime readers plus Studio. Active catalog resolves shared records independently of runtime sessions. Legacy unconfigured readers remain supported; malformed active authority fails closed. Shared writes save content-addressed prior versions and shared index only. Rollback before new authoring restores verified prior pointers; after new authoring reconciliation is mandatory. Verify synthetic writer/history/guards, old and active configs, path confinement, missing authority, preserved session paths, and actual read-only two-project resolution.

## Progress
2026-09-14: 12 records and three shared skill definitions activated after text restore/freshness checks. XAI 42 boundary/character/scene/night/default-reference tests plus 20 idea/provenance fixtures passed. Real XAI and Studio code consumers read identical shared paths/versions/hashes. Prior record/derived bytes and shared index/reference projections are preserved by the writer. No live authoring/generation or service restart. Publication gate fails inherited content plus generic resolver path/synthetic fixture checks, so this repository is staged but not committed/pushed; exact diff/base/hash is preserved in Private stage-3 evidence. Do not discard staged changes.

Initial reader split exists; review found index still wrote runtime and refresh lacked history. Completing these before activation. Backup preservation is tracked privately; no production records changed by tests.

## Next
Transition creation/run records and curated sets in a separate bounded contract; verify running service adoption before claiming live-service cutover. For legacy fixture runs, set XAI_WORKSPACE_FILE to an isolated existing Stage 1 locator without an active catalog; new active tests override it with synthetic catalogs. Never run fixture authoring against real shared records.

## Blockers
None for implementation. Existing publication baseline needs scoped review; no publication authorized.
