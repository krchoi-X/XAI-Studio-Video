# Noa First Live — production task

- Date: 2026-09-16
- Active editor: Codex
- Status: ACTIVE — Library/Gallery correction complete; awaiting morning-vlog selection

## Goal

Produce the approved single-character storyboard `ノアちゃん、初配信！` as a continuity-controlled Noa video. After this video is reviewed and completed, prepare three distinct storyboard candidates for a separate morning vlog in which Noa wakes in pajamas, waters and prunes the front-yard flower garden, notices she is late, and rushes to prepare for work. Produce the selected morning-vlog candidate only after the user's choice.

## Constraints / Must Preserve

- Keep one Noa, one fixed streaming room, one outfit and stable lighting throughout the first video.
- Treat `D:/AI_Studio/library/characters/ch-shindo-noa/imports/derived/noa-21-portrait.jpg` as the current default identity candidate, not a human-approved identity set.
- Use the approved storyboard image only for blocking, wardrobe and tone; do not let its illustrated face replace Noa's identity reference.
- Use short shots and explicit reference roles. Add Japanese titles/captions in post rather than asking the video model to render text.
- Preserve exact prompts, settings, references, hashes and run lineage in the governed project/session records.
- Hard stop for user review after representative sample generation. No silent final-quality batch.
- Keep the morning-vlog work sequential: three storyboard candidates only after the first-live video is completed; video generation only after the user selects one.

## Must NOT Do

- Do not edit canonical character DNA or mark any reference approved.
- Do not use the full illustrated storyboard as the sole identity reference.
- Do not generate both requested videos in one unattended batch.
- Do not overwrite, delete or reorganize earlier Hermes, Grok or WanGP sessions.
- Do not publish or push.

## Director route

- Primary: `placed_camera_vlog`
- Specialists: `placed_camera_opening`, `purposeful_action`, `continuity_handoff`
- Continuity anchors: face, ivory cardigan and black ribbon, charcoal skirt/tights, fixed camera axis, clean room background and warm-soft light.

## Plan

1. Create and visually review two photorealistic production masters: upper-body livestream master and matching wide dance-prep master.
2. Write the shot plan, prompts and reference-role manifest in a standalone governed project folder.
3. Render one representative low-cost motion sample and stop for user review.
4. Apply feedback, complete the remaining short shots, edit transitions/captions, and present the first-live video.
5. Only then draft and render three morning-vlog storyboard candidates for user selection.
6. Produce the selected morning-vlog video through the same sample-review gate.

## Contract impact

This task creates production artifacts only. It consumes the existing shared Noa record, character-reference resolver, WanGP recorder/submission contract and Gallery/import contract. It does not change their schemas or writers.

The completed first-live video and the three morning-storyboard images currently exist only in standalone project folders, so the Gallery has no character session to discover. Register them through `external_media_import` as two new `ch-shindo-noa` sessions. The standalone projects remain the producing sources; the importer copies bytes, records exact per-item provenance and publishes `batch.yaml` last. Consumers are the Studio sync endpoint and Gallery. Do not write the Gallery database directly, rename/move source projects, alter existing Noa sessions, or infer review approval. Rollback is limited to the newly created import sessions before review; source projects and their run records remain intact. Deterministic checks are dry-run validation, source/destination SHA-256 equality, manifest presence, sync response and Gallery/API discovery.

## Progress

- User approved the eight-beat first-live storyboard and requested production.
- Storyboard source and current Noa default portrait were located.
- Production approach fixed: separate identity and blocking references, two master stills, short clips, post-added Japanese text, representative sample review before batch completion.
- Created the photorealistic upper-body and matching wide masters and preserved them with SHA-256 reference records in `D:/AI_Studio/outputs/video-prompts/projects/noa-first-live-20260916/`.
- Rendered representative Shot D through local WanGP as run `run-20260916-234044-32c15a4f`; output is 4.46 s, 512x896, 24 fps and is awaiting user review.
- Frame review: identity, hair, outfit, background and both index-finger contacts are stable. Noted deviations: mouth opens despite the closed-mouth instruction and the ending smile is less restrained than intended.
- Recorder correctly retained the exact prompt/settings/input paths and artifact hash. WanGP's embedded prompt was reformatted, so its embedded prompt hash did not exactly match the source bytes; the run remains reviewable rather than approved.
- User accepted the representative sample and authorized continuation.
- Rendered and visually reviewed Shots A, BC, E and F. All four reached `needs_review` with preserved prompts, settings, references, events and artifact hashes; face/outfit/room continuity and required gestures were acceptable.
- Assembled Shots A, BC, accepted D, E, a 0.5 s editorial transition, and F into `noa-first-live-captioned-v1.mp4` with Japanese burned-in captions. Generated clip audio was intentionally omitted because separate clips do not guarantee a stable voice.
- Final technical result: 22.791667 s, 512x896, 24 fps, H.264, SHA-256 `eb030f24bf91b9001a5d04993900dd9d7fe294880f1ace12c7d59c85def5686b`.
- Final contact sheet and transition-frame review found correct shot order, readable uncropped captions, stable character/wardrobe/background, and a clean full-body reveal.
- Closed the first-live session as `completed` with a final manifest. The captioned final is ready for user review.
- Created and schema-validated the morning-vlog request and three storyboard candidates under `D:/AI_Studio/outputs/video-prompts/projects/noa-morning-garden-vlog-20260917/`.
- Rendered three six-panel GPT Image boards with one shared Noa identity candidate, pale-blue pajamas and the same small-home/front-garden premise: A cinematic slow-to-fast, B placed-camera vlog, C one-flower cause-and-effect.
- Morning-vlog status is `needs_user_choice`; no motion sample has been submitted.
- User reported that neither deliverable was discoverable in Gallery and clarified that character-bound finals belong under Noa's Library hierarchy.
- Imported the final first-live video into shared Noa session `IMPORT-20260917-noa-first-live` and the three morning storyboard candidates into `IMPORT-20260917-noa-morning-storyboards`; source standalone projects remain unchanged.
- Preserved all five WanGP shot prompts in the first-live import prompt/provenance and separate exact GPT Image prompts for storyboard candidates A/B/C.
- Studio sync succeeded. Gallery API now returns all four assets under `ch-shindo-noa`: video `ast_8534345aaea6075fa7b852df` and storyboards `ast_93cb7d80503614bb6ce74dae`, `ast_0b3adf3f80a6d6efef664a77`, `ast_91efe472a1f07aa4dfd9ac76`.

## Next

Present the corrected Library/Gallery locations and wait for the user's explicit morning-vlog choice or combination request before compiling a motion sample.

## Verification

- Visual identity/outfit/background comparison for both master stills.
- Deterministic validation of project manifests and exact file existence/hashes.
- WanGP run record and output checks before any edit assembly.
- External importer dry-runs: one planned video and three planned storyboard images, no errors or warnings.
- Apply: 4 copied, 0 failed; both `batch.yaml` records published.
- Source/destination SHA-256 equality checked for all four files.
- Studio sync returned 12 characters / 123 sessions and the Noa assets endpoint returned the two new sessions with three image assets plus one playable H.264 video.
