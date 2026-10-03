# Hermes project entrypoint

Load [AGENTS.md](AGENTS.md) as the shared policy and [shared agent workflow](docs/shared-agent-workflow.md) for installation/handoff. These rules apply to every LLM selected inside Hermes. The host remains Hermes; record the selected model separately when supported.

For production, read [artifact and review contract](docs/artifact-and-review-contract.md), then the applicable skill:

- Character identity and supported local still images: `skills/character-manager/SKILL.md`.
- Visual intent alignment and storyboard revision: `skills/storyboard-director/SKILL.md`.
- Approved storyboard through sample/final production: `skills/idea-to-production/SKILL.md` and its director decisions.
- Video: root `SKILL.md`.
- Local night batches: Character Manager skill and `tools/hermes_night_batch.py`.
- Explicit external engine: preserve it and use the shared external import route; do not substitute the local default.

For routine credit-sensitive character image/video work, follow the [Grok/Hermes production playbook](docs/grok-hermes-production-playbook.md), including its still-image DNA rule. “Transform this image” requires both the exact hash-bound source and canonical Stable DNA; wardrobe/pose text is a Scene Delta, never the identity definition. When a run exposes an identity, reference, continuity or recording problem that may need Codex/Claude review, create a durable report using the [production incident guide](docs/production-incident-and-agent-consultation.md) and its template before spending more credits.

## Where WanGP run records must be written

A run is only visible by name in the Control Tower when it sits inside a session directory. Do **not** pass the
repository root as `--runs-root`; a run at `D:\codex\XAI-studio\runs\<run_id>` has no session, so it can only be
listed by its `project_id` and cannot be grouped with the character, prompts or outputs it belongs to.

Put the session under the character it belongs to, register it once, then submit each shot into it:

```powershell
$session = "D:\codex\XAI-studio\characters\ch-jun\02_generations\VIDEO-20260909-154245-jun-cafe-call"
python tools/wangp_recorder.py session --session-dir $session --requested-by hermes `
  --engine WanGP --model minimax_h3_ref2va_pruned --character-id ch-jun `
  --title "Jun cafe call" --user-request "<operator request, verbatim>" --status running `
  --production-plan "$session\shot-production-plan-v2.json"

python tools/local_wangp.py submit --runs-root "$session\runs" `
  --prompt-file "$session\shot-01.txt" --settings-file "$session\shot-01.settings.json" `
  --project-id jun-cafe-call --prompt-id shot-01 `
  --output-dir "D:\AI_Studio\library\characters\ch-jun\videos\VIDEO-20260909-154245-jun-cafe-call" `
  --requested-by hermes --wait
```

`--wait` is mandatory when Hermes submits directly. The worker unloads every loaded Hermes llama.cpp model and
Ollama model, verifies at least 6144 MiB of free VRAM with low GPU utilization, suppresses Windows sleep for the
renderer lifetime, and records that handoff in `run.json`. The command does not return to Hermes until the run is
terminal, so Hermes cannot reload Huihui/Meromero in the middle of a WanGP render. If unload or telemetry
verification fails, rendering stops before WanGP initialization. For a night batch use
`python tools/hermes_night_batch.py create --plan-file PLAN.json --wait`; the foreground call covers every queued
item. Do not use the default detached start for a Hermes-hosted run, because Hermes would be free to reload its LLM.

For new character-video and multi-pack sessions, validate and register an approved schema-v2 production plan. Its
chunk `prompt_id` must match the submit command, and its ordered reference paths must exactly match the settings.
This freezes Stable DNA and mandatory prompt anchors and blocks unverified laterality, portrait-padded body/keyframe
roles, stale earlier-state references and missing boundary frames before a GPU worker starts. Existing unregistered
sessions continue to use the legacy character-default behavior described below.

`--requested-by hermes` is already being recorded correctly; keep it. Close the session with the same `session`
command and `--status completed` (or `failed`). Full rules: [WanGP recorder](docs/wangp-recorder.md#recording-a-production-session).

For a character Ref2VA video, do not paste an image path into every settings file. `local_wangp.py submit` reads the
session `character_id`, then injects that character's durable `reference_defaults.identity` record when `image_refs`
is empty. An explicit non-empty `image_refs` value always overrides it. If no durable default exists, submission stops
before a GPU worker starts; report that record gap instead of choosing the newest image yourself.

For the normal Jun Ref2VA workflow, leave `image_refs` as `[]`; the session location and its registered
`character_id: ch-jun` select Jun's durable default. **Do not pass `--character-id` to `local_wangp.py submit`**:
it is a `wangp_recorder.py session` option and the submit CLI will reject it. After each new kind of submission,
inspect `run.json` and confirm `reference_inputs[0].basis` is `character-default` before starting more shots.

The operator's current instruction controls each production run. Apply their specified reference images or frames,
prompt, video content, duration, resolution, and output destination to that run. Use the durable character default
only when the operator has not supplied a run-specific visual reference; never silently replace an explicit reference.

**Model ids**: `model_type` must be one of the ids listed in [WanGP model types](docs/wangp-models.md), which is
generated from the installation. Anything else fails WanGP validation before any GPU work starts — a bare
`minimax_h3` is not a model type; the installed H3 ids are `minimax_h3_ref2va_pruned` (reference image → video) and
`minimax_h3_fl2va_pruned` (first/last frame → video). Verify before submitting:

```powershell
python tools/wangp_models.py --check minimax_h3_ref2va_pruned
```

Resolve CLI paths from the verified repository checkout, not an installed skill copy. For direct supported local production use `--actor hermes`; use `web` only through the web worker. Preserve the exact request and canonical DNA. Execute a clear authorized request without making the user repeat it. Verify recorded outputs and sync separately; never mark a queued job complete. Use existing sequential local queues and shared Gallery destinations.

## Conditional Codex review

Hermes is the default operator. Do not switch ordinary planning, writing, image/video/music preparation or production execution to Codex. When a high-impact decision, two repeated comparable failures, unresolved creative/continuity conflict, or an expensive ambiguous choice meets an escalation gate, resolve and follow the shared `frontier-review-escalation` skill. Send one self-contained review packet through `delegate_task`; do not use Mixture of Agents for this route. Codex is review-only by default and cannot expand Hermes's mutation, spending, publication or architecture authority. Keep the main Hermes model and the delegated reviewer model as separate configuration choices.
