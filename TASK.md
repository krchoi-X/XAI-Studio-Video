# Current Task

Status: COMPLETE — every registered character is production-ready and visible to web batch creation.

## Goal

Register the newly synchronized Aoi DNA as a canonical Character Manager record so the web app's existing repository-driven character list includes her in immediate and night-batch production.

## Constraints / Must Preserve

- `characters/<id>/character.json` remains the production identity source of truth.
- Keep Aoi at candidate status; only human review may approve her or a visual reference.
- Keep outfits, activities, locations, and expressions in scene defaults or source notes rather than Stable DNA where appropriate.
- Existing Lia, Jung Hae-won, and Harim records and generated sessions remain untouched.

## Must NOT Do

- Do not expose draft-only characters as production-ready.
- Do not promote unrelated characters from the knowledge repository without an approved production DNA record.
- Do not generate images or start a batch.

## Plan

1. Normalize the synchronized private Aoi DNA into a schema-v1 draft.
2. Promote it through `tools/character_manager.py` and rebuild `characters/index.json`.
3. Validate all canonical character records and verify the Studio importer/UI path remains data-driven.

## Progress

- [x] Confirm the web app already lists every imported character with a non-null DNA version.
- [x] Confirm only Lia, Jung Hae-won, and Harim currently have canonical production records.
- [x] Register and validate Aoi.
- [x] Migrate the four remaining user-authored visual profiles: Yuna, Oh Ji-an, Lee Suan, and Han Seorin.
- [x] Verify importer and frontend production tests.
- [x] Synchronize the running Studio and confirm all eight API records have a non-null version.

## Next

Use the web app normally; refresh the Production page if it was already open before repository sync.

## Contract Impact

- Producer: Character Manager canonical registry and index.
- Consumers: Studio repository importer, `/api/characters`, Gallery, immediate production, and night-batch character selectors.
- Existing records: additive only; existing character IDs and database rows remain unchanged.
- Compatibility: the existing importer discovers `characters/ch-*/character.json`; no API or persisted schema change is required.
- Rollback: remove the additive Aoi candidate record and rebuild the index before it accumulates production sessions.
- Verification: Character Manager validation, importer API test, frontend production model/component tests.

## Blockers / Uncertainties

- Aoi's nationality, exact design specialty, and signature earring design remain intentionally unresolved in the source DNA.
- The four migrated legacy profiles intentionally preserve unresolved biography and exact-age fields.

## Verification

- `python tools/character_manager.py validate`: 8 canonical records passed.
- Studio `POST /api/sync`: 8 characters, 49 sessions, 517 existing assets skipped idempotently.
- Studio `GET /api/characters`: all 8 records report a non-null DNA version.
- Backend night-batch test: 1 passed.
- Frontend production tests: 86 passed across model, component, and interaction suites.
