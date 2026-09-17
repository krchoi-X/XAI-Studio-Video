# Remote pipeline material merge and review

- Date: 2026-09-17
- Active editor: Codex
- Status: COMPLETE — deterministic sidecar/compiler and Hermes operational skills verified; live render pilot deferred

## Goal

Merge the newly fetched `origin/main` material into the current local branch without losing local production work, then analyze the new directing, prompt-compilation, cutboard, Hermes-operation and Noa postmortem documents as the basis for a Codex-directed / Hermes-executed video pipeline revision.

## Constraints / Must Preserve

- Preserve all tracked and untracked local work, generated media, session records and review state.
- Do not reset, clean, delete, overwrite or publish.
- Keep remote source material distinct from conclusions verified against the current implementation and Noa production evidence.
- Treat Codex as director/integration owner and Hermes as the intended production executor; do not launch a new render during this review.

## Must NOT Do

- Do not push the merge.
- Do not silently resolve a conflict by discarding either side.
- Do not edit canonical character DNA, reference approval or Gallery records.
- Do not claim the pipeline is implemented merely because guidance documents were merged.

## Plan

1. Fetch and inventory remote commits, changed paths and overlap with the dirty worktree.
2. Merge `origin/main` with automatic tracked-change preservation; inspect and resolve any conflicts conservatively.
3. Read all new director/prompt/cutboard/Hermes/postmortem materials and relevant implementation diffs.
4. Compare the recommendations with the observed Noa transition failures and current pipeline capabilities.
5. Produce a bounded pipeline modification proposal with implementation order, contract impact and verification gates.

## Contract impact

The merge may update shared instructions and runtime producers/consumers including `character_scene`, `local_wangp`, character storage resolution and director-memory routing. Existing persisted sessions and standalone project outputs must remain readable. This review does not yet authorize schema changes or rendering. Rollback is the merge commit plus its automatically restored working-tree state; no destructive reset will be used. Verification: merge status, conflict scan, diff inspection, documentation references, focused tests only if implementation changes are subsequently authorized.

## Progress

- Fetched `origin/main` at `336c7f7`; local branch is four commits ahead and seven commits behind.
- Identified tracked working-tree overlap in `AGENTS.md`, `tools/character_scene.py` and `tools/local_wangp.py`; untracked production artifacts remain out of merge scope.
- Merged `origin/main` as local merge commit `e495642` with `--autostash`; the autostash reapplied cleanly and no conflict markers remain.
- Read the new prompt-compiler, cutboard, cinematic-technique, Hermes operational-skill and Noa production postmortem materials plus the updated pipeline handoff.
- Confirmed the Noa edit reproduces `FAIL-003`: Shot D exits with both fingertips on the cheeks, while Shot E explicitly resets both hands below frame; Shot F begins already several steps back in a separate wide master. The 0.5 s title card hides a camera-scale cut but does not supply a physical action handoff.
- Current implementation already has a selective Director router sidecar and a `continuity_handoff` skill description, but the frozen storyboard v1 schema still leaves `continuity` untyped and has no machine-checked entry/exit body state, dependency, handoff mode or last-frame binding. The renderer submit path records references but does not compile adjacent-shot state automatically.
- Added `shot-production-plan-v1` as a sidecar contract rather than changing the frozen storyboard schema. It separates editorial shots, beats, keyframes, renderer chunks and intentional edit transitions, with typed entry/exit state.
- Added deterministic semantic validation and an H3 execution-plan compiler. The validator rejects unexplained carried-state changes, missing Ref2VA chunk handoffs, missing FL2VA anchors, duplicate/out-of-order beat coverage and renderer chunks that claim to create edit cuts.
- Added and validated the Noa cheek-to-paw-to-occlusion-to-dance fixture. Seven focused checks pass, including a 20-second single-take case with multiple engine chunks and no implied edit cut.
- Added thin project adapters and canonical shared `storyboard-cutboard` / `continuity-check` skills. Both resolve through the shared-resource catalog, passed the skill validator and were deployed byte-identically to Hermes' configured external skill directory. `hermes skills list` reports both as local, enabled skills without invoking a model.

## Analysis decision

Do not enlarge the frozen `storyboard-candidates-v1` contract first. Add a versioned continuity sidecar keyed by existing storyboard/shot IDs. The minimum state for dependent cuts is entry state, dominant action phases, exit state, dependency, handoff mode, and explicit reference roles. A deterministic validator should catch an unexplained hand reset, prop-hand change, spatial jump or camera-scale jump before rendering.

The first operational implementation should distill only two Hermes/Meromero skills: `storyboard-cutboard` and `continuity-check`. Codex remains responsible for schemas, validators, renderer profiles and difficult review. Hermes generates/repairs bounded artifacts and submits the render queue. For high-dependency transitions, the compiler chooses one of: same continuous clip, previous accepted last frame as the next start reference, H3 FL2VA start/end anchors, or an intentional bridge/occlusion. It must never silently reset to the character master.

For the Noa example, cheek-poke to cat-paw should be one continuous action chain or a state-linked pair that begins with fingertips still at the cheeks. Cat-paw to dance setup needs a designed bridge (for example a motivated lens-cover/occlusion followed by the wide reveal) or a separate stand-and-step-back transition shot; a decorative title card alone is not physical continuity.

### User correction — shot, storyboard frame and render chunk are different units

Do not equate one storyboard image with a fixed 5- or 10-second generated clip. A `shot` is the director's continuous camera/take unit and its duration follows the dramatic action and attention hold. One shot may contain several internal beats and several storyboard keyframes while remaining a single 20-second long take. Conversely, one storyboard keyframe may describe only one state inside that shot.

Keep these levels separate:

```text
sequence
→ editorial shot / continuous take
→ internal beats and state transitions
→ optional storyboard keyframes
→ renderer chunks required by engine limits
```

Renderer chunks are an execution detail and must not create editorial cuts by default. If a 20-second shot must be rendered as several short chunks, they inherit the same shot ID, camera/world state and chained boundary frame, then are assembled to read as one uninterrupted take. A new shot begins only when the directing plan intentionally changes take, viewpoint, time, space or visual emphasis.

Example: entering an outdoor hot spring, sitting, settling into the warm water, looking toward distant mountains and sky, and humming may be one 20-second long shot with several internal beats. The cutboard should represent the shot's progression, not split it automatically into four unrelated five-second shots.

## Next

Run one bounded Hermes/Meromero pilot on an approved storyboard: produce the sidecar, validate it, compile the H3 plan and stop before submission for Codex review. Wire the sidecar into `idea_production_worker.py` only after that artifact round-trip proves the contract; do not launch a new full episode as the first test.

## Implementation scope

Public runtime repository:

- `schemas/shot-production-plan-v1.schema.json`
- `tools/shot_production_plan.py`
- `tests/test_shot_production_plan.py`
- `tests/fixtures/shot-production-plan/**`
- thin shared-resource adapters under `skills/storyboard-cutboard/` and `skills/continuity-check/`
- focused routing/documentation updates only where required

Private shared authority:

- canonical `shared-skills/storyboard-cutboard/SKILL.md`
- canonical `shared-skills/continuity-check/SKILL.md`
- catalog registration and a scoped task/deployment record

Hermes deployment:

- byte-identical installed copies under the configured `D:/AI_Studio/skills` external directory, only after source validation

The tool validates hierarchy and continuity, and compiles a renderer-neutral execution summary with H3 route/reference recommendations. It does not submit a render, invent keyframe files, modify Gallery state or change Character DNA. Existing frozen v1 storyboards remain readable and unchanged.

## Additional workflow gaps found in implementation audit

1. `tools/idea_production_worker.py` currently performs one local-LLM generation pass after deterministic skill routing. It does not persist a separate directing/cut-function plan, continuity review or board-prompt compilation pass. Add durable staged artifacts rather than asking one response to solve all three jobs.
2. `storyboard-candidates-v1` has a `shots` array, but `continuity` is an open object and the recent morning boards represented an entire six-panel sheet as one synthetic `shot_board_*`. Future producers must use `shots` for editorial takes, not board sheets or fixed-duration renderer requests. Preserve the frozen schema and add keyframe/render planning in a sidecar.
3. There is no explicit hierarchy connecting `shot -> internal beats -> storyboard keyframes -> renderer chunks -> edit cuts`. Add this to the continuity/production sidecar and compiler. Renderer duration limits must not invent editorial cuts.
4. There is no pre-grid cut-function allocation or board-quality gate in code. Add one dominant directing purpose per shot, reason for existence, feasibility/risk and a semantic review step before image generation.
5. Renderer-specific prompt compilation is still manual. Add a small H3 profile that chooses reference roles and handoff strategy (`ref2va`, `fl2va`, continuous extension or intentional bridge) from the approved shot plan; do not build a universal prompt DSL.
6. Approval checkpoints exist conceptually, but episode artifacts should explicitly persist the selected storyboard revision, approved shot plan and shot-local retry lineage so Hermes never reconstructs them from chat.
7. Production-cost comparison from the Noa postmortem is not automated. Start with a small manifest summary—elapsed time, premium-agent involvement, failed shots and rerenders—only after the core shot/continuity path works.

Do not prioritize a large cinematic-technique database, vector retrieval service, repository reorganization, new Gallery hierarchy or Character DNA changes. Those do not address the proven failure.

## Agent entrypoint

For both Hermes and Grok, this task is the first episode-specific decision record. They must also load their normal host entrypoint, `AGENTS.md`, current shared production rules and the canonical shared skill through `tools/shared_resources.py`; this file does not replace those authorities.

Shared concept to preserve:

```text
editorial shot / continuous take != storyboard keyframe != renderer chunk != edit cut
```

A shot follows the director's continuous-take intent and may contain several beats/keyframes and last longer than one renderer request. Engine-limited chunks remain under the same shot and should not introduce an edit unless the approved plan declares one.

Hermes production reading subset:

1. `HERMES.md`
2. root `SKILL.md`
3. this task
4. `docs/director-memory/hermes-meromero-operational-skills.md`
5. `docs/director-memory/cutboard-quality-improvement.md`
6. `docs/director-memory/prompt-compiler-principles.md`
7. canonical shared `storyboard-director` or `idea-to-production` skill selected for the stage

Hermes executes an approved structured plan, validates continuity, repairs only failed states/shots and records the real `hermes` actor. It must not reinterpret renderer chunks as new editorial shots.

Grok directing/research reading subset:

1. `GROK.md`
2. root `SKILL.md`
3. this task
4. `docs/director-memory/cutboard-quality-improvement.md`
5. `docs/director-memory/cinematic-technique-library.md` only when technique selection is relevant
6. canonical shared `storyboard-director` skill

Grok may propose an independent directing candidate or analyze references, but must return shot purpose, continuous-take boundaries, internal beats, keyframes and intended edit points separately. External/provider claims remain evidence-labelled and do not become renderer rules without local verification.
