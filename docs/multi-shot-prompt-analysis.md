# Analysis: a fully specified six-shot prompt, and what transfers to H3

Source: a 30-second, six-shot ramyeon-eating prompt supplied by the operator on 2026-09-14.
Written against what this project measured on 2026-09-13/14, where several of the same problems were hit
and solved badly or not at all.

---

## 1. What it is structurally

Twelve labelled blocks, in two groups:

| Global (applies to the whole generation) | Per-shot |
|---|---|
| FORMAT, SCENE CONTEXT, ACTIVE REFERENCES, LOCATION MAP, FIRST FRAME / BLOCKING, ACTION & PERFORMANCE, CAMERA & OPTICS, PHYSICS & ENVIRONMENT, LIGHT & COLOR, AUDIO, LOCKS & EXCLUSIONS | SHOT PLAN — six shots, each a contiguous `[start,end)` interval subdivided into sub-second beats |

This is the four-block Seedance shape (one-line summary / fixed information / timestamped segments / global
constraints) expanded, and it is a superset of what H3's own prompt format asks for. Our current H3 prompts
carry `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`,
`non_diegetic_music` — that is roughly SCENE CONTEXT + ACTIVE REFERENCES + SHOT PLAN + AUDIO, and **nothing
for location geometry, physics, or invariants**.

---

## 2. The eight techniques worth stealing

### 2.1 The cut list is declared once, globally, with "only"

> HARD CUTS at 4.0, 12.0, 17.0, 18.8 and 25.0 **only**.

Then restated at each boundary. Redundancy as enforcement, plus an explicit prohibition on extra cuts.

**Why this matters here:** `r2-bento` on 2026-09-14 was asked for three shots and produced nine frame
transitions above threshold. Nothing in the prompt forbade extra cuts. This one word would have.

### 2.2 A location map with a locked camera axis

> All cameras stay southeast, about 15 degrees toward Jian's left from straight-on.
> Window screen-left, light screen-right. Preserve room, props and axis.

This is the 180-degree rule written down. It fixes not just where each camera is but that they all stay on
one side of the action, so the light and the background stay on the same side of frame across every cut.

**Why this matters here:** the operator's complaint that the vlog angles were monotonous was one half of the
problem; the other half is that when the angle *did* change it changed arbitrarily, and space stopped being
readable. A location map solves both at once — it licenses varied angles precisely because it constrains
them to a coherent geometry. We have never written one.

### 2.3 Cut on action, always

> Cut as the chopsticks approach the noodles.
> Cut during this exact contact phase.
> HARD CUT **on matching descent** to face, noodles and plate.
> 18.80–19.15: SAME bundle finishes settling in SAME plate; **no replay**.

Every cut lands mid-gesture and the next shot resumes the same gesture. This is why the cuts disappear.

**Why this matters here:** our cuts sit between settled states, which is the most visible place to put one.
The operator's "억지로 붙인 것 같아" is exactly this. Note also the explicit "no replay" — without it a model
will happily re-perform the action it just showed.

### 2.4 Continuity written as physics, not as description

> Noodles shorten with intake, retain visible length during the pause, and **never sever or replenish**.
> Food/broth decrease causally. Set down each utensil before switching.
> Pot weight transfers between hands and trivet.

A rule that holds for the whole clip, rather than a per-shot restatement of what should be on screen.

**Why this matters here:** we spent 2026-09-13 writing "the same red basket" into consecutive prompts and
got a different basket each time, then spent 2026-09-14 solving it with FL2VA frame chaining — which
measured out as good for exactly one step and a different person by the second. A physics block costs
nothing and works *inside* a render, where our chain cannot reach.

### 2.5 Audio names which words are not speech

> Slurp, crunch and pot-contact words describe **synchronized food/Foley sounds, not spoken words**.
> Preserve every quoted utterance **exactly**.
> Jian alone speaks Korean with one consistent soft, clear, warm, slightly low-pitched voice.

**Why this matters here:** this is the direct fix for a bug we hit twice. On 2026-09-13 a delivery
instruction containing "never announcing" came out of her mouth as "You're announcing", and "I have stopped
pretending" leaked as "Never pretending". The model had no way to know which of our words were dialogue.
One sentence would have prevented it.

The voice is also specified once, globally, as a property — "one consistent soft, clear, warm, slightly
low-pitched voice" — rather than as a per-shot delivery note. Our voice direction was per-shot prose, which
is both why it leaked and why it was inconsistent.

### 2.6 The reference is scoped by exclusion, and disclaimed as the first frame

> @Image1: **sole** identity/costume reference. Preserve facial identity, hairstyle, hair color, body
> proportions, visible clothing and accessories exactly. **Exclude the reference image's text, background,
> multiple figures, pose, framing and lighting. This is not the opening frame.**

Three separate jobs: what to take, what to ignore, and what role the image does not play.

**Why this matters here:** our `subject_definitions` says what to preserve and never says what to ignore.
Every Noa clip inherits the reference's framing pressure, and the measured finding that "keeping the
reference's own room" was worth +0.13 ArcFace may partly be this — the model defaulting to the reference's
background because nothing told it not to.

### 2.7 Emotion specified as muscles, plus a disambiguation

> Both inner brows draw slightly together, eyes narrow a little, one tiny nod: **unexpectedly delicious,
> not pain or excessive salt**.

The physical description alone is ambiguous — that face could read as discomfort. The clause after the colon
resolves it.

**Why this matters here:** our best attempt was "a real, warm, unguarded smile ... the kind she does not
show other people", which names the intent and not the face. Naming both is strictly better.

### 2.8 Negatives are specific failure modes

> No pans, zooms or focus shifts **during slurping**. No display pause or slow motion.
> never repeated head-bobbing. No audience address, mugging or emotional reset.
> no freeze, black frame, fade, title, extra reaction or trailing footage.

Each one forbids a thing this kind of model actually does, and several are scoped to a moment rather than
the whole clip.

**Why this matters here:** on 2026-09-11 a broad negative — "generic idealized AI beauty face, symmetrical
perfect features, airbrushed poreless skin, beauty filter..." — was read by the model as "less beautiful"
and the whole grid was rejected by the operator. Narrow, mechanical negatives do not have that failure.

---

## 3. What does not transfer as-is

**The 30-second single generation.** H3 here produces 175 frames at 24 fps — 7.29 s — from
`video_length: 181`. `sliding_window_size` is 362, and the `17k+5` frame grid recorded in
`docs/toyxyz-h3-prompter-review.md` gives 362 = 17·21 + 5, so **362 may be reachable and would be ~15 s**.
Untested. Even so, 30 s in one generation is likely out of reach and a six-shot/30 s structure has to
become two or three generations.

**`@Image1` syntax.** H3 uses `<Picture N>` with `subject_definitions`. The *content* of the ACTIVE
REFERENCES block transfers; the syntax does not.

**Sub-second beat timing.** This prompt subdivides to 50 ms ("8.15–8.80", "27.45"). The Seedance guidance
the operator supplied says to use one-second intervals as the basic unit. Whether H3 honours anything finer
is unverified, and over-specifying may simply waste prompt budget — which is not free: ninety words of face
description per shot measurably flattened twenty clips on 2026-09-13.

**16:9.** Ours is 576x768, 3:4, cropped to 9:16 in post.

---

## 4. Proposed H3 template

Global blocks folded into H3's own fields, so nothing is invented that the format cannot carry.

```
subject_definitions:
<Subject 1> is the person in <Picture 1>, shown again in close-up in <Picture 2>.
Take from them: facial identity, hair, skin, body proportions.
Ignore: the reference images' background, framing, lighting and pose.
Neither picture is the opening frame of this video.

summary:
[reference generation] <one sentence: subject + place + event + camera>

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - ...

detailed_description:
SPACE. <where things are, and: every camera stays on the <side> of the action, with
        <landmark> screen-left and the light screen-right, in every shot.>
FIRST FRAME. <the exact instant the clip opens on.>
CUTS. Hard cuts at <t1> and <t2> only.
[Shot 1] (0.0-2.4) <crop from the table> <beats> <cut on: the gesture that carries over>
[Shot 2] (2.4-4.9) <resumes that same gesture, not a replay> ...
[Shot 3] (4.9-7.3) ...
PHYSICS. <what decreases, what is set down before what, what never replenishes.>
LOCKS. <end state; handedness; what must not appear.>

overall_soundscape: <ambience>. The quoted line is the only speech; every other sound word
here describes Foley, not something anyone says.
non_diegetic_music: <or None>
```

Two rules that come out of this analysis and are not in the source prompt, because they are ours:

- **Keep the identity anchor short and in one render only.** The source gets away with a long reference
  block because it has one generation; we have a chain, and our measurement says the anchor competes with
  behaviour for the model's attention.
- **A close-up is not required in every shot.** Framings with no face in them are shots too. The rule
  "every render needs a close-up so identity stays measurable" was a measurement convenience of ours and it
  was distorting the directing.

---

## 5. What to test first, in order

1. **`video_length: 362`** — one render. If it yields ~15 s, a six-shot structure fits in two generations
   instead of five, and the FL2VA chain depth problem mostly disappears.
2. **The Foley disclaimer sentence** — costs nothing, and closes a bug we hit twice.
3. **LOCATION MAP + cut-on-action** — one render against a matched control, on the vlog we already have,
   so "억지로 붙인 것 같아" gets a before/after rather than an opinion.
4. **The makeup question**, which is ours and unrelated to this prompt: asking for worn or absent makeup has
   cost identity three separate times against a reference with clean makeup and vivid lipstick, and has
   never been tested deliberately.
