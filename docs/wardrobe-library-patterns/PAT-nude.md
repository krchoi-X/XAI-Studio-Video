# PAT-nude — 누드 전용 / Nude-only

- **id:** `PAT-nude`
- **title KR/EN:** 누드 전용 / Nude-only
- **intent:** Produce a strictly nude-only adult still-library bucket with neutral, non-erotic full-body catalog/studio direction.
- **adult gate:** Mandatory and blocking. Read the character record and require explicit adult wording and adult proportions/context. If minor or ambiguous, refuse this pattern; do not infer adulthood or substitute suggestive clothing.
- **default engine:** `qwen21`
- **actor:** `hermes`
- **strategy:** `strict_translation`

## Run shape

Suggested night-batch shape: **20 scenes × `count: 4`** (80 images). Vary location, pose, neutral lighting, and camera distance while keeping every item nude-only. Keep the framing non-erotic and practical: studio reference, seated portrait extension, standing full-body, or natural uncluttered room.

## Hard policy

- No identity Soft and no identity-reference image on wardrobe-diversity fills.
- `immutable_constraints` / `constraints-json` is HARD and must be exactly `{"coverage":"none","wardrobe":"none"}` for every item.
- The English request must say completely nude and forbid clothing, towel, robe, sheet, censor, and invented objects. Do not add underwear, swimsuit, accessories, or footwear unless a separate pattern is selected; nude-only means no wardrobe.

## Sample items

### Item 01 — neutral studio standing

```json
{"coverage":"none","wardrobe":"none"}
```

English request snippet:

> Photoreal live-action photograph of exactly one adult woman, completely nude and barefoot, standing neutrally in a private matte studio; full-body head-to-toe, non-erotic catalog framing, soft even light; no clothing, towel, robe, sheet, censor, text, or other person.

### Item 02 — seated loft reference

```json
{"coverage":"none","wardrobe":"none"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman, completely nude and barefoot, seated neutrally on a simple wooden stool in a private uncluttered loft; non-erotic reference direction, no clothing or coverings, no censor, no text, no other person.

### Item 03 — natural window light

```json
{"coverage":"none","wardrobe":"none"}
```

English request snippet:

> Photoreal live-action photograph of exactly one adult woman, completely nude and barefoot, standing in a private room with soft window light and a plain background; head-to-toe, neutral non-erotic pose; no towel, robe, sheet, clothing, censor, or extra person.

## Output and never-list

Output root reminder: `D:\AI_Studio\library\characters\<id>\generations\`.

Never: parallel WanGP, stopping live Mira, any minor or ambiguous-age subject, identity Soft leak, `--identity-reference`, wardrobe text other than `none`, erotic/sexualized direction, censor workaround, or engine switching without instruction.
