# Creative Treatment / Production Storyboard role-split integration

- Date: 2026-10-04
- Active editor: Codex / GPT-6 Astra
- Status: COMPLETE — conditional integration implemented; empirical production trial remains future work

## Goal

Integrate the approved direction of remote proposal `8a77653b`: optional Frontier Creative Treatment for complex work, Hermes-owned Production Storyboard and engine prompts, explicit user approval before execution, Hermes Runtime submission, local rendering, independent first review, and frontier escalation only when warranted.

## Constraints / Must Preserve

- Intent Contract schema v2 remains the semantic enforcement boundary; role separation does not authorize post-approval rewriting.
- Creative Treatment is optional for simple work and is not render approval.
- Mature production details may be authored locally for clearly adult fictional characters, but must be visible in the Production Storyboard/Intent Contract and included in the user's final approval. Never encode hidden policy-evasion instructions.
- Preserve existing idea requests, shot-production plans, session records, character DNA, approvals, queues, and renderer behavior.
- Preserve the untracked `docs/storyboard-reika-onsen-maple.md` and all unrelated active scopes.

## Must NOT Do

- No GPU job, render, Gallery/database write, service restart, media mutation, policy weakening, public push, or unrelated refactor.
- Do not claim the proposal's empirical adoption criterion is complete; prior comparison tested Hermes prompt compilation, not Hermes storyboard authorship from a treatment.

## Plan

1. Merge the remote proposal without touching unrelated local work.
2. Define the smallest durable Creative Treatment artifact and validation path.
3. Bind treatment provenance and distinct role attribution into session registration without changing frozen production-plan schemas.
4. Update the canonical methodology, Intent Contract workflow, Hermes guidance, and shared skill routing so approval and authorship boundaries are explicit.
5. Add deterministic tests for approval gating, provenance, backward compatibility, and the no-hidden-detail boundary.

## Contract impact

Producer: optional Frontier Creative Director writes a Creative Treatment artifact; Hermes writes the Production Storyboard, Intent Contract prompt segments, and engine choices. Consumers: user approval, Hermes session registration, prompt compiler, submission gate, review, and escalation consultants. Existing sessions remain valid when no treatment or role attribution is present. New treatment-backed sessions store immutable treatment path/hash/ID and role records. Rollback removes the optional sidecar and provenance fields without changing existing production plans or media. Deterministic verification covers old session registration, treatment validation, hash binding, approval requirements, and role preservation.

## Progress

- Remote proposal reviewed; conditionally accepted as a role-policy overlay rather than a replacement for the Intent Contract methodology.
- Added closed schemas for a bounded Creative Treatment and explicit production-role attribution without changing the frozen production-plan schemas.
- Added a validator and WanGP session-registration gate. Treatment-backed work requires an approved production plan, matching treatment authorship, Hermes storyboard/prompt/submission/first-review roles, exact path+SHA-256 approval binding, and explicit review of any mature production detail.
- Updated canonical methodology, contract, recorder, Hermes, and shared-skill guidance. Mature details must be visible in the storyboard and Intent Contract; hidden policy-evasion instructions remain prohibited.
- Existing non-treatment sessions remain compatible. Relative approved-artifact paths resolve from the role-attribution document directory.
- Verification: 72 focused tests passed and 1 skipped; the only warning is an upstream FastAPI test-client deprecation. Python compilation, JSON parsing, diff checks, and both shared-skill validations passed.

## Next

Run one or two user-approved real productions through `Frontier Treatment -> Hermes Production Storyboard/Intent Contract -> Local Engine`, compare them with the earlier failed shots, and record failure attribution. That empirical work determines whether conditional adoption becomes the default for complex productions.
