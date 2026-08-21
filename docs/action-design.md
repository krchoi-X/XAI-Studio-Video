# Action Design

This document captures reusable action-generation principles for scenes with fast movement, multiple actors, impacts, stylized physical effects, or reactive camera work.

The goal is not to imitate one martial-arts prompt. The goal is to extract a general production grammar that can survive across models and genres.

## 1. Start with an Action Grammar, not adjectives

Avoid relying on vague instructions such as:

```text
fight intensely
move extremely fast
make the action cinematic
```

Instead, describe a causal chain of verbs:

```text
evade → parry → redirect → counter → sweep → recover
```

An Action Grammar defines how movement connects. It should answer:

- what triggers the action
- how one movement causes the next
- whether momentum is redirected or stopped
- whether the actor resets between actions
- where the chain settles

For continuous combat or chase scenes, explicitly discourage reset poses and turn-taking when they would make the action artificial.

## 2. Multi-agent action must specify interaction logic

When several actors are present, do not assume the model will infer simultaneous pressure correctly.

Useful interaction constraints include:

- attackers may overlap in time rather than wait politely
- one actor can force another actor's path to change
- collisions, blocks, and redirections should affect subsequent positions
- background actors should remain spatially accountable instead of disappearing
- the main subject should not teleport between opponents

For complex scenes, define entry and exit blocking for each major beat.

## 3. Use a Physics Lock for stylized effects

If the scene contains extraordinary speed, energy, impact effects, supernatural-looking particles, or exaggerated force, define the physical rules that make the effect believable.

A Physics Lock should specify four things:

```text
Source
→ what physically creates the effect

Allowed manifestation
→ how the effect may appear

Forbidden manifestation
→ what the model must not invent

World reaction
→ what nearby matter does in response
```

Example:

```text
Source: friction and direct physical contact
Allowed: brief branching static discharge at contact points
Forbidden: beams, projectiles, aura, teleportation
World reaction: dust, loose paper, hair, and fabric respond to velocity and impact
```

The key principle is that visible effects should emerge from readable causes.

## 4. Prove force through Reaction Evidence

Do not communicate impact only through the actor or VFX layer.

Use secondary evidence in the environment:

- dust wakes
- loose paper or debris displacement
- clothing compression or flutter
- hair responding to acceleration
- floor vibration or object roll
- light flicker caused by a defined event
- lens contamination, shake, or flare only when physically motivated

Reaction Evidence helps the viewer infer force from consequences rather than from arbitrary spectacle.

The sequence should be causally readable:

```text
physical event
→ local effect
→ secondary reaction
→ settling
```

## 5. Camera Imperfection can increase realism

A reactive camera should not always track superhuman movement perfectly.

Useful controlled imperfections include:

- slight tracking lag
- brief overshoot
- delayed whip-pan reacquisition
- imperfect focus recovery
- impact shake only after a physical event reaches the camera system

These imperfections should be motivated. Random shake, continuous wobble, or arbitrary focus hunting is not realism.

Pattern:

```text
subject accelerates
→ camera briefly loses ideal framing
→ camera reacts and reacquires
→ framing stabilizes
```

## 6. Micro-slow-motion is an emphasis tool, not a default style

Very short impact slowdowns can improve readability when used sparingly.

A useful pattern is:

```text
real-time action
→ acceleration burst
→ brief impact emphasis
→ immediate return to real time
```

Do not let slow motion become the dominant pacing unless the scene specifically calls for it.

The emphasized interval should correspond to a meaningful contact, reversal, reveal, or physical consequence.

## 7. Preserve emotional state through spectacle

Fast action should not erase the character.

Define emotional state before, during, and after the action:

```text
fear
→ involuntary competence
→ shock at own action
→ continued pressure
→ final emotional residue
```

This prevents the model from converting every action scene into a triumphant hero pose.

The character's emotional continuity is a separate invariant from physical choreography.

## 8. Time blocks should contain state, event, and consequence

For long or dense action prompts, divide the clip into temporal beats.

Each block should contain:

```text
Entry State
→ Trigger / Event
→ Action Grammar
→ Physical / Environmental Consequence
→ Exit State
```

This is stronger than listing actions alone because it gives the next block a stable starting condition.

## 9. Action readability outranks camera spectacle

Camera movement exists to clarify force, direction, surprise, pursuit, or emotional emphasis.

Avoid adding orbit, zoom, pan, roll, whip-pan, and focus shifts simply because the model supports them.

Prefer one motivated camera behavior per beat.

Examples:

```text
pursuit → reactive tracking
surprise → delayed whip-pan
impact → short shake and rapid settle
speed reveal → brief tracking lag / overshoot
orientation change → motivated roll or occlusion transition
```

## 10. Prompt structure for complex action

A useful model-agnostic action specification is:

```text
FORMAT / DURATION
IDENTITY LOCK
ACTOR RELATIONSHIPS
LOCATION / AUDIO
EMOTIONAL STATE
ACTION GRAMMAR
PHYSICS LOCK
TIMELINE BEATS
REACTION EVIDENCE
CAMERA BEHAVIOR
FORBIDDEN FAILURE MODES
```

The runtime adapter should compress or reorder these layers according to the target model.

## 11. Failure modes

Common failures include:

- attackers taking turns unnaturally
- repeated reset poses
- teleport-like displacement
- energy effects detached from physical contact
- environment remaining frozen while impacts occur
- camera tracking that feels supernaturally perfect
- camera chaos that destroys action readability
- VFX overpowering character identity
- emotional state resetting after every hit
- actor positions becoming spatially impossible

When correcting, preserve accepted layers and change the smallest plausible cause first.

## 12. Production rule

For difficult action scenes, prefer testing short high-value beats before committing to a long continuous generation.

A visually impressive long prompt may demonstrate model capability but still have low production reproducibility.

The studio should distinguish:

```text
capability demo
from
repeatable production pattern
```

Only repeated successes should be promoted into action primitives or adapters.
