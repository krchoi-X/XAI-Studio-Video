# PAT-dress — 드레스 / Dress

- **id:** `PAT-dress`
- **title KR/EN:** 드레스 / Dress
- **intent:** Create a dress-centered library that varies silhouette, length, fabric, color, and occasion without importing surprise layers.
- **adult gate:** Verify an explicitly adult character record before generation; do not infer age. This pattern is clothed, but an ambiguous character remains a blocking condition.
- **default engine:** `qwen21`
- **actor:** `hermes`
- **strategy:** `strict_translation`

## Run shape

Suggested night-batch shape: **22 scenes × `count: 4`** (88 images). Rotate shirt dress, wrap dress, knit dress, sundress, midi, maxi, slip-style, tailored, cocktail, and seasonal dresses. Name footwear and any intentional accessory; default to no jacket or coat.

## Hard policy

- No identity Soft and no identity-reference image on wardrobe-diversity fills.
- `immutable_constraints` / `constraints-json` is HARD: `{"coverage":"clothed","wardrobe":"<exact dress, footwear, named layers if any>"}`.
- Each item has one primary dress. The request must forbid invented cardigan, blazer, coat, undershirt, or trousers. Use neutral full-body, head-to-toe direction and exactly one adult woman.

## Sample items

### Item 01 — linen sundress

```json
{"coverage":"clothed","wardrobe":"sage-green linen midi sundress, flat leather sandals"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman in a sage-green linen midi sundress and flat leather sandals, in a sunlit botanical garden; no cardigan, blazer, coat, or invented layer; head-to-toe, natural pose.

### Item 02 — tailored shirt dress

```json
{"coverage":"clothed","wardrobe":"navy cotton shirt dress, narrow belt, black loafers"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing a navy cotton shirt dress with a narrow belt and black loafers, in a quiet office corridor; no jacket, trousers, or extra layer; full-body head-to-toe, realistic light.

### Item 03 — evening dress

```json
{"coverage":"clothed","wardrobe":"burgundy velvet ankle-length evening dress, low black heels"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing a burgundy velvet ankle-length evening dress and low black heels, in a softly lit gallery; no coat, shawl, or invented layer; neutral elegant pose, head-to-toe.

## Output and never-list

Output root reminder: `D:\AI_Studio\library\characters\<id>\generations\`.

Never: parallel WanGP, stopping live Mira, identity Soft leak, `--identity-reference`, dress plus unrequested jacket, wardrobe/coverage mismatch, sexualized framing, or engine switching without instruction.
