# PAT-mixed — 복합 / Mixed wardrobe library

- **id:** `PAT-mixed`
- **title KR/EN:** 복합 / Mixed
- **intent:** Mira-like breadth in one library: deliberately rotate nude, swimsuit, underwear, dress, shorts/everyday, and role scenes.
- **adult gate:** Mandatory. Read the character record first; the character must be explicitly adult. If age is minor or ambiguous, omit nude, swimsuit, and underwear and report the gate failure rather than infer adulthood.
- **default engine:** `qwen21`
- **actor:** `hermes`
- **strategy:** `strict_translation`

## Run shape

Suggested night-batch shape: **25 scenes × `count: 4`** (100 images), sequentially. Allocate the scenes across the six buckets rather than repeating one outfit: 4 nude, 5 swimsuit, 4 underwear, 4 dress, 4 shorts/everyday, and 4 role scenes. Change pose/location/lighting per item while preserving the wardrobe lock.

## Hard policy

- Wardrobe-diversity fills use **no identity Soft** and no `--identity-reference`; stable-DNA text may supply face/body/hair only.
- `immutable_constraints` / `constraints-json` is HARD for `coverage` and `wardrobe`. Nude items use `{"coverage":"none","wardrobe":"none"}`. Every clothed item uses `{"coverage":"clothed","wardrobe":"<exact outfit>"}`.
- Keep the request explicit about exactly one adult woman, full-body head-to-toe framing, TOP/BOTTOM/FOOTWEAR when clothed, or completely nude when nude. Do not invent layers.

## Sample items

### Item 01 — nude studio

```json
{"coverage":"none","wardrobe":"none"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman in a quiet studio, completely nude, barefoot, head-to-toe in frame; no clothing, towel, robe, sheet, censor, or extra person; soft neutral light.

### Item 02 — teal one-piece swimsuit

```json
{"coverage":"clothed","wardrobe":"teal square-neck one-piece swimsuit, barefoot"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing a teal square-neck one-piece swimsuit, barefoot, at an indoor pool; no cover-up, jacket, or invented extra layer; head-to-toe, natural daylight.

### Item 03 — everyday shorts role

```json
{"coverage":"clothed","wardrobe":"cream cotton T-shirt, blue denim shorts, white low-top sneakers"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman in a neighborhood cafe role, cream cotton T-shirt, blue denim shorts, and white low-top sneakers; no blazer or coat; relaxed standing pose, head-to-toe.

## Output and never-list

Output root reminder: `D:\AI_Studio\library\characters\<id>\generations\`.

Never: parallel WanGP, stopping the live Mira job, identity Soft leak, `--identity-reference`, wardrobe-only Soft text without HARD coverage, `creative_expansion`, invented layers, silent DNA edits, or switching engines without a new instruction and report.
