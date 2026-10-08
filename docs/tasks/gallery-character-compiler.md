# Task: Gallery-integrated Character Compiler

Status: LIVE WORKTREES INTEGRATED — awaiting explicit approval for service restart and first live render

Active editor: Codex (planning and cross-repository contract owner)

Planning checkpoint: 2026-10-07

## Why this task exists
The user wants character creation to stop being a long manual preparation loop. Once the user defines a character and explicitly approves one face as the **Master Face**, the Studio should automatically build the reusable identity references needed for later image/video production.

The inspiration is the staged ShoeCatch canvas pattern (reference → face → makeup/hair → comp card → outfit → editorial), but this Studio needs a stronger **persistent fictional identity** layer.

## Product decision
This belongs in the existing **Gallery / Character Manager** experience rather than becoming another standalone tool or repository.

Human decisions should be concentrated at two gates:
1. **Master Face approval** — user selects “this is the character”.
2. **Master Character Pack approval** — user checks the automatically generated identity pack before it becomes canonical.

Everything between those gates should be automatable.

## Proposed pipeline
```text
Character idea / existing Character DNA
        ↓
Character DNA + Face DNA + Skin Baseline
        ↓
candidate faces
        ↓
[HUMAN GATE 1] Master Face approved
        ↓
neutralized master reference
        ↓
multi-angle face generation
  front / left 30 / right 30 / left profile / right profile
        ↓
identity QA + candidate ranking
        ↓
body references
  front / 3/4 / side / back
        ↓
identity + proportion QA
        ↓
Master Character Sheet / Character Pack
        ↓
[HUMAN GATE 2] approve / reject individual views
        ↓
canonical Gallery character assets
```

## Canonical data separation
Do not collapse everything into one prompt.

- **Character DNA**: age, stature/proportions, overall presence, persistent non-face identity.
- **Face DNA**: facial geometry and relative landmarks.
- **Skin Baseline**: pores, microtexture, tonal variation, baseline complexion and physically plausible surface response.
- **Master Face**: visual identity anchor selected by the user.
- **Master Character Pack**: reviewed multi-view evidence.
- **Scene state**: hair, makeup, expression, outfit, pose, lighting, camera and environment. These remain variable and must not silently mutate canonical DNA.

A rendered “sheet” is a human-friendly view of the underlying references, not the only source asset.

## Suggested character asset shape
```text
characters/<character-id>/
  dna/
    character.md
    face.md
    skin.md
  master/
    face.png
  face/
    front.png
    left30.png
    right30.png
    left90.png
    right90.png
  body/
    front.png
    three-quarter.png
    side.png
    back.png
  sheets/
    face-sheet.png
    body-sheet.png
    master-sheet.png
  manifest.json
```

Adapt this to the repository's existing character schema rather than creating a parallel incompatible hierarchy.

## Gallery UX target
From an existing character card:
- show current Master Face;
- action such as **Build Character Pack**;
- generation progress by required view;
- thumbnails for candidates and selected references;
- identity/quality warning rather than silent promotion;
- approve/reject/regenerate per view;
- final **Approve Character Pack** action;
- subsequent scene generation can request the minimum appropriate references from this pack.

Do not require the user to hand-write prompts for every angle.

## Model/renderer strategy — deliberately unresolved
Do **not** hard-code the feature to Krea2, Qwen Image 2.1, or another model yet.

Build the workflow around an adapter contract so engines can be A/B tested. The current Qwen Image 2.1 identity pilot is directly relevant and should be reused rather than duplicated. Krea2 remains a candidate/baseline. Future ComfyUI identity adapters, FaceID/IP-Adapter-like approaches, or other edit/reference models may become better choices.

The first implementation should prove the workflow with whichever already-integrated renderer provides the best controllable reference-bound experiment. Record:
- identity preservation across angle;
- anatomy/proportion stability;
- skin/face beautification drift;
- latency;
- VRAM/runtime cost;
- manual rejection rate.

Model selection is an empirical decision made during implementation, not an architectural dependency.

## QA rules
- A generated view must never become canonical solely because generation succeeded.
- Automatic similarity scores may rank/filter candidates but are not the final authority.
- Reject obvious identity drift (eye geometry, brow-eye spacing, nose, mouth, jaw/chin, face length/width).
- Lighting and makeup may change surface appearance but must not be treated as permission to change anatomy.
- Avoid recursive derivation where a drifted generated angle becomes the sole parent for later views. Keep the approved Master Face / reviewed masters in the reference chain.
- Preserve provenance: renderer/model, workflow/adapter version, seed/settings where available, source master(s), generation timestamp and approval status.

## MVP
Use one existing character (Reika is a useful stress case) and implement:
1. Master Face input/selection from Gallery.
2. 5 face views.
3. Review UI with approve/reject/regenerate.
4. Master face sheet.
5. Persist reviewed assets + provenance.
6. Verify that downstream Gallery/character retrieval can use them.

Body views and automatic similarity ranking may follow immediately after the face MVP if the architecture supports them cleanly.

## Out of scope for first pass
- Character LoRA training by default.
- Automatic canonical promotion without human approval.
- Large hair/makeup/outfit variation libraries.
- Video generation.
- Making one renderer permanent before A/B evidence.
- New standalone repository or duplicated character database.

## Codex review / implementation request
Codex should first inspect the existing Gallery, Character Manager, character schema, reference-driven production pipeline, and the current Qwen Image 2.1 identity pilot. Then:
1. map this task onto the existing architecture;
2. identify the smallest Gallery integration point;
3. propose the renderer adapter interface and provenance fields;
4. implement the smallest end-to-end Master Face → reviewed multi-angle pack path;
5. add scoped verification;
6. update current priorities only according to the repository's one-active-P0 policy.

The key product principle is: **the user creates the character and chooses the face; the Studio compiles that decision into reusable identity evidence.**

## Existing architecture map

The smallest safe implementation is an extension of the current workflow, not a new character store.

- The Studio Character Workspace at `/library/characters/:characterId` already lets the operator assign a Gallery asset the `face_master` role through `character_references`.
- That role is presently a Gallery-local typed link. Multiple `face_master` links are allowed and shown as a conflict; assigning the role does **not** update canonical Character DNA or the generation default.
- Reference-bound generation reads only the shared-authority character record's `reference_defaults.identity`. This is resolved by Character Manager and is already consumed by Krea2 and Qwen21 without text fallback.
- Qwen21 is already a selectable, hash-bound reference engine. The Reika identity gate found it materially stronger than the current Krea2 route for frontal reconstruction, while 30/90-degree identity remains the weak and empirically unresolved area.
- New generation sessions and media belong in the configured Library. Existing immutable identity-set discovery under `library/characters/<id>/imports/derived` should be extended rather than creating the proposed parallel `dna/master/face/body` tree.
- Gallery remains the human review surface; Production owns generation and job controls. The Character Workspace may start a pack build and show results/status, but queue, retry and renderer controls stay in Production.

The missing bridge is therefore:

```text
Gallery asset + explicit Master Face approval
  -> maintained shared-authority writer records reference_defaults.identity
  -> durable character-pack job uses that exact path/hash/asset ID
  -> existing renderer adapter produces independent view candidates
  -> Gallery reviews candidates by required slot
  -> final approval snapshots an immutable reviewed identity set
```

## Product and contract decisions

1. **Role assignment is not approval.** Keep the existing `face_master` reference role for curation, but add a distinct `Approve as Master Face` action. The action must name one image, replace no prior master silently, and display the previous/new asset before confirmation.
2. **One canonical input.** Gate 1 records the selected asset's stable Gallery ID, absolute resolved path, SHA-256, byte count, approving actor and timestamp through a maintained Character Manager command. Studio must not edit the shared character JSON or live Gallery database directly.
3. **No duplicate media hierarchy.** Candidate views remain ordinary immutable generation outputs in one Library session. A candidate manifest groups them by slot. Final approval creates a fresh immutable identity-set snapshot under the existing derived-set root; individual files remain the actual references and sheets are derived review aids.
4. **Generation stays in Production.** The Gallery/Character Workspace CTA hands stable character/master IDs to a durable `character-pack` production job. Gallery shows progress and review links, but renderer selection, retry and cancellation follow Production ownership.
5. **No recursive drift.** Every slot generation binds the approved Master Face and the same Character DNA snapshot. A generated left/right view may not become the sole parent of another view. Regeneration creates a new candidate and preserves rejected candidates and lineage.
6. **Two explicit gates.** Generated candidates remain `needs_review`. Per-slot selection is reversible. Only `Approve Character Pack` creates the approved immutable set and updates canonical approved-reference links.
7. **Renderer-neutral record, empirical first adapter.** Persist logical view intent and adapter provenance independently. Implement Qwen21 first because the adapter and strongest current evidence already exist; retain Krea2 as an A/B baseline, not an architectural default.

## MVP state machine

```text
draft
  -> master_face_required
  -> ready
  -> generating
  -> needs_review
  -> partially_reviewed
  -> ready_for_pack_approval
  -> approved

Any generated slot may also be failed or rejected.
Regenerate appends a candidate; it never overwrites the selected or rejected asset.
```

Required face slots are stable logical IDs: `front`, `left30`, `right30`, `left90`, `right90`. Each slot can hold several candidates but at most one selected candidate in an approved pack.

## Renderer adapter contract

The pack orchestrator should call the existing reference-bound scene/WanGP route through a small capability adapter rather than duplicate model submission code. The adapter input is:

- character ID plus Character DNA version and stable hash;
- exact Master Face binding: asset ID, path, SHA-256 and byte count;
- logical view ID and engine-neutral view instruction;
- candidate count, seed policy and immutable identity/skin constraints;
- real requester/executor.

The adapter output is a compiled prompt/settings snapshot plus engine ID, exact `model_type`, adapter version and run/session identifiers. The initial Qwen21 adapter maps the five logical views to its existing `video_prompt_type: I` reference path. Krea2 may implement the same interface for comparison. Unsupported capabilities fail before queue submission; there is no engine or text-only fallback.

Every candidate record must preserve: `pack_job_id`, character/DNA version and hash, view ID, master asset/path/hash/bytes, renderer/model/checkpoint or quantization when available, adapter version, exact prompt and hash, settings and seed, requester/executor, run/session/output asset IDs, output hash, parent lineage, timestamps, automatic QA observations, and human review events.

## Implementation plan

### Phase 0 — contract checkpoint and old-record fixtures

1. Freeze representative legacy fixtures: a character with no master, a path-only `reference_defaults.identity`, a Gallery `face_master` link, and a conflicting multi-master Gallery state.
2. Define additive `character-pack-job-v1` and candidate-manifest schemas. Readers must continue accepting all current character, reference, generation and identity-set records.
3. Add the maintained Character Manager master-reference writer and dry-run/validation path. It must resolve the shared authority, verify character ownership/media type/path/hash, preserve history, regenerate the shared index, and require explicit operator approval metadata.
4. Add a rollback rule: the previous canonical default stays recorded in character history and restoring it requires another explicit approval; rollback never deletes media or review history.

### Phase 1 — Master Face gate in Character Workspace

1. Distinguish Gallery `face_master` role links from the active canonical Master Face in API and UI.
2. Add one explicit approval/replace action with conflict handling and a before/after confirmation.
3. On success, re-read shared authority and show the exact active master binding. Do not infer the active master from newest, favorite, cover or role order.
4. Add `Build Character Pack` only when the canonical master resolves and its current bytes match the recorded hash.

### Phase 2 — durable five-view job

1. Add a `character-pack` production job record and worker/orchestrator that creates the five required slots and calls the existing Qwen21 reference-bound adapter sequentially.
2. Freeze the Character DNA, skill revision and Master Face binding once per job. Record progress and failures per slot; resume incomplete slots without regenerating completed candidates.
3. Sync completed outputs through the existing importer so they receive stable Gallery asset IDs. Publish the candidate manifest only after its referenced outputs are durable.
4. Run Reika as the first bounded case. Use modest candidates per slot and fixed seeds suitable for A/B; do not launch this empirical run until the user authorizes GPU generation.

### Phase 3 — per-slot review and regeneration

1. Add a Character Workspace pack review surface with five slots, candidates, provenance, warnings and current selection.
2. Reuse Gallery decision semantics where they match, but keep pack-slot selection explicit and separate from Favorite/Keep. Reject and regenerate never delete originals.
3. Add automatic QA only as observations/ranking. Off-axis recognizer scores are not calibrated approval gates; expose geometry/face-detection failures and disagreements rather than hiding candidates.
4. Regenerate one slot from the original approved Master Face and frozen DNA snapshot while preserving the prior candidate and job lineage.

### Phase 4 — immutable approved pack and downstream retrieval

1. Require exactly one selected candidate for every required slot and no unresolved binding/hash failure.
2. Build a deterministic face sheet from selected individual assets. Record it as a derived artifact; downstream generation consumes individual members, not pixels cropped back out of the sheet.
3. Create a new immutable identity-set snapshot with view roles, Gallery asset IDs, hashes, source job/manifest hash and the human approval event. Add the selected asset IDs to canonical approved references through the maintained writer.
4. Extend `/api/characters/{id}/sets` and Character Manager retrieval to expose the approved pack without breaking older identity-set manifests. Require downstream callers to select an explicit pack/version; do not elect "latest" automatically.

### Phase 5 — body extension after face MVP acceptance

Add `body_front`, `body_three_quarter`, `body_side` and `body_back` using the same job/review/snapshot contracts. Body work must bind the Master Face plus Character DNA body proportions, add anatomy/proportion QA, and remain a new version rather than mutating the approved face pack.

## Expected file scope

Initial implementation is expected to touch only these bounded areas; exact additions must be recorded before coding:

- XAI runtime: `tools/character_manager.py`, a new pack orchestrator/worker and schemas/tests, plus existing Character Manager/shared-resource readers where required.
- Shared authority: `schemas/character-v1.schema.json` only for an additive master-binding/provenance shape if the current optional object is insufficient; shared Character Manager wording after code contracts are fixed.
- Studio backend: character authority adapter, schemas/API, durable job persistence/worker hookup and focused tests.
- Studio frontend: Character Workspace pack components/actions, the Production job handoff, shared API/types and focused tests.
- Documentation: this task, Studio `TASK.md` after its current completed scope is checkpointed, and current priorities only when implementation is actually selected as the one active P0.

Do not edit unrelated video, publication, importer, continuous-batch or Gallery-pagination work. The Studio worktree currently has overlapping uncommitted changes in backend/API/shared frontend files; implementation must wait for a reviewable checkpoint or an explicitly isolated file assignment. Planning does not take over those changes.

## Work packages and ownership

Overall integration editor: **Codex**. Claude owns only the bounded UI package linked below. The assignments become active in sequence; recording an owner does not authorize starting before its dependency gate.

### Package A — contracts, runtime and backend integration

Owner: **Codex**

Scope:

- legacy fixtures and additive character-pack schemas;
- maintained Master Face approval writer and shared-authority history/index update;
- durable pack job/manifest, resume behavior and final immutable identity-set builder;
- renderer capability adapter and per-slot engine choice;
- Studio backend endpoints, persistence, worker hookup and API/shared-type integration;
- cross-repository compatibility tests and final integration.

Engine policy in this package:

- `face` stage defaults to Qwen21 but every face slot records an explicit engine and may be regenerated with Krea2;
- `body` stage defaults to Krea2 because current Qwen body evidence is poor, while retaining an explicit per-slot engine field for later A/B work;
- no pack-wide implicit renderer and no fallback after submission;
- changing the engine appends a new candidate under the same logical slot and never overwrites prior output.

Codex owns integration files such as Studio `backend/app/main.py`, `schemas.py`, `database.py`, shared frontend API/types, router/App wiring and XAI/shared-authority contracts. Claude must not edit these files for this package.

### Package B — Character Pack review UI

Owner: **Claude Code**

Durable handoff: [Claude Character Pack UI package](gallery-character-compiler-claude-ui.md)

Scope is limited to pure Character Workspace presentation components, local state/handlers, styles and focused component tests. It consumes the committed Package A presentation contract through props and callbacks. It does not fetch, write canonical character records, submit renderer jobs, change the database/API, or edit integration-owned shared files.

### Package C — integration and empirical acceptance

Owner: **Codex** for code integration; **Hermes or Codex** may execute the bounded render matrix only after explicit user authorization.

Codex wires Package B into the app, runs backend/frontend/build regressions and verifies restart/resume. The production trial uses Qwen21 for face candidates and Krea2 for body candidates by default, records per-slot alternatives, and returns all results to Gallery as `needs_review`. Claude may review UI defects in its owned components after the first tablet pass; contract or API defects return to Codex.

## Ordered execution and gates

1. **Checkpoint current worktrees — Codex.** Preserve or isolate the existing Studio and XAI dirty changes. Record exact bases/diffs. No compiler implementation starts before this is reviewable.
2. **Contract checkpoint — Codex.** Land old-record fixtures, state machine, schemas, Master Face writer interface, pack job/manifest examples, renderer input/output contract and presentation props/callbacks. This commit/patch is the only source Claude should build against.
3. **Parallel implementation after Gate 2.**
   - Codex implements Package A runtime/backend and fake-renderer tests.
   - Claude implements Package B in its disjoint component files and tests, without modifying shared integration files.
4. **Deterministic package checks.** Each owner runs and records its focused tests. Claude hands off an exact commit or patch/base revision; Codex inspects the diff rather than relying on prose.
5. **Integration — Codex.** Wire the UI package to the committed API contract, reconcile shared types/routes, and run Studio backend tests, frontend tests/build, XAI schema/worker tests and old-fixture compatibility.
6. **Face MVP runtime trial — user approval required.** Generate the five Reika face slots with Qwen21 defaults and selected Krea2 comparisons. Verify sync, resume and review; do not approve the pack automatically.
7. **Face MVP review gate — user.** The user accepts/rejects/regenerates views. Contract or identity issues are repaired before body work.
8. **Body extension — Codex, then user-authorized execution.** Add four body slots with Krea2 default, per-slot engine override and proportion/anatomy observations. Qwen body generation is opt-in comparison only.
9. **Final pack approval gate — user.** Only after all required slots have one selected candidate does Codex verify the immutable set/sheet and explicit downstream retrieval.

Parallelism is deliberately limited to step 3. Steps 1-2, 5 and 9 are integration-owned and sequential; render trials wait for deterministic verification and explicit user approval.

## Contract impact

Producers are the Gallery Master Face approval endpoint, maintained Character Manager writer, character-pack orchestrator, renderer adapter, importer and final pack builder. Consumers are shared character/index readers, `character_scene`, night batch and video reference resolution, Studio character/set APIs, Character Workspace, Production Jobs and future body/LoRA builders.

Compatibility is additive: old path-only identity defaults, characters with no default, existing Gallery role links, generation sessions and identity-set v1 manifests remain readable. No automatic migration, media move, DB rewrite or newest-file inference is allowed. New writers activate only after old fixtures pass. Rollback disables the new endpoints/worker and leaves all candidate media, manifests, reviews and the prior canonical master recoverable.

## Verification plan

- Schema/CLI: old and new character fixtures; dry-run and apply; wrong character, non-image, missing/changed bytes, conflicting master and authority-unavailable rejection; index regeneration and history preservation.
- Worker: fake renderer/importer tests for five slots, exact master hash binding, sequential resume, one-slot failure, regeneration lineage, no fallback and idempotent restart.
- Studio backend: authorization/boundary checks, Master Face replace confirmation, job state transitions, old DB fixtures, per-slot review, final approval preconditions and set retrieval.
- Studio frontend: phone/tablet Character Workspace states, conflict/replace dialog, job handoff, five-slot review, reject/regenerate, partial progress, approval gating and accessible labels/touch targets.
- Deterministic artifact checks: selected output hashes, manifest/schema validation, sheet-member mapping, derived lineage and old identity-set reader compatibility.
- Runtime acceptance: one user-authorized Reika Qwen21 run, Gallery sync, desktop plus 768x1024 tablet review, service restart/resume and downstream explicit pack retrieval. Record latency, VRAM/runtime cost, rejection rate and the limits of off-axis identity scoring.

No GPU generation, canonical Master Face change, approved-reference promotion, service restart, push or deployment is authorized by this planning task.

## Progress / next

- Remote task and shared discovery commits were fetched and merged into the local `main` on 2026-10-07 without overwriting existing dirty work.
- Existing Gallery, Character Manager, shared authority, Qwen21 adapter/pilot, immutable set builder and Studio boundaries were inspected.
- Work is split between Codex Package A/C and Claude Package B with a contract-first handoff and disjoint file ownership.
- Step 1 evidence: [isolated worktree checkpoint](gallery-character-compiler-worktree-checkpoint-20261007.md). Original dirty worktrees were not stashed, reset or modified by this package.
- Step 2 XAI contract checkpoint: `618df72` on `codex/gallery-character-compiler-contract-xai`. It adds additive job/candidate/approval schemas, old-record fixtures and the dry-run-capable maintained Master Face writer.
- Step 2 Studio presentation checkpoint: `4799184` on `codex/gallery-character-compiler-contract`; completion/verification note: `f607c91`.
- Verification: XAI focused regression 58 passed; current 14 shared character records retained the known pre-existing Mira schema exception only; Studio contract test 3 passed and TypeScript/Vite build passed.
- Step 3 XAI runtime checkpoints: `53b7a9e` adds durable create/generate/resume/regenerate behavior; `04da113` adds recoverable review transitions and immutable approved identity-set publication.
- Runtime guarantees now covered by fake-renderer tests: frozen DNA/Master Face bytes, explicit per-slot engine, Qwen21 face default, Krea2 body default, no fallback, append-only regeneration, resume, exact selected-candidate requirements and immutable publication.
- Step 3 Studio checkpoints: `fcfb440` adds the pure backend adapter; `de7b1c2` adds the confined filesystem service; `851fe57` adds read/create/select/reject API routes and declares the XAI runtime's `jsonschema` dependency. XAI/Studio review method naming was reconciled in `bc50905`.
- Verification on 2026-10-07: XAI focused contract/runtime/Character Manager/set suite 33 passed; Studio focused adapter/service/API suite 12 passed. The broader Studio suite reached 148 passed / 10 failed, with failures tied to isolated-worktree environment assumptions (missing copied launcher/tool paths and writable default DB state), not the focused package.
- Claude completed Package B at Studio commit `ba8aaf0`, based on `c35c6e5`. Codex inspected the exact diff: only the assigned `frontend/src/apps/characters/character-pack/` subtree changed and the three read-only contract files remained untouched. Independent verification passed 113 character tests and the production frontend build.
- Added the append-only production worker and durable regeneration requests. Initial builds run candidate-less slots sequentially from the frozen Master Face and DNA; face defaults to Qwen21, body defaults to Krea2, each request has one explicit engine, and partial success survives a later slot failure.
- Studio now exposes explicit Master Face approve/replace, initial build, per-slot regenerate, select/reject and final pack approval endpoints. Generated outputs are reconciled to stable Gallery asset IDs by exact character/path/hash/byte match before final approval.
- Final approval publishes an immutable discoverable identity set with copied member hashes, the candidate-manifest snapshot and human-review-only face/body/master sheets. Sheets are derived aids; individual members remain the source references.
- Claude's review package is mounted at the separate Character Pack library view and wired to the real API. Initial creation includes body slots so Krea2 is the body default; every slot can still be explicitly regenerated with Qwen21 or Krea2 and never falls back silently.
- Deterministic verification on 2026-10-08: XAI focused runtime/worker/contracts/Character Manager/set suite 42 passed; Studio Character Pack/authority/worker-environment suite 31 passed; full frontend 656 passed; TypeScript/Vite production build passed. ESLint remains unavailable because this checkout has no `eslint.config.*`.
- Live-worktree verification on 2026-10-08: the complete Studio backend suite passed 172 tests, the complete frontend suite passed 656 tests, and the production build passed. XAI's focused Character Pack/runtime compatibility suite passed 42 tests. Existing continuous-production, pagination and Production UI changes remained present.
- User authorized the live restart, canonical Master Face approval and the full Qwen/Krea render on 2026-10-08. The maintained approval endpoint recorded Gallery asset `ast_25f17f445b5eafadf15e4645` as Reika's canonical Master Face with approval `mfa-8bc3d2bc901d4a4d8500b8f01255d224` and SHA-256 `ba3411fb8db4ac28aa5ce2807a1ac56e32fb9e47da4c357d4ac13734010a33b7`.
- Live job `cpj-1c6c6c95cc5c44f39947a92c613df460` completed without retries or failed slots: five Qwen21 face candidates and four Krea2 body candidates, one candidate per required slot. All nine outputs reconciled to stable Gallery asset IDs and their preview GET routes returned `200 image/webp`.
- The Studio service group is running after restart. Its existing backend virtual environment was missing the already-declared `jsonschema>=4.25,<5` dependency; the environment was synchronized and the services restarted without changing or replacing the existing database.
- Current gate: all nine candidates are `needs_review`; no candidate has been selected, rejected or regenerated, and the pack cannot be approved until the user reviews and selects one candidate for every required slot. No push or deployment was performed.
