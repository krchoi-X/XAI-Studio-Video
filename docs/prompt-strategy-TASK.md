# Scoped Task — Keep the operator's wording and still get the craft

Active editor: Claude Code (assigned by the user, 2026-09-19: "C랑 B랑 해줘")
Status: COMPLETE
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

## Progress (continued)

- C landed: `craft_expansion` compiles the strict prompt and appends photography only.
- B1 landed: `interpret()` compiles without reserving a session, exposed as a background
  draft job so reading a compilation is not a wait held open over HTTP.
- Local-model calls now go through one router, `cm.chat_json`, instead of five copies of the
  Ollama endpoint. The gateway key is discovered from the running server's command line,
  because Hermes issues a new one every launch and stores it nowhere.

## Measured, 2026-09-19

Routing through the Hermes gateway works and was verified live. The model behind it does not
fit this machine:

| Model | Shape | Observed |
|---|---|---|
| `Huihui-Qwen3.8-27B-abliterated` via gateway | dense 27B, FFN weights on CPU (`spilled: true`) | 30 output tokens in 36.2s, about 0.8 tok/s; a craft draft hit the 840s timeout |
| `meromero26b-a4b` via Ollama | MoE, roughly 4B active | craft drafts completed at 286s and, on a later run, 70s |

Qwen3.8 has no mid-size MoE: the released 27B is dense, and `Qwen3.8-35B-A3B` has only been
seen in a modelscope/ms-swift commit, unannounced. `Qwen3.6-35B-A3B` is released and is the
nearest A3B-class candidate; whether an abliterated GGUF of it exists is unchecked.

Decision: stay on meromero for now. `STUDIO_HERMES_BASE_URL` is commented out in
`backend/.env`; uncommenting that one line re-enables the gateway, and discovery handles the
key. Nothing else needs changing.

## GPU residency, measured 2026-09-19

The premise this started from was wrong twice, so the corrected version:

- There is no image model resident alongside the language model. What shared the card were
  **two 27B-class language models**: Hermes' llama.cpp worker and Ollama's, because the
  Studio was bypassing Hermes' router and opening its own.
- Both runtimes **already release their weights when idle**. An idle card reads
  **205 MiB of 8188** with the Hermes router still running; its supervisor holds nothing and
  its model workers had exited on their own.
- So permanent residency was never the problem. The problem is the window after a compile:
  the model that wrote the prompt is still warm when the render starts seconds later.

That is what `identity_batch.py` has always guarded and the Studio path never did, and it is
now fixed at `character_scene.submit`.

### Turning Hermes' local runtime off — investigated, not done

The switches exist and were found:

| Switch | Where | Effect |
|---|---|---|
| `local_runtime.enabled` | `hermes/config.yaml:609` | stops the local llama.cpp runtime entirely |
| default model / provider | `hermes model` (interactive only, no flags) | points Hermes somewhere other than llamacpp |
| `--sleep-idle-seconds`, `--no-models-autoload` | llama-server flags | Hermes passes its own args explicitly and there is no env override, so these are out of reach without changing how Hermes launches the server |

Not done, deliberately. `hermes status` shows every cloud API key unset; the only
authenticated providers are copilot (a gh token) and openai-codex. Turning the local runtime
off would send this project's character and production work to GitHub or OpenAI, which is
not a trade for a few gigabytes, and the abliterated local model was clearly chosen against
exactly that. The operator chose option A: leave Hermes alone and free the card at the
moment it matters.

## B2 delivered

The preview shows what a request compiled into before anything renders, each field labelled
in Korean with a lock. A locked field goes back as a Scene Spec entry, which the compiler
restores after the model answers, so it is the value that gets used rather than a request.
Editing a field locks it: changing a value you did not mean to keep makes no sense.

Verified end to end against the running studio. `craft_expansion` returned five fields;
locking `조명` and rewriting it sent `scene_spec {"lighting": "정오의 직사광, 그림자 강하게"}`,
and the next draft returned that value untouched while the model rewrote everything else
around it — styling became high-contrast grading and the negatives became "avoid soft-box
lighting, avoid diffused shadows". That is the behaviour the task set out to get: the
operator's wording kept, the craft still filled in.

## Next

Nothing outstanding in this task. Two things it touched are parked elsewhere:

1. When an A3B-class model serves on the Hermes router, uncomment `STUDIO_HERMES_BASE_URL`
   in `backend/.env` and re-measure. `Qwen3.6-35B-A3B` is the nearest released candidate;
   whether an abliterated GGUF exists is unchecked.
2. `build_scene_spec()` still populates only `coverage`, `wardrobe` and `hair_state` from a
   request, plus a six-phrase hair lookup. The preview now covers that gap by hand, which is
   the right place for it, but a request that names a wardrobe in prose still does not pin it
   until somebody locks the field.
