# Quiet evening vlog planning task

- Date: 2026-10-02
- Status: COMPLETE — Storyboard Draft 0 added; no production started
- Active editor: Codex

## Goal

Use the newly merged Muse reference analyses (#78–#79) to add one production-conservative, everyday vlog plan to the repository.

## Scope

- `docs/storyboard-draft-quiet-evening-vlog.md`
- `docs/quiet-evening-vlog-TASK.md`

## Constraints / Must Preserve

- Keep the plan character-neutral; casting must resolve current shared Character DNA later.
- Keep the Storyboard Spec model-neutral and mark it as Draft 0, not user-approved production truth.
- Separate corpus evidence from creative adaptation.
- Use one clear beat per shot, explicit continuity handoffs, and a small prop ledger.
- Preserve all existing local work and the merged upstream documents unchanged.

## Must NOT Do

- No Character DNA edits, reference inference, render submission, GPU work, Gallery mutation, publication, push, or claim of engine verification.
- Do not reuse the upstream fantasy rooftop scenario as an everyday vlog.
- Do not treat one Muse example as a universal model rule.

## Director routing

- Mode: `placed_camera_vlog` (`docs/director-memory/skill-router.json`)
- Selected skills: `placed_camera_opening`, `purposeful_action`, `continuity_handoff`
- Selected references: corpus #78, corpus #79, T-25/T-27, P-21/P-30

## Plan

1. Merge the disjoint upstream documentation commits with fast-forward only.
2. Extract the smallest reusable directing grammar from #78–#79.
3. Write one character-neutral vertical vlog Storyboard Draft 0.
4. Check links, whitespace, and Git scope; commit only the two owned documents.

## Progress

- Fast-forwarded local `main` from `ab711f2` to upstream `71c6e11`.
- Added an original five-shot everyday vlog draft using a placed phone, one beat per shot, natural sound, anti-commercial styling, continuity handoffs, and a prop ledger.
- No production or character state changed.

## Contract impact

None. Documentation-only addition. No schema, API, CLI, persisted manifest, runtime path, or production contract changes.

## Verification

- Markdown references and selected technique IDs checked against the merged source files.
- `git diff --check` and owned-file scope check required before commit.

## Rollback

Revert the dedicated documentation commit. The upstream fast-forward remains independently reversible by normal Git history; no existing local work needs to be rewritten.

## Next

User review of Draft 0. Casting, reference-role assignment, engine compilation, sample generation, and final production remain separate gated work.
