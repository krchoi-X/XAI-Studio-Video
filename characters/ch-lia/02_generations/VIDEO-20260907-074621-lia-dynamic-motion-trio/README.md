# Lia dynamic motion trio (MiniMax H3 Ref2VA)

Original idea: Previous intro clips felt too calm/vlog-continuous. Make more moving videos using DNA, including cafe stand-and-leave with a cut into beach walking in a short wind-blown dress. Same person identity is critical.

## Inputs

- Character DNA: `D:\codex\XAI-studio\characters\ch-lia\character.json` v2 (`bd4d3767...`)
- Cafe reference (runtime): `D:\AI_Studio\library\characters\ch-lia\generations\SCENE-20260906-134115-lia-scene-variation\outputs\krea2\run-20260906-134255-f8ffdd8c.jpg` sha256 `6954f1779ed1f5e29a297aa9c23d73c959df16681efe92a54c257bb29202952d`
- Beach short-dress reference (runtime): `D:\AI_Studio\library\characters\ch-lia\generations\SCENE-20260906-133257-lia-scene-variation\outputs\krea2\run-20260906-133438-8db5720b.jpg` sha256 `2acf40bfda49559e0cd3c64bcb1a47ac33de4abfa8a697a000b6e7788052de83`
- Face/home reference available: `D:\AI_Studio\library\characters\ch-lia\imports\inbox\GPT\ChatGPT Image 2026년 9월 4일 오후 10_31_54.png` sha256 `e2df345058cd5d29644f804b39612919ad773debe9388e6bb6cfaa5d64ad0502` (not primary for these shots)
- Settings basis: minimax_h3_ref2va_pruned / KI / 576x768 / video_length 243 / steps 20
- Packaging: FG, expected queue items 1

## Shots

| File | Episode | Motion |
| --- | --- | --- |
| dyn-01-cafe-exit-beach-cut.txt | Cafe exit → occlusion cut → beach short-dress wind walk | MEDIUM, two beats |
| dyn-02-beach-wind-stride.txt | Beach wind walk + head turn | MEDIUM-HIGH walk |
| dyn-03-lookback-exit.txt | Cafe exit look-back then outdoor stride | MEDIUM |

## Paths

- Session: `D:\codex\XAI-studio\characters\ch-lia\02_generations\VIDEO-20260907-074621-lia-dynamic-motion-trio`
- Outputs: `D:\AI_Studio\library\characters\ch-lia\videos\VIDEO-20260907-074621-lia-dynamic-motion-trio`
- Prompt project: `D:\AI_Studio\outputs\video-prompts\projects\VIDEO-20260907-074621-lia-dynamic-motion-trio`

## Run log

| Episode | Run | Result | Notes |
| --- | --- | --- | --- |
| 01 | `run-20260907-074642-c31f10a2` | needs_review (~129 min) | dual refs cafe+beach |
| 02 | `run-20260907-095602-0152a6a7` | needs_review (~120 min) | beach ref only |
| 03 | `run-20260907-115635-4dd42756` | needs_review (~120 min) | cafe ref only |


Expect ~1.5–2+ hours per shot on RTX 4070 Laptop at current denoise speed.
