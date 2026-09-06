# Task snapshot preserved before XAI Control Tower v0.1 implementation

Preserved: 2026-09-06 by Claude Code. This is the verbatim `TASK.md` that was active when Control Tower work moved into the active task slot. Nothing below has been edited; use it to recover the earlier publish/audit task and the completed generation tasks.

---

# Current Task

Status: IN PROGRESS — audit, commit, and push all suitable unpushed XAI-Studio-Video work so it is remotely accessible.

## Active Goal

Publish the completed Aoi vlog plan together with other pending repository records and the two commits already ahead of `origin/main`.

## Active Constraints / Must Preserve

- Review all untracked generation records before staging.
- Do not add large generated image/video binaries, credentials, locks, caches, or machine-private runtime files.
- Preserve existing user and agent work; include suitable prompt, manifest, settings, review-frame, and provenance records as requested.
- Verify the commit and push against the configured `origin`.

## Active Must NOT Do

- Do not rewrite history or force-push.
- Do not invent a remote for a separate repository that has none configured.
- Do not push private character material to an unrelated public repository.

## Active Plan / Progress

- [x] Inspected three related workspace paths.
- [x] Confirmed `D:\\codex\\XAI-studio` is on `main`, two commits ahead of `origin/main`, with pending generation records and the Aoi vlog plan.
- [x] Confirmed Personal Prompt Studio has local curation edits but no Git remote configured, so it cannot be pushed safely without a user-supplied destination.
- [ ] Audit pending XAI-Studio-Video files and sizes for binaries/secrets.
- [ ] Stage suitable work, review staged diff, commit, and push `main` normally.
- [ ] Verify local HEAD equals `origin/main` after push.

## Active Next

Audit pending content and stage only repository-safe records.

## Active Blockers / Uncertainties

- Personal Prompt Studio has no configured remote; its three curation changes will remain local unless a remote is supplied later.

## Active Contract Impact

None. Publishing existing additive records and documentation; no contract change.

---

## Previous Task Snapshot — Aoi vlog concept planning

Status: COMPLETE — five Aoi vlog concepts drafted and persisted; no image or video generation performed.

## Active Goal

Create and persist five distinct vlog concepts built from Aoi's canonical character DNA and established scene defaults. Each concept should establish a different facet of her confident young-adult nomadic-designer life and remain executable as a later short-form vlog.

## Active Constraints / Must Preserve

- Keep canonical Aoi Stable DNA unchanged.
- Treat career, wardrobe, location, dialogue, and emotional beats as concept/scene material, not Stable DNA additions.
- Preserve Aoi's emotionally open range, socially confident gaze, short dark bob, signature earring, professional competence, and believable young-adult presence.
- Include variety across work, travel, appearance confidence, setbacks/crying, and recovery.
- Plan only; do not generate media or enqueue renders.

## Active Must NOT Do

- Do not edit `characters/ch-mizuno-aoi/character.json`.
- Do not assume a fixed voice, relationship, home, or biography that is not canonical.
- Do not turn every episode into fashion posing or professional success; preserve everyday friction and emotional contrast.

## Active Plan / Progress

- [x] Read Aoi Character Core and the existing Lia vlog brief for planning granularity.
- [x] Wrote five distinct concepts with hook, beat sequence, emotional turn, visual identity, and production notes in `docs/aoi-vlog-concepts-01.md`.
- [x] Verified the document contains exactly five numbered concepts.
- [x] Confirmed no renderer submission or media generation was performed.

## Active Next

User review; select one concept for a later shot-level production brief if desired.

## Active Blockers / Uncertainties

- None. Dialogue language and exact episode duration remain intentionally open for later production.

## Active Contract Impact

None. Documentation-only concept planning; no schema, API, CLI, or persisted generation contract changes.

---

## Previous Task Snapshot — Aoi image review

Status: COMPLETE — regenerated Aoi's ten corrected images as three canonical sessions and synced all 10 assets into the running web review app (2026-09-06).

## Active Goal

Use the canonical character scene pipeline for `ch-mizuno-aoi` to generate 10 still images that preserve her early-twenties identity while emphasizing confident professional presence, open emotional range, and tasteful mini-dress looks with genuinely flat sandals and naturally long-looking legs. Sync the completed session so it is reviewable in the existing web app.

## Active Constraints / Must Preserve

- Preserve canonical Aoi Stable DNA; wardrobe, emotion, pose, lens, and framing are runtime Scene Delta only.
- Aoi must read as an adult age 22–24.
- Flat sandals must have zero heel, wedge, or platform.
- Correct the prior short-leg appearance through natural adult proportions, high-waisted styling, hip/waist-height camera, 70–85 mm portrait perspective, sufficient camera distance, and full head-to-toe framing.
- Include professional confidence, intense sorrowful crying, and relaxed appearance confidence.
- Use `tools/character_scene.py produce --actor codex` and preserve the exact request in Prompt Trace.
- Make the resulting session visible to the web/tablet review flow.

## Active Must NOT Do

- Do not edit `characters/ch-mizuno-aoi/character.json` or approve a reference automatically.
- Do not overwrite prior generated sets.
- Do not use sexualized, voyeuristic, or anatomically exaggerated framing.

## Active Plan / Progress

- [x] Recovered the interrupted task and read repository/character-manager instructions.
- [x] Confirmed prior manually generated images are not the canonical web-app generation path.
- [x] Generated three professional-confidence images in `SCENE-20260906-105340-mizuno-aoi-aoi-the-same-original-fictional`.
- [x] Generated two intense-crying images in `SCENE-20260906-105354-mizuno-aoi-aoi-the-same-original-fictional`.
- [x] Generated five long-leg mini-dress/flat-sandal images in `SCENE-20260906-105409-mizuno-aoi-aoi-the-same-original-fictional`.
- [x] Verified all three `batch.yaml` records completed and 3+2+5 output files exist.
- [x] Synced the repository through `POST /api/sync`; API imported 10 new assets and each session returns the expected asset count.
- [x] Verified the web app is serving HTML at `http://127.0.0.1:8787/`.

## Active Next

User review in the Aoi character workspace. Ignore the earlier composite session `SCENE-20260906-104136-mizuno-aoi-22-70-85mm`; visual QA found wardrobe/identity failures, so the three replacement sessions are the valid review set.

## Active Blockers / Uncertainties

- None. The replacement sessions are complete and indexed.

## Active Contract Impact

None expected. Additive generation session and review index records only; no schema or API changes.

---

## Previous Task Snapshot

Status: AWAITING USER REVIEW — Lia 10-second MiniMax H3 Ref2VA morning-coffee vlog, four episodes rendered (2026-09-06 00:26–02:05 KST).

## Goal

From one user-supplied Lia reference image (window-lit selfie holding a coffee mug, heather blue-gray T-shirt, sea through the window, three red-and-blue bracelets on the right wrist), render four 10-second H3 Ref2VA vlog clips with native audio, one after another, on the local WanGP background runner.

Prompts, settings, run records and review frames live in `characters/ch-lia/02_generations/VIDEO-20260906-lia-morning-coffee-vlog-candidates/` (see its `README.md`, including the Run log table). MP4 outputs are in `D:\AI_Studio\library\characters\ch-lia\videos\VIDEO-20260906-lia-morning-coffee-vlog-candidates\`.

## Constraints / Must Preserve

- Canonical Lia Stable DNA v2 unchanged; the reference image is a runtime reference only (copied to `D:\AI_Studio\library\characters\ch-lia\imports\inbox\GPT\ChatGPT Image 2026년 9월 4일 오후 10_31_54.png`, not approved).
- Same Ref2VA settings as the accepted pilot (`minimax_h3_ref2va_pruned`, 576x768, 20 steps, profile 4, vram-safety 0.8) except `video_length` 243 (17*14+5 = 10.125 s).
- Episodes follow `lia-life-dna-v1.1.md` (Private repo); the cat stays off-screen (sound only) because its appearance is not canon yet.
- Recorder run created before each submission; exact prompt, effective settings, events, logs and MP4 retained per run.

## Must NOT Do

- Do not edit Character DNA or approve the reference.
- Do not stop the user's WanGP Web UI (pid 28264, port 7860); killing processes was denied by the permission policy. All four 243-frame runs completed with it resident, so coexistence is now verified on the RTX 4070 Laptop 8 GB.

## Progress

- [x] Reference image located in Downloads and copied into the Lia inbox.
- [x] Prompts 01–04 and matching `*.settings.json` written.
- [x] Episode 01 `run-20260906-002654-ac69262f`: needs_review, identity held, sip / glance-down / lines present.
- [x] Episode 02 `run-20260906-005142-29e8ca26`: needs_review, identity held, head turn / hair tuck / lowered gaze present.
- [x] Episode 03 `run-20260906-011642-2f5f3a6f`: needs_review, identity held, sip / mug down / hair gather / line present.
- [x] Episode 04 `run-20260906-014111-04975d8a`: needs_review, identity held, mug down / ukulele strum / laugh / line present.
- [x] Each run ~24 min; all 10.125 s H.264 + AAC; review frames in `review-0N/`.

## Findings

- Identity, wardrobe, bracelets, mug and room held in every sampled frame of all four clips; no face drift observed.
- Action chains rendered in prompt order; H3 followed multi-beat 10-second instructions well.
- Recurring deviation: while speaking, the smile is wider and more toothy than the DNA's "faint quiet smile". If refining, add explicit "small closed-mouth smile, no wide grin" wording.
- Episode 04 ukulele reads tenor-sized rather than soprano.
- `prompt_exact_match` is false on every run, as in the pilot (WanGP embeds its own prompt copy); normalized match also false. Known, not a defect of these runs.
- Audio content (speech intelligibility, cat meow, ukulele) has not been listened to; only level presence was checked.

## Next

User decision: accept any of the four as vlog baselines, or refine (smile wording, ukulele size). Then decide whether the reference image should be promoted toward an approved Lia reference. Optionally listen to the audio tracks and record speech quality in the README.

## Blockers / Uncertainties

- Two stale `WanGPSession.get_model_schema` python processes from 2026-09-05 (pids 60100/67780) are still alive and consuming CPU; they could not be stopped under the current permission policy. They did not block generation.

## Contract Impact

None. Additive generation and run artifacts only; no schema, API, CLI, or application contract changed.
