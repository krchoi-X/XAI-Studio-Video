---
name: XAI Shot Menu
description: >-
  Use when planning or compiling character video (esp. WanGP MiniMax H3 Ref2VA)
  and the brief is story-level only — pick long take / long shot / medium / CU /
  dynamic cuts without needing shot-by-shot micromanagement.
---
# XAI Shot Menu (H3 / character vlog)

Reusable directing menu. Brief names story + tone; this skill picks framing and tempo. Does not publish.

## Why it exists

Repeating the same MCU + ~7.5s + Picture2 chain makes every episode look like the last. Vary **shot type + role** per beat while keeping identity locks.

## Identity locks (never break)

1. Picture 1 = face master (e.g. noa-21). Continuity = previous last frame as Picture 2 only.
2. Frame by **what fills the crop**, not by what is behind the subject.
3. Face must stay large enough to read when identity matters.
4. One primary movement per beat; physics: nothing in hands unless picked up on camera.
5. Character posture/personality from DNA.

## Shot roles

| Role | Use | Tempo |
|---|---|---|
| `hook` | First ~5s | Prefer dynamic or bold long-shot then punch-in |
| `info` | Facts, lists, dialogue, face lock | Prefer locked MCU/CU |
| `bridge` | Place/wardrobe/time change | Dynamic cut, match on action, or short long-take |

## Shot types

| Code | Name | When | FRAME template |
|---|---|---|---|
| `LT` | Long take | Unbroken action | A single unbroken take holds [crop] while she [one continuous action]; camera [locked|gentle lateral]; no cut inside the beat. |
| `LS` | Long shot | Place, full figure | A steady long shot holds her full figure in [place]; she is small-to-medium in frame on purpose for place, not identity. |
| `MS` | Medium | Body + some face | A steady medium shot holds her from [head to knees|waist]; [prop] enters lower frame. |
| `MCU` | Medium close-up | Default talk/work | A steady medium close-up holds her head and shoulders; [prop edge] at frame bottom. |
| `CU` | Close-up | Emotion / identity | A steady close-up fills the frame with her face [and X]; eyes share one target. |
| `DYN` | Dynamic | Hook / transition (sparingly) | Camera [push-in|lateral follow|snap pan] during [one action]; land on a held [MCU|CU] before speech. |

## Beat recipe

1. List 5–8 story beats from the brief.
2. Tag each `hook` / `info` / `bridge`.
3. Assign shot codes (do not stack 6× MCU).
4. Identity P0 beat → forbid pure `LS` alone; follow with MCU/CU or start tighter.
5. Compile H3: WEIGHT → TEXTURE → LIGHT → SOUND → FRAME; optional `<d>[lang]…</d>`.
6. Vary `video_length` when needed — do not default every shot to the same frame count.

## Anti-sameness

- Opening crop differs from previous episode
- At least one `LS` or `LT` and one `DYN` or `CU`
- No more than three consecutive identical codes
- Hook lands in first 5 seconds of assembly

## Out of scope

Publishing, DNA edits, FL2VA identity chains (prefer Ref2VA + portrait Picture 1).

## Library placement

Canonical: `XAI-Studio-Private/shared-skills/xai-shot-menu/`. Studio `skills/xai-shot-menu` is a mirror/adapter. Knowledge repo gets an index line only — do not mirror full skill text.