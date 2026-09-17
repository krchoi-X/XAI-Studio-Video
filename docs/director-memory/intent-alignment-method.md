# Visual Intent Alignment Method

## Objective order

1. Produce the best practical video that matches the user's intent.
2. Preserve the approved intent so Claude, Grok, Hermes, Codex or another agent can continue it.
3. Learn from real results so later productions improve.

The second and third objectives support the first. Do not lower the creative result to make the workflow easier to standardize.

## Why the storyboard comes early

The user may recognize the right scene before being able to describe it precisely. Repeated prose can make both sides more confident without making their mental images more similar.

A rough storyboard is therefore a visual question, not merely a finished plan:

```text
incomplete user intent
→ AI states its interpretation and unresolved choices
→ AI presents one or two cheap visual hypotheses
→ user points to what feels right or wrong
→ AI revises only the affected choices
→ user approves the visual intent
→ approved Storyboard Spec
→ engine-specific compilation
```

Use the smallest number of hypotheses needed to expose a meaningful ambiguity. Do not create cosmetic alternatives merely to satisfy a count.

## What the user reviews

The rough board should make it easy to respond without film terminology. Give every panel a stable ID and ask about visible choices:

- Is this the right situation and emotional direction?
- Is the character, space or object receiving the right attention?
- Is the camera too close, distant, active or static?
- Does the sequence feel natural and interesting?
- What should stay exactly as shown?
- What feels wrong even if the reason is hard to name?

Treat responses such as “A feels right,” “too commercial,” “show the room first,” or “this expression, but that composition” as directing evidence. Translate them into explicit accepted, rejected and unresolved decisions; do not require the user to translate them into lens or blocking terminology.

## Choose the storyboard renderer per agent

The method is shared; the drawing tool is not. Before rendering, the active agent must inspect the image tools it can actually use and choose the best authorized route for the decision being tested.

- An agent with native high-quality image generation, such as Codex with GPT Image or Grok when its image tool is available, may render the board directly.
- Claude or Hermes should use the existing local production route with available engines such as Krea 2 or Z-Image rather than pretending to draw.
- If an agent has no usable renderer, it preserves the Storyboard Spec and hands the render request to an authorized executor; it must not claim a board exists.

Use low-cost images for simple composition choices. Use a higher-quality board when identity, acting, expression, environment or subtle mood is what the user needs to judge. Do not force every agent onto the weakest common renderer.

Record the real executor, provider/model, prompt/spec revision, reference roles and output IDs so another agent can understand how the board was made.

## Approval boundary

The visual alignment loop ends only when the user approves the intent represented by the board or explicitly delegates approval. Approval applies to the recorded Storyboard Spec revision, not to an unversioned image.

The approved spec must preserve:

- story and emotional intent;
- beat and reveal order;
- panel/shot purpose;
- composition and blocking that matter;
- identity, spatial, prop, action and emotional continuity;
- timing or relative emphasis;
- accepted and rejected choices;
- hard invariants and remaining creative freedom.

The rough board may be regenerated or discarded. It is evidence attached to the approved spec, not the sole source of truth.

## Compile for the engine

Do not assume a video engine reads a contact sheet exactly as the user does. Compile the approved spec through the active engine adapter.

The compilation may use:

- separated storyboard panels as first, last or timed keyframes;
- a whole storyboard sheet as an additional multimodal reference when supported;
- canonical character, wardrobe, location and prop references with explicit roles;
- text describing motion between frames, camera behavior, duration, dialogue/audio and continuity handoff;
- one request per shot when the engine cannot reliably perform the full sequence.

The engine packet must state which reference controls identity, composition, motion, environment or timing. A storyboard reference must not silently replace canonical identity authority.

## Quality gate

Before production, check that the approved plan is:

- faithful to the user's intended experience;
- interesting enough to justify continued viewing;
- readable as action, emotion and progression rather than a collection of attractive frames;
- internally coherent in story, space and causality;
- continuous where continuity is intended;
- feasible for the chosen engine and available references.

After generation, compare the result with the approved spec. Fix the smallest failed unit while preserving accepted shots and decisions. Only real, reusable production evidence should be proposed for shared memory.

## Multi-agent rule

Every agent reads the same approved spec and its decision history. Agents may propose different interpretations before approval, but after approval they must preserve accepted intent unless the user reopens it. Record the real actor/model and the exact skill/spec revision used.
