# Scoped Task — Keep the operator's wording and still get the craft

Active editor: Claude Code (assigned by the user, 2026-09-19: "C랑 B랑 해줘")
Status: IN PROGRESS
Repos: `XAI-studio` (scene compiler) and `personal-prompt-studio` (Studio API and UI)

## Why

The Studio's 제작 tab makes the operator choose between two things they want at once.
`exact` sends their sentence untouched but skips Character DNA entirely, so the render is
not that character. `creative_expansion` applies DNA and adds craft, but nothing protects
the operator's wording: `build_scene_spec()` only fills `coverage`, `wardrobe` and
`hair_state`, plus a six-phrase Korean hair lookup, so a free-text request leaves the Scene
Spec nearly empty and every field is open to reinterpretation.

The mechanism to combine them already exists. `local_scene_delta()` overwrites any field
present in the Scene Spec after the model answers, so a Scene Spec field is provably
LLM-proof. `SCENE_FIELDS` has fourteen of them; the app sends three and never sends
`scene_spec` at all.

## Delivering

**C — `craft_expansion` strategy.** The operator's sentence stays verbatim as the scene and
Character DNA applies, exactly as `strict_translation` does; the local model contributes
camera, lens, lighting and styling only. Meaning fields (pose, expression, outfit, location,
action) are never asked for and never accepted.

**B — interpretation preview with per-field locks.** A draft endpoint returns the compiled
fields before anything renders. The operator edits or locks any field; locked fields are sent
as `scene_spec` on submit, which the existing overwrite makes binding.

## Constraints / Must Preserve

- Existing strategies keep their exact behaviour and their compiled output byte-for-byte.
- Scene Spec stays authoritative over any model output; never the reverse.
- No new prompt text is invented for fields the operator did not ask about beyond craft.
- `prompt-trace.json` keeps recording every stage, including which mode ran and whether the
  local LLM was used.
- No GPU work is started by a draft.

## Must NOT Do

- Do not touch `importer.py`, the legacy video reader, or any Gallery write path.
- Do not change what `strict_translation`, `creative_expansion` or `exact` produce.
- Do not infer Scene Spec fields from free text by guessing; only the operator's explicit
  locks and the existing immutable constraints populate it.

## Contract impact

- Producer: `tools/character_scene.py` (`--strategy`, `--scene-spec-json`) and
  `POST /api/characters/{id}/generation-jobs` (`prompt_strategy`, `scene_spec`).
- Consumers: Studio backend `GenerationRequest`/`NightBatchRequest` (`schemas.py`),
  `tools/hermes_night_batch.py`, `tools/web_generation_worker.py`, the Studio frontend
  `PromptStrategy` union, and any recorded session whose `prompt_strategy` is read back.
- Compatibility: `craft_expansion` is a new value, additive. Old sessions keep their recorded
  strategy and replay unchanged. `validate_scene_spec()` must accept the new mode or a draft
  of it fails validation - that is the one place an old reader would reject new data.
- Rollback: revert; no persisted rows change and no migration is involved.
- Deterministic verification: the compiled `craft_expansion` prompt must start with exactly
  the `strict_translation` prompt for the same input, which is what makes "craft cannot change
  meaning" a fact rather than a claim.

## Plan

1. C: `craft_expansion` in the compiler, with tests, then the Studio schema and the UI option.
2. B: a draft endpoint that compiles without rendering, then the lock panel that sends
   `scene_spec`.

## Progress

- Diagnosed against the running code: the overwrite loop, the three-field Scene Spec, and
  `exact` dropping both DNA and the identity reference.

## Next

Implement C in `tools/character_scene.py`.
