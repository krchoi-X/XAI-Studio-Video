# Directing Principles

## 1. Choose a viewing strategy deliberately

Do not let vague terms such as `vlog`, `introduction`, `daily life`, or `casual` silently choose the camera grammar.

Before writing shots, decide how the episode reveals itself. Useful families include:

- character-first;
- face-first;
- body-first;
- space-first;
- object-first;
- action-first;
- sound/off-screen-first;
- aftermath/trace-first;
- reverse-order or delayed reveal.

The family is a choice, not a permanent character rule.

## 2. Separate narrative intent from shot construction

First state what the beat must communicate. Then decide how to show it.

Example:

```text
Intent: Noa introduces herself while feeling self-aware but prepared.
Possible construction A: fixed wide shot; she enters frame and settles before speaking.
Possible construction B: close detail of the action camera; pull back or cut to reveal the full setup.
```

This prevents a language model from treating one common visual cliché as the only interpretation of the story intent.

## 3. Distinguish long take, multi-cut, and hybrid

These are not interchangeable formatting choices; they create different emotional results.

### Long take

Use when spatial continuity, natural body language, observation, awkward pauses, or realism are important.

Typical strengths:
- stronger sense of place;
- continuous performance;
- less editorial manipulation;
- useful for everyday vlog realism.

Typical risks:
- more difficult motion/identity continuity;
- more ways for generated action to drift inside one clip;
- weak pacing if too little changes.

### Multi-cut

Use when rhythm, compression, visual emphasis, object details, or controlled reveals matter.

Typical strengths:
- each shot can be tightly controlled;
- failed shots can be regenerated independently;
- easier to vary scale and point of view;
- useful for stylized or information-dense openings.

Typical risks:
- continuity errors between shots;
- over-editing ordinary behavior;
- generic montage if every beat becomes a cut.

### Hybrid

Use when one continuous performance benefits from a small number of purposeful inserts or reveals.

Do not default to one construction for all episodes.

## 4. Action before dialogue is often stronger, but not mandatory

When a talking scene becomes visually flat, give the character something physically meaningful to do before or while speaking: enter frame, place an object, adjust the camera, sit, check a window, open a bag, pick up a cup, react to a sound.

This should reveal character or space. Do not add random fidgeting merely to create motion.

## 5. Preserve spatial logic

For each shot, define enough of the space that a later agent can reproduce it:

- fixed landmarks;
- screen-relative character/object position;
- facing direction;
- camera position and support;
- important movement path;
- lighting direction when continuity depends on it.

If the scene spans several cuts, explicitly preserve the state that carries forward: where the character ended, what hand holds the object, whether a door is open, where the camera has moved, and so on.

## 6. Use the environment as narrative material

A character-driven video does not need to begin with the character's face. Rooms, objects, weather, traces of recent action, sound, or a meaningful prop can introduce the episode.

The object or environment must have causal or thematic relevance. Avoid random 'interesting' imagery that does not connect to the scene.

## 7. Avoid generic model defaults by specifying the missing decisions

When a result repeatedly falls into a cliché, identify the decision the prompt left unspecified.

Examples:

- unwanted selfie close-up → specify camera support + subject scale + reveal strategy;
- wrong spatial relationship → specify anchors + screen positions;
- action jumps → specify start state, action beat, and handoff state;
- style drift → bind the correct identity/reference source instead of adding more descriptive adjectives;
- too many cuts → state long-take intent and permitted cut count;
- static talking head → define an action path or purposeful environmental beat.

## 8. Prefer two strong alternatives over many weak ones

Default deliverable for a director is two candidates that differ in construction, not merely wording.

A good pair often looks like:

- Candidate A: production-safe / continuity-first;
- Candidate B: more exploratory / visually distinctive.

If both candidates share the same opening family, same camera scale, same shot count, and same reveal order, they are probably not meaningfully different.

## 9. Production feasibility is part of directing

A storyboard should consider the actual toolchain before promising an effect.

Check:
- whether an identity reference is available;
- whether a clean starting still is needed;
- whether motion control/reference would materially help;
- whether one long generated clip is realistic for the action;
- whether the scene should be split to reduce failure cost;
- whether audio/dialogue needs separate treatment;
- whether approved shots can be reused instead of regenerated.

Do not make the storyboard dull merely because a tool is limited, but label risk honestly and offer a practical route.

## 10. Still-board before expensive video when composition is uncertain

When camera placement, body scale, object layout, or reveal order is still undecided, validate those decisions with stills or rough storyboard frames before spending on long video generations.

Use video generation to test motion and performance, not to discover every basic composition decision at once.

## 11. Learn principles, not literal templates

Approved work is evidence of taste and feasibility. It is not a mandate to repeat the same opening, lens, camera height, edit rhythm, or prop in future episodes.

Ask:
- What made this work?
- Which constraint was important?
- Which part was specific to this episode?

Reuse the first two; vary the third.

## 12. Human selection remains authoritative

AI directors propose. The user selects, rejects, combines, or revises.

When the user explains why a candidate was liked or disliked, record the reason because that reason is more reusable than the binary selection itself.

## 13. Prefer a motivated change over a forced match or a hidden seam

When a state differs across a cut, there are three routes, not two.

1. **Match it.** Declare the cut dependent and carry the state. Correct when the state is easy to
   hold — screen position, facing, wardrobe, which hand holds a prop.
2. **Hide it.** Cover the seam with an edit. This is the weakest route and it fails outright when
   the cover is decorative. A caption card laid over the join does not supply a cause, and the
   viewer still reads a body that arrived in a state nobody performed. Only use a cover that is
   itself motivated in the action: a hand passing the lens, someone crossing frame, a turn into a
   wall.
3. **Motivate it.** Let the state change, and put a visible cause on screen. She reaches over and
   switches on the light. She pulls the curtain. She sits down. She resets her position and
   restarts. The difference stops being an error and becomes a beat.

Route 3 is usually the cheapest and reads the most natural, and it is under-used because the
default instinct is to fight for a match. Some states are genuinely hard to hold across separately
generated clips — exposure and colour temperature, hair, small posture, hand micro-position. For
those, trying to match is the expensive path and hiding is the fragile one.

The requirement is that the cause is **visible or immediately inferable on screen**. A cause that
exists only in the plan is not a motivated change; it is an unexplained jump with a comment
attached.

Origin: the Noa first-live join from Shot A to Shot BC read as a small jump because the body
shifted slightly and the image became a little brighter at the same time. Neither difference is
large. Together they tell the viewer that something was reset between the two clips. The practical
fix is not tighter exposure matching but letting Noa turn on a light, so the brightness change has
a reason and the small body shift rides along with it.

This can be used today without any contract change: write the causing action as a beat in one of
the two shots. What the contract cannot yet express is the distinction itself — a declared change
with an on-screen cause is not the same thing as `intentional_discontinuity`, which only means
"do not check this join". Recorded for the schema owner.
