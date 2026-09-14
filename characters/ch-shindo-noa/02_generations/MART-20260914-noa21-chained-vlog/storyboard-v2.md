# Storyboard — Noa, after work, v2

Status: **draft for review. Nothing rendered.**

Supersedes the six-render v1 in this session. v1 proved the mechanism (the FL2VA seam is invisible, the
basket survived a cut, Japanese speech works) and failed on design: state changes were split across renders
instead of being shown, and three shots lost their crop instruction and came out at 61-84 px of face.

## The rule this is built on

> Every change that would break continuity happens **inside** a render, on screen.
> A render only ends when the new state is stable.
> The final frame of that render starts the next one.

Continuity is then never something the model guesses between renders. This is the operator's formulation of
2026-09-14 and it matches `docs/vlog-production-orchestration.md` §4: use more than one look reference
"only when the transformation itself matters inside the shot".

Five transitions in this vlog. Each one sits in the middle of a render, never on a cut:

| # | Transition | Render | Shot |
|---|---|---|---|
| 1 | hair down → ponytail | R1 | S2 |
| 2 | empty hands → shopping basket | R2 | S1 |
| — | **not cooking → cooking** (the story's turn, not a prop) | R2 | S2-S3 |
| 3 | basket → paper bag | R3 | S3 |
| 4 | blazer → home tee | R4 | S2 |
| 5 | pot calm → boiled over | R5 | S1 |

## The arc

v1 and the first draft of this had no turn in them: she says she does not want to cook, then buys
ingredients and cooks. The operator caught it. A vlog still needs a reason for the thing that happens.

```
tired, does not want to cook        R1
  → reaches for the easy way out    R2 S2   (a bento)
  → puts it back                    R2 S2   ← the turn
  → wants something specific        R2 S3 / R3 S1
  → buys more than she meant to     R3 S2
  → small mishap                    R5 S1
  → it turns out well               R5 S3
```

The turn is an action, not an explanation: she holds the bento, puts it down, and her hand stays on it a
moment. The line after it only confirms what the hand already said.

## Shape

Five renders of 7.3 s, three shots each — **15 cuts, about 36 s, 2.4 s per cut.** v1 was six renders and six
cuts at 7.3 s each, which is the montage pacing the operator rejected.

Multi-shot inside one render is **not yet verified on this machine**. The evidence for it: the H3 prompt
format writes `<Subject 1> (appears in [Shot 1])`, which only means something if a subject can appear in a
subset of several shots; `docs/toyxyz-h3-prompter-review.md` states that later shot boundaries create cuts;
and in v1 `m3-unusual` moved from the street to inside the shop within one render without being asked to.
**R1 is the gate.** If its three shots come out as one continuous take, the rest is re-planned, not queued.

## Framing, stated as where the crop falls

Not as shot-scale words. "A medium shot of her on the pavement with the street behind her" produced a figure
a tenth of the frame twice in two days; "holds her head and shoulders, cropped below the collarbone"
produced a close-up every time.

| Code | Crop wording used in the prompt | Face |
|---|---|---|
| **CU** | holds her head and the top of her shoulders, cropped just below the collarbone, her face filling most of the frame | 250-400 px |
| **MS** | holds her from the top of her head to her waist, her upper body filling most of the frame | 120-180 px |
| **OTS** | looks down past her shoulder at what her hands are doing, her hands and the objects filling most of the frame, her face at the top edge | 60-90 px |

**Every render carries at least one CU.** That is deliberate: identity below ~150 px of face measures
framing rather than drift, so v1 could not tell whether the chain was decaying. With a CU in each render the
chain-drift question gets an answer at every depth.

---

## R1 — leaving work · Ref2VA anchor

Carried in: nothing (anchor). Carried out: **ponytail, blazer, night street, paper-free hands.**

| Shot | Time | Crop | Action | Line |
|---|---|---|---|---|
| S1 | 0.0-2.4 | CU | Tired, hair down and untidy, a few strands stuck to her cheek, makeup worn down. Pushes hair off her face with the back of her wrist. | EN "I am tired. I do not want to cook." |
| S2 | 2.4-4.9 | MS | **Gathers her hair back, twists the tie twice, pulls it into a low ponytail, tugs it tight.** | — |
| S3 | 4.9-7.3 | CU | Ponytail done. Looks past the camera at the shop door; her face settles into something decided. | — |

The only render that carries the identity anchor sentence, and a short one.

## R2 — the bento goes back · FL2VA ← R1 final frame

**This render is the hinge of the whole thing.** She said she did not want to cook; she has to change her
mind on camera or the rest does not follow.

Carried in: ponytail, blazer, her face. Carried out: **red basket, still nearly empty.**

| Shot | Time | Crop | Action | Line |
|---|---|---|---|---|
| S1 | 0.0-2.4 | MS | Through the door, **takes a red plastic basket** from the stack and hooks it over her arm. Straight to the ready-made shelf. | — |
| S2 | 2.4-4.9 | OTS | **Picks up a packed bento. Holds it. A beat. Puts it back on the shelf** and her hand stays on it a moment longer. | — |
| S3 | 4.9-7.3 | CU | Something across the aisle has her attention; she is already turning toward it. | EN "No. I want to make something." |

S3's line answers R1's line directly, which is the point of it.

## R3 — what she actually wanted · FL2VA ← R2 final frame

Carried in: basket, ponytail, blazer. Carried out: **paper grocery bag, no basket.**

| Shot | Time | Crop | Action | Line |
|---|---|---|---|---|
| S1 | 0.0-2.4 | OTS | At the fresh shelf, **picks up the thing she came back for** — something she does not usually buy — turns it over once and puts it in with a small private half-smile. | JA 「これ、いつもは買わないけど。」 |
| S2 | 2.4-4.9 | MS | Basket visibly fuller now. Shifts it to her other hand, looks down into it. | EN "That is more than I planned." |
| S3 | 4.9-7.3 | MS | **Lifts a full paper bag against her hip** and pushes out through the door into the night. | — |

The "more than I planned" line only earns itself here: she walked in for one bento.

## R4 — home, and out of the blazer · FL2VA ← R3 final frame

Carried in: paper bag, blazer, ponytail. Carried out: **home tee, no blazer, no bag.**

| Shot | Time | Crop | Action | Line |
|---|---|---|---|---|
| S1 | 0.0-2.4 | MS | Inside the flat, **sets the bag down** on the counter, shoulders dropping. | — |
| S2 | 2.4-4.9 | MS | **Pulls the blazer off and hangs it over the back of a chair**, then pulls a soft grey tee straight at the hem. | — |
| S3 | 4.9-7.3 | CU | In the tee now, ponytail still up, turning toward the stove. | — |

The transition the operator named. It is in the middle of a render so the blazer leaves on camera; v1 simply
had her in a different top with no explanation.

## R5 — the mistake, and the payoff · FL2VA ← R4 final frame

Carried in: home tee, ponytail, kitchen.

| Shot | Time | Crop | Action | Line |
|---|---|---|---|---|
| S1 | 0.0-2.4 | OTS | **The pot climbs and boils over**, foam down the side, hissing on the ring. | — |
| S2 | 2.4-4.9 | MS | Lifts the lid fast, pulls her hand back from the steam, turns the dial down, one flustered breath that is almost a laugh at herself. | — |
| S3 | 4.9-7.3 | CU | Tastes a spoonful. A beat. **A real, warm, unguarded smile** — the one she does not show people. | EN "Oh. That is actually good." |

---

## Continuity object

Stable keys, so a reviewer can diff them against the render.

| key | R1 out | R2 out | R3 out | R4 out | R5 out |
|---|---|---|---|---|---|
| `hair` | ponytail | ponytail | ponytail | ponytail | ponytail |
| `top` | blazer + white | blazer + white | blazer + white | grey tee | grey tee |
| `carrying` | — | red basket, near empty | paper bag | — | — |
| `place` | street, night | shop | street, night | flat | flat kitchen |
| `state` | tired, resigned | turning | wry | settled | pleased |

## What is deliberately not in the prompts

The identity anchor appears once, in R1, and short. In the twenty vlog shots of 2026-09-13 a ninety-word
face description rode on every shot against roughly fifteen words of behaviour, and the result was an
average face doing very little — the operator's "평균으로 회귀". The record's restraint is the baseline, not
the content of every scene: the untidy hair, the unusual packet, the boil-over and the real smile are not in
the DNA and should not be.

## Open risks

1. **Multi-shot is unverified.** R1 is the gate; if it renders as one take the whole shape changes.
2. **A four-deep FL2VA chain is untested.** v1 got one clean step. Each render has a CU so the answer will
   be measurable this time, and R4 is the natural place for a Ref2VA re-anchor if it decays — at the cost of
   losing the on-camera blazer removal.
3. **Direction outside `<d>` can be spoken** — it happened twice on 2026-09-13. Wording near the dialogue
   stays short and avoids anything that reads as a line.
4. **Voice.** English is unchanged from the version the operator called too American; the Japanese line in
   R2 is the only sample of the alternative and it worked, transcribing back as Japanese.
