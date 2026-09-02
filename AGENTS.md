# AGENTS.md — XAI-Studio-Video

## Repository role

This repository is the implementation workspace for the user's AI video prompt/storyboard/workflow project.

The broader research and decision history lives separately in the private repository `krchoi-X/personal-ai-knowledge`. A Codex session attached to this repository may not have that repository or the original ChatGPT conversation in context.

## Mandatory startup read order

Before choosing new work or interpreting an old TODO, read in this order:

1. `docs/current-priorities.md` — current project-specific execution order and rationale.
2. `docs/architecture.md` — durable architecture decisions.
3. `SKILL.md` — current skill behavior and prompt rules.
4. Other relevant files under `docs/`, `skills/`, `adapters/`, and `templates/`.

If the user gives a direct objective in the current Codex session, that objective overrides the handoff file.

## Priority interpretation

Do not treat `P0` as permission to install, integrate, or rewrite code immediately.

For each priority item, read:
- `Context`
- `Priority rationale`
- `Depends on`
- `Blocks`
- `Next action`
- `Not now`

A review/research task can be P0 because it prevents duplicate implementation. In that case, perform the review first and stop at the requested deliverable.

## Relationship to personal-ai-knowledge

- `personal-ai-knowledge` is the canonical source for broad research/history.
- `docs/current-priorities.md` is the local execution snapshot for this repo.
- Do not attempt to mirror the whole knowledge base here.
- When a local task is completed, record the implementation result in this repo; the central knowledge repo can later be updated with the outcome.
- If a priority item references an external repo, do not vendor or adopt it until the handoff explicitly says integration is approved.

## Scope discipline

Prefer reuse and comparison before rebuilding functionality already implemented elsewhere. Preserve existing project architecture unless the current priority item explicitly calls for an architectural change.

## Character image request routing

Natural-language requests to generate still images of an existing character must use the same canonical pipeline as Hermes and the tablet app: `tools/character_scene.py produce`. Read `skills/character-manager/SKILL.md` before translating the request. The user does not need to know CLI syntax, session folder conventions, prompt strategies, or per-engine count semantics.

When character, engine, count, and prompt are clear, translate and execute the request. Do not create an ad-hoc batch script or guessed generation directory. Use `--actor codex` for Codex-originated CLI submissions, `--actor hermes` for Hermes, and `--actor web` only through the web worker. A pasted identity prompt is runtime input, not authorization to edit canonical DNA. Report any meaningful mismatch with `character.json`, preserve the canonical record, and keep the exact request in Prompt Trace.
