# Hermes pipeline — step 1 findings

- Date: 2026-10-02
- Author: Claude Code (acting executor), scope of [hermes-autonomous-pipeline-TASK.md](hermes-autonomous-pipeline-TASK.md)
- Evidence level: **reading of documents and skill sources only.** Nothing was run, rendered or validated by a
  tool. Every judgment below is a model judgment unless it cites a file line the reader can check.

## 1. The orchestration skill mostly exists already

Shared skill sources (resolved through `tools/shared_resources.py`, physically in
`D:\codex\XAI-Studio-Private\shared-skills\`) already cover most of what step 1 planned to write:

| Need | Existing shared skill | What it already does |
|---|---|---|
| Local-first loop from candidates to one gated sample | `adaptive-video-production` | brief → candidates (generation only) → independent review → select or abstain → `storyboard-director` → `storyboard-cutboard` → continuity check → one local sample; stops before render unless authorised |
| Independent comparison of candidates | `video-candidate-generator`, `video-candidate-review` | separate generation and review passes; review returns `selected` / `needs_user_choice` / `blocked` |
| Hermes asks Claude/Codex for judgment | `frontier-review-escalation` | Hermes-owned gate; self-contained review packet; reviewer is read-only; `approve` / `revise` / `block`; at most one targeted re-review |
| Idea → candidates → sample → final with user stops | `idea-to-production` | frozen v1 JSON contracts; two hard user stops (choice, sample review) |
| Agent rules, escalation duties | `control/agents/production-roles.md` | frozen runs, durable feedback, two-failure stop, who may edit skills |

So the earlier plan item "write the orchestration skill draft" is replaced by the gaps below. Creating a
second orchestration skill would duplicate and eventually contradict these.

### Real gaps (still open)

1. **Intake.** No skill or queue turns "own idea / external prompt / trend research" into
   `idea-production-request-v1`. Everything starts from a request that already exists.
2. **Multi-stage chaining under unattended operation.** `adaptive-video-production` stops "before submission
   unless the current task already authorizes the sample". Nothing describes the unattended sequence
   request → candidates → user choice → plan v2 → user approval → night video batch as one hand-off chain
   with the Studio as the approval surface.
3. **Video night batch.** `hermes_night_batch.py` is image-only; video goes through per-shot `local_wangp.py`.
4. **Escalation reviewer configuration.** `frontier-review-escalation` names an "independent OpenAI Codex
   review" via Hermes `delegate_task`. Codex credit is short for about three days, and the user accepts
   Claude or Codex as consultant. Whether Hermes's configured delegation provider can be pointed at Claude
   is **unverified**; the skill text says the configured provider selects the reviewer.
5. **Consultation cap.** The skill limits re-review to one per decision but has no per-day or per-batch call cap.
6. **Studio command surface** and **background DNA** (unchanged from the task document).

## 2. Is Muse's storyboard at the quality the user wants?

Only Muse/Somni's [scenario-rooftop-5am.md](scenario-rooftop-5am.md) is a Muse-authored storyboard in the
repository. [storyboard-draft-quiet-evening-vlog.md](storyboard-draft-quiet-evening-vlog.md) was written by
Codex from Muse's corpus, so it is a different author's work. The user's own taste is **not** established
from text: `approved-storyboards.md` contains no `APPROVED-` entry yet, only a seed example. A text review
can find structural defects; it cannot say whether the result feels right to the user. That needs samples
the user looks at (section 3).

### 2.1 What the rooftop storyboard does well (checkable in the file)

- Every shot has INTENT, ACTION, FRAME, CAMERA, CONTINUITY with start and end state, HANDOFF and NEGATIVES.
- Handoffs are chained by an unfinished action (finger rising → finger completes → head turn → breath → hand
  lowered), which is the T-33 inertia connection the user complained about in #75.
- Prop ledger (P-30) with a new item registered at S5; negatives are phrased as observed failures (P-21).
- Bookend S1/S6 (T-34) and static protagonist with a kinetic world (T-39).

### 2.2 Defects and risks found by reading

| # | Finding | Where | Kind |
|---|---|---|---|
| 1 | **Self-contradicting camera.** The camera is Jihoon's phone, and S5 uses a lens-POV feather. The same shot then cuts to a close-up of Jihoon's face, which his own phone cannot film. | S5 FRAME | Logic defect |
| 2 | **Several framings inside one 5-second clip**, against the document's own "one beat per shot" rule and `capabilities.md` ("avoid too many unrelated actions in one clip"). S2: ECU finger → medium laundry line plus camera jolt. S4: face CU → sky WS → MS. S5: MS → feather ECU → face CU. | S2, S4, S5 | Producibility risk |
| 3 | **Handoff mechanism unspecified.** "Unfinished motion" carries state, but an image-to-video chain from the last frame cannot also change framing (S1 ends wide, S2 starts on an extreme close-up of the finger). The plan does not say how the boundary frame is produced. | S1→S2 | Risk (inference) |
| 4 | **Characters are generic, not the user's DNA.** The lock is "young Korean woman, long black hair, white shirt, jeans"; 민서 and 지훈 are not roster characters. It cannot enter the DNA-bound pipeline without casting. | §4 LOCK | Not production-ready |
| 5 | **Second character has no identity lock.** Jihoon appears on screen in S5 but only the woman is locked. The corpus's own two-person lock (P-16, from #77) is not applied. | §4, S5 | Gap |
| 6 | **Dialogue and audio dependence.** Korean off-screen lines drive S1, S2, S4, S5, S6. The sections of `capabilities.md` read do not establish that the active engine generates matching speech. | §4 prompts | Unverified capability |
| 7 | **Timing inside a shot.** "One full second of stillness" (S5) is an absolute-time instruction; the corpus (P-02, P-03) says models keep order, not time. | Prompt S5 | Minor |

Verdict (model judgment): strong as a directing document and a good test of the corpus grammar; **not yet a
production plan.** Defects 1–3 are fixable in the storyboard itself; 4–5 need casting; 6 needs a capability
check against the real engine.

### 2.3 Draft 0 ("quiet evening") seen with the same checks

It keeps one beat per shot more strictly, but S2 (three items, kettle, half-open lid) and S3 (pour, lid,
chopsticks, timer, one-second wait) are action-dense for 5–6 seconds; the document already names S3/S4 as
the first things to sample. Casting is still open, so it has defect 4's gap as well.

## 3. How to check storyboard quality without guessing

Three layers, cheapest first. The user's own reaction is the only layer that measures "my quality".

| Layer | Who | Cost | Result |
|---|---|---|---|
| A. Static review against a fixed rubric | Hermes with local LLM; one frontier consultation only for disputed items | no GPU | list of structural defects like section 2.2 |
| B. Deterministic validation of the v2 plan | `shot_production_plan.py validate` | no GPU, no LLM | pass/fail on DNA hash, references, handoff fields |
| C. Sample render of the riskiest shots, then the user looks | Hermes via the single queue, with the user's GO | local GPU time only | the user's accept / reject, recorded as an `APPROVED-` or `FAIL-` entry |

Proposed rubric for layer A (taken from `storyboard-director` Evaluation, `candidate-template.md`,
`capabilities.md` and the T/P databases, not invented):

1. Intent survives: premise, emotional movement, payoff are stated and each shot has one purpose.
2. One beat per clip; list every framing change inside a clip and justify or split it.
3. Camera logic: who or what holds the camera, and every shot is physically filmable from that position.
4. Handoff is mechanically realisable: name the boundary frame source and any framing change across it.
5. State ledger: every prop, wound, costume and position has a per-shot state; nothing materialises.
6. Casting: each on-screen person has a DNA record and reference role; off-screen voices are marked.
7. Capability: each demand (speech, long hold, lens POV, mirror) is supported by the active engine or flagged.
8. Never-Render list (T-08) and the named failure memory (`failures.md`) are checked.
9. Cost and repairability: smallest regeneration unit is named.

Layer C is where "does Muse's storyboard reach my quality?" is actually answered, and its outcome is the first
real `APPROVED-` evidence the repository lacks.

## 4. Consequence for the plan

- Step 1 becomes: this gap analysis plus the rubric; no new orchestration skill.
- Editing a canonical shared skill needs a bounded edit assignment naming Claude for that skill
  (`production-roles.md`). None has been given. Any change to `adaptive-video-production` or
  `frontier-review-escalation` goes through shared-skill feedback or a separate scoped assignment.
