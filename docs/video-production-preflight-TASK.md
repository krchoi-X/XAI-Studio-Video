# Scoped task — Character-video production preflight v2

Active editor: Codex
Status: COMPLETE
Date: 2026-09-30

## Goal

Implement the seven accepted corrections from the Lia/Reika/Suan production review so future Grok/Hermes character-video sessions can fail before GPU submission when their DNA snapshot, mandatory identity anchors, reference laterality/composition, pack-specific state or continuity handoff is incomplete.

## Scope

- New versioned shot-production plan schema and fixture.
- `tools/shot_production_plan.py` validation/compilation.
- `tools/local_wangp.py` pre-submit contract enforcement and run snapshot.
- `tools/wangp_recorder.py` session link to an approved production plan.
- Focused tests for the plan, local submit and requester/session provenance.
- WanGP/Grok/Hermes/playbook documentation.
- Track the existing 2026-09-30 know-how and incident documents; submit structured shared-skill feedback after the affected source is resolved.

## Constraints / Must Preserve

- Existing schema-1 plans and sessions remain readable and runnable.
- Existing explicit `image_refs` remain authoritative for legacy sessions.
- Character DNA, approval state, historical prompts/settings, outputs and run IDs remain unchanged.
- No actual GPU job is needed for verification.
- Current user GO gates remain mandatory for a sample, remake, multi-pack or night run.

## Must NOT Do

- No media generation, deletion, movement or overwrite.
- No Stable DNA edit, reference approval, shared-skill source edit, deployment, push or publication.
- No automatic visual claim: laterality/composition require a named human verification record; code validates the declaration, file/hash and dimensions, not semantic pixels.
- No unrelated refactor or changes to another active scope.

## Plan

1. Add a backward-compatible schema v2 for character contracts and execution-ready reference metadata.
2. Extend deterministic plan validation for DNA hashes, prompt anchors, anatomical laterality, native-landscape body/keyframes, forbidden state tags, pack-specific references and boundary frames.
3. Link an approved plan from session provenance and enforce the matching chunk before `local_wangp` creates a run or starts a worker.
4. Snapshot the accepted production contract into `run.json`.
5. Update operator documentation and submit evidence-backed shared-skill feedback.
6. Run focused unit tests, schema validation, compile checks, link checks and diff checks.

## Contract impact

Producers: Grok/Hermes or another planner writes schema-2 shot plans and registers them with `wangp_recorder.py session --production-plan`. Consumers: `shot_production_plan.py`, `local_wangp.py`, run records and operators/reviewers. Existing schema-1 plans and sessions without a linked plan keep their legacy behavior. A linked schema-2 plan becomes an opt-in hard gate: its status, DNA hashes, prompt terms, exact reference paths/hashes and chunk continuity must pass before a run directory is created. Rollback removes the new CLI option/consumer and schema-2 files; schema-1 behavior remains the compatibility baseline. Deterministic verification uses fixtures and a fake detached worker only; no GPU execution.

## Progress

- Re-read governance, production roles, video skill/architecture, recorder contract, verification guide and the catalog-resolved production-skill-maintenance evidence rules.
- Confirmed the existing shot-plan validator already owns Ref2VA/FL2VA chunk boundary semantics, so the new contract will extend that path rather than create a parallel manifest.
- Added schema v2 with frozen character record/version/Stable-DNA hash, mandatory prompt terms, exact per-chunk reference packets, reviewer-declared anatomical laterality/composition, forbidden state tags and chunk/shot handoff roles.
- Made approved v2 plans registerable in `session-provenance.json` with a plan SHA-256. `local_wangp submit` now rejects a changed plan, changed DNA, missing prompt anchor, wrong model, wrong reference order/hash/dimensions or missing continuity contract before creating a run or worker.
- Preserved schema-v1 and unregistered-session behavior. Passing `--production-plan` is an opt-in execution hard gate; the operator guides require it for new character-video and multi-pack work.
- Added a reusable Lia-shaped fixture and focused schema, preflight, session-registration and no-run-on-failure tests.
- Updated the WanGP recorder, Grok, Hermes and shared production playbook documentation.
- Submitted shared-skill feedback `skillfb-20260930T073407Z-2ea98800` against `storyboard-cutboard`; the current shared source still mandates v1, so the proposal asks the integration owner to retain v1 planning compatibility while adopting v2 for approved execution.

## Verification

- `uv run --with pytest --with jsonschema --with pillow python -m pytest -p no:cacheprovider --basetemp .tmp/pytest-v2 tests/test_shot_production_plan.py tools/test_local_wangp.py tools/test_wangp_recorder.py -q` → **29 passed**.
- `python tools/shot_production_plan.py validate --plan tests/fixtures/shot-production-plan/lia-pack-contract-v2.json --json` → `ok: true`.
- `python -m py_compile tools/shot_production_plan.py tools/local_wangp.py tools/wangp_recorder.py` → passed.
- `git diff --check` → no whitespace errors; only existing line-ending notices.
- No GPU worker, renderer, media mutation, DNA edit, deployment, push or publication was performed.

## Known boundary

The code verifies that a named reviewer declared anatomical laterality and native composition, checks the frozen file hash, and checks native-landscape pixel dimensions. It cannot determine from pixels whether the declared wrist is truly anatomical right or whether a wide image contains deceptive portrait padding. The playbook therefore keeps visual pixel inspection as a mandatory human review step.

## Next

Use the approved v2 plan for the next new character-video/multi-pack session. Do not retrofit or rerender the Lia r2 outputs without a new user GO and approved native-landscape/right-wrist references. Triage the open shared-skill feedback separately; feedback submission did not authorize a canonical shared-skill edit.
