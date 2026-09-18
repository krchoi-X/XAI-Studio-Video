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
