# Autonomous Video Quality Guide

Audience: Claude, Muse/Somni, Hermes/Meromero, and other XAI video-production agents.
Purpose: turn an approved idea or an autonomous ordinary-vlog brief into a coherent, reviewable production plan
without depending on frontier-model intervention for routine decisions.

This is an execution guide, not a catalogue of prohibitions. The goal is a result the user enjoys, not maximum
prompt compliance. It distills recurring lessons from `failures.md`, `../failure-db.md`, production incidents, and
Claude's Hermes pipeline review. Those sources remain the evidence; this document is the compact operating layer.

## Definition of a good default result

Unless the user asks for spectacle or experimentation, prefer a vlog that has:

- one immediately understandable everyday premise;
- one place, or a clearly motivated move between places;
- a small visible change: intention → action → consequence → quiet payoff;
- restrained, natural behavior rather than exaggerated acting;
- enough environmental detail to feel lived-in, but no story-critical clutter;
- few enough cuts that identity, space, props, and emotion can remain coherent.

“Ordinary” does not mean generic. Give the episode one specific human observation, object, habit, inconvenience, or
small pleasure. Do not compensate for a weak premise with more shots, dialogue, props, or camera tricks.

## Compact autonomous procedure

Hermes/Meromero should execute these as separate bounded passes. Do not ask one generation pass to invent,
validate, compile, and review the whole episode.

### 1. Recover the actual intent

Read the user's request and current approved brief again. Write three short fields:

```yaml
viewer_should_understand:
viewer_should_feel:
must_remain_true:
```

Do not evaluate a planned element as a mistake merely because it was forgotten during review. If the intent is
ambiguous, choose the least assumption-heavy ordinary interpretation; do not manufacture complexity.

### 2. Choose the smallest story that delivers it

Use one main event and one payoff. Prefer one location. Add a location change, second character, important dialogue,
or mechanical prop only when it carries the premise.

Default ordinary-vlog shape:

```text
space and current state
→ one motivated action
→ one readable consequence or discovery
→ a restrained emotional response
→ a short settling image
```

If removing an element does not damage that chain, remove it from the production plan.

### 3. Select clip boundaries from story logic

- Give each generated clip one primary beat and one coherent camera state.
- Cut when place, time, viewpoint, or dramatic function genuinely changes—not at an arbitrary fixed duration.
- A continuous action with important spatial state is safer in one clip when the renderer can support it.
- A cut creates a continuity obligation. Name the handoff source: accepted last frame, location plate, first/last
  frame anchors, deliberate occlusion/bridge, or an intentional montage discontinuity.
- Independent clips with text-only continuity are a montage unless proven otherwise. Do not pretend that the engine
  remembers the preceding clip.

For a simple 20–30 second vlog, start with two to four production clips, not six fixed five-second clips. This is a
candidate default supported by repeated seam failures, not a universal duration law; validate it per engine.

### 4. Build the visible-world packet before prompts

For every location, record fixed landmarks and screen direction. For every clip, record entry and exit state:

```yaml
where:
camera_owner_or_support:
screen_direction:
people_and_positions:
worn:
held_left:
held_right:
important_props:
body_pose_and_hand_height:
emotion_and_visible_cause:
time_or_ellipsis_evidence:
entry_state:
exit_state:
```

Only track details the viewer will notice. Key objects need stable shape, color, material, owner, and purpose. A
problem-and-solution beat must state the problem, visible cause, fixing action, and visible proof. Gaze targets must
be physically present or the framing must make their absence intentional.

### 5. Bind references by role and reject contradictions

- Keep identity, wardrobe, location, pose/action, and boundary-frame roles separate.
- Check actual anatomy, left/right orientation, aspect ratio, crop, and visible content; filenames are not evidence.
- Send only references needed for the current clip. Do not send sitting, standing, and walking states together merely
  because all may appear somewhere in the episode.
- Do not allow an earlier-state pose or prop reference to compete with the required current state.
- Prefer a native-aspect reference. Record any intentional crop or padding instead of silently accepting it.

Character DNA preserves identity; it does not replace temporal state. A boundary frame preserves temporal state;
it does not become a new identity master.

### 6. Respect the renderability boundary

Classify every difficult transition:

```text
DIRECT            render the complete transition
PARTIAL           render only reliable portions
HIDE              place the unreliable state change behind a cut or occlusion
CONSEQUENCE_ONLY  omit the fragile mechanism and show its readable result
```

Prefer the simplest class that preserves the story. Small mechanisms, precise contact, long dialogue synchronization,
and several framings inside one short clip are risks to redesign, not invitations to add more prose.

### 7. Compile one prioritized runtime prompt

Compile from the approved packet; do not concatenate complete identity, portrait, storyboard, and camera prompts.
Put hard visible invariants first, describe temporal changes in order, then add only useful style detail. Prefer
positive observable states over a wall of negatives.

Before submission ask:

1. Is there one coherent subject count, body state, place, and camera state at each moment?
2. Does the clip contain one primary beat?
3. Do the prompt and references agree on aspect, laterality, clothing, props, pose, and entry state?
4. Is the turning point's cause visible?
5. Is the exit state usable by the next clip?

If the answer is no, repair the packet or split/recombine the story before changing engines.

### 8. Review independently and repair narrowly

The authoring pass must not be the only review. Use a separate review pass before rendering and again on the finished
video. Review the moving video and audio when judging motion, timing, gaze transitions, or speech; sampled frames
cannot prove them.

Review in this order:

1. Does the intended small story read without explanation?
2. Are place, screen direction, time, and cause-and-effect coherent?
3. Do identity, wardrobe, carried objects, body state, and emotion persist?
4. Are actions physically plausible and the important objects recognizable?
5. Does the result feel natural and pleasantly specific rather than merely compliant?

Preserve accepted clips. Repair only the failed responsibility layer or clip. After two materially similar failures,
stop and diagnose or escalate; do not hide the problem with repeated generation.

## Failure diagnosis order

When a result fails, examine causes in this order:

```text
contradictory or unsuitable inputs
→ overloaded story / wrong clip packaging
→ missing spatial, causal, or state information
→ runtime-prompt compilation
→ engine or model limitation
```

Do not begin by adding locks. First remove contradictions and reduce the task. Switch engines only after the input
and packaging are coherent enough to make the comparison meaningful.

Record `observed`, `evidence`, `cause_hypothesis`, `confidence`, `correction`, and `rerun_result`. “A principle was
written” is not the same as “the correction was verified.” Keep model/version-specific findings scoped to that
model/version.

## Learning the user's taste

A guide can reduce known defects but cannot guarantee taste. The system learns taste from durable decisions:

- preserve why the user accepted or rejected a storyboard or result;
- distinguish a correctness defect from a creative preference;
- promote repeated preferences, not isolated guesses;
- retain successful outputs and their exact inputs as comparison evidence;
- use the smallest representative sample when a new directing choice is genuinely uncertain.

Failure memory is a toolbox and warning system, not a gate. Approved examples and rejection reasons should gradually
shift the default choices, while explicit current direction always wins.

## Division of responsibility

- **Muse/Somni:** curate evidence and creative lessons; label inference and avoid turning one recipe into canon.
- **Claude:** identify story, continuity, and production-package defects; keep judgment separate from verified facts.
- **Hermes/Meromero:** execute the compact passes, emit structured artifacts, validate, review independently, and
  stop uncontrolled retries.
- **Codex/integration owner:** promote repeated lessons into validators, adapters, or shared skills when evidence and
  contract impact justify it.

The desired end state is not Hermes copying Claude or Muse. It is Hermes making a small number of sound decisions,
checking them mechanically where possible, and spending creative freedom only where failure will not break the story.
