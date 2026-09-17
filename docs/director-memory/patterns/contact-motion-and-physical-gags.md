# Contact Motion And Physical Gags
Last updated: 2026-09-17

## Purpose

This document records two high-value AI-video production domains:

1. **contact motion**
   - martial arts / sparring
   - grabs, catches, pulls, turns
   - partner dance
   - pilates / posture correction
   - guided movement between two people

2. **physical gag / impossible everyday comedy**
   - trip-and-recover comedy
   - food-tray or object fake-outs
   - exaggerated but readable recovery
   - realistic everyday world + stylized comic physics

These scenes are structurally difficult for generative video and should be treated as specialized directing/production pattern families rather than ordinary vlog/action prompting.

## Why these scenes often fail

These scenes require the model to preserve, across time:

- relative position of two or more people;
- left/right hand state;
- contact points;
- prop ownership and location;
- physical connection continuity;
- action order;
- recovery/payoff timing.

A loose instruction such as "the instructor corrects her posture" or "he grabs her wrist" hides several causal state transitions. For difficult contact scenes, the planner should represent the motion as a sequence of readable states rather than one compressed action phrase.

## Pattern Family 1: Contact Motion

### Examples

- martial-arts wrist grab and release;
- defensive movement training;
- instructor correcting pelvis / shoulder alignment in pilates;
- dance partner guiding shoulder, waist, arm, or foot position;
- one person catching another after loss of balance;
- pulling, restraining, turning, or guiding the body.

### Core difficulty

The difficulty is not merely "two people in frame." The difficulty is preserving:

- body-to-body relation;
- hand placement;
- contact persistence;
- order of force transfer;
- readable state change.

### Recommended interpretation

Treat contact motion as:

```text
initial state
→ preparation
→ contact established
→ guided movement / controlled force
→ resulting pose
→ release / settle
```

### Required constraint skills

- `multi_actor_blocking`
- `hand_state_continuity`
- `contact_point_continuity`
- `action_decomposition`
- `spatial_continuity`
- `locked_end_state`
- `reaction_or_recovery_timing`

## Pattern Family 2: Physical Gag / Impossible Everyday Comedy

### Examples

- carrying food and getting tripped;
- tray or objects thrown upward but visually controlled;
- impossible but readable recovery;
- object spill fake-out that resolves cleanly;
- realistic environment with stylized cartoon-like physics.

### Why this matters

This is a strategically valuable AI-video category because it can depict short-form comic situations that are difficult, expensive, unsafe, or nearly impossible to stage practically while remaining immediately understandable to viewers.

The creative advantage is not generic spectacle. It is:

```text
grounded everyday setting
+ simple readable cause
+ exaggerated but coherent physical event
+ clean payoff
```

### Core formula

```text
setup
→ trigger
→ escalation
→ recovery/control
→ payoff
```

### Required constraint skills

- `multi_actor_blocking`
- `prop_state_choreography`
- `hand_state_continuity`
- `action_decomposition`
- `spatial_continuity`
- `stylized_physics_lock`
- `reaction_timing`

## Key production rule

**Prefer one clear state transition per shot or beat.**

Bad:

```text
approach + grab + rotate + correct + release + reaction
```

Better:

```text
shot 1: approach
shot 2: hand placement
shot 3: contact maintained
shot 4: posture / force change
shot 5: corrected end pose
shot 6: release or reaction
```

The same principle applies to physical gag choreography:

```text
trigger
→ loss of balance
→ object/tray release
→ airborne state
→ body recovery
→ object catch
→ restored state
→ reaction/payoff
```

## Required internal representation

Do not rely only on long freeform prose.

Use structured state-based planning where relevant:

- character positions;
- left-hand state;
- right-hand state;
- contact points;
- prop owner;
- prop location;
- physical connection;
- locked end state.

Recommended per-shot fields:

```yaml
shot_id:
duration:
framing:
camera_position:
camera_operator:
initial_state:
micro_beats:
contact_points:
prop_state_change:
locked_end_state:
transition:
production_route:
```

Optional:

```yaml
physics_lock:
reaction_focus:
```

## Micro-beat design

For difficult contact scenes, decompose each shot into 3–5 readable micro-beats when useful:

1. establish / hold;
2. preparation;
3. contact or core action;
4. settle / recovery;
5. optional final hold.

This is especially valuable for:

- handoffs;
- grabs;
- body guidance;
- posture correction;
- two-person action with props.

## Example decompositions

### Martial arts

```text
attacker reaches for wrist
→ defender secures / acknowledges contact
→ weight shifts
→ defender turns out
→ both reset stance
```

### Pilates correction

```text
instructor approaches from the side
→ right hand supports pelvis
→ left hand guides shoulder line
→ student adjusts pelvis / torso
→ corrected posture is held
→ instructor releases
```

### Partner dance

```text
lead establishes hand at upper back
→ other hand guides forearm
→ follower pivots
→ both settle into the new orientation
```

## Router metadata

### when_to_use

Use this pattern family when:

- humor/action depends on physical interaction;
- hand placement matters;
- body guidance matters;
- props and contact must remain visually consistent;
- the audience must clearly understand cause and effect;
- the physical event is exaggerated, nearly impossible, or choreographically complex.

### when_not_to_use

Do not prioritize this family when:

- the scene is mainly emotional conversation;
- humor is verbal only;
- there is no meaningful physical contact;
- the action is visually simple and non-sequential;
- the shot is mostly static portrait or ordinary vlog observation.

## Creative Skills vs Constraint Skills

### Creative skills

Examples:

- school comedy;
- awkward daily-life comedy;
- deadpan payoff;
- stylized slow-motion reveal;
- martial-arts realism;
- instructor/student discipline;
- partner-guidance intimacy.

### Constraint skills

Examples:

- `multi_actor_blocking`
- `hand_state_continuity`
- `contact_point_continuity`
- `prop_state_choreography`
- `action_decomposition`
- `spatial_continuity`
- `locked_end_state`
- `stylized_physics_lock`
- `reaction_timing`

Do not load all action or comedy references at once. The Director Core / Skill Router should select only the subset relevant to the chosen directing strategy.

## Reference-example handling

For complex physical-interaction prompt examples, extract:

- reference-role separation;
- initial-state definition;
- persistent invariants;
- state-transition sequencing;
- readable multi-actor blocking;
- reaction/payoff structure;
- decomposition into visual beats.

Do **not** blindly copy:

- exact setting;
- exact prop;
- exact dialogue;
- exact shot count;
- exact timing;
- exact slow-motion use;
- exact comic physics style.

## Codex implementation note

Codex should add high-level routes such as:

- `contact_motion`
- `physical_gag`

The system should:

1. classify the scene;
2. load only relevant creative and constraint skills;
3. build a structured state-based storyboard;
4. compile it into renderer-specific prompt language;
5. preserve warnings as warnings rather than turning every risk into a hard block.

This should be treated as a first-class production pattern family, not a giant universal prompt template.
