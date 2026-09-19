# Continuity as Story Language

## Source context

This note records a transferable lesson from an experienced film/video creator working with AI video.

The central claim is:

> Storyboarding is not only a list of attractive shots. It is the design of continuity, and continuity is what lets shots become understandable story and emotion.

This is especially relevant to AI video because current generators are already capable of producing strong individual shots, while cross-shot continuity and intentional shot relationships remain separate planning problems.

## Core lesson

A storyboard translates written narrative into visual language.

The unit of interest is not only the individual cut, but the relationship between cuts:

- what the viewer sees first;
- what information is withheld;
- what is revealed next;
- whose point of view or eyeline organizes the sequence;
- what reaction follows;
- what emotional meaning is created by the order.

A sequence such as:

```text
character sees something
→ show what they see
→ return to reaction
```

is not merely three camera setups. It is an information-and-emotion chain.

Changing shot order changes meaning because shot order controls the release of information.

Do **not** encode a simplistic rule such as “reaction-first means horror.” Reaction-first can create suspense, mystery, comedy, horror, or another effect depending on timing, sound, framing, performance, and reveal content.

The reusable principle is:

> shot order controls information release, and information release shapes emotion.

## Continuity should be split into three layers

### 1. Physical continuity

Tracks observable state across cuts:

- character position and orientation;
- left/right hand state;
- props and ownership;
- contact points;
- wardrobe;
- scene layout;
- lighting/time baseline;
- action end state.

This is necessary for generative stability.

### 2. Informational continuity

Tracks what the audience knows and what remains hidden:

- what a character has noticed;
- what the viewer has or has not seen;
- what a prior eyeline points toward;
- what question a shot creates;
- what the next shot answers or delays;
- whose viewpoint organizes the sequence.

### 3. Emotional continuity

Tracks the emotional effect of the information flow:

- anticipation;
- curiosity;
- surprise;
- tension;
- relief;
- embarrassment;
- satisfaction;
- fear;
- comic payoff.

A shot should inherit not only physical state but, when relevant, an informational or emotional handoff.

## Scene / continuity unit

Traditional film practice often describes a scene around one location. For AI production, use a more practical continuity unit:

```text
location
+ time / lighting
+ wardrobe
+ character state
+ important props
+ spatial layout
+ narrative continuity
```

The same physical place may become a different continuity unit when time, light, wardrobe, or story state changes materially.

The location asset remains important. Each scene/continuity unit should have a stable spatial reference before complex shot variation is attempted.

## Shot function comes before camera decoration

Do not begin by choosing a “cool” angle.

First determine why the shot exists.

Useful shot functions include:

- establish;
- orient;
- introduce;
- create question;
- reveal;
- confirm;
- reaction;
- contrast;
- decision;
- action;
- transition;
- payoff;
- aftermath.

Only after the shot function is known should the system select:

- framing;
- camera position;
- angle;
- movement vs fixed camera;
- blocking;
- timing;
- transition.

This keeps visual technique subordinate to narrative purpose.

## Recommended visual-language pipeline

```text
Scenario
↓
Scene / continuity-unit segmentation
↓
Location / scene asset planning
↓
Scene dramatic goal
↓
Beat design
↓
Information + emotion flow
↓
Shot functions
↓
Shot order
↓
Camera / framing / blocking
↓
Physical continuity check
↓
Storyboard
↓
Storyboard images / scene grid
↓
Renderer-specific compilation
↓
Video generation
```

This refines the existing Visual Language Translator.

## Lightweight storyboard schema change

Do not expand the schema into a large professional shot database.

Add one explicit field:

```yaml
shot_function: reveal what the character noticed
```

And reinterpret continuity as three internal subtypes when needed:

```yaml
continuity:
  physical: cup remains on right side of table
  informational: answers the previous eyeline
  emotional: turns curiosity into mild panic
```

These subfields do not need to be present in every trivial shot. Use them when the relationship between cuts matters.

## Example

```yaml
shot_id: S03
shot_function: reveal what Noa noticed
framing: close
camera: fixed observer angle
action: spilled coffee is visible beside the laptop
continuity:
  physical: mug remains to the right of the laptop
  informational: answers S02 eyeline
  emotional: converts curiosity into mild panic
duration_s: 1.8
production_route: storyboard still -> H3/WanGP I2V
```

## Implication for the Director / Visual Language Translator

Before skill routing for camera style, the planner should determine:

1. scene goal;
2. narrative beat sequence;
3. information release;
4. emotional progression;
5. shot functions;
6. physical continuity requirements.

Only then should it choose directing skills such as:

- environment-first;
- object-first;
- character-first;
- observational long take;
- rhythmic montage;
- contact motion;
- physical gag;
- reaction emphasis;
- delayed reveal.

This prevents “attractive but disconnected” storyboards.

## Implementation rule

Do not over-engineer this into a separate service unless repeated real use justifies it.

The first implementation can simply:

- add `shot_function` to candidate output;
- allow `continuity_anchor` to carry physical / informational / emotional handoff notes;
- add an automatic check asking whether adjacent cuts preserve or intentionally transform those handoffs.

## Core principle to preserve

> Good AI video direction is not a collection of individually strong shots. It is a designed sequence in which each shot passes physical state, information, and emotion to the next.

