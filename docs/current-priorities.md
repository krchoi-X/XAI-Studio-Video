# Current Priorities — XAI-Studio-Video

Updated: 2026-08-25

## P0 — Codex-controlled Hermes Character Manager

- Source: GitHub issue #2
- Status: `IN PROGRESS` — schema, deterministic control CLI, Hermes skill, and Jung Hae-won/Harim migrations implemented
- Next action: connect the tablet app to `characters/index.json`, expose candidate review, and promote human-approved references without making SQLite the identity source of truth

The control plane takes precedence over additional bulk character generation. Hermes + the configured local Ollama model drafts repetitive character records; repository validation, Stable DNA hashing, promotion rules, and indexing remain deterministic and Codex-controlled. See `docs/character-manager.md`.

This file is the project-local handoff from the broader `krchoi-X/personal-ai-knowledge` research/backlog. It exists because the Codex project attached to `XAI-Studio-Video` may not have access to that private knowledge repository or the ChatGPT conversation that produced the priorities.

## P0 — Analyze toyxyz MiniMax-H3-prompter before building more H3 prompt/timeline UI

- Source: https://github.com/toyxyz/ComfyUI_toyxyz_test_nodes
- Central reference: `personal-ai-knowledge/backlog/2026-08.md` → `2026-08-25 — toyxyz MiniMax-H3-prompter 선행 구현 분석`
- Priority: `P0`
- Status: `COMPLETE` — static decision recorded in `docs/toyxyz-h3-prompter-review.md`; no installation or integration performed

### Context

XAI-Studio-Video has been evolving toward a prompt-first H3 workflow with storyboard/shot structure, timeline-aware prompting, image/video/audio references, VIDEO-DNA-style constraints, and model/backend adapters. Before this discovery, a reasonable path was to implement more of that H3 timeline/prompter layer directly in this repository.

On 2026-08-25, `toyxyz/ComfyUI_toyxyz_test_nodes` added a `Minimax-H3-prompter` that already covers a large part of the same problem space:

- editable shot timeline
- `@alias` insertion for image/video/audio references
- Auto/T2VA/I2VA/FL2VA/L2VA/REF2VA routing
- first/last/exact-frame/subject image roles
- video roles such as motion, camera, cuts/rhythm, continuation/editing
- audio roles such as voice, dialogue/lyrics, ambience, music/rhythm
- H3 `17k+5` frame-grid alignment
- Qwen3.8-27B + Vision prompt expansion for REF2VA and all modes
- lighter H3 Prompt Rewriter 8B path for non-REF2VA modes
- prompt constraints for action progression, hand/object continuity, locomotion, style/reference-medium locking, and action visibility

This overlaps enough with planned XAI-Studio-Video work that continuing to design a new H3 prompter first creates a real duplicate-development risk.

### Priority rationale

This is P0 **not because the external node should be installed or adopted immediately**, but because its architecture must be understood before more local H3 prompt/timeline code is written.

It outranks new H3 UI/prompter implementation because a short reverse-engineering pass can eliminate unnecessary work and reveal reusable schemas or compiler rules.

### Depends on

`None` for static analysis.

Runtime tests depend on an appropriate local/cloud environment and model files, but those are not required for the first deliverable.

### Blocks

Until this analysis is complete, defer decisions on:

- creating a new H3 shot-timeline UI
- finalizing XAI-Studio-Video reference-role schema
- writing a new H3 prompt compiler from scratch
- committing to an internal H3 mode-routing design

### Next action

Codex should perform a static architecture review first. Do not start with installation.

Inspect at minimum:

1. `nodes/minimax_h3_prompter.py`
2. related JS/web frontend code used by the prompter
3. prompt/system-prompt JSON or configuration files
4. `test_minimax_h3_prompter.py`

Compare toyxyz against current XAI-Studio-Video using these axes:

- shot schema
- timeline model
- reference asset schema (`asset + role + strength + timeline placement`)
- H3 mode routing
- prompt compiler / constraint layers
- generated outputs and downstream interface
- separation between frontend state, prompt compiler, and ComfyUI node execution

Produce one short decision note with three options:

- `reuse`
- `fork/adapt`
- `borrow-pattern-only`

For each option, estimate maintenance burden, coupling to toyxyz, amount of duplicate code avoided, and compatibility with XAI-Studio-Video's storyboard/VIDEO-DNA direction.

Default evaluation bias: **reuse-first, but modular-backend-first**. A one-node UI does not automatically imply that XAI-Studio-Video should become a monolithic custom node internally.

### Not now

Do **not**:

- vendor the entire `ComfyUI_toyxyz_test_nodes` repo into XAI-Studio-Video
- install all CaptureCam/ComfyCouple/legacy utilities just to study the H3 prompter
- replace existing storyboard rules immediately
- build a new competing H3 timeline/prompter UI before the comparison note exists
- treat Qwen3.8-27B or LightX2V model choices as permanently fixed architecture

## After P0

Do not automatically start another research item just because the P0 note is finished. Use the P0 result to decide the next implementation step.

Relevant broader references already tracked in the central knowledge repo include:

- MiniMax H3 Motion Context — long clip chaining / continuity
- MiniMax H3 Director — multi-mode/segment execution and rerender patterns
- MMH3 Ultimate Upscale — low-VRAM latent finishing
- H3 × Z-Image checkpoint — quality/detail A/B candidate
- Hanimix PiD_AIO — useful as a general AIO/workflow-abstraction reference, but it is **not currently ahead of the H3 prompter analysis for this video repo**

These are context, not an instruction to implement them all.

## Handoff maintenance rule

When ChatGPT/personal-ai-knowledge changes the priority of a video/H3/XAI-Studio-Video item, this file should be updated as the local execution snapshot. Detailed research history remains in `personal-ai-knowledge`; this file should stay concise enough for Codex to determine the next action without reading unrelated AI research.
