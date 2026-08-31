---
name: character-manager
description: Create, inspect, or update XAI-Studio character records with Stable DNA protection and Scene Delta separation. Use for natural-language requests to make or revise a character; do not use for merely rendering an already-defined prompt.
---

# Character Manager

Use the repository CLI as the authority; do not invent a parallel folder convention.

Run commands from the XAI-Studio-Video Git root containing `HERMES.md` and `tools/character_manager.py` (currently `D:\codex\XAI-studio`). If the current directory differs, change to that root first. Never resolve `tools/` relative to the installed external-skill copy.

## New character

1. Read `characters/index.json` and inspect likely overlaps under `characters/ch-*/character.json`.
2. Run `python tools/character_manager.py draft --request "<user request verbatim>"`. The configured local Ollama model writes a validated draft under `characters/.drafts/`.
3. Inspect the draft for duplicate identity, accidental biography, scene details inside Stable DNA, and adulthood.
4. For a genuinely new character, run `python tools/character_manager.py promote <draft-character.json>`.
5. Report the character ID, changed files, Stable DNA hash, and unresolved fields.

## Existing character

Read the canonical `character.json` before drafting. Pose, expression, outfit, camera, lens, lighting, location, and action are Scene Delta data; do not change Stable DNA for them.

The CLI blocks changed Stable DNA by default. Only use `--allow-stable-change --reason "..."` when the user explicitly approved that identity change. Never silently work around this guard.

## Rules

- `characters/<id>/character.json` and its generated Markdown are the source of truth.
- The web app is a review/control view, not the identity database.
- Keep model-neutral English base prompts in `01_prompts/`; renderer adapters own model-specific syntax.
- Write files instead of only printing proposals.
- Run `python tools/character_manager.py validate` after every promotion.
- Never infer personality, biography, exact age, or relationships from appearance.
- Never mark references approved unless a human review selected them.

Read [references/schema.md](references/schema.md) when adding fields or integrating another tool.

## Review comments to DNA proposal

When the operator requests a DNA revision from tablet comments, use the app's explicit proposal trigger. Freeze the current selections, comments, favorites, and review decisions into `workspace/dna-proposals/<proposal-id>/snapshot.json`; do not read later edits into an already queued job.

The local worker may classify repeated evidence and draft `proposal.json` plus `proposal.md`, but it must not edit canonical `character.json`. Treat pose, outfit, expression, camera, lighting, and one-off preferences as Scene Delta findings. Stable DNA changes require cited evidence IDs and remain `needs_review` until a human explicitly approves a later apply operation.

Do not infer a stable trait from a single unexplained star. Preserve contradictions and uncertain findings as questions instead of forcing consensus.

## Pose / outfit variation and image production

For an existing character, use the scene pipeline instead of editing Character DNA:

```powershell
python tools/character_scene.py produce --character ch-harim --request "긴 코트를 입고 창가에 기대 선 상반신 사진" --count 4 --strategy strict_translation --actor hermes
```

Pass `--model <ollama-model-name>` when the user selects another installed local LLM; otherwise use the configured MeroMero default.

When the request changes a normally stable visual field for one scene, compile it as an authoritative Scene Spec override instead of appending contradictory DNA. Hairstyle requests are detected deterministically; for other explicit overrides use `--scene-spec-json`, for example `--scene-spec-json '{"hair":"a sleek shoulder-length bob; no hair below the shoulders"}'`. For a bounded state use `{"hair_state":"A"}` and require that state to exist in the character's `bounded_identity.hair_states`; never send the literal state ID as the hairstyle. The runtime compiler must omit the replaced `stable_dna.hair` sentence, preserve canonical DNA on disk, and record the override in Prompt Trace.

Use `strict_translation` for identity, reference, wardrobe, coverage, and consistency work. Use `creative_expansion` only when the operator wants non-conflicting scene enrichment. The legacy strategy names remain accepted for old jobs. Every new session must pass Scene Spec validation before WanGP is invoked.

The local LLM writes a Scene Delta and one exact runtime prompt, then local WanGP renders Z-Image and Krea2 sequentially. The command waits until artifacts are durably recorded. Keep the per-engine count modest (default 4, maximum 20) so tablet review remains practical.

Use `prepare` instead of `produce` when the user wants to inspect the prompt before rendering. Never describe a render as complete until `batch.yaml` and the recorder run both say completed and the output files exist.

To submit a session that was already prepared, reuse it instead of regenerating a new Scene Delta:

```powershell
python tools/character_scene.py produce --session-dir "characters/ch-jung-haewon/02_generations/<session-id>"
```

`--session-dir` is mutually sufficient; do not also pass `--character` or `--request`. The command skips completed engine jobs and refuses to duplicate a job already marked running. When executing several prepared sessions, run them sequentially and record each failure without assuming a failed session invalidates the others.

Generated session records live under `characters/<id>/02_generations/<session-id>/`. They include the original request, Scene Delta, Stable DNA version/hash, exact prompt/hash, settings, run records, and an asset manifest. Large image/video outputs live under `D:\AI_Studio\library\characters/<id>/generations/<session-id>/outputs`; `batch.yaml` records the absolute `asset_root`. The tablet app joins the repository records with this Library during sync.

## Face-first discovery

When the operator asks to distinguish Hae-won or Harim's face, do not use the general Scene Delta pipeline. Read `docs/character-face-discovery-workflow.md` and run the dedicated deterministic direction prompt:

```powershell
python tools/face_discovery.py produce --character ch-harim --direction HARIM-B --engines z-image --count 8
python tools/face_discovery.py produce --character ch-jung-haewon --direction HAEWON-C --engines krea2 --count 8
```

Valid directions are `HAEWON-A` through `HAEWON-D` and `HARIM-A` through `HARIM-D`. The tool rejects a direction belonging to the other character. It intentionally omits body DNA and minimizes signature hair so face separation is not confused with styling separation.

Treat seeds as exploration samples, not identity. Keep studio variables locked, generate a modest direction batch, and let the human classify results as overlap rejection, alternate, face candidate, or master face. Do not modify canonical DNA or approved references merely because a batch completed.

## Hermes night-batch trigger

Treat a user message beginning with `야간 배치:` or asking `오늘 밤 ... 만들어줘` as an explicit request to prepare and start a durable Hermes batch. Do not require a magic command beyond that natural-language intent.

Translate the request into a JSON plan with `title`, `source_request`, and `items`. Each item must contain `character_id`, `prompt`, `engines`, `count`, and may contain `prompt_strategy`, `immutable_constraints`, `scene_spec`, and `variation_axes`. Preserve the user's original wording in `source_request`. Default to `strict_translation` and both local engines unless the user specifies otherwise. A batch may generate up to 240 images across at most 48 items.

For character-attractiveness discovery, build a labelled variation matrix. Record axes such as `hair`, `scene`, `lighting`, `wardrobe`, and `expression` in `variation_axes`. Prefer a broad first pass with one image per engine for each combination, then use a later batch to generate several seeds only for combinations the operator liked. Avoid a full Cartesian product when it creates redundant combinations: use a balanced subset that gives every axis value comparable exposure. Good discovery scenes include a beach cafe, reclining on a beach in swimwear, and idol-like cute dance; useful light axes include hard sunlight, controlled studio light, sunset, and morning light. Keep the face and core identity fixed while exploring these presentation axes.

Save the plan to a durable local JSON file and enqueue it with:

```powershell
python tools/hermes_night_batch.py create --plan-file "<absolute-plan.json>"
```

The queue runs items sequentially, continues after an individual failure, syncs each successful session into the tablet app, and records status under `D:\AI_Studio\workspace\hermes-night-batches`. Never launch a second active batch. Report the batch ID, item count, expected generated-image count, variation axes, and status path. Do not claim completion merely because it was queued.
