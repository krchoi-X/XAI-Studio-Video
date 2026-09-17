# Storyboard Candidate Template

Use this format when proposing production-ready storyboard options.

The goal is not maximum prose detail. The goal is to preserve directing intent well enough that another agent can produce stills/video without reconstructing the original chat.

## Candidate header

```text
Candidate ID:
Title:
Construction: long_take | multi_cut | hybrid
Opening family:
Primary emotional/visual intent:
Why this fits the episode:
Production confidence: high | medium | exploratory
```

## Shot / beat table

For each shot or continuous beat:

```text
S01 / 0.0–3.0s
Purpose:
Subject scale:
Camera:
Camera support:
Character/object position:
Action / performance:
Environment / spatial anchors:
Dialogue / sound:
Continuity from previous:
Handoff to next:
Reference needs:
Renderer approach:
Risk / fallback:
```

For a true long take, keep one shot ID and divide it into timed beats rather than pretending each beat is a cut.

Example:

```text
S01 / 0.0–10.0s — fixed-camera introduction
Construction: long_take

0.0–2.0
- empty medium-wide room
- camera fixed on shelf, eye-level
- Noa enters from screen right

2.0–5.0
- she checks framing from a distance
- full body remains visible
- she takes one small step back

5.0–7.0
- slight awkward smile, small wave

7.0–10.0
- she sits / settles and begins speaking

Continuity requirement:
- room layout, camera position, wardrobe, lighting, and prop states must remain unchanged through the take.
```

## Production plan

Every candidate must end with a compact executable plan:

```text
Identity authority:
Still-board needed: yes/no
Still frames needed:
Motion/control reference needed:
Planned renderer:
Clip count:
Expected regeneration unit:
Audio plan:
Finishing/upscale plan:
Most likely failure:
Fallback construction:
```

## Comparison notes

When two or more candidates are presented, explicitly explain how they differ in **visual construction**, not merely wording.

Compare at least:

- reveal order;
- subject scale progression;
- camera support/movement;
- long take vs edit rhythm;
- use of environment/object;
- continuity risk;
- production cost/risk.

## Candidate-generation constraints

- Do not default every vlog to face-first selfie framing.
- Do not default every correction to a fixed wide shot either.
- Do not create multiple candidates that are essentially the same shot sequence with different adjectives.
- Do not assume a renderer will invent continuity correctly when it has not been specified.
- Do not require unavailable tools.
- Do not copy an approved storyboard literally unless the user asks for a repeatable format.
- Do not turn a failure lesson into a permanent aesthetic ban.

## Default proposal strategy

When a visible comparison will help the user discover an unresolved intent, propose:

- **Candidate A — continuity-first / production-safe**
- **Candidate B — visually distinctive / exploratory**

When the visual intent is already sufficiently clear, one strong storyboard draft is enough outside an active contract that requires a candidate count. A third candidate is justified only when it represents a genuinely different construction family.

## Human review questions encoded as checks

The AI should self-check these before presenting:

- Can I describe what the first frame shows without ambiguity?
- Do I know who/what is holding or supporting the camera?
- Is the character's scale deliberate?
- Is the environment doing useful narrative work?
- Does every cut have a reason?
- If it is a long take, does something meaningful evolve inside the frame?
- Are continuity states written where needed?
- Can this actually be produced with current tools?
- Is the second candidate meaningfully different from the first?
