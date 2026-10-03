# PAT-hanbok — 한복 / Hanbok

- **id:** `PAT-hanbok`
- **title KR/EN:** 한복 / Hanbok
- **intent:** Build a clothed hanbok library with explicit jeogori, chima, ribbon, silhouette, and color rotations across traditional and modern settings.
- **adult gate:** Verify an explicitly adult character record before generation and never infer age. This pattern is clothed, but ambiguity still blocks unverified character work.
- **default engine:** `qwen21`
- **actor:** `hermes`
- **strategy:** `strict_translation`

## Run shape and required rotation

Suggested night-batch shape: **24 scenes × `count: 4`** (96 images). Every item is clothed and must name the full combination. Hermes should rotate:

- **Jeogori:** ivory, white, pale pink, jade, navy, short modern, long traditional, patterned, or embroidered.
- **Chima:** cream, coral, rose, teal, indigo, emerald, charcoal, gold-beige; vary full and modern midi silhouettes.
- **Ribbons / goreum:** red, deep navy, jade, coral, ivory, contrasting two-tone, or a clearly named embroidered ribbon.
- **Color sets:** pastel spring, white-and-indigo, coral-and-cream, jade-and-gold, navy-and-rose, monochrome charcoal, and muted autumn earth tones.
- Include a mix of traditional full hanbok and restrained modern hanbok, but never let a modern item lose the named jeogori/chima structure.

## Hard policy

- Coverage is always **clothed**: `{"coverage":"clothed","wardrobe":"<exact jeogori, chima, ribbon, footwear>"}`.
- No identity Soft and no identity-reference image on wardrobe-diversity fills.
- `immutable_constraints` / `constraints-json` is HARD for coverage and the complete wardrobe string. Do not invent Western jacket, coat, blouse, trousers, or extra layers. Exactly one adult woman, full-body head-to-toe, respectful non-caricatured styling.

## Sample items

### Item 01 — pastel traditional

```json
{"coverage":"clothed","wardrobe":"ivory jeogori, pale pink full-length chima, coral goreum ribbon, simple white traditional shoes"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing an ivory jeogori, pale pink full-length chima, coral goreum ribbon, and simple white traditional shoes, in a quiet hanok courtyard; coverage fully clothed, no Western jacket or extra layer, head-to-toe.

### Item 02 — indigo and jade

```json
{"coverage":"clothed","wardrobe":"deep jade short jeogori, indigo chima, ivory-and-navy two-tone ribbon, white beoseon socks, flat traditional shoes"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman in a deep jade short jeogori, indigo chima, ivory-and-navy two-tone ribbon, white beoseon socks, and flat traditional shoes, in a museum courtyard; fully clothed, no invented coat or blouse, realistic daylight.

### Item 03 — modern autumn hanbok

```json
{"coverage":"clothed","wardrobe":"charcoal modern jeogori, muted rust midi chima, gold-embroidered navy ribbon, black traditional flats"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman wearing a charcoal modern jeogori, muted rust midi chima, gold-embroidered navy ribbon, and black traditional flats, on an autumn street; modern hanbok remains fully specified and clothed, no blazer or extra layer, head-to-toe.

## Output and never-list

Output root reminder: `D:\AI_Studio\library\characters\<id>\generations\`.

Never: parallel WanGP, stopping live Mira, identity Soft leak, `--identity-reference`, caricature/costume distortion, missing jeogori/chima/ribbon locks, coverage mismatch, invented Western layers, or engine switching without instruction.
