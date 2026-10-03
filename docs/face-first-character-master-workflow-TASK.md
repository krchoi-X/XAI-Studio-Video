# Face-first character master construction

Active editor: Claude Code (assigned by the user)
Status: READY FOR CLAUDE — plan and bounded first implementation
Date: 2026-10-01

## User intent

Start from an imagined character and its written Stable DNA, but do not expect prose alone to lock a unique face.
Codex or Claude compiles the DNA into an engine-neutral face-discovery brief and engine-specific prompts. Generate
with any suitable engine (local Krea 2/Qwen Image 2.1 or explicitly authorized external Gemini, GPT Image, Grok
Image, etc.) until the operator selects a face with the right underlying feeling. The operator then uses Xpade Face
Liquify for small geometric changes that make the face more distinctive. Separately find or generate a compatible
adult body/pose, using Krea 2 or Qwen when they are the appropriate supported engines, and combine the sculpted face
with the body through a bounded head/face swap. Human review, not generation or similarity scoring, decides whether
the result becomes a master.

The written DNA remains the conceptual starting authority. A visual master is a reviewed realization of that DNA,
not a replacement for the DNA and not proof that every angle has been solved.

## Desired workflow

```text
imagined character + Stable DNA
        ↓
engine-neutral face-discovery brief
        ↓
per-engine prompt adapters
        ↓
face candidates from Krea/Qwen/Gemini/GPT/Grok/other authorized engines
        ↓  human shortlist and feedback
selected base face
        ↓
Xpade micro-sculpt on a copy
        ↓
sculpted face-master candidate
        ↓                         separate lane
        │                 DNA-guided body/pose candidates
        │                         ↓ human selection
        └──────────────→ BFS head/face swap onto body target
                                  ↓
                       composite visual-master candidates
                                  ↓
                  human review → approve / revise / reject
                                  ↓
             Face Master + Body Master + Composite Identity Master
                                  ↓
                    later multi-angle/expression validation
```

## Artifact roles

Keep these roles separate even if one file temporarily fills more than one role:

- `concept_dna`: canonical written Stable DNA and its exact version/hash.
- `face_discovery_brief`: model-neutral interpretation of the facial feeling, separability and exclusions.
- `face_candidate`: an untouched engine output with exact provider/model/prompt/settings provenance.
- `base_face_selection`: the operator-selected candidate used as Xpade input; selection is not approval.
- `sculpted_face_candidate`: an Xpade-derived copy with source/output hashes and an edit note or exported parameters.
- `face_master`: a sculpted or untouched face explicitly approved by the operator.
- `body_target`: a body, pose, wardrobe and composition candidate; it does not supply facial identity.
- `composite_candidate`: a BFS or other explicitly selected swap result; always `needs_review` initially.
- `body_master`: an explicitly approved proportion/silhouette reference.
- `composite_identity_master`: an explicitly approved face/head/body realization for later production.

`reference_defaults.identity`, `approved_references`, favorites, review decisions and canonical DNA are different
states. Never infer one from another.

## UI decision

The durable product surface will eventually be Studio, not a separate permanent application. The operator has
explicitly deferred all Studio UI work so it can be redesigned coherently with the broader Studio UX later.

- Add the workflow only during the later Studio-wide UX redesign, likely as a guided `Create Character Master`
  action from the character/Gallery workbench, reusing existing assets, review decisions, comparison views, jobs and
  restricted-media access.
- Reuse the current Production/Transformation job infrastructure for backend execution and the current
  Gallery/Review surfaces for selection. Do not create another asset browser, review database or media library.
- Phase 0 and Phase 1 add no Studio UI, including no temporary action/status panel. The pilot uses existing import,
  sync, Gallery/Review and durable CLI/job records as they already exist.
- Xpade remains an external manual local step during the first pilot because its package and runtime behavior are not
  yet verified. Studio records the exported derivative and its lineage; it does not iframe, bundle or silently launch
  the unverified package.
- After the pilot, choose explicitly between (a) a verified local Xpade handoff opened from Studio, or (b) a small
  audited native liquify editor implemented inside Studio. Do not copy unknown third-party code into Studio merely to
  avoid the handoff.
- A temporary developer harness is permitted only for compatibility testing and must stay outside the user workflow.
  It is not a user-facing destination and must not become a second product by accident.

The intended eventual Studio sequence is a deferred UX requirement, not part of the current implementation:

```text
Character page → Create Character Master
  1. Review DNA-derived face brief
  2. Generate/import and shortlist face candidates
  3. Export a copy to Xpade / import the sculpted derivative
  4. Select or generate a body target
  5. Run Head Swap or Face Swap
  6. Compare all parents and the composite
  7. Approve an explicit master role, or reject/revise
```

## Prompt and discovery rules

1. Read the current canonical character record through the shared-resource resolver. Freeze its path, version and
   Stable-DNA hash into the discovery record.
2. Compile one engine-neutral brief before making provider prompts. It must preserve the operator's intended feeling,
   adulthood, major facial geometry, skin/hair anchors and explicit separability from existing characters. Do not add
   biography, personality or resemblance to a real person.
3. Provider adapters may translate syntax and photographic craft but must not silently change the identity brief.
   Store the exact final prompt actually sent to each engine.
4. Generate modest labelled batches. The user chooses when a face is promising; no score or agent may declare that
   the search is finished.
5. Later feedback such as "eyes narrower" or "jaw slightly longer" is a bounded exploration delta, not an immediate
   Stable-DNA edit. Preserve each round and its parent candidate.
6. External engines require their authorized route, real provider/model attribution and existing importer/Gallery
   contracts. Never copy an external output into an agent-specific folder or write the Studio database directly.

## Xpade micro-sculpt stage

Xpade Face Liquify is a manual deterministic finishing candidate, not an identity generator.

- Work on a copy; preserve the untouched base face.
- Use only subtle face-geometry changes such as eye size/spacing/angle, nose width, mouth/corners, jawline, face width
  and chin height. It does not repair texture, lighting, occlusion or perspective.
- Record `derived_from`, input/output SHA-256, byte count, tool/version if known, operator, time and a concise edit
  note. If Xpade can export parameters or a mesh, preserve them; otherwise explicitly record that the operation is
  not numerically replayable.
- Compare at 100% and 200% zoom, checking eyelids, irises, nostrils, lip edges, hairline, jaw and background warping.
- Do not make the source or result canonical without a separate human review action.
- Before first use, inspect the distributed HTML/JS and all external scripts, model URLs, network requests and
  telemetry. The current source is a shortened URL and remains unverified. Use expendable copies in an isolated
  folder/profile for the first test.

## Body-target stage

- Body exploration remains DNA-guided: adult proportions, silhouette and stable body traits come from current DNA;
  pose, wardrobe, coverage, setting and lighting remain Scene Delta.
- Use an engine that supports the authorized request and desired coverage. Krea 2 and Qwen Image 2.1 are the first
  local candidates; an engine choice does not relax project safety, consent or provenance rules.
- Prefer a body target whose head angle, light direction, crop, skin illumination and neck visibility are compatible
  with the selected face. A technically impressive body image is a poor target if the swap boundary cannot blend.
- The body target stays immutable. A swap produces a derivative candidate rather than overwriting it.

## BFS first adapter

First compatibility target: `Alissonerdx/BFS-Best-Face-Swap`, MIT licensed.

Use the Krea 2 head-swap path first because its supplied workflow names the same Krea 2 Turbo int8 ConvRot family
already present locally:

- weight: `bfs_head_swap_v1.1_krea2.safetensors` (approximately 914 MB);
- workflow: `Head Swap Krea 2 - V1 Simple Workflow.json`;
- Image 1: base/body target;
- Image 2: reference face/head;
- starting prompt: `head_swap: replace the head with the reference head.`;
- supplied workflow guidance: Turbo around 10 steps / CFG 1; RAW around 40 steps / CFG 3-4.

Also evaluate, but do not mix into the first test:

- Qwen Image 2.1 head swap: `bfs_head_v1.1_qwen_2.1.safetensors` (recommended, approximately 260 MB);
- Qwen alternative: `bfs_head_v1.1_alternative_qwen_2.1.safetensors` when expression transfer matters more than
  the smallest head-pose error;
- Krea body swap: `bfs_body_swap_v1_krea2.safetensors`, experimental, starting around strength 0.5;
- Qwen body swap: `bfs_body_swap_v1.0_qwen_2.1.safetensors`, separate later experiment.

The Hugging Face repository contains multiple incompatible model families. Never download or activate the whole
repository as one model. Pin the selected revision, exact filename, SHA-256, byte count, base model, input order,
workflow and license receipt. Confirm WanGP can load the LoRA against the exact local checkpoint before claiming
compatibility. A ComfyUI example is evidence of intended use, not proof that WanGP's GGUF/int8 loader accepts it.

Head swap and face swap are separate operations. Use head swap when hair/head shape belong to identity; use face-only
swap when the target hair must remain. Do not label head swap as face swap in persisted records. BFS Qwen Image Edit
2509 includes a face-only weight, but it is not automatically compatible with the installed Qwen Image 2.1 base.

## Review gates

Every boundary needs a human decision:

1. DNA/brief review: does the brief express the imagined character without inventing facts?
2. Base-face selection: does the operator like the underlying face enough to sculpt it?
3. Xpade review: did the change create distinctiveness without visible warping?
4. Body-target selection: are the adult proportions, silhouette and composition right independently of the face?
5. Composite review: inspect identity, head size, neck, skin tone, hairline, ears, lighting, expression, hands,
   clothing, background and text.
6. Master approval: explicitly choose the artifact role(s); do not infer approval from favorite, similarity or use.
7. Validation: later test frontal/three-quarter/profile and expression changes. A single approved frontal composite
   is not a complete multi-angle identity pack.

Face-recognition scores may rank candidates or flag drift but never override the operator. Scores across large yaw
changes are not directly comparable to frontal thresholds.

## Contract impact

Potential producers: Character Manager discovery compiler, external importer, Xpade manual import, BFS adapter and
Studio transformation jobs. Potential consumers: Gallery/Review, Character Manager default/approved-reference
reader, identity-set builder, later LoRA dataset builder and video reference selection.

The first implementation should use additive records and existing review/import contracts. It must not rename or
move existing sessions, alter old asset IDs, overwrite originals, change existing review states or make a new media
hierarchy. Before adding schema/API fields, name all producers/consumers, provide old-record compatibility and add a
fixture for a record without the new fields. Rollback disables the new writer/adapter while retaining all generated
and imported candidates as readable history.

## Implementation phases

### Phase 0 — compatibility and contract review

1. Reconstruct current code and dirty-worktree state before editing.
2. Read current shared Character Manager source, artifact contract, production roles, existing reference
   transformation schemas/workers, Studio asset/review model and historical identity-lock evidence.
3. Inspect the Xpade package without production media and report network/security findings.
4. Inspect BFS Krea workflow and safetensors metadata; confirm whether the exact WanGP Krea loader accepts an
   additional BFS LoRA and two ordered image inputs. Do not infer support from an empty `activated_loras` field.
5. Produce a focused compatibility decision and exact first-test settings. Stop rather than downloading another base
   model, modifying WanGP, or widening scope implicitly.

### Phase 1 — bounded manual pilot

Use one user-selected existing fictional adult character. Reuse its canonical DNA and create fresh immutable
sessions/derivatives.

1. Compile and expose the engine-neutral discovery brief plus one local provider prompt.
2. Import or select one face candidate through the existing Gallery contract.
3. Round-trip a copy through Xpade and record before/after lineage.
4. Select or generate one compatible body target.
5. Run at most one Krea BFS head-swap candidate after explicit approval for the model download and GPU job.
6. Sync the candidate as restricted/`needs_review`; compare source face, sculpted face, body target and composite.
7. Stop for human review. No retry, default-reference change, approval or promotion.

### Phase 2 — reusable workflow

Only after the pilot proves useful, add typed artifact roles, a durable recipe and engine adapters. Preserve
external-provider neutrality and use the same contract for imported Gemini/GPT/Grok results. Record UI requirements
for the later Studio-wide redesign, but do not implement isolated Studio workbench changes in this task.

### Phase 3 — identity pack and LoRA preparation

After an explicit master decision, create multi-angle/expression candidates, build a new immutable reviewed identity
set and later prepare a LoRA dataset. Do not make LoRA training a prerequisite for the first master workflow.

## Must preserve

- Canonical Stable DNA, exact version/hash and shared-authority resolution.
- Original files, source/output hashes, provider/model/prompt/settings and parent-child lineage.
- Real requester/executor/provider attribution.
- Restricted visibility and existing Gallery review decisions.
- Human authority over face selection, Xpade edits, body selection and master approval.
- Existing Qwen/Krea identity-edit behavior and old records.

## Must not do

- No automatic loop that spends credits or GPU time "until it looks good."
- No model or LoRA download, external paid generation or GPU run without explicit authorization for that operation.
- No silent engine substitution, text-only fallback or whole-repository download.
- No direct Studio database writes, parallel Gallery, agent-specific media folders or destructive file moves.
- No automatic Stable-DNA edit, `approved_references` update, default-reference change, favorite, keep or promotion.
- No use of public figures or non-consenting real people as identity sources.
- No claim that Xpade geometry editing, BFS swap or one frontal master solves multi-angle identity.

## Acceptance criteria for the first implementation

- One self-contained record connects exact DNA → discovery brief → face candidate → Xpade derivative → body target
  → BFS composite through stable asset IDs/paths and hashes.
- The untouched inputs remain byte-identical and independently reviewable.
- Engine/provider/model, exact sent prompt, LoRA filename/hash/strength, ordered inputs and effective render settings
  are visible in durable evidence.
- Old reference-transformation and generation records still pass deterministic fixtures.
- A failed or rejected composite leaves all sources and decisions intact and does not trigger a retry.
- The user can review all four visual checkpoints in the existing Studio surfaces before any master approval.

## Claude Code execution directive

Use this section as the direct instruction to Claude Code:

> Implement the bounded first slice of the face-first character-master workflow described in this task. Begin by
> reading `AGENTS.md`, the root and relevant scoped task records, current Git status/diff, the generated Claude
> governance entrypoint, `control/agents/production-roles.md`, the catalog-resolved Character Manager skill,
> `docs/artifact-and-review-contract.md`, `docs/shared-agent-workflow.md`,
> `docs/image-production-dna-and-master-TASK.md`, `docs/task-character-identity-lock.md`, and the existing Studio/XAI
> reference-transformation contracts. Treat code and current shared authority as newer than stale prose.
>
> The product intent is: start from imagined Stable DNA; compile an engine-neutral face-discovery brief and faithful
> provider prompts; let the operator select a promising face from any authorized generator; preserve an Xpade-edited
> copy as a derived sculpted-face candidate; select a separate DNA-consistent adult body target; then use a bounded
> BFS head/face-swap adapter to create a review candidate. DNA supplies the base feeling, pixels supply the chosen
> identity, Xpade supplies subtle off-prior geometry, the body target supplies pose/proportions, and only the operator
> may approve a master.
>
> First perform Phase 0 compatibility work. Inspect the Xpade distribution for scripts, models, network access and
> telemetry without using production originals. Inspect the official `Alissonerdx/BFS-Best-Face-Swap` Krea 2 guide,
> exact workflow and safetensors metadata. The first adapter target is
> `bfs_head_swap_v1.1_krea2.safetensors`, with body target as Image 1 and reference head as Image 2. Verify whether
> the exact local WanGP Krea Turbo/int8 ConvRot loader can load this additional LoRA and preserve ordered two-image
> conditioning. Do not assume compatibility merely because settings contain `activated_loras`.
>
> Record a scoped task with exact owned files, contract producers/consumers, old-record compatibility, checks and
> rollback before editing. Preserve all unrelated dirty work. Prefer an additive recipe/lineage record and existing
> importer/Gallery surfaces over a new database or folder hierarchy. Add deterministic fixtures before enabling a
> writer. Do not change current Qwen/Krea identity-edit behavior. The operator has deferred Studio UI work to a later
> holistic UX redesign: do not add or modify Studio screens, routes, panels or navigation in this task.
>
> Implement only the safe deterministic portion that the compatibility review supports. Do not download model
> weights, modify the WanGP installation, launch a GPU job, call a paid external generator, or promote any reference
> without the operator's explicit authorization. When a live pilot is ready, report the exact proposed character,
> inputs, BFS file/revision/hash/size, destination, settings, expected single output and review route, then stop for
> approval. The pilot is one composite candidate with no automatic retry. Completion means durable lineage and
> reviewability, not master approval.

## Next

Claude performs Phase 0 and returns a compatibility report plus the exact bounded file scope for Phase 1. The user
then selects the first fictional adult character and authorizes any required BFS download and one GPU pilot.

## Phase 0 scoped record — Claude Code, 2026-10-01

Operator restatement (2026-10-01): pick the best-liked face from any engine (Krea 2, Gemini, GPT Image, Grok Image,
...), subtly re-proportion it in Xpade for a distinctive feel, then use head swap / face swap to give it a fitting
body. This matches the workflow above; no change of intent.

Idea source: `personal-ai-knowledge/watch/workflows.md` § "Face Liquify v1.0 (Xpade Studio)" (P1 manual utility,
no integration; distribution is `https://bit.ly/4d22JEk`, unverified).

### Phase 0 scope (read-only plus notes; no product code)

Owned writes: this task file and a Phase 0 compatibility report under `docs/`. Nothing else is edited.
Preserved: all unrelated dirty work (19 modified tracked files at session start, including the Qwen-integration
edits to `tools/local_wangp.py`, `tools/reference_variation_worker.py` and
`tools/reference_transformation_contract.py`, which belong to the Qwen integration scope).

Contract impact: none in Phase 0 (no schema, API, manifest or CLI change). The Phase 1 contract section above stays
the governing draft. Rollback: delete the report; nothing else changed.

### Progress

- Read AGENTS.md, generated Claude governance, production-roles, artifact/review contract, shared workflow,
  `image-production-dna-and-master-TASK.md` and the reference-model registry in `tools/local_wangp.py`.
- Finding: `REFERENCE_MODELS` registers only `krea2_raw_edit`, `krea2_turbo_edit` (max 2 refs) and the Qwen 2.1 GGUF
  (max 4 refs, needs `video_prompt_type` `I`). No LoRA field exists in the validated reference path, so a BFS LoRA
  cannot yet be named, hashed or recorded by it. This must be settled before a writer is enabled.
- Xpade download: `bit.ly/4d22JEk` redirects to a Google Drive file (id `1hbqxk7J29uc6bd5ZXLPGkSLxr17_m0NL`) that
  requires a Google sign-in (HTTP 401 unauthenticated). Nothing was downloaded; no credentials were used. The
  operator must supply the file (see Next).

### Phase 0 result (2026-10-01)

Full findings: [Phase 0 report](face-first-character-master-phase0-report.md).
- Xpade is a hosted web app, not a download. Its obfuscated script was decoded statically: no uploads, telemetry
  or cookies; models and `human.js` load from public CDNs. Site files and models are pinned with hashes in
  `.tmp/xpade-inspect/` (untracked scratch). The Drive link was not used.
- BFS Krea LoRA (rank 128, 914,159,816 bytes, SHA-256 `abc6c468...b836`) has a key set identical to WanGP's
  installed Identity Edit LoRA; WanGP stacks model LoRAs with `activated_loras` and keeps ordered refs.
  Compatibility is strongly indicated but unverified. The local base is quanto int8, not ConvRot as stated above.
- Missing in code: the reference path records no LoRA name, hash or strength.

### Operator approval and progress (2026-10-01)

Operator approved the BFS LoRA download and the additive lineage module. The approval did not name the character,
face or body target, so **no GPU run has been started**; that waits for those three inputs.

- Download: `bfs_head_swap_v1.1_krea2.safetensors` at revision `0ca3913a...` into `D:\AI\WanGP\loras\krea2\`, written as
  `.part` and renamed only after size and SHA-256 match. No other repository file is fetched.
- Added `tools/face_master_lineage.py` and `tests/test_face_master_lineage.py` (new files only). Candidate roles
  only; approval roles are refused; hashes computed at registration; originals never moved; `verify` re-hashes.
  `init` checked against the real ch-shindo-noa shared DNA path (scratch file removed). 11 unit tests pass with
  `python -X utf8 -m unittest tests.test_face_master_lineage` from the repo root.
- Not changed: `tools/local_wangp.py`, schemas, Studio, any existing record.

### Next

1. Operator names the fictional adult character, the face candidate and the body target for the single pilot.
2. Claude then records the brief and inputs in a lineage file, runs one `krea2_turbo_edit` BFS composite per the report
   (no retry), registers it as `composite_candidate`, and syncs it as restricted `needs_review`.
3. LoRA evidence in `tools/local_wangp.py` waits for the pilot and for the Qwen scope's editor.

## Pilot log — ch-hana (2026-10-01, Claude Code)

Operator chose the new fictional adult character Hana (`ch-hana`, Stable DNA SHA-256 `9c2628fc3b7a...`, v1, status
candidate) for the pilot and said to proceed. Interpreted as authorizing: one local face-discovery batch (8 images,
Moody Krea 2 V7 INT8, local GPU, no external spend). Not yet authorized: any BFS GPU run (needs a chosen face and body).

1. Face discovery: session `SCENE-20261001-202733-hana-front-facing-head-and-shoulders`
   (`D:\AI_Studio\library\characters\ch-hana\generations\`), `character_scene.py prepare` then `produce --session-dir`,
   actor `claude`, strict_translation, seed 1001202734, 768x1024, 8 steps. GPU was idle (no Ollama model resident).
2. Next: operator reviews the 8 candidates in Studio Gallery (restricted, needs_review) and picks one, then runs it
   through Xpade (hosted tool, copy only), saves the export as a new file, and a body target is chosen or generated.
3. Then the single BFS composite per the Phase 0 report, with a lineage record via `tools/face_master_lineage.py`.

## UX requirement note — 2026-10-01 (deferred; no implementation)

After running the pilot by hand the operator found the workflow inconvenient and said it needs an easy UI/UX: a web
app used by touch on the tablet. The operator then clarified this is **not** a request to build it now. The Studio UI
deferral above stays in force; no Studio code was changed.

Manual friction seen in the pilot (input for the later Studio-wide UX redesign):
- Locating the session `outputs/` folder and saving the Xpade export by hand; the export landed in the same
  `outputs/krea2/` folder as the Krea originals.
- Having to tell the agent which candidate number was sent to Xpade (the parent was inferred by pixel difference).
- Comparing source and edited face side by side, and judging warping at 100%/200%.
- Registering lineage and choosing the next step via CLI/agent messages.
- Studio is already the tablet web app (served over the tailnet), so the eventual guided `Create Character Master`
  flow should live there and reuse Gallery/Review, jobs and restricted media as described in "UI decision".

Pilot state: face candidate #6 selected by the operator (recorded as `base_face_selection` in
`face-master-lineage.json`); Xpade copy `liquify-result.png` registered as a sculpted candidate; next is a body target.

### Pilot log update — body target (2026-10-01)

Body candidates session `SCENE-20261001-223552-hana-standing-photo-from-head-to` (4 images, local Moody Krea 2, white
bikini, head-to-mid-thigh, front). Operator chose **B3** (`run-20261001-223555-4259ae36_2.jpg`, SHA-256
`981bd7f2...5e87`); registered as `body_target` plus a `body_target_selection` in `face-master-lineage.json`.
Finding: `local_wangp.py submit` already persists `activated_loras`/`loras_multipliers` in the run's
`effective-settings.json`, so the pilot needs no code change there; the LoRA file hash is recorded in the lineage
record. A BFS composite session still needs a Gallery-sync route (the recorder `session` command does not write
`batch.yaml`); proposed route is the existing `external_media_import` dry-run, to be confirmed before syncing.
No BFS GPU run has been started; waiting for operator approval of the exact run below.

### BFS pilot result (2026-10-01, Claude Code) — FAILED, no retry

Session `HEADSWAP-20261001-hana-pilot1`, run `run-20261001-225219-72a8ffec`: `krea2_turbo_edit` + `KI`, refs
[B3 body, Xpade face #6], BFS LoRA strength 1, Identity Edit v1.2 also active (model default), 768x1024, 10 steps,
seed 20261001. Run status `needs_review`; ~2 min render. Worker log shows both LoRA files loaded without error.
The output is corrupt: full-frame colour noise with a faint silhouette. Registered in the lineage record as
`composite_candidate` with the failure noted; sources unchanged and byte-identical. No default reference, approval
or Gallery sync was touched.
Compatibility status: LoRA *loads* in WanGP; the stacked configuration *does not produce a usable image*. Untested
hypotheses (do not treat as findings): the two LoRAs together over-shoot; BFS strength 1 on quanto int8 is too high;
RGBA PNG reference; missing `ref_boost`. Any retry changes one variable and needs the operator's approval.

### Direction change — face-referenced body generation (2026-10-01, operator decision)

After the failed BFS composite the operator chose to skip head swapping: keep the Xpade face and generate the body
around it. Run through the existing supported route (`character_scene.py produce --identity-reference <path>
--engines krea2`, actor `claude`): session `SCENE-20261001-225740-hana-standing-photo-from-head-to`, `krea2_turbo_edit`
+ `KI`, the Xpade copy as the single hash-bound reference (SHA-256 `ffbfa363...`), 4 images, 768x1024, 8 steps. Run
status `needs_review`; nothing synced, approved or promoted.
Observation (Claude's visual read, not a verdict): the face is consistent across the four; framing is head to upper
thigh; the garments read closer to a sports top and briefs than a bikini; the bust is more modest than the DNA's
"full and prominent". Not yet in `face-master-lineage.json`: the lineage roles have no slot for a face-referenced body
generation, so the role (or a new additive one) must be decided once the operator picks an image.

### Studio registration (2026-10-01, operator request)

Ran the existing Studio sync (`POST /api/sync` on 127.0.0.1:8787): ch-hana now shows 3 sessions and 17 assets, all
`restricted` (`/api/characters` row; `/api/characters/ch-hana/assets` is empty unless `include_restricted=true`).
Sessions: face candidates `SCENE-20261001-202733...` (8 images + the Xpade copy, which the importer lists as a
`krea2` asset because it sits in `outputs/krea2/` and carries the Krea prompt - its true origin is in
`face-master-lineage.json`), bodies `SCENE-20261001-223552...` (4) and face-referenced bodies
`SCENE-20261001-225740...` (4). `HEADSWAP-20261001-hana-pilot1` was not synced: it has no `batch.yaml` and its only
output is the failed composite. The operator marks/reviews in the existing Gallery Library/Review surfaces.

## Codex review and operator direction — 2026-10-02

Codex independently checked the pilot records, run settings, manifests, output images and lineage tests after the
operator asked for a progress review. Deterministic verification:

- `python -X utf8 -m unittest tests.test_face_master_lineage -v`: 11/11 passed.
- The BFS run loaded both the default Krea Identity Edit LoRA and BFS LoRA, but its only output is a corrupt
  full-frame colour mosaic. Treat this configuration as a failed experiment, not as a usable adapter. Do not retry
  or make BFS part of the primary workflow without a new explicit experiment request.
- The face-referenced Krea run bound the Xpade export as its sole identity reference by SHA-256
  `ffbfa363...480bd`. All four outputs are coherent images and preserve the intended identity substantially better
  than the swap route, although identity varies slightly between candidates and human selection remains required.
- Xpade produced a clean, useful micro-sculpted derivative in this pilot. The operator wants Xpade capability in
  Studio eventually, but the earlier decision to defer Studio UI/UX work until the broader redesign still applies.

The operator has replaced the swap-first production direction with this primary path:

```text
Stable DNA -> face discovery -> human face selection -> Xpade micro-sculpt
           -> use that face as the identity reference while generating the body
           -> human selection/revision -> explicit face/body/composite master approvals
```

Consequences for the next implementation:

1. Face/head swap and the separately generated `body_target` lane are optional fallbacks, not the default path.
   Preserve the failed BFS output and its evidence, but do not sync, promote or silently retry it.
2. Add an additive candidate role for a body/composite generated from an approved-or-selected face reference, for
   example `identity_conditioned_body_candidate`. It must record the face artifact parent, exact reference hash,
   DNA version/hash, provider/model, prompt and settings. It must start as `needs_review`; it is not a master merely
   because the render succeeded.
3. Register the four outputs of `SCENE-20261001-225740-hana-standing-photo-from-head-to` under that role only after
   the schema/tool supports it. The operator has not selected or approved one yet.
4. Fix provenance placement during the later integration: an Xpade export must not be classified as a Krea output
   merely because it was saved under `outputs/krea2/`. Keep external/manual derivatives in a role-aware location or
   make the importer honor explicit lineage provenance.
5. During the deferred Studio-wide UX redesign, include an audited native Xpade-like micro-proportion editor or a
   verified Xpade handoff/import flow. Reuse Gallery/Review and the shared asset lineage; do not create a separate
   permanent UI or library.

No product code or Studio UI was changed by this review. The existing pilot files and downloaded BFS weight were
left intact.
