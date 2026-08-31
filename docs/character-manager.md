# Hermes Character Manager

This is the local control plane for GitHub issue #2. Codex owns the schema, validator, and integration contract. Hermes uses the configured local Ollama model for repetitive drafting and file creation.

## Source of truth

```text
characters/
  index.json
  ch-<slug>/
    character.json
    00_character-core/character_core.md
    01_prompts/base_appearance.txt
    02_generations/
    03_selected/
    04_training/
    05_content-tests/
```

`character.json` is canonical. Markdown is generated for humans. The web app consumes the index and records but does not own identity.

## Operator workflow

```powershell
python tools/character_manager.py doctor
python tools/character_manager.py list
python tools/character_manager.py draft --request "새 캐릭터 하림 만들어줘"
python tools/character_manager.py promote characters/.drafts/<run>/character.json
python tools/character_manager.py validate
```

Create and render a different pose/outfit without changing identity:

```powershell
python tools/character_scene.py produce --character ch-harim --request "검은 재킷을 입고 의자에 비스듬히 앉아 카메라를 보는 상반신 사진" --count 4
```

Hermes uses the local LLM to write `scene-delta.json` and compile `prompt.txt`. WanGP then runs Z-Image and Krea2 sequentially and stores outputs, settings, prompt lineage, and recorder runs inside the character's `02_generations` folder.

Large generated media is stored under `D:\AI_Studio\library\characters`. The Git repository keeps Character DNA, requests, prompts, Scene Deltas, settings, run journals, `asset-manifest.json`, hashes, and the external `asset_root`. The tablet app joins these records with the Library at sync time.

New characters become `candidate`, not `approved`. Existing Stable DNA changes fail unless the operator supplies both `--allow-stable-change` and a meaningful `--reason`. Human review in the tablet app remains the approval boundary.

## Tablet review to DNA proposal

The character page exposes **지금까지의 코멘트로 DNA 수정안 만들기** only for normalized characters with canonical `character.json` data. Pressing it creates a frozen evidence job under the app workspace:

```text
workspace/dna-proposals/<proposal-id>/
  snapshot.json
  status.json
  proposal.json
  proposal.md
  worker.stdout.log
  worker.stderr.log
```

The snapshot includes saved selections/comments and the character's favorited or reviewed assets. Hermes/MeroMero separates proposed Stable DNA changes from Scene Delta preferences, records conflicts and questions, and cites evidence IDs. A completed job is marked `needs_review` and is shown on the tablet.

This workflow never edits `characters/<id>/character.json`. Applying an accepted proposal is a separate, human-approved operation and must use the Stable DNA guard, reason, version update, validation, and hash reporting.

## Tablet image generation queue

The character page accepts a natural-language scene request, one or both local engines (`z-image`, `krea2`), and a modest per-engine count. The app creates a durable job under `workspace/generation-jobs/<job-id>/` and immediately returns control to the browser. Only one local GPU job runs at a time.

`tools/web_generation_worker.py` calls the Stable-DNA-safe `character_scene.py produce` pipeline, preserves the exact request and runtime lineage, and asks the app to sync completed assets. The tablet polls durable status files, survives browser reconnects, and reveals finished assets through the separate restricted-media view. Failed jobs retain their error and render log for diagnosis.

## Hermes night batches

`tools/hermes_night_batch.py` is the durable multi-item queue above the single-scene pipeline. Hermes converts an explicit night-work request into a reviewed JSON plan, then enqueues it. The queue permits at most 48 scene items and 240 resulting images, executes WanGP jobs sequentially, continues after item-level failures, syncs every successful result to the tablet app, and refuses a second active batch. Queue state lives outside the repository at `D:\AI_Studio\workspace\hermes-night-batches`; prompts and generation provenance still live in each canonical character session.

Discovery batches use labelled `variation_axes` so hair, scene, lighting, wardrobe, and expression can be compared instead of becoming an untraceable pile of prompts. The preferred pattern is breadth first (one image per engine per balanced combination), human review second, and seed expansion only for selected combinations.

Do not treat the free-form text box as permission to change canonical Character DNA. It controls Scene Delta only. DNA revision remains the separate proposal and human-approval workflow above.

### Prompt precedence and trace

Web generation preserves this order: explicit user constraints, immutable Scene Spec fields, Stable Character DNA, bounded identity variables, scene requirements, style enrichment, then optional detail. The default `strict_translation` strategy deterministically combines the raw scene with identity and does not call a local LLM. `creative_expansion` allows MeroMero to expand the scene under immutable constraints. Legacy names `identity-merge` and `enriched` remain accepted as aliases. `exact` sends the raw prompt to the image engine without DNA or LLM rewriting.

Every new scene session writes `prompt-trace.json` containing the raw input, DNA-merged prompt, optional enriched prompt, final image-engine prompt, immutable fields, and whether Hermes or a local LLM was used. The tablet production-detail sheet exposes the same trace.

Scene Spec fields replace conflicting Stable DNA fields during runtime compilation; they are not merely placed earlier in the prose. For example, a scene-level `hair` value suppresses the canonical `stable_dna.hair` sentence for that render while leaving the character record unchanged. `prompt-trace.json` records both `scene_spec` and `suppressed_stable_dna_fields`. Natural-language hairstyle requests receive a deterministic strict normalization, and callers can provide any explicit field with `--scene-spec-json`.

Never add implicit wardrobe or coverage normalization. If `coverage`, `wardrobe`, or `hair_state` is locked, enrichment cannot change it. Local outputs remain restricted regardless of prompt strategy.

Every prepared session now persists `scene_spec.json` conforming to `schemas/scene-spec-v1.schema.json`. Generation stops before the renderer when the character/version does not match, an unknown field is supplied, a bounded Hair State is undefined, or structured coverage and wardrobe conflict. Prompt Trace records the structured spec, validation result, optional expansion, Hermes handoff (when present), final engine prompt, and DNA fields suppressed for that render.

## Local model

Hermes is configured at `%LOCALAPPDATA%\hermes\config.yaml` to use Ollama at `http://127.0.0.1:11434/v1`, currently with `meromero26b-a4b-hermes:latest`. The manager calls Ollama only for draft JSON; validation, hashing, Markdown rendering, promotion, and indexing are deterministic local code.

## App mapping

- `characters/index.json` → character navigation/discovery
- `character.json` → identity and version display
- `approved_references` → selected/master image links
- generation metadata → model, seed, prompt lineage, review notes
- Stable DNA hash → drift warning and generation lineage

The current app can add a repository adapter without changing its SQLite review-event model. Generic character discovery should replace hard-coded character buttons.

## Limits

- Local LLM output still requires a candidate review; it is not trusted as a source of biological or biographical truth.
- Reference-image approval remains human-controlled.
- Version 1 validates required structure deterministically but does not measure semantic similarity between two different descriptions.
