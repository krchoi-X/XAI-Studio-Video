# Director Core / Skill Router — first implementation

Active editor: Codex / GPT-6 Astra
Status: COMPLETE
Date: 2026-09-16

## Goal

Implement the smallest usable Director Core router from `codex-pipeline-handoff.md`: select a bounded, coherent and meaningfully different directing-skill subset for each storyboard candidate, inject only that selected context into the existing local-LLM worker, and preserve the routing decision for another agent.

## Scope

- `docs/director-memory/skill-router.json`
- `schemas/director-routing-v1.schema.json`
- `tools/director_skill_router.py`
- `tools/idea_production_worker.py`
- `tests/test_director_skill_router.py`
- `tests/test_idea_production_worker.py`
- `docs/director-memory/README.md`
- `D:/codex/XAI-Studio-Private/shared-skills/storyboard-director/SKILL.md`
- `D:/codex/XAI-Studio-Private/shared-skills/storyboard-intent-alignment-TASK.md`
- this task record

## Must preserve

- User intent and result quality outrank routing convenience.
- Preserve the frozen `storyboard-candidates-v1` and all existing request/renderer contracts.
- Load only a bounded selected context; do not copy the full Director Memory into each prompt.
- Preserve real character/reference resolution, actor/provider attribution and existing artifact paths.
- Preserve unrelated working-tree and production files.

## Must not do

- No video/image generation, GPU work, service restart, schema migration, Gallery/database change, deployment, push or publication.
- No vector database, workflow engine, broad repository cleanup or speculative capability claims.
- Do not promote routing outcomes into shared memory automatically.

## Contract impact

Producer: `tools/idea_production_worker.py` creates a new optional `director-routing.json` sidecar before storyboard generation and finalizes it with returned storyboard IDs. Consumer: the same worker prompt plus later Claude, Grok, Hermes or Codex sessions. Existing `request.json`, `storyboards.json`, `status.json` and v1 schemas remain unchanged. Old job readers may ignore the new sidecar. Rollback removes the sidecar writer/router and returns the worker to its previous prompt construction.

## Plan

1. Define a small manifest of directing modes and specialist skill metadata.
2. Add a deterministic, schema-validated router with bounded and distinct candidate subsets.
3. Inject only selected skill records into the worker prompt and persist the routing sidecar.
4. Add focused tests for selection, bounded context, candidate mapping and unchanged failure behavior.

## Verification

- focused pytest for router and idea-production worker;
- existing idea-to-production fixture validator;
- JSON Schema validation and `git diff --check`;
- no live Ollama, renderer or GPU call.

## Progress

Merged remote commit `61f7c31` through merge commit `498fd21`, then implemented the first Director Core router without changing frozen v1 storyboard contracts.

Implemented:

- lightweight mode/skill metadata in `skill-router.json`;
- schema-validated `director-routing.json` sidecar with manifest SHA-256, bounded selected skills and storyboard-ID mapping;
- deterministic candidate routing with distinct safe/exploratory subsets;
- worker prompt injection containing only the selected context, not the full Director Memory;
- canonical shared-skill instructions so Claude, Grok, Hermes and Codex use the same convention.

Verification:

- focused router/worker tests: 6 passed;
- frozen idea-to-production fixtures: 435 checks passed, 0 failed;
- changed Python modules compiled;
- canonical `storyboard-director` passed `quick_validate.py` and resolved through the active catalog;
- public and Private `git diff --check` passed;
- `origin/main` is an ancestor of the current HEAD;
- no live LLM, renderer, GPU, service, deployment, push or publication was used.

## Next

Run one real Hermes storyboard request through the worker. Inspect whether the selected modes/skills match the user's intent, then revise routing metadata only from observed misroutes. Do not add more automation before that pilot.
