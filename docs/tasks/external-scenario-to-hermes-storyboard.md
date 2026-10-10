# External scenario → Hermes storyboard

- **Status:** COMPLETE — Claude review follow-up incorporated
- **Active editor:** Codex
- **Started:** 2026-10-10
- **Direct user objective:** Accept a revisable external scenario, let Hermes restage it without rewriting its story, and store independently revisable storyboards beside the scenario collection.

## Goal

Add a small shared `screenplay-to-storyboard` skill and repository convention that:

- preserves each writer scenario revision verbatim;
- separates story locks from staging proposals;
- creates a traceable Hermes storyboard revision without overwriting its source;
- catches demonstrated legibility, causality, source, continuity, scope and H3 feasibility failures before video rendering;
- hands an approved storyboard to the existing Intent Contract and cutboard workflow.

## Scope

- Shared canonical skill under `XAI-Studio-Private/shared-skills/screenplay-to-storyboard/`.
- Shared-resource registration and public runtime adapter.
- `storyboards/` sibling of `scenarios/`, with revision and source-binding rules.
- Human-readable storyboard template and deterministic metadata validator.
- Focused tests for revision binding; the demonstrated preflight failure categories remain semantic skill/template checks rather than brittle wording tests.
- Hermes routing documentation.

## Constraints / Must Preserve

- Existing files under `scenarios/` are not moved or rewritten.
- Writer source and Hermes revision remain separate artifacts.
- Scenario and storyboard revisions advance independently.
- A storyboard binds the exact scenario path, declared revision and SHA-256.
- Existing `idea-production-request-v1`, Intent Contract, shot-plan, renderer, Gallery and WanGP contracts remain unchanged.
- H3 observations from the 2026-10-09 experiment stay engine-scoped candidate evidence, not universal filmmaking rules.
- Existing untracked character, output and task files are unrelated and must remain untouched.

## Must NOT Do

- Do not render media, spend generation credits, modify character DNA, move legacy scenarios, or push changes.
- Do not silently change event order, causality, knowledge timing, ending, dialogue or prohibited reveals.
- Do not build a UI or a general production orchestrator. A bounded Hermes authoring runner with deterministic file/preflight gates is now in scope by direct user request.

## Contract impact

- **Producer:** an external writer or user supplies a scenario revision under `scenarios/`; Hermes authors a storyboard revision under `storyboards/<scenario-id>/`.
- **Consumers:** Hermes, human reviewers, `storyboard-director`, `video-intent-contract`, `storyboard-cutboard`, and later renderer adapters.
- **Compatibility:** existing flat scenario files are treated as revision 1 unless they explicitly declare another revision. No existing reader or persisted artifact is changed.
- **New binding:** every new storyboard begins with parseable metadata containing its own identity/revision and the exact source scenario path/revision/hash. Parent storyboard metadata is optional for revision 1 and required for later revisions.
- **Deterministic readiness sidecar:** every newly gated storyboard has a `storyboard-preflight-plan-v1` JSON sidecar. It maps exact source event/dialogue/constraint IDs to render units and is the only machine readiness authority; Markdown self-review is advisory.
- **Bounded runner:** `tools/storyboard_pipeline.py` invokes Hermes at most twice, verifies that both output files actually changed, returns only field-level validator failures, and stops on unresolved writer/user decisions. It does not invoke Codex or Claude as a routine final reviewer.
- **Rollback:** remove the new shared skill registration, adapter, `storyboards/` convention, template, validator and focused tests. Existing scenarios and production contracts remain valid.
- **Verification:** shared skill resolution; skill quick validation; metadata validator fixtures; focused unit tests; JSON/catalog syntax; whitespace diff check.

### 2026-10-10 review amendment

- Replace byte-level Markdown hashing with canonical UTF-8 text hashing: strip one UTF-8 BOM and normalize CRLF/CR to LF before SHA-256. Add scoped LF attributes for scenario/storyboard files. There are no persisted screenplay-storyboard bindings yet, so no migration is required; future bindings record this v1 canonical hash rule.
- Add critical-information preview frames, declared partial production range, writer-facing feedback, and post-render source-vs-staging attribution without changing the existing top-level `storyboard / compiler / renderer / edit` vocabulary.
- Extend only the H3 candidate-evidence profile with the observed dialogue and multi-location behavior; do not promote these observations to renderer-neutral rules.

## Plan

1. Define independent scenario/storyboard revision and storage rules.
2. Create the shared skill with renderer-neutral locks, staging, preflight and change-log behavior.
3. Isolate H3-specific observed limits in a conditional reference.
4. Add the runtime adapter, Hermes routing entry and storyboard template.
5. Add a deterministic metadata validator and fixtures covering valid binding, stale hash, missing parent and invalid path cases.
6. Run focused validation and update this record with evidence.
7. Replace frontier final review with a deterministic source catalog, preflight sidecar and bounded Hermes repair loop.

## Progress

- Read governance, shared production roles, current shared storyboard/intent/cutboard/continuity skills, Claude's experiment feedback and the current scenario collection.
- Confirmed Claude feedback commit `7154d46` is present locally.
- Confirmed the working tree contains unrelated untracked files that will be preserved.
- Added the canonical shared `screenplay-to-storyboard` skill with separate storage/revision, renderer-neutral preflight and H3-scoped evidence references.
- Registered the skill in shared authority and added the public runtime adapter and Hermes routing entries.
- Added sibling `storyboards/` storage, an external-screenplay storyboard template, independent scenario/storyboard revision rules and SHA-256 lineage binding.
- Added `screenplay-storyboard-v1` metadata schema and `tools/storyboard_revision.py` for source/parent validation and hashing.
- Added focused tests proving valid revision binding and detecting overwritten source files, overwritten parent storyboards, missing parents and out-of-collection artifacts.
- Added `storyboard_preflight.py`, a machine-readable plan schema and stable source catalog IDs. The gate checks exact event coverage/order, exact dialogue, constraint acknowledgement, declared scope, duration, action density, nested screen/photo handling, direction keyframes, continuation depth and unresolved decisions.
- Added `storyboard_pipeline.py`; it rejects Hermes's false “written” reports when files are absent/unchanged, retries only with validator repair items, stops after two attempts and reserves human input for real source/intent decisions.
- Updated the canonical shared skill and runtime documentation so a prose all-pass table is no longer completion evidence.

## Next

Forward-test the bounded runner on a new normalized scenario. Do not use Codex/Claude as a routine final pass; stop only for user approval, a source contradiction or a two-attempt machine failure report.

## Blockers / uncertainties

- Arbitrary prose without stable scene headings and numbered actions cannot be proven complete deterministically. The runner blocks before Hermes and requests the normalized external-writer format instead of asking a frontier reviewer to infer coverage.

## Verification

- `18 passed` — `test_storyboard_revision.py`, `test_shared_authority.py`, `test_director_skill_router.py` using the established Studio backend Python and `tools` on `PYTHONPATH`.
- Canonical and runtime-adapter skill validation: pass.
- Shared-resource full resolution: pass; `screenplay-to-storyboard` resolves from the Private authority.
- New JSON Schema meta-validation: pass.
- `py_compile tools/storyboard_revision.py`: pass.
- Public and Private `git diff --check`: pass (line-ending warnings only).
- No media generation, character mutation, migration, push or deployment performed.

### Claude review follow-up verification

- Added scoped `.gitattributes` LF policy for `scenarios/**` and `storyboards/**`; `git check-attr` confirms both paths resolve to `text: set`, `eol: lf`.
- Changed binding hashes to canonical UTF-8 text hashes (BOM removed; CRLF/CR normalized to LF) and added a regression proving BOM+CRLF and LF validate as the same content.
- Added critical-information preview frames, declared full/partial/teaser scope, writer-facing feedback and external-writer input template.
- Extended downstream render attribution with `source_scenario` versus `hermes_staging` subtypes while preserving the established top-level defect owner vocabulary.
- Added the two missing H3 observations at the same candidate-evidence level; retained the existing Ref2VA aspect observation.
- `36 passed` — revision, shared authority, director routing and video Intent Contract focused tests.
- Canonical screenplay and video-intent skills plus runtime adapter quick validation: pass.
- Public and Private `git diff --check`: pass (unrelated tracked files still report existing line-ending conversion warnings).

### Deterministic-gate follow-up verification

- Real RW-001 extraction: 12 scenes, 62 ordered source events, 2 dialogue occurrences and 108 must/forbidden constraint items receive stable IDs.
- `14 passed` — storyboard preflight, bounded pipeline and revision tests.
- Skill Creator quick validation of the canonical shared `screenplay-to-storyboard` skill: pass under UTF-8 mode.
- The runner tests prove that a successful Hermes process which writes no files is rejected twice and then stopped, and that unstructured source prose is blocked before any Hermes call.
