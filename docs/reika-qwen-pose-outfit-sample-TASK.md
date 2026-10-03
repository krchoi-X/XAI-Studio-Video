# Reika Qwen pose/outfit sample — 2026-09-30

- Status: COMPLETE — one unreviewed candidate generated and synced
- Active editor: Codex
- Requester: user
- Executor: Codex through local Qwen Image 2.1 / WanGP

## Goal

Generate exactly one review candidate that keeps Mizuki Reika's canonical identity and the user-selected face master while applying only the pose, outfit, environment, and lighting intent from the attached structured prompt.

## Inputs

- Character: `ch-mizuki-reika`
- Canonical record: `D:/codex/XAI-Studio-Private/characters/ch-mizuki-reika/character.json`
- User-selected identity master: `D:/AI_Studio/library/characters/ch-mizuki-reika/generations/GPT-20260906-reika-face-09-editorial/outputs/gpt/face-09-editorial-1.png`
- Expected master SHA-256: `ba3411fb8db4ac28aa5ce2807a1ac56e32fb9e47da4c357d4ac13734010a33b7`
- Gallery asset: `ast_25f17f445b5eafadf15e4645`
- Structured prompt source: `C:/Users/krcho/.codex/attachments/84435df1-123b-475f-bd70-9b8c9404e111/붙여넣은 텍스트.txt`
- User authorization: `실행해봐`

## Constraints / Must Preserve

- Use canonical Reika DNA and the exact hash-verified master as identity authority.
- Extract only Pose Block, Outfit Block, Environment & Props, and Lighting & Optical Style as scene changes.
- One image, one person, portrait orientation, fixed seed, Qwen Image 2.1 reference mode.
- Record real requester/executor/model and preserve the result as an unreviewed candidate.

## Must NOT Do

- Do not treat pasted Character Sheet, Identity Rule, Photo DNA, mood, or reuse notes as canonical identity edits.
- Do not silently change DNA, promote the result, mark it kept/favorite, replace the master, or generate a batch.
- Do not automatically retry a weak or failed result.

## Plan

1. Resolve canonical record and verify master path, size, and SHA-256.
2. Verify WanGP and GPU readiness.
3. Compile a bounded scene request from the four permitted prompt blocks.
4. Submit one `qwen21` reference-bound generation with deterministic seed `20260930`.
5. Inspect the output and record identity/pose/outfit observations without promoting it.

## Progress

- Governance initialization succeeded.
- WanGP doctor passed; RTX 4070 Laptop GPU reports 0 MiB used and 0% utilization before submission.
- Control Tower check could not open its read-only SQLite state database; this does not indicate a WanGP engine failure and is retained as a preflight limitation.
- Canonical record and exact master path were resolved. File size `1,990,236` bytes and SHA-256 `ba3411fb8db4ac28aa5ce2807a1ac56e32fb9e47da4c357d4ac13734010a33b7` matched the recorded identity binding.
- Prepared session `SCENE-20260930-214102-mizuki-reika-one-adult-woman-in-a-s20260930`. Prompt Trace passed constraint validation; Qwen settings were 608x832, 40 steps, CFG 4, seed `20260930`, `video_prompt_type: I`, one hash-bound identity reference, and `allow_text_fallback: false`.
- Completed run `run-20260930-214120-5f059ec9` at 2026-09-30 21:45:50 JST. Run state is `needs_review`; requester is `codex`, executor is `local-wangp-worker`.
- Output: `outputs/qwen21/run-20260930-214120-5f059ec9.jpg`, 160,688 bytes, SHA-256 `10c73379ba2fda206968b4d4122fc1b9a8b0ecd2033c67e957cf765cf16736c0`.
- Studio sync imported one restricted candidate: asset `ast_e37ab25f69135f702ec5c9a6`, decision `null`, favorite `false`, 608x832, model `qwen_image_21_uncensored_q4_k_m`.
- Visual review: cream camisole, light denim shorts, kneeling pose, forearms on carved low table, bright curtained interior, plants, and soft daylight were applied. The result simplified the requested overlap of legs/feet, and the chin/arms relationship is looser than specified. Identity appears recognizably Reika-like but remains a review judgment.
- Identity measurement: SFace `0.7356`, ArcFace `0.7238`, nominal verdict `drift`; however the detected face was only about 98x145 px, below the documented ~150 px reliability floor, so the scores are retained as a warning and not treated as a valid identity rejection.
- No retry, favorite, keep decision, master replacement, DNA edit, or promotion was performed.

## Next

- Human review in Studio. If identity is rejected, test one variable at a time rather than rerunning blindly; the first candidate is a closer crop or larger face while retaining the same seed, master, and scene constraints.

## Blockers / uncertainties

- Reika is currently marked `candidate` in the local runtime snapshot. This run uses the private canonical record and the explicitly selected master but does not change approval status.
- A frontal portrait master may preserve facial identity less strongly in the requested side-kneeling full-body composition; the single result must be reviewed rather than assumed valid.
- `batch.yaml` names `scene_spec.json`, but that standalone file was absent after preparation; the validated structured Scene Spec is preserved in `prompt-trace.json`. This did not block the render, but the producer's standalone-file contract should be checked separately.
