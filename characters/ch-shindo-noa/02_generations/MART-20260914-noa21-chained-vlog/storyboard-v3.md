# Storyboard — Noa, after work, v3

Status: **draft. Nothing rendered.** The machine goes back to Codex.

Same story as v2 — the arc survived review — rebuilt around three things v2 measured and one thing the
operator supplied.

| What v2 established | What v3 does about it |
|---|---|
| Multi-shot works: one 7.3 s render gave 3 shots and 2 clean cuts (frame diff 73/80 vs 24-46 within shots) | Keep it. Five renders, fifteen cuts, ~36 s. |
| The FL2VA chain holds one step and is a different person by the second (0.735 → 0.776 → 0.324 → 0.017 → 0.066, ceiling 0.551) | **No chain.** Every render is its own anchor — see "Joining" below. |
| The camera was in the same place in every shot, because a measurement rule was driving the directing | Placed cameras at home, two shots with no face in them, and a location map per place. |
| Nine transitions came out of a render asked for three | Cut list declared once with **only**. |

Plus the techniques from `docs/multi-shot-prompt-analysis.md`: cut on action, physics as a global rule, the
Foley disclaimer, reference scoped by exclusion, emotion as muscles with a disambiguation.

Long single renders are the real answer to joining, and they are possible — the operator has made
thirty-second pieces — but a thirty-second render costs six to eight hours here. That belongs on a rented
GPU. This plan is for the 7.3 s unit.

---

## Joining: the one untested idea this plan rests on

v2 joined renders by starting each on the previous one's final frame with FL2VA, and identity collapsed by
the second step. But Ref2VA takes **two** reference pictures, and we have only ever used them as
portrait + face crop.

**Every render here is Ref2VA with `<Picture 1>` = the `noa-21` portrait and `<Picture 2>` = the previous
render's final frame.** Identity comes from the portrait every time, so chain depth is always zero;
continuity comes from the frame. Earlier work found dual reference *helps* H3 while it hurt the krea2 edit
path, which is the reason to expect this to work at all.

**This is unverified.** R1→R2 is the gate: if R2's identity drops the way FL2VA's depth-2 did, or if the
model reads `<Picture 2>` as a second person rather than a continuation, the plan stops and gets rethought
rather than queued.

The fallback, if it fails: an anchor still per location. Do **not** generate one — `krea2_raw_edit` was
tried on 2026-09-14 and scored 0.559 then 0.616 while also having to invent a room. `VLOG-20260913`'s
`d1-washed` already has Noa at home in a grey tee at 0.791-0.799 and 264-269 px. Use a real frame.

---

## Global blocks (go into every prompt)

### References

> Take from `<Picture 1>` and `<Picture 2>`: her facial identity, hair, skin and body proportions.
> **Ignore their background, framing, lighting and pose.** `<Picture 2>` is the state this shot continues
> from: the same clothes, the same hair, the same props in the same hands. **Neither picture is the opening
> frame of this video.**

### Physics

> Nothing appears in her hands that she was not shown taking. Nothing is put down without being set down on
> camera. The basket fills and never empties; the bag she carries out is what the basket held. Steam rises
> only from hot things. She never changes clothes off camera.

### Audio

> She is the only person who speaks, in one consistent voice: quiet, low, unhurried, a little dry, an
> ordinary Japanese-accented English that never performs. Only the text inside `<d>` tags is spoken;
> **every other sound named here is Foley, not something anyone says.** Continuous quiet room tone under it.
> No music louder than the voice, no subtitles, no added dialogue.

### Locks

> Hard cuts only at the two times named in this prompt. No pans, zooms or focus pulls during a spoken line.
> No slow motion, no freeze, no fade, no title, no trailing footage. She is right-handed throughout.

---

## Location maps

**A · outside the shop.** Shop front north, road south; she stands on the pavement facing the shop. Every
camera stays south of her, on the road side. Shop window and its light screen-left, dark street screen-right.

**B · inside the shop.** Aisle runs north-south, shelves both sides. Every camera stays at the south end
looking north; the lit chiller runs screen-left down the whole aisle.

**C · the flat.** Kitchen is a narrow galley, stove and counter along the west wall, window at the north
end, doorway south. **Her phone is standing on the counter or on a shelf — it is not in her hand.** Every
camera stays on the east side looking west, so the stove is always screen-left and the dark window is always
at the top of frame.

---

## R1 · outside, leaving work · anchor only (no `<Picture 2>`)

Hard cuts at 2.4 and 4.9 only.

| | Crop | Beats | Line |
|---|---|---|---|
| S1 | Her head and shoulders, cropped below the collarbone, face filling the frame | Tired: hair down and untidy, strands stuck to her cheek. She pushes them back with the back of her wrist and breathes out. **Cut as her hands start to rise toward her hair.** | EN "I am tired. I do not want to cook." |
| S2 | Head to waist, upper body filling the frame | **Her hands continue the rise they began** — gathers her hair, twists the tie twice, pulls it into a low ponytail, tugs it tight. **Cut as her hands drop away from it.** | — |
| S3 | Head and shoulders again | Hands still falling. Ponytail done. She looks past the camera at the shop door; her jaw sets slightly. | — |

Carries out: ponytail, blazer, empty hands, night street.

## R2 · the bento goes back · the hinge

Hard cuts at 2.4 and 4.9 only.

| | Crop | Beats | Line |
|---|---|---|---|
| S1 | Head to waist | In through the door, lifts a red plastic basket off the stack, hooks it over her arm and goes to the ready-made shelf. **Cut as her free hand reaches out.** | — |
| S2 | Down past her shoulder at her hands; her face at the top edge | **That same hand closes on a packed bento.** She holds it. A beat. She sets it back on the shelf and her hand stays on it a moment longer. **Cut as her head starts to turn.** | — |
| S3 | Head and shoulders | **The turn continues.** Her eyes catch something down the aisle. Both inner brows lift a little and her mouth is not quite a smile: she has thought of something she wants, not resignation. | EN "No. I want to make something." |

Carries out: red basket, nearly empty. The line answers R1's line, which is why it is there.

## R3 · what she actually wanted

Hard cuts at 2.4 and 4.9 only.

| | Crop | Beats | Line |
|---|---|---|---|
| S1 | Down past her shoulder at her hands and the shelf | Picks up the thing she crossed the shop for, turns it over once, puts it in the basket. A small private half-smile that does not reach a full one. **Cut as the basket starts to swing up.** | JA 「これ、いつもは買わないけど。」 |
| S2 | Head to waist | **The basket completes that swing** into her other hand, visibly fuller and heavier. She looks down into it. | EN "That is more than I planned." |
| S3 | Head to waist, outside now | A brown paper bag against her hip, walking away from the lit door into the dark street. | — |

Carries out: paper bag, no basket.

## R4 · home · placed camera, no face in any shot

Hard cuts at 2.4 and 4.9 only. Location map C applies: the phone is propped on the counter.

| | Crop | Beats | Line |
|---|---|---|---|
| S1 | Locked off low on the counter across the galley, seeing the whole narrow kitchen with her at about half frame height | She comes in from the doorway with the bag, sets it on the counter, shoulders dropping. **Cut as her hands open the bag.** | — |
| S2 | Locked off low beside the bag; only her hands and the food, no face | **Those hands continue** — a packet out, two vegetables, something cold set aside. | — |
| S3 | Locked off on the counter beside her at chest height, her in profile at the edge of frame, the stove centre | The blazer comes off and goes over the chair back; she pulls a soft grey tee straight at the hem and reaches for a pot. | — |

Three shots, **no close-up**. That is deliberate: a close-up in every render was a measurement convenience
of ours and it put a camera in the air in front of someone cooking.

Carries out: grey tee, no blazer, pot on the stove.

## R5 · the mistake, and the payoff

Hard cuts at 2.4 and 4.9 only.

| | Crop | Beats | Line |
|---|---|---|---|
| S1 | Locked off close above the stove; only the pot, the ring and the counter, no face at all | The pot climbs and boils over, foam down the side, hissing on the ring. **Cut as a hand enters frame for the lid.** | — |
| S2 | The locked-off wide again from across the galley | **That hand lifts the lid**, she pulls back from the steam, turns the dial down, then stands still a second with one hand on the counter and lets out a short breath that is almost a laugh at herself. **Not alarm: this happens to her.** | — |
| S3 | Her head and shoulders, face filling the frame | A spoonful to her mouth. Eyes down for a beat. Then her cheeks lift, her eyes narrow at the outer corners and crease, and her lips part — **an involuntary smile, pleasure and slight surprise, not politeness.** | EN "Oh. That is actually good." |

Final state: pot on the stove with the ring turned down, spoon in her hand, the smile still alive.

---

## Continuity object

| key | R1 out | R2 out | R3 out | R4 out | R5 out |
|---|---|---|---|---|---|
| `hair` | ponytail | ponytail | ponytail | ponytail | ponytail |
| `top` | blazer + white | blazer + white | blazer + white | grey tee | grey tee |
| `carrying` | — | basket, near empty | paper bag | — | spoon |
| `place` | street A | shop B | shop B → street A | kitchen C | kitchen C |
| `face in frame` | 3 of 3 | 2 of 3 | 1 of 3 | **0 of 3** | 1 of 3 |

## Open questions, in the order they would be answered

1. **Does `<Picture 2>` as the previous final frame work?** R1→R2 is the gate. Everything rests on it.
2. **Does "hard cuts at 2.4 and 4.9 only" stop the extra transitions** that v2's R2 produced nine of?
3. **Do the cut-on-action pairs actually join?** This is the operator's "억지로 붙인 것 같아" and it now has
   a specific mechanism to test rather than an opinion.
4. **Does the makeup wording cost identity?** R1 asks for tired, worn makeup. It scored 0.735 in v2 where
   clean turnaround clips score 0.90-0.95, and the same thing happened twice more the same day. Still never
   tested on purpose; R1's number is a free data point but not a controlled one.
