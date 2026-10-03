# Failure Memory

This file stores directing failures that should inform future storyboard proposals.

A failure entry is **not** a universal prohibition. Record what failed, why it failed, and what decision was left unspecified. Future directors should avoid repeating the failure blindly while remaining free to use the same technique intentionally in a different context.

## Failure entry template

```text
## FAIL-XXX — Short name

Context:
- Character / episode type:
- Intended effect:

Observed result:
- What actually happened:

Why rejected:
- Specific user or production reasons:

Likely cause:
- Missing or ambiguous directing decision:

Reusable lesson:
- What future directors should remember:

Alternatives:
- Option A:
- Option B:

Do not overgeneralize:
- What remains valid when intentionally chosen:
```

---

## FAIL-001 — Generic face-filling selfie vlog opening

Context:
- Character / episode type: Noa vlog / self-introduction.
- Intended effect: a natural but properly prepared self-recorded introduction.

Observed result:
- Multiple models interpreted `vlog introduction` as an action-camera or phone selfie.
- The first frame became dominated by Noa's face.
- The room, body language, and deliberate camera setup disappeared from the visual storytelling.

Why rejected:
- The opening felt like a generic influencer default rather than a considered directorial choice.
- The viewer learned too little about the space.
- Full-body or larger-scale body language could not contribute to the introduction.
- The result did not communicate that Noa had intentionally positioned the camera before recording.

Likely cause:
- `vlog`, `introduction`, and `natural` were treated as sufficient directing instructions.
- Camera support, subject scale, and reveal strategy were unspecified.
- The model filled those missing decisions with a common selfie prior.

Reusable lesson:
- When a self-recorded introduction matters, explicitly choose the camera relationship before writing the prompt.
- Specify whether the camera is handheld, tripod-mounted, shelf-mounted, table-mounted, or otherwise fixed.
- Specify the opening subject scale and whether the environment should be visible.
- Consider action before speech: enter frame, check framing, sit, settle, then address the camera.

Alternatives:
- Fixed medium-wide/full-body camera; Noa enters, settles, then introduces herself.
- Object-first: action camera or recording light, followed by a wider reveal of Noa and the room.
- Detail-to-reveal: intentional close-up followed by a pull-back or cut to spatial context.

Do not overgeneralize:
- Close-up and selfie openings remain valid when intimacy, spontaneity, motion, travel, urgency, or direct personal energy are deliberately desired.

---

## FAIL-002 — Conversational improvement trapped inside one chat

Context:
- Character / episode type: repeated vlog/storyboard work across Claude, Grok, Hermes, and other models.
- Intended effect: accumulated improvement across sessions and models.

Observed result:
- Repeated prompting inside one chat gradually improved shot choices and continuity.
- A different model or a fresh session did not inherit those corrections and often repeated earlier mistakes.

Why rejected:
- Useful production knowledge remained transient.
- User effort had to be repeated.
- Different agents could not benefit from prior rejection reasons or successful alternatives.

Likely cause:
- Directing lessons existed only as conversation context rather than durable project artifacts.

Reusable lesson:
- Record reusable reasons, not entire chat transcripts.
- Approved storyboard rationale and recurring failure causes belong in Director Memory.
- Character DNA must not absorb one-off camera/editing decisions.

Alternatives:
- Retrieve relevant failure and approved-storyboard entries before ideation.
- Keep fresh candidate generation independent across models, then compare.

Do not overgeneralize:
- Fresh models should not be forced to imitate the previous model's exact answer. Shared memory should constrain repeated mistakes while preserving exploration.

---

## FAIL-003 — Shot sequence loses state between cuts

Context:
- Character / episode type: multi-cut character vlog generated through separate image/video stages.
- Intended effect: several short cuts that feel like one coherent situation.

Observed result:
- Individual shots can look acceptable while the sequence feels disconnected.
- Character position, held objects, body orientation, environment state, or action progression may reset between cuts.

Why rejected:
- The viewer perceives separate generated clips instead of one continuous event.
- Regeneration becomes expensive because the source of the continuity error is unclear.

Likely cause:
- Each shot was described locally without explicit input state and handoff state.
- Visual anchors and continuity facts were assumed rather than written.

Reusable lesson:
- Every cut that depends on the previous one should declare `continuity_from` and `handoff_to`.
- Record persistent state: character screen position, facing, prop hand, wardrobe state, door/window/object state, time/light, and relevant camera relation.
- Split only where a cut creates value or reduces generation risk.

Alternatives:
- Use one long take when spatial continuity is the core appeal and the motion is feasible.
- Use a shared end/start anchor still or reference when separate clips must join.
- Reframe the edit so the cut intentionally hides a state transition.

Do not overgeneralize:
- Discontinuity can be intentional for montage, jump cuts, comedy, memory, or temporal compression. It is a failure only when continuity was intended.

### 2026-09-18 update — second occurrence, and one listed alternative did not work

The completed Noa first-live video reproduced this failure, so it is now a pattern rather than a
single candidate observation. The user reported two separate bad joins on viewing:

- Shot D (cheek poke) into Shot E (cat paw): the fingertips are on the cheeks at the exit and the
  hands are already reset below frame at the entry. This is the plain FAIL-003 shape.
- Shot E into Shot F (dance challenge): the edit hid the join behind a 0.5 s caption card and a
  camera-scale change. The user still read it as wrong.

The second case matters more than the first. "Reframe the edit so the cut intentionally hides a
state transition" is listed above as Alternative C, and **it did not work here**. A decorative
cover over the join is not a physical handoff; the viewer still notices that the body arrived in a
state nobody performed. Treat that alternative as valid only when the covering element is itself
motivated in the action (a hand passing the lens, someone crossing frame, a turn into a wall), not
when it is a title card laid on top of the seam.

Shot A into Shot BC was also reported as slightly jumpy. Cause identified on review: the body
shifts slightly and the image becomes a little brighter at the same time. Neither difference is
large alone; together they read as a reset. The prescribed fix is not tighter exposure matching
but a motivated change — let Noa switch on a light, so the brightness has a visible cause and the
small posture shift rides along with it. See principle 13.

---

## FAIL-004 — Too much freedom delegated to the renderer

Context:
- Character / episode type: idea described in prose, then passed quickly to WanGP/video generation.
- Intended effect: model invents attractive directing details automatically.

Observed result:
- Camera scale, cut structure, timing, reveal order, and action staging drift toward generic defaults.
- Further conversational corrections improve the result but are expensive and session-local.

Why rejected:
- The user's actual idea is under-specified at the visual level.
- Video generation is used to discover composition, blocking, editing, and motion simultaneously.

Likely cause:
- No storyboard/still validation layer between narrative idea and video renderer.

Reusable lesson:
- When visual interpretation is uncertain, first turn the idea into 2–3 storyboard candidates.
- Validate uncertain composition with rough stills before expensive video generation.
- Use the renderer primarily to solve motion/performance after basic spatial decisions exist.

Alternatives:
- text storyboard + spatial sketch;
- still board + I2V;
- one low-cost/low-resolution previz before final render.

Do not overgeneralize:
- Simple or intentionally open-ended shots can still be generated directly when the cost of failure is low.

---

## FAIL-005 — High camera angle changes body proportion and apparent age

Context:
- Character / episode type: Noa first-live video, dance-challenge shot (Shot F), wide framing.
- Intended effect: a wide shot that reveals the whole body and the room for the dance.

Observed result:
- The camera reads as positioned above the subject.
- Noa briefly appears short and childlike, with proportions that do not match her established
  adult character.
- The effect is short but breaks the identity the rest of the video established.

Why rejected:
- The character's age impression is part of her identity, not a framing preference.
- A single shot that reads younger makes the cut feel like a different person, which undoes the
  identity work done by the reference images.

Likely cause (inference, not verified against the engine):
- The plan specifies framing, support and movement, but not camera **height** relative to the
  subject, nor the intended head-to-body ratio at that scale.
- A wide shot with an unspecified height tends toward a slightly high, convenient angle, which
  foreshortens the body and enlarges the head.

Reusable lesson:
- For any shot wider than a medium, decide camera height explicitly: below eye level, at eye
  level, or above, and say what that choice is for.
- An identity reference locks the face. It does not lock body proportion under perspective.
  Proportion is a camera decision.
- Check apparent age on every wide shot of an adult character, not only the close-ups.

Alternatives:
- Option A: place the camera at or slightly below the subject's eye level for full-body shots.
- Option B: keep the high angle but compensate with a longer lens and greater distance so the
  foreshortening is reduced.
- Option C: if a high angle is dramatically wanted, make it motivated (a shelf-mounted phone, a
  window) so the viewer reads it as a camera position rather than a proportion error.

Do not overgeneralize:
- High angles remain valid for vulnerability, comedy, scale contrast, or an explicitly mounted
  camera position, when the resulting proportion is the intended effect.

---

## FAIL-006 — No performance register, so the vlog tone disappears

Context:
- Character / episode type: Noa first-live video, a character recording herself for an audience.
- Intended effect: the awkward-but-endearing feeling of someone filming their own first stream.

Observed result:
- The individual shots are technically acceptable and continuity was largely preserved.
- The user still reported that the "trying to make a cute vlog, a bit awkward about it" quality
  came through weakly.
- The result reads closer to a character being filmed than a character filming herself.

Why rejected:
- That tone is the reason the episode exists. Losing it costs more than any single continuity
  error, because a technically clean video can still miss the point entirely.

Likely cause (inference, not verified against the engine):
- The plan records `camera_relation` as a framing fact (for example "three-quarter eye-level
  medium close-up"), not as a relationship. Nothing anywhere states whether the character knows
  the camera is there, is performing to it, is checking it, or is ignoring it.
- With that decision unstated, the renderer defaults to a neutral observed subject.

Reusable lesson:
- Before writing shots, choose the performance register explicitly and keep it fixed for the
  episode: ignores the camera / aware but not performing / performing to the camera / performing
  and slightly self-conscious about it.
- The register is a separate axis from framing, and it is what separates a vlog from footage of a
  person. External reference material confirms the axis is real and lockable: a found-footage
  piece succeeds by forbidding every camera-directed behavior, which is the same decision made in
  the opposite direction.
- Small self-conscious actions carry this register better than expression adjectives: glancing at
  the lens to check framing, adjusting the camera, restarting a sentence, a small reaction after a
  line lands badly.

Alternatives:
- Option A: give each shot one explicit camera-directed action, however small.
- Option B: keep one recurring self-conscious beat across the episode as a signature.
- Option C: open with the character setting up or checking the camera, so the register is
  established before any performance.

Do not overgeneralize:
- Registers other than "performing to camera" are correct for drama, observational footage, and
  any episode where the camera is not diegetic. The failure is leaving the axis unstated.

---

## FAIL-007 — Closed-mouth instruction is not honoured

Context:
- Character / episode type: Noa, `minimax_h3_ref2va_pruned`, short single-take character shots.
- Intended effect: a silent shot with no dialogue and no lip-sync, stated as "closed mouth, no
  dialogue and no lip-sync" in the prompt.

Observed result:
- The mouth opens anyway, in a way that reads as speaking or about to speak.
- First-live Shot D, 2026-09-16: mouth opens despite the closed-mouth instruction.
- Morning-vlog shot_01, 2026-09-18: mouth clearly open around the 2.3 s mark while she pushes
  herself upright.

Why rejected:
- A silent beat that looks like speech implies dialogue that does not exist, and the edit then has
  to either add a line nobody wrote or cut around the frames.

Likely cause (inference, not verified):
- The instruction is a negative state. The model is given nothing to do with the mouth instead.
- Both occurrences happen during effortful movement, where a parted mouth is a natural motion
  prior.

Reusable lesson:
- This is now a **pattern**, not a single observation: two comparable failures on the same engine.
- Do not rely on "closed mouth" alone. Give the mouth a positive state to hold, for example lips
  pressed together, or a small closed-mouth exhale through the nose.
- Prefer placing silent beats where the body is still. During a push-up, a turn or a reach, expect
  the mouth to open.

Alternatives:
- Option A: write the mouth as a positive held state rather than a prohibition.
- Option B: plan the silent beat on a static pose and put the effort on an adjacent beat.
- Option C: accept the open mouth and design the edit so a line or a breath belongs there.

Do not overgeneralize:
- This is recorded for `minimax_h3_ref2va_pruned`. Other engines are untested.

---

## FAIL-008 — A plan constraint that does not survive the prompt compile is not a constraint

Context:
- Character / episode type: Noa morning vlog, shot_01, first render from the `revision-v6` plan.
- Intended effect: her own enclosed yard, because the episode's sleepwear premise only works if
  the yard is not overlooked. The plan states it on every outdoor shot: walled or hedged on all
  sides, no street, sidewalk, neighbouring window or passer-by in any frame.

Observed result:
- The bedroom window shows a neighbouring house with visible windows, a concrete block wall and
  overhead power lines: an ordinary overlooked suburban view.
- The plan was not wrong. The compiled prompt only said "her own walled garden". The rest of the
  rule was dropped during compilation.

Why rejected:
- The constraint carried the premise of the whole episode, and it was the one thing most likely to
  be filled in with a generic prior if left unsaid.

Likely cause:
- Compiling a structured plan into a prompt is lossy by nature, and there is nothing that
  distinguishes a constraint that may be summarised from one that must be copied.

Reusable lesson:
- Mark premise-carrying constraints and copy them into every prompt that could violate them, at
  full length, even when it feels repetitive.
- A useful test before rendering: for each hard constraint in the plan, find the words in the
  compiled prompt that enforce it. If you cannot point at them, the renderer will not honour it.
- A generic prior fills every gap. "Walled garden" does not exclude the neighbour's window,
  because the model has seen ten thousand walled gardens overlooked by houses.

Alternatives:
- Option A: keep a per-episode list of hard constraints and append it verbatim to every prompt.
- Option B: state the constraint as a visible positive: what should be seen beyond the wall, for
  example only sky and treetops.
- Option C: validate deterministically that each hard constraint's keywords appear in the compiled
  prompt before submission.

Do not overgeneralize:
- Not every plan field belongs in every prompt. Signal density still matters. This applies to the
  small set of constraints that carry the premise.


---

# Added 2026-10-03 — Rooftop 5AM test and the 2026-10-02 night batch (Claude, acting executor)

Evidence labels used below: **[user]** what the user reported after watching; **[prompt]** what the submitted prompt
files say (they are in the session folders); **[frames]** what Claude saw in sampled frames; **[inference]** a
reading of cause that was not tested. Sessions are under `D:\AI_Studio\library\videos\`:
`VIDEO-20261002-112000-rooftop-5am` and `VIDEO-20261002-230503-01-farm-milking` ... `-230841-06-alley-cat`.
All were generated with `minimax_h3_ref2va_pruned`, one identity reference, six (or three) independent clips of about 5 s,
joined afterwards. The user's verdict: Rooftop 5AM and the night batch were better than earlier productions, and
still had many logic defects. Most of the lessons below repeat records that already exist (#24, #66, FAIL-003,
FAIL-004, FAIL-008). They are recorded again because the repetition happened in this project, with a plan written
by Claude, and because a few causes are new.

## FAIL-009 — A beat has no WHERE, and screen direction is not declared

Context:
- Episode type: multi-clip daily-life vlogs (farm, bus trip, rainy morning, alley cat) and the Rooftop 5AM test.
- Intended effect: a place and a layout the viewer can follow from clip to clip.

Observed result:
- [user] Farm: the cow and the people are not positioned consistently; milking happens "under the cow's neck".
- [user] Bus: there are two bus stops; the bus moves backward partway through.
- [user] Rainy morning: the starting location is odd.
- [user] Alley cat: she goes to see the cat, then sits at the first place again and the cat comes to her.
- [prompt] Farm shot 2-3 say "sits on a small stool beside the flank of a calm cow" but never say where the cow's head,
  rear and udder are relative to her. Bus shot 1 says "the bus stop" and shot 5 says "a seaside stop" with no anchor tying
  them to one place; no clip says which way the bus travels. Alley shot 3 does not say where she and the cat are.

Why rejected:
- The viewer reads separate places and contradictory geometry, so the story stops being one event.

Likely cause:
- [inference] Same mechanism as corpus #24: each beat lists actions but not the place; a generic prior fills the
  place, and a different place is invented per clip. Direction of travel is a separate unstated decision.

Reusable lesson:
- Before writing shot prompts, write a stage plan: fixed landmarks, where each character and animal stands relative
  to them, and which way things move on screen. Repeat the anchor phrase in every clip of that place
  ("the same stop with the same bench, bus arriving from screen left").
- A bus, car or walker needs one declared screen direction for the whole piece.
- When a story really does go to a second place, say so as a cut with a visible reason, not as a continuation.

Alternatives:
- A set plate still of the location with positions fixed, supplied as a location reference (reference roles stay
  separate from identity).
- A rough still board validated before video (FAIL-004).
- Fewer, longer clips in one place (FAIL-014).

Do not overgeneralize:
- Not every beat needs a map. A single static location with one actor (rooftop radio) mostly held.

---

## FAIL-010 — Carried objects and body state are not restated in each clip

Context:
- Episode type: rainy morning, Rooftop 5AM, rooftop radio.

Observed result:
- [user] Rainy morning: where are the shoes (the prompt has her slip into sneakers in clip 1 and never mentions them again), an umbrella stands next to the jacket but is not taken
  though it is raining heavily, and the shoulder bag is put down and forgotten.
- [user] Rooftop radio: she starts by holding shoes in her hand.
- [user] Rooftop 5AM (2026-10-02): in shot 1 the arm is raised high; in all of shot 2's variants the hand is at face
  or chest height, which reads as showing the number one instead of calling the wind.
- [prompt] Rainy shot 1-2 say the bag stays on her shoulder; shot 3 never mentions the bag. The umbrella appears only in
  the still's description. Rooftop 5AM shot 1 and shot 2 say "finger" and never say how high the arm is. The radio's
  subject definition lists "white canvas sneakers" together with the garments.

Why rejected:
- Objects and poses reset between cuts, or appear without a reason. The viewer notices the missing bag and umbrella.

Likely cause:
- [inference] Same as corpus #66: an object exists only in clips whose text mentions it; it vanishes when a clip
  omits it and can return when mentioned again. For the radio shoes, listing footwear next to garments probably made
  it a carried object (untested).
- The plan had no per-clip ledger covering worn, carried and body-pose state.

Reusable lesson:
- Keep a state ledger per clip (start and end): what is worn, what is held in which hand, where bags and umbrellas are,
  arm and hand height, door state. Restate every carried item in every clip where it must still exist.
- Handle transitions that need hands (putting on a jacket while carrying a bag) with an explicit step or a cut:
  "she lifts the bag off her shoulder, puts the jacket on, puts the bag back".
- Write footwear as worn ("on her feet"), not as a list item beside props.
- A story premise (heavy rain) implies props (umbrella): decide them, do not leave them to the set dressing.

Alternatives:
- A shared end/start anchor still between clips (FAIL-003), or a longer clip that contains the transition.

Do not overgeneralize:
- Props that are irrelevant to the story may stay unmentioned; the risk is for objects the viewer tracks.

---

## FAIL-011 — The cause of the story's turning point is never written

Context:
- Episode type: rooftop radio (30 s, one place).

Observed result:
- [user] The batteries look odd, and the reason the radio gets fixed is unclear. She also sits apart from the radio.
- [prompt] Clip 2 says she "checks two batteries and presses them back into place", then switches on and still hears
  static; clip 3 extends the antenna and rotates the radio; clip 4 the melody breaks through. No clip states what was wrong or why
  that action fixes it. Clip 5-6 say she sits in the chair "beside the table" with no distance.

Why rejected:
- The turning point reads as luck, so the emotional payoff has nothing under it.

Likely cause:
- [prompt] The plan listed repair actions, not a cause: problem, cause, fix, and the visible proof.
- [inference] The model renders actions, not the logic between them.

Reusable lesson:
- For any problem-then-solution beat, write one line: what is wrong, what makes it wrong, what action fixes it, and
  what the viewer sees as proof (the radio's dial light turns on when the battery is turned the right way).
- Prefer one clear cause over a sequence of plausible actions.

Alternatives:
- Pick a story whose fix needs no small mechanism (a sunset arriving, someone arriving).
- Show only the result and let the viewer assume the repair (ellipsis, T-01), when the repair itself is not the point.

Do not overgeneralize:
- A quiet atmosphere piece does not need a puzzle. The lesson applies once the story promises a fix.

---

## FAIL-012 — Time and distance are not designed

Context:
- Episode type: bus trip to the sea, alley cat.

Observed result:
- [user] Bus: the sea is visible right after boarding; the last spoken line is unclear.
- [user] Alley cat: unclear whether it is the same day or a sequence in time.
- [prompt] Bus clip 2 says nothing about the outside and clip 3 only "the passing town"; the sea first appears in my
  clip 4 text, yet the rendered clip 2 interior already shows it [frames]. Alley clip 1-3 give no marker that the morning is continuous.

Why rejected:
- A journey that takes no time and a day with no order read as editing mistakes.

Likely cause:
- [inference] The renderer fills unspecified surroundings with its most likely image, and a bus window next to a sea
  scene gets the sea. Time passing is not visible unless something changes visibly (scenery, light).

Reusable lesson:
- Specify a progression of what is seen outside (town, then fields, then a strip of sea) and where it first appears.
- Say whether clips are continuous in real time or separated by an ellipsis, and show the proof (same light, a
  clock, scenery that has changed).
- Keep a spoken line short and plain; if its sound matters, check it before relying on it.

Alternatives:
- Cut to the destination with a clear change in light or place.

Do not overgeneralize:
- Why the final bus line was unclear is not known; the audio was never checked by Claude.

---

## FAIL-013 — Objects named but not described; small mechanisms at the model's limit

Context:
- Episode type: village market, rooftop radio.

Observed result:
- [user] The market keeps calling napa cabbage lettuce; the scale looks odd; it is unclear whether the wrapping is
  newspaper or a plastic bag. The radio's batteries look odd.
- [prompt] The market dialogue says lettuce (상추) while the visual text says "lettuce" without a description of leaf
  shape. The same prompt set also gives a reusable cloth bag in clip 2 and newspaper wrapping in clip 3, so the
  plan itself left two materials unresolved.

Why rejected:
- A spoken noun that disagrees with the picture, and objects whose material changes, break believability.

Likely cause:
- [inference] A name alone selects the model's average object; leafy vegetables and market scales are ambiguous
  without shape and material. Battery compartments and scale needles are small mechanisms that are rendered
  unreliably (see also T-08 for contact moments).

Reusable lesson:
- Describe each key object by shape, color and material, and make the spoken noun match what the picture shows
  ("loose-leaf lettuce with ruffled green leaves, not round heads").
- Decide one material per purpose (wrapping in one paper kind, one bag type) across all clips.
- Avoid small mechanisms as the story's turning point; show their result instead.

Alternatives:
- Choose a simpler prop (a basket instead of a scale).
- Cut away before the mechanism is operated and show the outcome.

Do not overgeneralize:
- Background props need no description. The lesson is for props that are handled or named on screen.

---

## FAIL-014 — Splitting a short story into many independent clips multiplies the seams

Context:
- Episode type: all night-batch productions (six clips of about 5 s per 30 s) and the Rooftop 5AM test.

Observed result:
- [user] Most items in FAIL-009 to FAIL-013 are position, state and time breaks that occur at cuts between clips.
- [prompt] Every clip received only the same identity reference and its own text. No clip received the previous
  clip's last frame, a location plate, or the state of the previous clip beyond what the text repeated.

Why rejected:
- Each seam is a place where the model can re-invent the place and the objects.

Likely cause:
- A choice made by Claude: 5 s clips were what worked for the first test, and the night batch copied it. FAIL-003
  already says to split only where a cut creates value or reduces generation risk; this split did neither for scenes in one place.
- [frames] In the shot-2 experiment the 8 s clips (with in-clip cuts) looked fuller than the 4.5 s ones; [inference] fewer, longer
  clips would remove seams, but this has not been tested on these stories.

Reusable lesson:
- Decide the clip boundaries from the story: cut where a place or time really changes, not at a fixed duration.
- Where a cut is needed, hand off by a shared end/start still or a location plate, not by text alone (untested here).

Alternatives:
- Three clips of about 10 s with `[Shot N] At 00:0x` cuts inside each clip.
- Use the first-and-last-frame model (`minimax_h3_fl2va_pruned`) to chain clips (not tested).

Do not overgeneralize:
- The bus trip held two separate identities across six clips and its failures were about place and time, not identity. Splitting
  is not the only cause of any single defect.

---

## FAIL-015 — The author's own frame review checked identity and props but not logic

Context:
- Process: Claude wrote the prompts, rendered, then reviewed sampled frames before reporting to the user.

Observed result:
- [frames] Claude reported the night-batch videos as rendered "as designed", and Rooftop 5AM shots 1-3 as matching the storyboard,
  after checking identity consistency, key props and a few frames per clip.
- [user] The same videos contain the defects in FAIL-009 to FAIL-013, which a viewer sees on first watching.

Why rejected:
- The report overstated quality, so the user's first look was a surprise instead of a confirmation.

Likely cause:
- The review looked at what the plan listed (identity, a few props) and not at the logic across clips (where is the
  cow, which way is the bus going, where did the bag go). The author reviewed their own plan.

Reusable lesson:
- Review against a fixed checklist: layout and direction, per-clip state, cause of turning points, time order, object
  appearance, spoken line audibility. Report which items were checked and which were not (for example, motion and sound are not judged from stills).
- Have a different pass than the author do the logic review (video-candidate-review, or a frontier consultation for the
  disputed items) before rendering, and again after on the finished video.

Alternatives:
- Check the plan before rendering by finding, for each hard constraint, the words that enforce it (FAIL-008).

Do not overgeneralize:
- Frames still cannot judge motion, timing or sound; those stay with the viewer.

---

## Not yet explained

- The farmer's explaining scene is odd [user]; the cause is unknown. The prompt describes only an open-hand gesture and a bucket placement.
- The market scale looks odd [user]; shape and mechanics were not specified, so FAIL-013 is a suspected cause only.
- The last bus line is unclear [user]; whether the cause is wording, audio generation or mixing was not checked.
