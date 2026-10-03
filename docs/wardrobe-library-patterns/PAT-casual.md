# PAT-casual — 평상복 / Casual-everyday

- **id:** `PAT-casual`
- **title KR/EN:** 평상복 / Casual-everyday
- **intent:** Fill a practical everyday wardrobe library with believable daily outfits, roles, locations, and full-body poses.
- **adult gate:** Verify the character record before generation; use only an explicitly adult character for this library. Do not infer age from appearance. This pattern is clothed, but ambiguity still blocks unverified character work.
- **default engine:** `qwen21`
- **actor:** `hermes`
- **strategy:** `strict_translation`

## Run shape

Suggested night-batch shape: **24 scenes × `count: 4`** (96 images). Rotate errands, cafe, commute, home office, market, library, weekend walk, and weather-appropriate daily scenes. Use one explicit outfit per item with TOP, BOTTOM, and FOOTWEAR.

## Hard policy

- No identity Soft and no identity-reference image on wardrobe-diversity fills.
- `immutable_constraints` / `constraints-json` is HARD: `{"coverage":"clothed","wardrobe":"<exact top, bottom, footwear>"}`.
- Say no invented blazer, coat, cardigan, extra shirt, or accessories. If a layer is desired, name it in the wardrobe string and request. Keep exactly one adult woman, full-body head-to-toe, photoreal live-action.

## Sample items

### Item 01 — cafe

```json
{"coverage":"clothed","wardrobe":"cream cotton T-shirt, straight-leg blue jeans, white low-top sneakers"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman at a neighborhood cafe, cream cotton T-shirt, straight-leg blue jeans, and white low-top sneakers; relaxed standing pose, head-to-toe; no blazer, coat, or invented layer.

### Item 02 — rainy commute

```json
{"coverage":"clothed","wardrobe":"mustard knit sweater, black ankle-length trousers, brown ankle boots, transparent raincoat"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman on a rainy city commute, mustard knit sweater, black ankle-length trousers, brown ankle boots, and a transparent raincoat; every layer is intentional, no extra clothing; head-to-toe documentary light.

### Item 03 — weekend market

```json
{"coverage":"clothed","wardrobe":"striped short-sleeve shirt, khaki shorts, canvas slip-on shoes"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman at a weekend market, striped short-sleeve shirt, khaki shorts, and canvas slip-on shoes; candid but clear head-to-toe framing, no jacket or extra layer, natural daylight.

## Output and never-list

Output root reminder: `D:\AI_Studio\library\characters\<id>\generations\`.

Never: parallel WanGP, stopping live Mira, identity Soft leak, `--identity-reference`, unnamed outfit layers, coverage/wardrobe mismatch, creative expansion, or engine switching without instruction.
