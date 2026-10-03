# Hermes wardrobe-library pattern pack

A named, docs-only pattern pack for filling character still libraries with local WanGP Qwen Image 2.1 jobs. This pack is an index and a set of reusable Hermes templates; **do not start generation from this documentation alone**. Generation waits for an explicit user instruction.

## Base playbook

Read the canonical playbook first:

- `D:\codex\XAI-studio\docs\hermes-wardrobe-library-stills-playbook.md`
- `D:\AI_Studio\docs\hermes-wardrobe-library-stills-playbook.md`

The playbook defines adult gating, preflight, one-GPU-job sequencing, output layout, immutable constraint encoding, and completion reporting.

## Pattern index

| ID | Korean / English | Use when | Coverage focus |
|---|---|---|---|
| `PAT-mixed` | 복합 / Mixed | A broad Mira-like wardrobe library is wanted in one run. | Nude, swimsuit, underwear, dress, shorts/everyday, and role scenes; adult gate applies. |
| `PAT-swimsuit` | 수영복 전용 / Swimsuit-only | Swimwear variety is the only target. | Clothed; rotate named swimsuit types and silhouettes. |
| `PAT-nude` | 누드 전용 / Nude-only | A deliberately nude-only adult library is requested. | `coverage: none`, `wardrobe: none`; adult gate is mandatory. |
| `PAT-casual` | 평상복 / Casual-everyday | Natural daily-life wardrobe and locations are wanted. | Clothed; explicit top, bottom, footwear, and no invented layers. |
| `PAT-dress` | 드레스 / Dress | Dress silhouettes, lengths, fabrics, and occasions are wanted. | Clothed; one named dress per item, no surprise jacket/coat. |
| `PAT-hanbok` | 한복 / Hanbok | Traditional or modernized hanbok variation is wanted. | Clothed; jeogori/chima and ribbon/color variants are explicit. |
| `PAT-athletic` | 운동복 / Athletic-sportswear | Training, sport, and activewear scenes are wanted. | Clothed; named sport kit, footwear, and setting are explicit. |

## How Hermes picks one

1. Confirm the character ID and adult status before any pattern containing nude, swimsuit, or underwear. Refuse disallowed or ambiguous cases; do not infer adulthood.
2. Select the narrowest matching pattern. Use `PAT-mixed` only when the request intentionally combines multiple wardrobe classes.
3. Copy its item shape into a Hermes night-batch plan. Keep `engine=qwen21`, `actor=hermes`, `strategy=strict_translation`, and one sequential WanGP job.
4. Keep each item's `immutable_constraints` aligned with the request. `coverage` and `wardrobe` are HARD, not Soft-only prose.
5. Choose pose, location, lighting, and color variants without changing the selected pattern's wardrobe lock. Do not add identity references for a wardrobe-diversity fill.
6. Generation begins only after a separate explicit user instruction; this pack itself never starts a job and must not stop the live Mira job.

## Shared defaults and guardrails

- Default engine: `qwen21`
- Actor: `hermes`
- Strategy: `strict_translation`
- Wardrobe fill Soft policy: **no identity Soft** / no identity-reference image on diverse wardrobe fills.
- Constraints policy: `immutable_constraints` / `constraints-json` is HARD for both `coverage` and `wardrobe`.
- Recommended shape: 20–25 scenes × `count: 4` (about 80–100 images), sequentially; stay within the base playbook and night-batch limits.
- Output root: `D:\AI_Studio\library\characters\<id>\generations\`
- Never start image generation, kill or stop the live Mira job, run parallel WanGP, or message Contents Creator from this pack.

## Files

- `PAT-mixed.md`
- `PAT-swimsuit.md`
- `PAT-nude.md`
- `PAT-casual.md`
- `PAT-dress.md`
- `PAT-hanbok.md`
- `PAT-athletic.md`
