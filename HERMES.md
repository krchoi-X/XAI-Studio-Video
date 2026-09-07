# Hermes project entrypoint

Load [AGENTS.md](AGENTS.md) as the shared policy and [shared agent workflow](docs/shared-agent-workflow.md) for installation/handoff. These rules apply to every LLM selected inside Hermes. The host remains Hermes; record the selected model separately when supported.

For production, read [artifact and review contract](docs/artifact-and-review-contract.md), then the applicable skill:

- Character identity and supported local still images: `skills/character-manager/SKILL.md`.
- Idea/storyboard/sample/final: `skills/idea-to-production/SKILL.md` and its director decisions.
- Video: root `SKILL.md`.
- Local night batches: Character Manager skill and `tools/hermes_night_batch.py`.
- Explicit external engine: preserve it and use the shared external import route; do not substitute the local default.

Resolve CLI paths from the verified repository checkout, not an installed skill copy. For direct supported local production use `--actor hermes`; use `web` only through the web worker. Preserve the exact request and canonical DNA. Execute a clear authorized request without making the user repeat it. Verify recorded outputs and sync separately; never mark a queued job complete. Use existing sequential local queues and shared Gallery destinations.
