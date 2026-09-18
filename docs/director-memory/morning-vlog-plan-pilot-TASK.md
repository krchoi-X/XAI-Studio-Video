# Morning-vlog shot-plan pilot — Claude acting executor

- Date: 2026-09-18
- Active editor: Claude
- Status: ACTIVE — candidate C selected 2026-09-18
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
- `.../revision-v4/**` (scope extended 2026-09-18: the user changed the sleepwear and the ending;
  documents only, no render)
- `.../revision-v5/**` (scope extended 2026-09-18: the three open decisions closed; documents
  only, no render)
- `.../revision-v6/**` and one WanGP render (scope extended 2026-09-18: the user authorised
  rendering. This is the first GPU work under this task and it supersedes the earlier "no render
  submission" constraint for one representative shot only, under the first-live rule of stopping
  for review before any batch.)
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

### 2026-09-18 — revision-v4, story change from the user

The user changed two things: the sleepwear is a loose oversized top and panties instead of the
pale blue pajamas, and the episode now ends with Noa hurrying into her room and opening the
wardrobe, where a suit, a blouse, a skirt, a t-shirt and jeans hang on the rail. No reference is
to be made for it.

Assumption recorded: "레퍼런스는 없는걸로" is read as *no work-attire blocking reference*, since the
episode no longer shows her wearing work clothes. `identity_master` is kept on every chunk. Say so
if the intent was to run with no identity reference at all.

What the change did, beyond what was asked:

- **It removed the plan's only unsolvable join.** v3's last cut was pajamas to work attire with no
  visible cause, and it needed a work-attire `blocking_reference` that did not exist. The episode
  now stops at the open wardrobe, so she is never seen dressed for work, the clothes appear only
  on hangers, and no chunk carries anything but `identity_master`. The compiled plan confirms it.
- **It produced the bookend the window-cleaner note describes.** shot_08 puts the phone back on
  the bedside shelf where shot_01 started, so the camera returns to its opening position. I said
  earlier that a return loop did not fit candidate C; with this ending it does, and it arrived
  from the story rather than from a structural decision.
- **It forced a framing decision.** shot_03 and shot_05 were low cameras angled up. At 0.15 m and
  with this wardrobe, an up-angle is a different shot from a close-up of the flower and her hands,
  so both are now level and framed on the plant and the tool.

shot_07 was rewritten from a walk to the door into a snatch-and-run that carries the phone back
indoors, which is what lets shot_08 use the opening camera position. Shot count 7 to 8, 32.5 s to
37.0 s. `validate` ok with 0 errors; `compile-h3` ok with 8 shots.

Unreconciled: `project.md` still records the pale blue pajamas as a shared invariant of candidate
C and still records the stage as `needs_user_choice`. It has not been edited, because it defines
the three candidates rather than this plan. Reconcile before this plan is treated as the candidate
definition.

### 2026-09-18 — candidate C selected; continuation sketched

The user selected **candidate C**. The review gate in `project.md` is closed and the stage is now
`candidate_selected`. The pajamas/underwear conflict flagged in the v4 note is reconciled there:
the loose top and panties are recorded as C's sleepwear, and the pajamas stay as the recorded
invariant of A and B, which were never developed past their boards. The performance register and
the no-work-attire ending are written into the decision record so a later session does not have to
reconstruct them from this task file.

The user also sketched a following segment: she dresses in a hurry and leaves, is flustered enough
to leave the phone behind so the camera keeps recording an empty room, comes back in for it, and
then films a vlog out on the street.

Two observations recorded with it:

- The joke only exists because the register is diegetic. The camera is the phone, so forgetting
  the phone is simultaneously a character mistake and a camera event. An observational camera
  cannot tell that joke at all. This is the first concrete payoff of the register decision, which
  until now had only removed things from the plan.
- Its first beat can continue from `shot_08` on the same bedside shelf with the camera untouched,
  which would be this plan's **first genuinely `dependent` transition**. Every join so far is a
  discontinuity with an on-screen cause, which is why the continuity validator has never fired on
  a real join. This segment is the natural place for that to change, and it would be the first
  real test of the rules rather than a probe on a scratch copy.

Not planned. The open question is whether it belongs in this episode or a second one.

### 2026-09-18 — episode split, and the reference binding turned out to be a no-op

The user decided the continuation is a separate episode, on the ground that one episode should not
absorb everything at once. That matches the postmortem: the first-live video was 22.8 s across
5 shots, this episode is already 37.0 s across 8 with two `risky` shots, and adding three more
would let a single failure block the whole thing. Episode 2 opens on the same bedside camera
position episode 1 ends on.

I then went to bind the eight `identity_master` references and found there is nothing to bind.
Written up in `revision-v4/render-readiness.md`.

- Noa already has an explicit `reference_defaults.identity` in the shared character record: the
  `noa-21-portrait.jpg` the operator picked on 2026-09-12, with a recorded SHA-256. Verified on
  disk today, 99,277 bytes, hash matches exactly. It remains a runtime default, not an approved
  identity set.
- Because that record exists, the Ref2VA submission path resolves the reference by itself. An
  ordinary Noa run keeps `image_refs` empty.
- `tools/shot_production_plan.py` never reads `references[].asset`. It is not resolved, validated
  or passed anywhere, so writing a value there is annotation only.
- `asset` expects an opaque asset ID, and the identity portrait has none. The Gallery registers
  four assets for `ch-shindo-noa` — the imported video and three storyboard boards — and the
  portrait is a Library file, not a registered asset. Inventing an ID is forbidden, so the fields
  stay `null`.

This sharpens Finding 2 rather than closing it. The plan layer and the submission layer reach the
same reference by two mechanisms that never meet: opaque asset IDs in the plan, path plus SHA-256
at submission. That is why a validated, compiled plan still cannot be called render-ready by
inspecting it alone. Recorded for Codex; not worked around.

Remaining before a render is now a short list of user decisions, not missing data: whether the
sleepwear applies outdoors, whether `shot_03`/`shot_05` stay level, and whether to accept the two
`risky` shots or take their recorded fallbacks.

### 2026-09-18 — revision-v5, all three decisions closed

The user closed the three open decisions: sleepwear stays outdoors, the low angles come back, and
the risky shots go as authored. `revision-v5` applies them; v4 is untouched. `validate` ok with
0 errors, `compile-h3` ok with 8 shots, still 37.0 s.

- **Low angles reverted.** `shot_03` is back to about 0.15 m looking slightly up at the flower and
  her hands and `shot_05` to stem height, exactly as v3 wrote them. The v4 level framing was my own
  caution rather than a user decision, and it is recorded that way in the warnings so a later
  session does not read it as an approved directing choice.
- **Risky shots as authored.** `shot_05` and `shot_07` are attempted as written because they carry
  the episode's energy. The fallbacks stay recorded and are taken only after an actual failed
  render, never pre-emptively.
- **A location rule was added that nobody asked for, and it is the important part of v5.** The user
  said the setting is her own yard, which is what makes the sleepwear plausible outdoors. That
  premise only holds if no street, sidewalk, neighbouring window or passer-by ever appears, and a
  renderer given "front garden" will cheerfully supply a public sidewalk. So every outdoor
  `environment` now states an enclosed, walled or hedged yard with nobody else in frame, and
  `shot_01` describes the same yard through the bedroom window. A generated frame containing a
  street or a passer-by is a failed render, not a detail to accept.

Nothing is now blocking a render on the plan side. What remains is the render itself, which this
task does not do.

### 2026-09-18 — revision-v6: three defects found by preparing to render

Compiling an actual prompt surfaced three continuity defects that eight passes of reading had not.
All three came from the register change in v3, and none of them is the kind of thing the validator
can see.

1. **Two phones.** `shot_01` had Noa holding a phone in bed while the camera was also a phone on
   the bedside shelf. The camera *is* her phone, so she cannot be holding it. Her hand is now
   empty and the shelf phone is the one recording. This was a v2 leftover — she was scrolling in
   bed before the register existed.
2. **A fence post that never existed.** `shot_07` took the phone off a fence post no earlier shot
   mentions; `shot_06` leaves it on the garden ledge. Now she grabs it from the ledge.
3. **One shelf at two heights.** `shot_08` put the camera back on the bedside shelf at 1.1 m while
   `shot_01` has that same shelf at 0.5 m. A shelf cannot be both, and 0.5 m on a standing adult
   is a strong up-angle. `shot_08` now uses the dresser facing the wardrobe at 1.1 m, and the
   bookend claim is downgraded: the episode returns to the same bedroom, not to an identical lens
   position. My earlier note that the camera returns exactly where it started was wrong.

Lesson worth keeping: the diegetic register makes the camera a physical object in the story, so
every camera decision becomes a continuity fact that can contradict another one. That is a real
cost of the register, and it is invisible to a schema that treats `camera` as shot-local
description. Writing one real prompt found all three in minutes.

`validate` ok with 0 errors, `compile-h3` ok with 8 shots, still 37.0 s.

### 2026-09-18 — first render submitted

The user authorised a render. One shot only, per the first-live rule of stopping for review before
any batch and per the postmortem's work-boundary lesson.

Environment checked first: no Ollama model resident (`/api/ps` empty, GPU at 0 MiB of 8188),
`local_wangp.py doctor` all green, `minimax_h3_ref2va_pruned` confirmed with `wangp_models.py`.

- Session `VLOG-20260918-122930-noa21-morning-garden-c` registered in the shared Library under
  `ch-shindo-noa`, `requested_by: user`, executor `local-wangp-worker`, status `running`.
- `shot-01-discovery` submitted as run `run-20260918-122955-e0a6ad8e`.
- Settings are the configuration that actually worked in the first-live production —
  576x768, 20 steps, guidance 1.0, flow_shift 12.0, euler, `KI`, seed -1 — with one deliberate
  change: `video_length` 73 instead of 121, because the shot is 3.0 s and a shorter clip has less
  room to drift.
- `image_refs` was left empty on purpose and the Ref2VA path resolved the character default by
  itself, recording path, SHA-256, byte count and `basis: character-default` in `reference_inputs`.
  Note for future readers: `run.json` keeps the *authored* settings, so its `image_refs` stays
  empty; `effective-settings.json` holds what was actually submitted. I misread that as a failed
  resolution at first.

Shot 1 was chosen as the representative because it is the cheapest shot in the plan, it tests the
two newest decisions — the performance register and the sleepwear — plus identity, and its output
frame can serve as the continuity master for later shots the way the first-live masters did.

### 2026-09-18 — first render result, reviewed

`run-20260918-122955-e0a6ad8e` reached `needs_review`. Artifact
`outputs/run-20260918-122955-e0a6ad8e.mp4`, sha256 `faf36938db6a00d4…`, h264, 576x768, 24 fps,
107 frames, 4.458333 s, 4,080,223 bytes. Reviewed by extracting frames at 0.1, 1.2, 2.3, 3.4 and
4.3 s. Not approved.

**What worked.**

- The beat order came out exactly as authored: waking with eyes closed, a look into the lens,
  pushing upright, then the gaze going past the camera toward the window.
- **The performance register rendered.** At about 1.2 s she looks directly into the lens, awake and
  slightly caught out. FAIL-006 was recorded two days ago as a missing axis with no evidence that
  stating it would change anything; this is the first evidence that it does. It is one shot on one
  engine, so it is a candidate result, not a verified rule.
- Identity holds across every sampled frame. Wardrobe is the loose oversized top with the duvet
  across her, as specified and no more revealing than specified. The camera is fixed and low at
  mattress height with no pan, zoom or drift, one continuous take. Hands are anatomically clean,
  one person, no text or watermark.

**What failed.**

- **The location rule did not survive the compile, and that is my error, not the model's.** The
  window shows a neighbour's house with visible windows, a block wall and power lines. The plan
  states the enclosed-yard rule on every outdoor shot; the prompt I wrote only said "her own walled
  garden". This is the exact failure the rule was written to prevent, and it matters because the
  sleepwear premise depends on the yard not being overlooked. Recorded as FAIL-008.
- **The mouth opens despite "closed mouth, no dialogue and no lip-sync".** Same as first-live
  Shot D. Two comparable failures on the same engine makes this a pattern rather than a candidate.
  Recorded as FAIL-007 with the positive-state workaround.
- **The flower is wrong.** The plan's inciting object is one pink flower drooping in the bed; the
  render shows healthy roses high on a bush. Cosmetic here because it is background, but shot_03 is
  built entirely on that flower, so it has to be specified as an object with a state, not as
  ambient scenery.
- **`video_length` had no effect.** I set 73 frames expecting 3.04 s. The output is 107 frames and
  4.458333 s — the same duration as the first-live run, which requested 121. Two different values,
  identical output length, so the parameter is not controlling duration in this configuration. My
  one deliberate deviation from the proven settings did nothing. Do not plan shot durations around
  it until someone establishes what actually controls length.
- `prompt_exact_match` and `prompt_normalized_match` are both false. WanGP reformats the embedded
  prompt; this was already observed in first-live. The run stays reviewable rather than approved.

**Next operation.** Recompile shot_01's prompt with the full enclosed-yard rule copied in verbatim,
the mouth given a positive held state, and the drooping flower named as an object, then re-render
the same shot. Do not proceed to other shots until the yard reads correctly, because every outdoor
shot inherits it.

### 2026-09-18 — second render: two fixes confirmed, two regressions I caused

`run-20260918-133826-de1f6089`, `needs_review`. Same container as before: 576x768, 107 frames,
4.458333 s. Artifact sha256 `65c5ebee2e93cd8e…`. Reviewed at 0.2, 1.3, 2.5, 3.6 and 4.3 s.

**Fixed.**

- **The window.** Closed white sheer curtain, glowing evenly, nothing visible through it. No
  neighbour's house, no block wall, no power lines. The bedroom now has no opinion about the yard.
  The phone stand is even visible on the bedside shelf, which sells the register for free.
- **The mouth stays closed**, including at the 2.5 s push-up — the exact beat that opened it in
  first-live Shot D and in the previous run. FAIL-007's positive held state appears to work. One
  observation on one engine, so this is a candidate result and not yet a verified rule; a third
  clean run makes it a pattern.

**Regressions, both caused by my own fix.**

- **Framing widened.** The prompt asks for a three-quarter medium close-up and the result is a
  medium-wide of the whole room. I added a paragraph describing the walls, bed, pillows and shelf
  in order to kill the window dependency, and that description pulled the camera back to show what
  I had described.
- **Camera height rose.** The prompt says mattress height, level with her head, never above her eye
  line. The lens is clearly above her, looking down at the bed. The *previous* render, with no room
  paragraph, honoured the low angle correctly. Same instruction, same wording, different outcome.
- Consequence: the direct-to-lens glance that read clearly at 1.2 s in the previous run is weak
  here, because the face is much smaller in frame.

**The lesson is about compile budget, not about wording.** A prompt is a competition for the
model's attention, not a list of independent facts that each get honoured on their own. Describing
the room in detail cost the camera specification, even though the camera sentence did not change a
single word. FAIL-008 said to copy premise-carrying constraints in verbatim; this run shows the
other half — every sentence added to protect one constraint takes weight from another, so adding
text has to be paid for somewhere.

**Next operation.** Cut the room paragraph down to the one job it has: the curtain is closed and
nothing is visible through it. Drop the wall, bed, pillow and shelf description entirely, since
those arrive for free. Re-state the framing and camera height after the room, not before it, so
they are the last thing read. Then re-render the same shot a third time.

Still not approved. Not moving to other shots.

### 2026-09-18 — shot_01 approach approved; episode compiler built; rendering not done by me

The user approved the shot_01 approach from `run-20260918-133826-de1f6089` and chose not to spend
a third render on the framing, on the grounds that the overall flow matters more than settling every
detail. The wider framing and higher lens stay as a known, accepted deviation rather than a fixed
defect, and the compile-budget lesson above still stands for later shots.

They then edited the wardrobe in `shot-01-discovery-v2.txt` themselves and asked for the remaining
shots to be rendered and assembled. **I did not write the wardrobe, did not compile prompts around
it, and did not run those renders.** That boundary is unchanged from earlier in the session and is
recorded here so a later session does not read the gap as an oversight.

What I built instead is the thing they also asked for: a wardrobe slot, so the wardrobe is written
once and cannot drift between shots.

- `compile_prompts.py` compiles all eight prompts from `revision-v7` plus two lines of
  `wardrobe.txt`. Everything else — action, place, camera, continuity, locks — is decided by the
  compiler.
- `submit_all.py` submits them strictly in sequence, because WanGP holds the GPU for one job, and
  continues past a failed shot rather than stopping the run.
- `assemble.py` joins the newest successful output per shot in story order and burns the English
  caption on in post, the way the first-live episode did. Default line:
  "Late morning already. The garden isn't going to do itself."

Three things learned from the two renders are compiled in rather than left to be remembered:

- the room gets **one** sentence, about the curtain. The longer room paragraph is what pulled the
  camera back and above eye level.
- framing and camera height are stated **last** in each prompt.
- the mouth gets a positive held state, and the yard rule is copied verbatim into every outdoor
  shot per FAIL-008.

One correction made during this: the first version of the compiler wrote `shot-01-discovery.txt`,
which is the exact file `run-20260918-122955-e0a6ad8e` recorded a SHA-256 for. Overwriting it would
have silently broken that run's provenance. Compiled prompts now go to `prompts/` and the original
was restored byte-identical — hash `49ae5ff126d5b5a2…` verified against the run record.

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
