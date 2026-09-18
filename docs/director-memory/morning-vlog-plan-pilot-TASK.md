# Morning-vlog shot-plan pilot — Claude acting executor

- Date: 2026-09-18
- Active editor: Claude
- Status: ACTIVE
- Supersedes nothing; this is the scoped execution of the `Next` recorded in
  [remote-pipeline-review-TASK.md](remote-pipeline-review-TASK.md),
  [director-router-TASK.md](director-router-TASK.md) and
  [intent-alignment-TASK.md](intent-alignment-TASK.md).

## Assignment context

Codex is unavailable for several days from 2026-09-18 because its credit window is exhausted.
The user assigned Claude as the acting executor with an explicitly bounded scope: keep the
existing architecture, do a moderate amount of work, and keep a durable written history.
Codex remains the integration owner for schemas, validators and renderer profiles; this task
does not transfer that ownership and does not rewrite Codex's plans.

## Goal

Close the artifact round-trip that all three completed director tasks name as their next step:
take the existing `revision-v2` shot production plan for the Noa morning-garden vlog, validate it
deterministically, compile the H3 execution summary, and stop before any render submission.
Report what the contract catches and what it misses, as evidence for the later Codex review.

## Scope

- `D:/AI_Studio/outputs/video-prompts/projects/noa-morning-garden-vlog-20260917/revision-v2/**`
  (validation and compile evidence files only, alongside the existing `draft-v0` and
  `revision-v1` convention)
- `.../revision-v3/**` (scope extended 2026-09-18 on the user's instruction: apply the three
  writing rules from the first-live review to a new revision, documents only, no render)
- this task record

## Constraints / Must Preserve

- Preserve the existing `shot-production-plan-v1` schema, `storyboard-candidates-v1`, the
  validator, the compiler and every renderer/importer/Gallery contract exactly as they are.
- Preserve `revision-v2/shot-production-plan.json` byte-for-byte; evidence is written beside it.
- Preserve the pending user choice. `project.md` still records `needs_user_choice`; candidate C
  (`sb_noa_garden_one_flower_rev`) is the only one Codex developed into a plan, and that is a
  pilot subject, not an approved production decision.
- Record `claude` as the real actor. Keep inference separate from verified engine behavior.

## Must NOT Do

- No render submission, GPU work, Ollama call, service restart or queue change.
- No schema, validator, compiler, worker or router change. A defect found here is reported,
  not fixed by widening the contract.
- No Character DNA edit, reference approval, Gallery/database mutation, push or publication.
- No new episode, no second candidate developed on my own initiative, no repository restructuring.

## Contract impact

None. This task only reads the existing plan and writes evidence files into the standalone
project folder, following the naming already used by `draft-v0/validation.json` and
`revision-v1/validation.json`. Consumers are the user and the later Codex review. Rollback is
deleting the new evidence files.

## Plan

1. Record this task before touching anything (done).
2. `shot_production_plan.py validate` on `revision-v2`, capture the exact result.
3. `shot_production_plan.py compile-h3` on the same plan, capture the execution summary.
4. Read both against the plan's own `warnings` and the `FAIL-003` continuity lesson in the
   pipeline review; separate what the validator proved from what it cannot see.
5. Record progress, findings and the next operation here. Stop before submission.

## Progress

Evidence lives beside the plan in
`D:/AI_Studio/outputs/video-prompts/projects/noa-morning-garden-vlog-20260917/revision-v2/`.
`shot-production-plan.json` was not modified.

- `validate` on `revision-v2/shot-production-plan.json`: `ok: true`, 0 errors
  (`revision-v2/validation.json`).
- `compile-h3`: `ok: true`, 7 shots (`revision-v2/h3-execution-plan.json`). 27.0 s of estimated
  editorial duration, one `h3_ref2va` chunk per shot, no chunk claiming an edit cut.
- The compiler carried through the plan's three authored warnings: the pajamas-to-work-attire
  wardrobe jump needs a real `blocking_reference` before rendering, and the macro shears close-up
  (`shot_05`) and the full-body walk (`shot_07`) are rated risky for single-cut H3 ref2va.

### Finding 1 — the clean validation does not yet prove the dependent-cut contract

All six transitions are declared `intentional_discontinuity` / `time_jump` with empty
`carry_fields`. The validator's continuity rules only fire on a declared dependency, so this plan
passes without ever exercising the path the sidecar exists for. A producer can obtain `ok: true`
for any episode by declaring every cut discontinuous. Whether a cut is genuinely discontinuous is
a directing claim and cannot be settled mechanically, so this is a gap in what the pilot proves,
not a validator defect.

I verified the rules do work, on throwaway copies in the session scratchpad, never on the project
plan:

- declaring the `shot_06 -> shot_07` cut `dependent` with `carry_fields: [wardrobe, right_hand]`
  produced two `continuity_mismatch` errors naming exactly the wardrobe and right-hand states that
  differ — the `FAIL-003` shape is caught once a dependency is declared;
- declaring it `dependent` with empty `carry_fields` produced `dependent_without_carry`.

### Finding 2 — a validated, compiled plan is still not submittable

Every compiled reference is `{"role": ..., "asset": null}`, which `shot-production-plan-v1` allows.
Nothing between `validate` and `compile-h3` requires a reference to resolve to a real file, and
`shot_07` additionally needs a work-attire `blocking_reference` that does not exist yet. The
submission path itself still fails closed (the Krea2/Ref2VA route rejects a missing reference
before GPU work), so this is a missing pre-render binding gate at the plan layer, not a safety
hole. Reported for Codex, not fixed here.

### 2026-09-18 — first-live self-review recorded in failure memory

Separate item under the same acting-executor assignment. The user watched the completed
`ノアちゃん、初配信！` and named five problems. Recorded in `failures.md`, which is the project's
own failure collection and is deliberately separate from the knowledge repository's
`video-notes/`, where only external material is kept.

- FAIL-003 amended: the Noa video is a second occurrence, so this is now a pattern, not a
  candidate. More importantly its listed Alternative C — hide the join with an edit — was tried
  (0.5 s caption card over the cat-paw to dance join) and the user still read it as wrong. The
  alternative is now scoped to covers that are motivated in the action.
- FAIL-005 added: a high camera angle on the dance wide shot made Noa read short and childlike.
  The plan specifies framing, support and movement but never camera height; an identity reference
  locks the face and not body proportion under perspective.
- FAIL-006 added: no performance register. `camera_relation` records framing, not whether the
  character knows and plays to the camera, so the "awkward but cute, filming herself" tone came
  through weakly. This is the user's largest complaint and the one with no prior memory entry.
- Open: Shot A into Shot BC was reported as slightly jumpy; cause not identified, awaiting detail.

Both new entries mark their `Likely cause` as inference; neither was verified against the engine.

### 2026-09-18 — revision-v3 applies the review findings, no schema change

The user asked to apply the writing rules that came out of the first-live self-review.
`shot-production-plan-v1` is a closed schema, so every change went into existing fields.
`revision-v2/shot-production-plan.json` is unchanged (sha256 begins `e373b32ebd8a384a`).

- **Performance register (FAIL-006).** Declared at episode level and written into every state's
  `camera_relation`: Noa sets up, carries and repositions the phone herself and knows it is
  recording. This forced the camera supports to become things she can physically do, so v2's
  gimbal, shoulder mount and macro lens are gone — they implied a crew, which is what made the
  first-live footage read as a character being filmed rather than filming herself.
- **Camera height (FAIL-005).** Stated on all seven shots in `camera.axis`. `shot_07` is
  explicitly at or below eye level with distance, because the first-live dance wide read high and
  made Noa look short and childlike.
- **Motivated change (principle 13).** Five joins gained an on-screen cause as a beat: the door
  opening explains the brightness rise, setting the phone on the step explains the low camera,
  picking up the can and shears explains tools that previously appeared between cuts, and passing
  the shears between hands explains a swap that previously just happened. The sixth join, pajamas
  to work attire, has no visible cause and still needs the work-attire `blocking_reference`.
- `shot_04` exit and `shot_05` entry now describe the right hand in the same words
  (`holding the pruning shears`), with the momentary detail moved into beats. That is the writing
  rule the earlier probe implied: states carry invariants, beats carry progression.

Result: `validate` ok, 0 errors; `compile-h3` ok, 7 shots; 32.5 s estimated, up from 27.0 s
because four beats were added.

**v3 still has zero `dependent` transitions, and that is now defensible rather than evasive.** A
self-filmed vlog cuts between camera setups she physically moves, so no join carries character
state forward. The important part is that the validator cannot tell v2 from v3 — both are
`intentional_discontinuity` everywhere and both return ok. Finding 1 therefore stands and is
sharper: the contract has no way to express "declared change with an on-screen cause". That is now
the top schema request for Codex.

Open decision for the user: the register is an episode-level choice. Flipping it back to an
observational camera reverts most of v3.

## Verification

- `tools/shot_production_plan.py validate` and `compile-h3`, exit 0, outputs preserved.
- Two negative probes in the scratchpad confirming `continuity_mismatch` and
  `dependent_without_carry` fire as documented.
- `python -X utf8`; no Ollama, renderer, GPU, queue, Gallery or DNA access; the project plan and
  every existing evidence file are byte-unchanged.
- Not verified: whether the seven declared time jumps are the right directing choice, and whether
  H3 actually holds identity across them. Both need a real render, which this task does not do.

## Next

1. The user chooses A, B or C (or a combination) for the morning vlog. Candidate C is the only one
   with a developed plan; that is a pilot artifact, not an approval.
2. Before any render of C: create the work-attire `blocking_reference`, bind every `asset: null`
   to a real file, and re-validate.
3. For Codex on return: decide whether the plan layer should require resolved references before a
   plan may be called render-ready, and whether an all-discontinuous transition set deserves an
   explicit reviewer flag rather than a silent pass.

## Blockers / uncertainties

- The user's A/B/C morning-vlog choice is still open, so nothing here authorizes production of
  candidate C.
- Codex is the integration owner for the schema, validator and compiler and is unavailable; both
  findings above are recorded for review rather than implemented.
