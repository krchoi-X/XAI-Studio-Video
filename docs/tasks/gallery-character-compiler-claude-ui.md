# Scoped task: Character Pack review UI

Parent: [Gallery-integrated Character Compiler](gallery-character-compiler.md)

Status: COMPLETE — Claude UI package committed at Studio `ba8aaf0`; Codex diff review and independent checks passed

Active editor: Claude Code (after the checkpoint is recorded below)

Integration owner: Codex

## Goal

Build the tablet-first Character Workspace presentation for a reviewed multi-angle character pack: current canonical Master Face, build status, five face slots, later four body slots, candidate comparison, select/reject/regenerate requests and final approval readiness.

## Start gate

Do not start from this planning document alone. Codex must first record here:

- XAI and Studio base revisions;
- the committed/patch presentation contract and example fixture;
- exact callback/type definitions;
- any files removed from this package because of overlapping worktree changes.

Checkpoint:

- XAI base: `2791df509c23aae2de5ddc177ea1f161d7cd0c67`
- XAI contract: `618df72` on `codex/gallery-character-compiler-contract-xai`
- Studio base: `500384f0e67d3db5ae9ced9c8c30ec9a792f2654`
- Studio presentation contract: `4799184` on `codex/gallery-character-compiler-contract`
- Studio completion note: `f607c91`
- Read-only input files for this package:
  - `frontend/src/apps/characters/character-pack/contract.ts`
  - `frontend/src/apps/characters/character-pack/contract.fixture.ts`
  - `frontend/src/apps/characters/character-pack/contract.test.ts`
- Contract verification: XAI focused regression 58 passed; Studio contract test 3 passed; Studio TypeScript/Vite build passed.

Claude must inspect these revisions and the actual diffs before editing. If the contract needs to change, stop and hand the request back to Codex rather than changing the read-only files.

## Owned files

After the start gate, Claude may create a dedicated subtree such as:

```text
frontend/src/apps/characters/character-pack/
  CharacterPackWorkspace.tsx
  MasterFaceGate.tsx
  PackProgress.tsx
  PackSlot.tsx
  CandidateStrip.tsx
  PackApprovalBar.tsx
  model.ts
  handlers.ts
  character-pack.css
  *.test.tsx
```

Claude may edit an existing Character Workspace component or stylesheet only if Codex adds that exact path to the checkpoint. New pure components should receive view data and callbacks through props.

The three checkpoint files under this same subtree are Codex-owned contract inputs and are excluded from Claude's owned file list.

## Must not edit

- Studio `backend/**`, database/schema/migrations or API routes;
- `frontend/src/App.tsx`, router/shell files, `frontend/src/shared/api.ts`, `types.ts`, or other shared integration files;
- XAI runtime tools/schemas, shared-authority character records or shared skills;
- renderer prompts, engine defaults, queues, manifests or persisted job state.

Codex owns those files and performs final wiring.

## UI requirements

- Clearly distinguish a Gallery `face_master` role from the active canonical Master Face.
- Display the current Master Face and require an explicit before/after confirmation when the supplied action requests replacement.
- Show five stable face slots: front, left 30, right 30, left profile and right profile.
- Support four later body slots: front, three-quarter, side and back without redesigning the component contract.
- Show the engine per candidate. Face candidates may use Qwen21 or Krea2; body candidates default to Krea2 but still display the actual recorded engine.
- Rejecting or regenerating must read as recoverable. Regenerate emits a callback for the logical slot and selected engine; it never removes a candidate locally.
- Final approval stays disabled until the supplied view model says all required slots are selected and valid.
- Automatic QA is a warning/ranking aid, never an approval badge.
- Follow the current warm editorial design, 44px minimum touch targets and 768x1024 tablet acceptance size.

## Acceptance checks

- Focused component/model/interaction tests cover empty, generating, partial, failed, needs-review, ready-to-approve and approved states.
- Tests cover multiple candidates, engine switching requests, Master Face replacement confirmation, recoverable rejection and disabled final approval.
- No network or persistence behavior exists inside the owned components.
- Frontend focused tests and build pass in the intended Studio checkout.
- Handoff records exact commit or patch/base revision, commands/results and any remaining visual uncertainty.

## Handoff back to Codex

Claude stops after the isolated package is verified. Codex reviews the diff, performs shared API/type/router integration, runs the combined regressions and owns runtime/tablet acceptance.

Handoff result (2026-10-08): Claude changed only new files under `frontend/src/apps/characters/character-pack/` and committed `ba8aaf0` on top of `c35c6e5`. Codex independently verified 113 character tests and `npm run build`. Shared mounting remains intentionally deferred until all UI actions have working backend endpoints.
