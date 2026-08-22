# Repository Working Rules

- Preserve the approved design in `SKILL.md`, `docs/`, `skills/`, `templates/`, and `adapters/`.
- Do not introduce new concepts, files, layers, adapters, workflows, or dependencies unless the requested work requires them.
- Extend the structure only when an observed production failure cannot be handled by the existing design. Record the failure and the reason for the extension.
- The user decides creative and production direction. Codex executes that direction, makes assumptions visible, and asks before changing approved intent.
- Keep canonical creative specifications renderer-independent. For self-hosted or local renderers, do not automatically propagate hosted-provider policy constraints; apply only relevant creative and technical constraints.
- Preserve accepted work and change the smallest plausible responsibility layer when correcting a failure.
- Do not install image-generation models, create ComfyUI workflows, add training pipelines, or introduce large frameworks unless explicitly requested.
- After work, summarize changed files, why each change was needed, and the tests or checks performed.
