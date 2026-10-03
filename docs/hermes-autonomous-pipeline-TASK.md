# Hermes autonomous idea-to-night-batch pipeline

- Date opened: 2026-10-02
- Active editor: Claude Code (acting executor)
- Status: ACTIVE — design and guidance only; no implementation, render or Studio change started
- Assignment context: Codex has too little credit for about three days from 2026-10-02 and can only do
  overall organisation. The user assigned Claude to carry this work. Codex stays the integration owner
  for schemas, validators and renderer profiles; this task does not transfer that ownership. See the
  earlier precedent in [morning-vlog-plan-pilot-TASK.md](director-memory/morning-vlog-plan-pilot-TASK.md).

## Goal

Let Hermes (local Gemma4-based LLM, WanGP renderer, no Claude/Codex credits by default) run the whole
chain by itself, with the user only choosing and approving from the Tailscale tablet:

```text
idea intake (own idea / external idea or prompt / trend research)
 → idea-production-request-v1
 → storyboard candidates (director skills + technique DBs)
 → [user chooses]
 → cut and camera design bound to Character DNA and background DNA → shot-production-plan-v2
 → [user approves — GO gate]
 → night video batch (WanGP) → session records → Gallery / Control Tower review in the morning
```

Claude and Codex author the guidance, contracts and tools. Hermes executes. Claude/Codex are consulted by
Hermes only at defined escalation points.

## Role split (decided by the user, 2026-10-02)

| Role | Owns |
|---|---|
| Hermes | Running every stage, with the local LLM and local WanGP |
| Claude / Codex | Skills, contracts, tools, validators; paid consultation when Hermes escalates |
| User | Choices and GO approvals from the Studio UI on the tablet |

The user accepts spending a limited amount of Claude/Codex credit on consultation. The limit must be
explicit in the design (see Consultation budget), not assumed.

## Existing parts to reuse (verified by file presence only, not by running them)

- `tools/idea_production_worker.py` — compiles a durable request into storyboard candidates with the local
  LLM and stops at `needs_user_choice`. Contract: [idea-to-production-contracts.md](idea-to-production-contracts.md).
- `tools/director_skill_router.py`, [skill-router.json](director-memory/skill-router.json) — mode and technique routing.
- [directing-technique-db.md](directing-technique-db.md) (T-01…T-39) and [prompt-craft-db.md](prompt-craft-db.md) (P-01…P-31).
- `tools/shot_production_plan.py` — v2 plan validation before any GPU submission.
- `tools/local_wangp.py`, `tools/wangp_recorder.py` — single-shot submission with session records.
- `tools/hermes_night_batch.py` — durable batch queue, currently images only.
- Control Tower — read-only observation; Studio — existing storyboard-choice API surface.
- [production-incident-and-agent-consultation.md](production-incident-and-agent-consultation.md) — existing
  incident-report path for Codex/Claude consultation.
- Existing shared skills `adaptive-video-production`, `video-candidate-generator`, `video-candidate-review`,
  `frontier-review-escalation` (in `D:/codex/XAI-Studio-Private/shared-skills/`) already cover orchestration and escalation.
- First test input: [storyboard-draft-quiet-evening-vlog.md](storyboard-draft-quiet-evening-vlog.md) (Draft 0).

## Known gaps

1. No single orchestration skill that chains the stages with their stop points, and tells Hermes when to
   escalate.
2. No video batch queue; only per-shot submission and an image-only night batch.
3. No idea-intake queue format the user can feed from the tablet.
4. No trigger by which Hermes picks up approved work (image night batches show the polling pattern).
5. No Studio screens for idea queue, storyboard choice, plan approval, night start, morning review.
   Control Tower is read-only by design and should stay so.
6. No formal background (location) DNA record; character DNA is mature, background is not.
7. Unknown: whether a Gemma4-class local LLM can write a valid v2 plan from the technique DBs. Only a real
   Hermes run can answer this; the guidance should be revised from its results, not guessed.

## Consultation budget (proposed, needs user confirmation)

Escalate to Claude/Codex only for judgment that a deterministic check cannot make:

- review of storyboard candidates for technique fit and Never-Render (T-08) violations;
- final review of a v2 plan, only after `shot_production_plan.py validate` passes;
- diagnosis after two similar failures of one shot or an identity/continuity break.

Never escalate for intake, format conversion, queue execution, result filing, or anything a validator,
test or schema can decide. Each consultation is a fixed request packet (question, evidence files, wanted
answer) and its answer is stored beside the session. A per-day / per-batch call cap stops the run and
notifies the user when exceeded. The cap value is an open decision.

## GPU job ownership (decided by the user, 2026-10-02)

The WanGP submission API (`tools/local_wangp.py submit`) can be called by any actor. To keep one ordered
queue, **Hermes is the single submitter**:

- Studio only records an approved request in the queue; Hermes reads it and submits when the GPU allows.
  Hermes therefore polls the queue (the image night-batch pattern); Studio does not launch workers.
- Claude, Codex and Grok Bot hand requests to Hermes and do not submit directly.
- Exception: the user explicitly orders a direct submission while the GPU is idle. Recording stays
  mandatory (`wangp_recorder.py session`, real `--requested-by`).
- Fact from code: the GPU lock is a single-worker door; a submission against a held lock fails instead of
  queuing. Only the caller retries (the image night batch retries lock conflicts after 10/20/40 seconds).
- This is a convention, not enforcement; nothing technical stops a direct call. A warning for submissions
  that bypass the Hermes queue would change a CLI/contract and is Codex's integration area — follow-up only.
- Unverified, to read before the video batch design: whether the WanGP web UI used directly and the
  Studio `web_generation_worker.py` go through the same lock.

## Authorised production run — Rooftop 5AM test (user GO, 2026-10-02)

The user directed: make a video from Muse's storyboard [scenario-rooftop-5am.md](scenario-rooftop-5am.md),
instruct Hermes to do as much as possible, and have Hermes also join the clips into one video.
The user judged storyboard findings 1–3 (camera logic, framings per clip, handoff mechanism) not important and
postponed Character DNA ("after it works"). The off-screen second camera in a vlog is accepted.

- Purpose: first end-to-end test of the Hermes-executed chain and a first look at Muse's storyboard quality.
- Roles: Claude compiles the runtime prompts and settings and prepares the session and driver script;
  Hermes (host, local `meromero26b-a4b-hermes` via Ollama) runs the stills, the six clips, and the join and
  reports; `requested_by` is the real requester. Executor is the local WanGP worker.
- Engine: `minimax_h3_ref2va_pruned` (the only usable H3 Ref2VA weights), prompt mode FG, enhancer off, one
  identity reference per clip. Identity reference is a generated generic still (no roster character).
- Aspect: landscape 832x480 with a landscape-native reference. Basis: local evidence in
  [the 2026-10-01 night batch incident](production-incidents/2026-10-01-night-batch-home-cvstore-prompt-vs-actual.md)
  — portrait references remapped output to 512x768 while landscape-native references held 832x480.
  The storyboard did not specify an aspect, so this is an assumption.
- Output: a normal library session under `D:\AI_Studio\libraryideos\VIDEO-<date>-<time>-rooftop-5am`.
- Stop and report on any two similar failures; do not remake overnight without a new GO.

## Constraints / Must Preserve

- Existing contracts, schemas and persisted records stay readable; no field renamed, no enum widened.
- Stable Character DNA is read-only during production; production never edits it.
- Every user GO gate in AGENTS.md remains: sample, remake, multi-pack and night runs need a current GO.
- Claude does not execute the pipeline in Hermes's place; it builds what Hermes needs, then reviews what
  Hermes reports.
- Keep the scope moderate: take the documented `Next` steps; report contract defects for Codex's return
  rather than widening a contract to make something pass.

## Must NOT Do

- No Gallery mutation, Character DNA edit, publication or push as part of this task. Render and GPU work
  are limited to the authorised production run below; any other render needs a new user GO.
- No Studio UI or API change until its own scoped task names consumers and checks.
- No schema or CLI change without a `Contract impact` section and a compatible reader first.
- No automatic web scraping or trend collection in the first iteration; intake starts as a manual queue.
- Do not touch the unrelated pending working-tree changes already in the repository.

## Plan

Each step is a separate checkpoint; stop and record after each.

1. **Gap analysis and quality rubric (done 2026-10-02).** The orchestration skill already exists in the shared
   skills (`adaptive-video-production`, `frontier-review-escalation`); see
   [step 1 findings](hermes-pipeline-step1-findings.md). No new skill is written. The same document reviews
   Muse's rooftop storyboard and defines a storyboard quality check (static rubric, deterministic plan
   validation, user-watched samples).
2. **Intake contract.** Define the idea-queue file format and location Hermes polls. Docs and a fixture only.
3. **Hermes dry run request.** Prepare an input package from Draft 0 that Hermes can run to a v2 plan and
   validation without GPU. Hermes runs it; Claude reviews the result and revises the guidance.
4. **Video batch design.** Contract-impact note for a video batch queue modelled on the image night batch.
   Implementation only after the user and Codex integration ownership are clear.
5. **Studio command surface design.** List screens, API calls and approval gates; implement only under a
   separate scoped task.
6. **Background DNA.** Propose the record shape; hand to Codex for the schema decision.

## Progress

- 2026-10-02: Reviewed Draft 0, the technique and prompt-craft DBs and the existing pipeline parts.
  Recorded the role split and the consultation model above. No implementation started.
- 2026-10-02: Step 1 done as analysis: [findings](hermes-pipeline-step1-findings.md). Existing shared skills
  cover orchestration and escalation; real gaps are intake, unattended chaining, video batch, escalation
  reviewer (Claude vs Codex, unverified) and a call cap. Muse's rooftop storyboard reviewed: strong as a
  directing document, not production-ready (7 findings). Quality is checked in three layers; only the user's
  reaction to samples measures the user's own standard.

- 2026-10-02: Rooftop 5AM run completed, status `needs_review` (nothing approved). Session
  `D:\AI_Studio\libraryideos\VIDEO-20261002-112000-rooftop-5am`; final
  `outputs/rooftop-5am-final.mp4` (26.7 s, 832x480, h264+aac). Hermes ran the identity still, the six H3 clips
  (about 10 min each) and the join through the session driver `run_chain.py`; Claude compiled prompts and
  picked the identity still. One driver defect (empty `artifacts` in the submit result stopped the chain after
  shot 1) was found and fixed; shot 1 was registered manually and the chain resumed without re-render.
  Frame review of all six clips: events follow the storyboard; known deviations — S6 opens with her facing
  the camera rather than the S1 back-view composition (bookend not exact), S5's feather lands on the phone
  edge held in hands rather than a lens, Korean dialogue audio not verified by listening. Clips are about
  4.5 s each, not 5 s.

- 2026-10-02 (later): user feedback on the first cut — the wind looked unnatural, Korean speech came out well,
  the timing felt odd, and it was better than earlier productions. Ran a shot-2 wind/birds experiment: five
  variants, same seed and reference as the baseline, rendered by Hermes through `run_chain.py exp shot02`
  (about 10 min for ~4.5 s, about 16 min for ~8 s). Variants: B cause-and-effect chain, C element-by-element
  directed, D chain + 8 s, E directed + 8 s, F one continuous take. Evidence level: single sample each,
  judged from sampled frames only; motion smoothness, timing and audio need the user's viewing. Frame notes:
  baseline shirts mostly hang while pigeons burst; B shows shirts flipping, hair strands lifting in the
  close-up and a staggered bird launch; C shows the shirts leaning in one direction and a larger staggered
  flock; D/E keep the wind going and let the flock wheel away (a fuller arc); F shows a stray second pointing
  finger in the wide frames and still changed framing mid-clip. Hermes reported the launch as "Background
  process started" instead of the requested `detached pid=` line (the chain was running; reporting format not
  followed). Outputs: `outputs/exp/shot02/*.mp4`, labelled comparison `outputs/exp/shot02-comparison.mp4`.

- 2026-10-02 (night): user asked Claude to select 3-4 collected ~30 s video prompts for an overnight run. Selected
  from `D:\AI_Studio
ef-videos6-09-22-directing-patterns` and the corpus: farm milking (friend-cam), village
  market vegetable stall (#53), rooftop radio at golden hour (#23), early-2000s bus trip with a friend (#77). Excluded
  fights/swords/water/fire/crowd spectacle and costume- or body-focused pieces. Each is compiled as six ~5 s clips
  (132 frames, estimated from the 120->107 and 200->192 frame measurements) in the Rooftop 5AM grammar, with explicit
  pose/prop state per clip. Sessions are `prepared` (visible on /productions), no GPU used yet. Driver:
  `D:\AI_Studio\libraryideos\_night-batch-20261002
ight_chain.py`. Awaiting the user's GO for stills and the night run.

- 2026-10-02 23:25 (user GO: run overnight, finish and join, two more if time allows; user returns in about 7 h):
  six productions queued in `_night-batch-20261002` (four 30 s: farm milking, village market, rooftop radio, bus trip;
  two 15 s extras last: rainy jacket, alley cat). Hermes generated the identity stills (it re-ran the stills command a
  second time after its first call returned early, against the "do not retry" instruction; harmless, duplicate
  candidates only) and started `night_chain.py run --detach` (pid 24156). Claude picked one still per production
  and watches `night.log`. Clips are expected at about 10 min each, 30 clips in total.

- 2026-10-03 05:07: night batch finished with no failure and no manual intervention after the start: 30 clips
  (about 11 min each; four 30.9 s and two 15.5 s productions), joined by Hermes through the session drivers.
  Frame review by Claude (stills only; motion, audio and timing not judged): bus trip held two separate identities
  with same-direction walking and tickets; rooftop radio held the prop physics, the antenna state and the light
  change; farm and market held the main identity but secondary people vary between clips (farmer clothing,
  customers); rainy jacket and alley cat usable with small prop quirks. Statuses set to `needs_review`
  (nothing approved). Drive: 176 production files present and hash-verified, the scheduled task already copied most
  of them at 04:40. Hermes retried the stills command once against instruction; otherwise followed its briefs.
  Verdicts on quality belong to the user.

- 2026-10-03 user review of the six night productions (verbatim themes, not Claude's judgement):
  farm — cow and people positions do not match (milking under the cow's neck), the farmer's explanation scene is odd;
  market — napa cabbage called lettuce in the dialogue, odd scale, unclear wrapping (newspaper or plastic bag);
  radio — odd batteries, starts holding shoes in the hand, the reason it got fixed is unclear, she sits away from
  the radio; bus — two bus stops, the sea is visible right after boarding, the bus moves backward mid-way, the last
  line is unclear; rainy morning — odd starting location, where are the shoes, umbrella beside the jacket is left
  behind, the bag is put down and forgotten; alley cat — goes to see the cat, then sits at the first place and the
  cat comes to her, unclear whether same day or sequence. The user asked for guidance-level opinions (guideline,
  storyboard/planning, prompt), not per-video fixes. Claude's frame review of the same videos had only checked
  identity and props, not location, direction, causality or time, and was too generous. Opinion given in chat:
  most defects are decisions left unspecified (layout, prop/body state, cause, time, screen direction, object
  appearance) plus independent 5 s clips that cannot carry state; proposed a mandatory continuity-design sheet and a
  logic review before prompts, simpler single-location stories, visual object specs, fewer and longer clips with a
  location plate image; first experiment: remake one story both ways and compare. Awaiting the user's decisions.

## Contract impact

None yet; this task is documentation. Steps 2, 4 and 6 will each add their own `Contract impact` section
(producers, consumers, old examples, compatibility, rollback, deterministic verification) before any writer
is enabled.

## Open decisions for the user

1. Consultation cap per day or per batch, and which of Claude or Codex is the default consultant.
2. ~~Polling vs Studio launching the worker~~ — RESOLVED 2026-10-02 by the user, see GPU job ownership below.
3. Background DNA: new record type, or carry location through reference images for now.
4. Whether idea intake stays manual at first (recommended).

## Verification

Documentation only: links resolve and the git scope contains only the files named here plus the one-line
root pointer. Later steps use the repository's deterministic checks first (`docs/verification.md`).

## Rollback

Revert the documentation commit; nothing else changes.

## Next

Step 2 (intake contract) and a layer-A static review run by Hermes on one real storyboard. Before that, ask
the user whether to (a) fix the rooftop storyboard's defects 1–3 in a revision, or (b) leave it as evidence
and test Draft 0 first. Wait for the user's answers to the open decisions before step 4.
