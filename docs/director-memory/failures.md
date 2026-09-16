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
