# Lia Vlog Pilot 01 — A Quiet Day by the Sea

Updated: 2026-09-06
Status: production brief / execution handoff
Priority intent: **make Lia content first; refine architecture from production evidence later**

## Purpose

This document is a concrete production brief for Lia's first 1–2 minute everyday vlog. It is intended to be executable later by Codex, Hermes, and WanGP/H3 without requiring the user to reconstruct the concept from chat history.

This is deliberately **not** a request to finish Character DNA, Voice DNA, Look Pack schemas, or a general orchestration framework before production. Use the smallest workable reference set, make the vlog, observe failures, then improve the system only where repeated production evidence justifies it.

> **Important character boundary**
>
> Do not mix Aoi's lifestyle into Lia. The swimming-pool-before-work / nomad-designer routine belongs to Aoi, not Lia. Lia's core everyday world is the seaside home, cat, convenience-store part-time work, beach walks, simple cooking, laundry, quiet hobbies, and low-key domestic moments.

---

## 1. Pilot concept

### Working title

**Lia — A Quiet Day by the Sea**

### Target duration

- preferred first cut: **~85–95 seconds**
- acceptable range: **60–120 seconds**
- do not extend toward 2 minutes merely to fill time

### Tone

- quiet, believable everyday vlog
- seaside small-town atmosphere
- warm but not sentimental
- character charm comes from behavior, gaze, timing, and small reactions rather than overt posing
- avoid making every shot look like a polished fashion commercial
- natural skin, ordinary lived-in spaces, plausible wardrobe, modest camera movement

### What this pilot should establish

1. Lia feels like the same person across multiple locations and wardrobe states.
2. Her cat and seaside environment feel like recurring parts of her life.
3. Her personality reads as calm, gentle, understated, and lightly playful.
4. Her convenience-store job feels mundane and believable rather than staged.
5. The production team learns what reference information H3/WanGP actually needs.

---

## 2. Lia continuity anchors

Use the existing canonical Lia definition as the source of truth. Do not redesign her for this pilot.

Key visible anchors:

- young adult East-Asian-looking woman with globally neutral identity
- tall, slender build
- slightly long/slender oval face, gently tapered lower face, not sharp V-line
- large soft slightly elongated dark eyes
- natural clear skin
- long dark hair
- understated, translucent, calm beauty rather than idol/glamour styling
- faint quiet smile as a recurring expression
- recognizable thin ethnic-style bracelets on the right wrist when practical

Cat anchor:

- tabby cat
- dark black stripes
- odd eyes: one blue, one green
- relaxed, slightly lazy personality
- not fat

### Identity-reference rule

Start simple:

```text
FACE_MASTER
+ BODY_MASTER if needed
+ current LOOK reference
```

Do not assume every shot needs all available identity references. If the face is stable with one strong face reference and one look reference, do not add more merely because they exist.

---

## 3. Look states for this episode

Five look states are enough for the pilot. They are production states, not permanent Character DNA requirements.

### LOOK A — Sleepwear

- ivory or pale neutral sleeveless/short-sleeve sleep top
- soft pale-pink or neutral frill shorts
- barefoot or house slippers if visible
- no fashion styling
- hair: naturally loose, slightly messy from sleep

Use for: waking scene only.

### LOOK B — Morning Home Casual

- simple white/light short-sleeve T-shirt
- relaxed light-blue or neutral home shorts
- recognizable bracelets retained if visible
- hair: loose natural down hair, quickly hand-neatened rather than styled

Use for: water, cat feeding, small morning activity.

### LOOK C — Convenience-store Work Uniform

- realistic convenience-store staff uniform
- light blue/white or other plausible clean corporate palette
- dark pants
- comfortable sneakers
- name tag if stable enough to render without distracting artifacts
- hair: neat low ponytail

Use for: preparation, stocking, checkout, leaving work.

### LOOK D — After-work Seaside Casual

- simple white short-sleeve blouse or light summer top
- light denim shorts or relaxed summer bottoms
- canvas tote bag
- casual shoes/sandals appropriate for the scene
- hair: loose natural hair or relaxed half-up style

Use for: seaside walk.

### LOOK E — Evening Homewear

- oatmeal/neutral oversized T-shirt
- dark relaxed shorts
- hair: loose and relaxed; optional small practical hair clip if needed

Use for: cat brushing, phone/music, final quiet evening beat.

### Hair-state rule

Hair is a scene state, not a new character identity. Use only the state needed for the current shot:

```text
messy_down
natural_down
work_low_ponytail
relaxed_half_up_or_down
relaxed_evening_down
```

Do not build an elaborate hair-state system before this episode is attempted.

---

## 4. Proposed sequence and shot plan

Target: approximately 89–94 seconds before final trimming.

### Sequence 1 — Morning at Home

#### Shot 01 — Wake / window

- target duration: 8 s
- strategy candidate: long continuous
- look: A / sleepwear
- hair: messy_down
- location: bedroom
- action:
  - Lia wakes slowly
  - sits up rather than springing awake
  - remains still for a short beat
  - looks toward the window/light
- acting:
  - sleepy, low energy
  - no exaggerated yawn required
  - subtle breathing and eye adjustment
- dialogue: none preferred
- purpose: establish Lia, pace, home atmosphere

#### Shot 02 — Water in the kitchen/veranda area

- target duration: 7 s
- strategy candidate: medium independent shot
- look: B / morning home casual
- hair: natural_down
- action:
  - pours or retrieves water
  - takes a drink
  - briefly stands in quiet thought
- camera: simple medium framing; no complicated move
- purpose: transition from sleep state to ordinary morning

#### Shot 03 — Feed / greet the cat

- target duration: 9 s
- strategy candidate: long continuous
- look: B
- hair: natural_down
- required ref: CAT_MASTER
- action:
  - puts food down or checks the cat's bowl
  - cat approaches/rubs nearby
  - Lia responds without interrupting the task dramatically
- gaze:
  - mostly cat / bowl
  - not camera
- reaction:
  - small smile when cat engages
- optional short line: `배고팠어?`
- purpose: establish relationship and recurring cat behavior

Sequence target: ~24 s

---

### Sequence 2 — Work

#### Shot 04 — Getting ready for work

- target duration: 6 s
- strategy candidate: short/medium independent shot
- look: C
- hair: work_low_ponytail
- action:
  - checks low ponytail or ties it
  - adjusts uniform sleeve/collar
  - picks up essentials
- note: this is a state-establishing cut, not a makeover montage

#### Shot 05 — Stocking shelves

- target duration: 8 s
- strategy candidate: long continuous
- look: C
- hair: work_low_ponytail
- environment: convenience-store master
- action:
  - places or straightens products
  - entrance sound/visitor causes eyes or head to shift briefly
  - she acknowledges the customer while continuing work
- optional line: a natural short greeting
- acting principle: ongoing task + response + gaze, not staged posing

#### Shot 06 — Checkout interaction

- target duration: 8 s
- strategy candidate: medium shot
- look: C
- hair: work_low_ponytail
- action:
  - handles one simple purchase
  - gaze alternates naturally among product, register, and customer
  - faint polite smile at the end
- avoid:
  - continuous direct eye contact
  - exaggerated customer-service performance
  - complex hand choreography if it causes generation failures

#### Shot 07 — Leaving work

- target duration: 5–6 s
- strategy candidate: short transition shot
- look: C
- hair: work_low_ponytail
- prop: one bottle of water if reliable
- action:
  - exits the store
  - slight release of posture/energy indicating shift from work to private time
- purpose: clean sequence boundary

Sequence target: ~27–28 s including Shot 07; final edit may trim.

---

### Sequence 3 — After-work seaside walk

#### Shot 08 — Changed and heading to the sea

- target duration: 4–5 s
- strategy candidate: transition/insert
- look: D
- hair: relaxed_half_up_or_down
- prop: canvas tote
- action:
  - simple departure / walking transition
- note: do not show literal clothing change unless it becomes an intentional experiment; cut directly to the new look

#### Shot 09 — Main beach walk

- target duration: 10 s
- strategy candidate: long continuous
- look: D
- hair: relaxed_half_up_or_down
- environment: seaside walk / beach master
- optional prop: ice cream or cold drink, only if hand/object reliability is acceptable
- action:
  - walks at an unhurried pace
  - looks toward water once
  - hair/clothing react lightly to coastal breeze
- acting:
  - relaxed after work
  - no fashion runway movement
- camera:
  - side-follow or gentle three-quarter tracking is preferred
  - prioritize identity and natural motion over ambitious camera choreography

#### Shot 10 — Quiet pause at sea

- target duration: 4–6 s
- strategy candidate: medium independent or continuation candidate
- look: D
- hair: same as Shot 09
- action:
  - stops near railing/bench/path edge
  - watches the sea
  - faint smile or relaxed exhale
- purpose: emotional breathing room

Sequence target: ~19–21 s

---

### Sequence 4 — Night at Home

#### Shot 11 — Brush the cat

- target duration: 9 s
- strategy candidate: long continuous
- look: E
- hair: relaxed_evening_down
- environment: floor room/veranda master
- required ref: CAT_MASTER
- action:
  - Lia brushes the cat while seated
  - cat shifts once
  - Lia briefly pauses, reacts, resumes
- gaze:
  - predominantly on cat
- optional line: `오늘은 얌전하네.`
- acting principle:
  - ongoing action must continue through speech

#### Shot 12 — End-of-day quiet moment

- target duration: 8–10 s
- strategy candidate: long continuous
- look: E
- hair: relaxed_evening_down
- props: phone and/or earphones, but avoid unnecessary prop complexity
- action:
  - sits or leans comfortably
  - listens to music / casually checks phone / looks out toward the yard or window
  - only near the end does her gaze briefly meet the camera
  - small familiar Lia smile
  - settle rather than cut at the peak of expression
- dialogue: none preferred
- purpose: recurring-series closing signature candidate

Sequence target: ~17–19 s

---

## 5. Duration and shot-strategy policy for the pilot

Do **not** hard-code one universal cut duration before testing.

This pilot should compare three practical strategies where useful:

```text
A. short independent shot
B. long single H3 shot
C. continuation / sliding-window workflow in WanGP
```

Working assumptions to test, not permanent rules:

- new location -> usually new shot
- wardrobe change -> usually new shot
- hair-state change -> usually new shot unless transition is the point
- high hand/prop complexity -> prefer shorter retry unit
- emotional/acting continuity -> consider longer shot
- calm same-location activity -> longer shot may feel more natural
- expensive/high-risk generation -> shorter retry unit may be cheaper
- continuous action that exceeds comfortable generation length -> test continuation/sliding window

### Required experiment

Choose one representative 10–12 second everyday action and compare:

1. two independent short clips;
2. one long H3 clip;
3. WanGP continuation/sliding-window version if practical.

Record:

- face consistency
- body consistency
- wardrobe/hair consistency
- action continuity
- gaze/acting continuity
- audio/voice continuity if used
- background drift
- generation time
- retry cost
- editability

Do not decide the permanent shot-length policy before this test and real production experience.

---

## 6. Minimum reference assets required

The pilot should not wait for a perfect full Character DNA pack. Create or select only what is necessary.

### Character identity

Required minimum:

- `LIA_FACE_MASTER`
- `LIA_BODY_MASTER` or a body reference only where H3 demonstrates a real need

Preferred character-sheet experiment:

- one clean face close-up
- one neutral body/front-back or equivalent body reference
- current episode look

The character-sheet format itself is provisional. Change it if real results indicate another layout is more reliable.

### Look references

Create/select:

- `LIA_LOOK_SLEEP`
- `LIA_LOOK_HOME_MORNING`
- `LIA_LOOK_WORK_UNIFORM`
- `LIA_LOOK_SEASIDE_CASUAL`
- `LIA_LOOK_HOME_EVENING`

A look reference should communicate current clothing and hair state without becoming a giant all-purpose character sheet.

### Environment references

Minimum useful set:

- bedroom/home morning environment
- kitchen/veranda or domestic common area
- convenience store
- seaside walk / beach
- evening home/floor-room/veranda

Where several scenes reuse one physical home, prefer a coherent environment master and consistent derived views rather than unrelated independently generated rooms.

### Cat reference

- `CAT_MASTER`

Keep the cat reference stable across shots.

### Voice

Voice DNA is important for the long-term character, but **do not block the pilot on perfect voice design**.

If a reliable Lia voice master already exists or can be made cheaply, test it in the two short dialogue moments. Otherwise the first pilot may use minimal/no dialogue and establish voice later.

Candidate dialogue moments only:

- cat morning: `배고팠어?`
- evening cat brushing: `오늘은 얌전하네.`

Do not fill the vlog with narration merely because audio is available.

---

## 7. Generation-packet principle

Each shot should receive only the references required to make that shot coherent.

Example:

```yaml
shot: 09
character: lia
references:
  identity:
    - LIA_FACE_MASTER
  look:
    - LIA_LOOK_SEASIDE_CASUAL
  environment:
    - SEASIDE_WALK_MASTER
  voice: []
  props: []
strategy:
  type: long_continuous
  target_duration_sec: 10
```

Do not blindly attach every Lia image, every hairstyle, every environment, and every prop to every job.

The stable principle is:

```text
rich internal character knowledge
→ smallest coherent shot-specific reference packet
→ renderer-specific job
```

---

## 8. Role split for later execution

### Hermes — production planner / coordinator

Hermes should read this brief plus the current Lia canonical character data and produce an execution manifest.

Expected output per shot:

- shot id
- narrative purpose
- target duration
- shot strategy candidate
- Lia look state
- hair state
- environment
- props
- dialogue/audio requirement
- required references
- missing-asset list
- H3/WanGP job notes
- retry/evaluation criteria

Hermes should not redesign Lia or create a new architecture project before producing the manifest.

### Codex — deterministic preparation / tooling

Codex should help where deterministic work reduces friction:

- locate existing approved Lia references and metadata
- assemble/copy/register reference assets
- generate machine-readable job manifests
- prepare WanGP/H3 input files or scripts where the existing repo supports them
- preserve prompt/settings/output traceability
- record source-reference lineage
- add lightweight automation only where it directly helps this pilot

Codex should **not** make schema completion or UI redesign a prerequisite for the vlog.

### WanGP + H3 — renderer/runtime

WanGP/H3 should execute the prepared shot jobs.

Renderer priorities:

1. Lia identity
2. wardrobe/hair continuity
3. natural acting and gaze
4. environment continuity
5. shot readability
6. camera ambition

If a complex camera move harms identity or motion, simplify the camera rather than expanding prompts indefinitely.

### Human review

The user remains the final curator for:

- whether Lia still feels like Lia
- whether the look is attractive/believable
- whether the acting feels natural
- whether a failed shot is worth retrying
- which results become future canonical/master references

---

## 9. Failure handling

When a shot fails, retry the smallest plausible unit.

Examples:

```text
face drift
→ adjust identity/look reference packet

wrong outfit
→ adjust look reference

hair wrong
→ strengthen hair state only if recurrent

cat unstable
→ simplify interaction or adjust cat reference

hands/checkout fail
→ simplify action or shorten shot

acting stiff
→ rewrite ongoing action + gaze + reaction

background drifts
→ strengthen environment reference / simplify camera

long shot fails late
→ compare against shorter split or continuation strategy
```

Do not rebuild all Lia assets after one bad generation.

Repeated failure across multiple shots is evidence for improving DNA/reference infrastructure. One-off failure is not.

---

## 10. Acceptance criteria for Pilot 01

The pilot is successful if:

- one complete 60–120 second edit exists;
- Lia is recognizably the same character in most usable shots;
- at least 3 distinct look/location states work convincingly;
- cat interaction works in at least one scene;
- convenience-store work feels believable enough to establish her routine;
- seaside sequence works as a recurring visual identity for the series;
- at least one quiet end-of-day shot feels strong enough to reuse as a style reference;
- production notes identify which reference types were actually useful;
- failed experiments are recorded without turning them into unnecessary architecture work.

Perfection is not an acceptance criterion.

---

## 11. After the pilot

Only after the first complete vlog exists, review whether to improve:

- Character Sheet layout
- Face/Body master selection
- Look Pack structure
- Hair-state handling
- Voice DNA / voice master
- Acting/Expression primitive library
- environment consistency method
- H3 shot-length defaults
- WanGP sliding-window/continuation policy
- automatic Reference Pack assembly

Promote only repeated, high-value lessons into durable schemas or skills.

---

## Agent handoff summary

> **Codex / Hermes / future production agents:**
>
> The task is to make Lia's vlog, not to complete the studio architecture first. Treat this file as the creative/production brief. Use existing assets where possible, create only missing references that directly block a shot, and keep shot jobs traceable. Start with the simplest reference packet that works. Test long vs short vs continuation strategies during actual production. Preserve successful results, retry failed shots locally, and use repeated failures to decide what infrastructure deserves improvement.

### Canonical pipeline for this pilot

```text
Lia canonical identity
+ episode look states
+ simple story/shot plan
        ↓
Hermes execution manifest
        ↓
missing reference assets only
        ↓
shot-specific reference packets
        ↓
WanGP / H3 generation
        ↓
review + timeline assembly
        ↓
retry failed shots only
        ↓
complete Lia vlog
        ↓
production evidence informs future system design
```
