# Hermes project entrypoint

Load [AGENTS.md](AGENTS.md) as the shared policy and [shared agent workflow](docs/shared-agent-workflow.md) for installation/handoff. These rules apply to every LLM selected inside Hermes. The host remains Hermes; record the selected model separately when supported.

For production, read [artifact and review contract](docs/artifact-and-review-contract.md), then the applicable skill:

- Character identity and supported local still images: `skills/character-manager/SKILL.md`.
- Idea/storyboard/sample/final: `skills/idea-to-production/SKILL.md` and its director decisions.
- Video: root `SKILL.md`.
- Local night batches: Character Manager skill and `tools/hermes_night_batch.py`.
- Explicit external engine: preserve it and use the shared external import route; do not substitute the local default.

## Where WanGP run records must be written

A run is only visible by name in the Control Tower when it sits inside a session directory. Do **not** pass the
repository root as `--runs-root`; a run at `D:\codex\XAI-studio\runs\<run_id>` has no session, so it can only be
listed by its `project_id` and cannot be grouped with the character, prompts or outputs it belongs to.

Put the session under the character it belongs to, register it once, then submit each shot into it:

```powershell
$session = "D:\codex\XAI-studio\characters\ch-jun\02_generations\VIDEO-20260909-154245-jun-cafe-call"
python tools/wangp_recorder.py session --session-dir $session --requested-by hermes `
  --engine WanGP --model minimax_h3_ref2va_pruned --character-id ch-jun `
  --title "Jun cafe call" --user-request "<operator request, verbatim>" --status running

python tools/local_wangp.py submit --runs-root "$session\runs" `
  --prompt-file "$session\shot-01.txt" --settings-file "$session\shot-01.settings.json" `
  --project-id jun-cafe-call --prompt-id shot-01 `
  --output-dir "D:\AI_Studio\library\characters\ch-jun\videos\VIDEO-20260909-154245-jun-cafe-call" `
  --requested-by hermes
```

`--requested-by hermes` is already being recorded correctly; keep it. Close the session with the same `session`
command and `--status completed` (or `failed`). Full rules: [WanGP recorder](docs/wangp-recorder.md#recording-a-production-session).

For a character Ref2VA video, do not paste an image path into every settings file. `local_wangp.py submit` reads the
session `character_id`, then injects that character's durable `reference_defaults.identity` record when `image_refs`
is empty. An explicit non-empty `image_refs` value always overrides it. If no durable default exists, submission stops
before a GPU worker starts; report that record gap instead of choosing the newest image yourself.

**Model ids**: `model_type` must be one of the ids listed in [WanGP model types](docs/wangp-models.md), which is
generated from the installation. Anything else fails WanGP validation before any GPU work starts — a bare
`minimax_h3` is not a model type; the installed H3 ids are `minimax_h3_ref2va_pruned` (reference image → video) and
`minimax_h3_fl2va_pruned` (first/last frame → video). Verify before submitting:

```powershell
python tools/wangp_models.py --check minimax_h3_ref2va_pruned
```

Resolve CLI paths from the verified repository checkout, not an installed skill copy. For direct supported local production use `--actor hermes`; use `web` only through the web worker. Preserve the exact request and canonical DNA. Execute a clear authorized request without making the user repeat it. Verify recorded outputs and sync separately; never mark a queued job complete. Use existing sequential local queues and shared Gallery destinations.
