# Intent-preserving video methodology migration

- Date: 2026-10-03
- Active editor: Codex / GPT-6 Astra
- Status: COMPLETE — enforcement revision v1.1 and artifact schema v2 verified; renderer-output review remains human

## Goal

Preserve the current video methodology as an immutable Git-backed baseline, publish one canonical intent-preserving storyboard-to-video guide, and make future storyboard-derived video work use a portable, enforceable Intent Contract across Codex, Claude, Grok, Muse/Somni and Hermes/Meromero.

## Scope

- methodology backup manifest and local Git baseline tag;
- canonical runtime methodology and contract guide;
- shared `video-intent-contract` skill and references in `XAI-Studio-Private`;
- routing updates in shared storyboard/video skills and runtime agent entrypoints;
- artifact gates and deterministic validation guidance;
- focused validation of skill structure, catalog resolution, links and existing tests affected by edited guidance.

## Constraints / Must Preserve

- Preserve all existing user, character, production, review, storage and publication approvals.
- Preserve the useful camera, motion, continuity, model-adapter and failure-memory knowledge already present.
- Keep existing persisted records readable; do not silently widen a frozen schema. The stronger deterministic format is schema v2, while v1 remains a legacy reader path.
- Do not modify or absorb Claude's active productions/Drive/Catch Me work or unrelated character changes.
- The contract must be usable without the originating conversation and must include bounded background and rationale.
- Narrative meaning is deny-by-default after approval; only an explicit creative-envelope allow-list may change.

## Must NOT Do

- No render, GPU job, paid API, service restart, media/database change, publication or push.
- No per-agent methodology fork and no duplicated agent-specific canonical policy.
- No claim that documentation alone is a deployed renderer gate.
- No destructive cleanup of prior guidance or history.

## Plan

1. Record immutable baseline commits and hashes for the current runtime guidance and shared skills.
2. Add a stable canonical methodology document with cross-agent background, Intent Contract lifecycle, enforcement levels, override rules and migration map.
3. Add a focused shared `video-intent-contract` skill; route existing director, cutboard, continuity and adaptive-production skills through it without duplicating their responsibilities.
4. Update runtime agent entrypoints and production artifact gates so future storyboard-derived video work must create, acknowledge and validate the contract before renderer handoff.
5. Validate skill metadata, catalog resolution, Markdown references, diffs and relevant deterministic tests.

## Contract impact

Producer: the director/storyboard stage creates the Intent Contract beside the approved Storyboard Spec. Consumers: cinematographer pass, model compiler, semantic checker, shot planner, renderer submission boundary, human review and Clypra segment selection. Schema v2 adds locked prompt segments, enumerated creative values and a template version. The checker dispatches by schema version; v1 remains readable with its original weaker checks, while new work must use v2. Rollback selects the v1 reader and removes v2 artifacts without touching production assets.

## Progress

- Task recorded before runtime/shared-skill edits.
- Claude's review and the user requirement for cross-agent background plus enforceable constraints were incorporated in the Private migration source.
- Preserved the runtime and shared-skill baselines with local annotated tags and a file-hash recovery manifest.
- Added the canonical runtime methodology and contract guide, closed v1 contract/compiler-IR schemas, and `tools/video_intent_contract.py`.
- Added and registered the canonical shared `video-intent-contract` skill; connected director, cutboard, continuity and adaptive-production stages without replacing their responsibilities.
- Updated common agent routing and the root video workflow. New storyboard-derived video work must produce the contract, acknowledgement, compiler IR and passing hash-bound check before submission.
- Added a native local WanGP gate for sessions registered with `--methodology intent-preserving-v1`. Submission now requires the exact storyboard, contract, compiler IR and prior semantic-check record, recomputes the check before run creation/GPU start, and stores verified evidence in `run.json`.
- Verification: 69 focused tests passed with 1 skipped after the v1.1 review fixes; the affected shared skill passed `quick_validate.py`; Python compile and diff checks passed. The original broader migration validation (five shared skills and catalog resolution) also remains valid.
- No render, GPU work, service restart, media/database change, publication or push occurred.

## Next

Claude's review was received and the reproducible semantic-enforcement findings were accepted. v1.1 work makes locked prompt prose deterministic, constrains creative values, removes substring lint as an authority, and closes the approved-production-plan opt-out. Other renderer backends still need the same native boundary; user-approval evidence binding and segment-level enforcement remain follow-ups.

## Codex disposition of Claude review — 2026-10-04

- Accepted and implemented in artifact schema v2: deterministic full-prompt rendering from director-approved contract segments; exact prompt comparison; enumerated creative values; regression fixtures for all three reproduced cases. Frozen schema v1 remains readable and is not silently widened.
- Accepted and implemented: approved contracts no longer allow L3; `HIDE_TRANSITION` was removed from the feasibility enum; new approved production-plan registration automatically enables the intent gate. Pre-existing legacy records remain readable and are not silently reclassified.
- Accepted as a remaining limitation: `approved_by` still describes rather than cryptographically proves human approval. Binding it to a durable review event requires a separate approval-record contract and migration plan.
- Accepted as future expansion: renderer-job-request and Clypra segment boundaries need native enforcement equivalent to local WanGP.
- v1.1 completion means compiler fidelity is mechanically enforced for the supported deterministic template. It does not mean rendered-video fidelity is automated; Stage C remains human review.

## Handoff note — Claude review of 7d9f353 + 72a91c9 (2026-10-04)

Author: Claude Code (claude-opus-5-5), review-only; no code changed. Reviewed runtime commits `7d9f353`, `72a91c9` and Private shared-skill commits `8275a30`..`f3051f4`. Codex remains Active editor and decides what to accept.

Done well: shared-skill routing stays at handoff boundaries; hash binding, stale-record rejection and pre-GPU recheck in `tools/local_wangp.py` are sound; prior review items (allow-list default, joint approval, relative timing, failure attribution, segment inheritance, audited override) are reflected in guidance.

Main finding: the checker protects contract-file integrity, not prompt meaning. Status `COMPLETE` overstates semantic enforcement until items 1–3 are addressed.

Reproduced with the `artifacts()` fixture from `tests/test_video_intent_contract.py` (scratch copy, repo untouched):

| Runtime prompt / IR change | Expected | Actual |
|---|---|---|
| "She elegantly walks to the door, occasionally glancing at the camera, picks up her bag, then walks down the corridor as the camera slowly pushes in." | fail (early gaze, added action, restored omission, camera move) | **pass** |
| "Static camera, no push-in, no orbit. She reaches the door, pauses, looks at the lens only at the very end, and exits." | pass | **fail** `forbidden_phrase_in_prompt` |
| IR `creative_choices.lens_family = "85mm with a slow dolly toward her face"` + same text in prompt | fail | **pass** |

1. **IR equality is self-reported.** `compare()` checks `compiler_ir.locked == contract.locked`, but the compiler writes the IR by copying the contract; the prompt prose is not derived from it. Current gaze/order/omission/direction tests mutate the IR directly, so they never exercise prose drift. Fix: render locked prompt segments deterministically from the IR (versioned per-model template), and have the checker re-render and compare those segments to the submitted prompt. The LLM writes only the allow-listed creative slots.
2. **Forbidden-phrase lint is substring-based.** False positive on negated constraints ("no push-in"), false negative on inflections/synonyms ("pushes in", "dolly toward"). Negative wording should come only from template-generated or negative-prompt segments, which are excluded from the lint; maintain a per-model synonym list for camera ops and forbidden additions.
3. **Creative slot values are unchecked.** Allow-list validates keys only. Constrain values (controlled vocabulary per key) or at least run the camera/action lint over values.
4. **Gate is opt-in.** Enforcement applies only when a session registers `--methodology intent-preserving-v1`; an agent that omits it submits as before. Consider requiring it whenever the session has an approved storyboard/production plan, or at least recording `methodology: null` runs as non-faithful in review. External renderer paths (`renderer-job-request`) are still ungated (already noted in Next).
5. Minor:
   - `approval.approved_by` is free text, so an agent can self-approve as `"user"`; bind it to a recorded approval or restrict actors.
   - Schema allows `creative_envelope.level: L3` on an approved contract; methodology forbids re-direct after lock.
   - Feasibility enum adds `HIDE_TRANSITION`, re-expanding the vocabulary that was meant to merge.
   - `locked.gaze` is a free key/value map, so gaze timing relative to `ordered_events` is not structurally checkable; v1-acceptable, but the delayed-gaze case is not yet a structural check.

Suggested next regression fixtures: the three table rows above (expected fail / pass / fail).
