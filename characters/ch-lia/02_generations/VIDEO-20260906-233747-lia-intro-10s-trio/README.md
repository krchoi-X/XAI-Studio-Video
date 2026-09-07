# Lia intro 10s trio (MiniMax H3 Ref2VA)

Original request: make about three ~10-second Lia introduction videos with WanGP, expressing her from Stable DNA.

## Inputs

- Character DNA: `D:\codex\XAI-studio\characters\ch-lia\character.json` (id `ch-lia`, version 2, stable_dna_sha256 `bd4d3767ef3ee0094e3de67cf2f6b7be30f17351029bf2847ef7580f77c63061`)
- Recognition anchors used in prompts: slim slightly elongated oval face, soft dark-brown eyes, translucent pale natural skin with fine pores, soft rose-beige closed-mouth lips, long near-black lived-in bangs, exactly three thin red-and-blue knotted bracelets on the right wrist, faint quiet closed-mouth smile
- Start / reference image (runtime only, not approved canonical): `D:\AI_Studio\library\characters\ch-lia\imports\inbox\GPT\ChatGPT Image 2026??9??4???ㅽ썑 10_31_54.png`
  - sha256: `e2df345058cd5d29644f804b39612919ad773debe9388e6bb6cfaa5d64ad0502`
  - bytes: 2195395
- Settings basis: copy the successful morning-coffee / ice-cream H3 Ref2VA pattern ??`minimax_h3_ref2va_pruned`, `video_prompt_type: KI`, `resolution: 576x768`, `video_length: 243` (17*14+5 @24fps = 10.125 s), `num_inference_steps: 20`, `guidance_scale: 1.0`, `flow_shift: 12.0`
- Packaging: WanGP prompt mode `FG` (All the Lines are Part of the Same Prompt), expected queue items 1, Prompt Enhancer off
- Durable prompt project: `D:\AI_Studio\outputs\video-prompts\projects\VIDEO-20260906-233747-lia-intro-10s-trio`

## Shots

| File | Episode | Dialogue |
| --- | --- | --- |
| intro-01-hi-im-lia.txt | Direct soft self-intro | "Hi. I'm Lia." |
| intro-02-quiet-presence.txt | Near-still identity presence | (none) |
| intro-03-this-is-home.txt | Seaside-home lifestyle intro | "This is home." |

## Paths

- Session: `D:\codex\XAI-studio\characters\ch-lia\02_generations\VIDEO-20260906-233747-lia-intro-10s-trio`
- Runs: `D:\codex\XAI-studio\characters\ch-lia\02_generations\VIDEO-20260906-233747-lia-intro-10s-trio\runs`
- Video outputs: `D:\AI_Studio\library\characters\ch-lia\videos\VIDEO-20260906-233747-lia-intro-10s-trio`
- Prompt project: `D:\AI_Studio\outputs\video-prompts\projects\VIDEO-20260906-233747-lia-intro-10s-trio`
- Handoff: `D:\codex\XAI-studio\characters\ch-lia\02_generations\VIDEO-20260906-233747-lia-intro-10s-trio\handoff.json` and `D:\AI_Studio\outputs\video-prompts\projects\VIDEO-20260906-233747-lia-intro-10s-trio\handoff.json`
- Sequence status: `D:\codex\XAI-studio\characters\ch-lia\02_generations\VIDEO-20260906-233747-lia-intro-10s-trio\sequence-status.json`
- Sequence log: `D:\codex\XAI-studio\characters\ch-lia\02_generations\VIDEO-20260906-233747-lia-intro-10s-trio\sequence-log.txt`

## Run log

| Episode | Run | Result | Notes |
| --- | --- | --- | --- |
| 01 intro-01-hi-im-lia | run-20260906-233805-e06397d6 | needs_review, 10.125 s, 608x736 H.264 + AAC, ~122 min render | Artifact: `D:\AI_Studio\library\characters\ch-lia\videos\VIDEO-20260906-233747-lia-intro-10s-trio\run-20260906-233805-e06397d6.mp4`. Lineage updated. `prompt_exact_match` false (WanGP embeds its own prompt copy). |
| 02 intro-02-quiet-presence | run-20260907-014509-869cf294 | needs_review, 10.125 s, 608x736 H.264 + AAC, ~122 min render | Artifact: `D:\AI_Studio\library\characters\ch-lia\videos\VIDEO-20260906-233747-lia-intro-10s-trio\run-20260907-014509-869cf294.mp4`. Lineage updated. `prompt_exact_match` false. |
| 03 intro-03-this-is-home | run-20260907-035336-51283fc4 | needs_review, 10.125 s, 608x736 H.264 + AAC, ~123 min render | Artifact: `D:\AI_Studio\library\characters\ch-lia\videos\VIDEO-20260906-233747-lia-intro-10s-trio\run-20260907-035336-51283fc4.mp4`. Lineage updated. `prompt_exact_match` false. |

One GPU job at a time via `tools/local_wangp.py`. Observation: `python -m control_tower --check`.
