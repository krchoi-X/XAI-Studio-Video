# PAT-swimsuit — 수영복 전용 / Swimsuit-only

- **id:** `PAT-swimsuit`
- **title KR/EN:** 수영복 전용 / Swimsuit-only
- **intent:** Build a swimsuit-only library while rotating clearly named silhouettes, coverage levels, colors, and sport/leisure contexts.
- **adult gate:** Mandatory for this adult wardrobe library. Verify explicit adult status in the character record before use; never infer age. If ambiguous, stop before generation.
- **default engine:** `qwen21`
- **actor:** `hermes`
- **strategy:** `strict_translation`

## Run shape and required rotation

Suggested night-batch shape: **20–25 scenes × `count: 4`**. Every item remains swimsuit-only and clothed. Hermes must rotate, not collapse into generic swimwear, through these named variants (repeat only after the list is covered):

1. classic solid one-piece
2. square-neck one-piece
3. asymmetric one-shoulder one-piece
4. athletic racerback one-piece
5. bikini with triangle top and matching brief
6. bandeau bikini with matching brief
7. high-waist bikini
8. high-waist retro two-piece
9. sport bikini / swim-training two-piece
10. micro bikini (adult-only, non-erotic catalog framing)
11. tankini with matching swim bottoms
12. long-sleeve rash-guard swimsuit
13. cutout one-piece
14. swim dress
15. surf suit / short-sleeve wetsuit-style swimsuit

Each request must name the exact swimsuit type, color/material, and whether footwear is absent or specified. No cover-ups, towels, robes, jackets, or street clothes unless the selected item explicitly says so; the pattern default is swimsuit-only.

## Hard policy

- No identity Soft and no identity-reference image on a wardrobe-diversity fill.
- `immutable_constraints` / `constraints-json` is HARD: use `{"coverage":"clothed","wardrobe":"<exact swimsuit type and color>"}` for every item.
- Use `strict_translation`; do not let creative expansion soften or replace the swimsuit lock. Full-body head-to-toe framing, exactly one adult woman, no text or other people.

## Sample items

### Item 01 — high-waist bikini

```json
{"coverage":"clothed","wardrobe":"cobalt high-waist bikini, matching top and bottom, barefoot"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing a cobalt high-waist bikini with a matching top and bottom, barefoot beside a quiet pool; swimsuit-only, no cover-up or extra layer, head-to-toe, natural daylight.

### Item 02 — athletic one-piece

```json
{"coverage":"clothed","wardrobe":"black athletic racerback one-piece swimsuit, white swim goggles"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing a black athletic racerback one-piece swimsuit with white swim goggles, at an indoor lap pool; no towel, robe, jacket, or extra clothing; full-body, documentary sports lighting.

### Item 03 — tankini

```json
{"coverage":"clothed","wardrobe":"coral tankini top, matching swim bottoms, simple pool sandals"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing a coral tankini top with matching swim bottoms and simple pool sandals, at a seaside changing-deck area; swimsuit-only, no cover-up, no invented layer; head-to-toe.

## Output and never-list

Output root reminder: `D:\AI_Studio\library\characters\<id>\generations\`.

Never: parallel WanGP, stopping live Mira, identity Soft leak, `--identity-reference`, generic untyped swimsuit, cover-up invention, erotic framing, minors/ambiguous age, or engine switching without instruction.
