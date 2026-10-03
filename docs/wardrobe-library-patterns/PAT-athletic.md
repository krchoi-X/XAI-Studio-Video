# PAT-athletic — 운동복 / Athletic-sportswear

- **id:** `PAT-athletic`
- **title KR/EN:** 운동복 / Athletic-sportswear
- **intent:** Fill an activewear library with sport-specific kits, practical footwear, movement poses, and varied training environments.
- **adult gate:** Verify an explicitly adult character record before generation; do not infer age. If identity/age is ambiguous, stop before generation.
- **default engine:** `qwen21`
- **actor:** `hermes`
- **strategy:** `strict_translation`

## Run shape

Suggested night-batch shape: **24 scenes × `count: 4`** (96 images). Rotate yoga, running, tennis, swimming training, cycling, hiking, basketball, strength training, dance rehearsal, and warm-up. Name sport, top, bottom, footwear, and any intentional protective gear.

## Hard policy

- No identity Soft and no identity-reference image on wardrobe-diversity fills.
- `immutable_constraints` / `constraints-json` is HARD: `{"coverage":"clothed","wardrobe":"<sport-specific exact kit>"}`.
- Full-body head-to-toe, exactly one adult woman, practical non-erotic sports direction. No invented street clothes, coat, blazer, or accessories. Keep sports kit and footwear consistent with the named activity.

## Sample items

### Item 01 — running

```json
{"coverage":"clothed","wardrobe":"teal breathable running tank, black running shorts, white running shoes, sports watch"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman preparing for a park run, teal breathable running tank, black running shorts, white running shoes, and sports watch; athletic catalog framing, no jacket or extra layer, head-to-toe.

### Item 02 — yoga

```json
{"coverage":"clothed","wardrobe":"plum long-sleeve yoga top, charcoal high-waist leggings, barefoot"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman in a quiet yoga studio, plum long-sleeve yoga top, charcoal high-waist leggings, barefoot; one controlled standing stretch, no towel, coat, or invented layer, full-body head-to-toe.

### Item 03 — tennis

```json
{"coverage":"clothed","wardrobe":"white tennis polo, cobalt pleated tennis skirt with integrated shorts, white tennis shoes, visor"}
```

English request snippet:

> Photoreal live-action full-body photograph of exactly one adult woman on a tennis court, white tennis polo, cobalt pleated tennis skirt with integrated shorts, white tennis shoes, and visor; sport-specific kit only, no jacket or extra clothing, natural daylight, head-to-toe.

## Output and never-list

Output root reminder: `D:\AI_Studio\library\characters\<id>\generations\`.

Never: parallel WanGP, stopping live Mira, identity Soft leak, `--identity-reference`, sport/footwear mismatch, sexualized direction, invented street layers, coverage mismatch, or engine switching without instruction.
