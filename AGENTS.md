# AGENTS.md — XAI-Studio-Video

## Repository role

This repository is the implementation workspace for the user's AI video prompt/storyboard/workflow project.

The broader research and decision history lives separately in the private repository `krchoi-X/personal-ai-knowledge`. A Codex or Claude Code session attached to this repository may not have that repository or the original ChatGPT conversation in context.

## Mandatory startup read order

Before choosing new work or interpreting an old TODO, read in this order:

1. `AGENTS.md` — durable agent operating rules.
2. `TASK.md` — current task intent, constraints, progress, and next step.
3. `docs/current-priorities.md` — current project-specific execution order and rationale.
4. `docs/architecture.md` — durable architecture decisions.
5. `SKILL.md` — current skill behavior and prompt rules.
6. Other relevant files under `docs/`, `skills/`, `adapters/`, and `templates/`.

If the user gives a direct objective in the current session, that objective overrides `TASK.md`, but update `TASK.md` before implementation so another agent can recover the work later.

## Durable cross-agent handoff protocol

This repository is intentionally designed so work can move between Codex and Claude Code without relying on either model's conversation history or on a final handoff message.

Why this exists:
- subscription/credit limits can be reached without a useful warning;
- an agent may disappear before it can summarize its work;
- copying prompts manually between agents is error-prone and wastes context;
- the repository, not an agent conversation, must be the durable shared state.

Therefore:

### Before modifying code for a new task

1. Read this file and `TASK.md`.
2. Inspect the relevant code and Git state.
3. Create or refresh `TASK.md` with, at minimum:
   - Goal
   - Constraints / Must Preserve
   - Must NOT Do
   - Plan
   - Progress
   - Next
   - Blockers or uncertainties, if any
4. Only then begin implementation.

Do not defer task documentation until the end of a session.

### During implementation

- Keep `TASK.md` concise and reasonably current after meaningful milestones, not after every minor edit.
- Prefer coherent Git checkpoints/commits when practical so another agent can reconstruct progress from history.
- Do not spend large token budgets narrating internal reasoning. Record only durable facts needed for recovery: what changed, what remains, important constraints, failed approaches that should not be repeated, and relevant files.
- Never assume there will be an end-of-session handoff opportunity.

### If inheriting work from another agent

Do not ask the user to reconstruct the previous conversation unless repository evidence is genuinely insufficient.

Reconstruct state in this order:

1. actual code and working tree;
2. `git status`, `git log`, and relevant `git diff`;
3. tests / typecheck / lint / build results;
4. `TASK.md`;
5. prior agent prose, if available.

Code and Git state outrank stale task notes. If `TASK.md` conflicts with the implementation, verify the code and update `TASK.md` rather than forcing the code back to an obsolete note.

### Verification before LLM review

Use deterministic checks first whenever they can judge correctness:
- tests;
- typecheck;
- lint;
- build;
- schema validation or other project-specific checks.

Do not invoke a second LLM merely to repeat checks that deterministic tools can settle. Escalate to another strong model/reviewer mainly when correctness is not mechanically verifiable, the change radius is large, or architecture boundaries may have drifted.

### Retry and scope guardrails

- After two materially similar failed implementation attempts, stop repeating the same approach. Re-scope the task, diagnose the underlying issue, or escalate to a stronger planner/executor.
- Treat expected file scope and diff size in `TASK.md` as guardrails. If the implementation expands materially beyond them, pause and reassess before continuing.
- Do not perform unrelated refactors while completing a scoped task.

For the rationale and examples, read `docs/agent-handoff-protocol.md`.

### Contract impact and integration-owned files

File ownership is not enough when a change affects another agent's reader or existing records. Before changing a schema, API, CLI, persisted manifest, directory convention, or other producer/consumer boundary, add a concise `Contract impact` section to `TASK.md` naming producers, consumers, old persisted examples, compatibility/migration behavior, rollback, and deterministic verification. Prefer a backward-compatible reader and old-version fixture before enabling a new writer.

Files outside a bounded package are not ownerless. Shared schemas, migrations, CLI entry points, package/build configuration, root launch scripts, architecture documents, and cross-module fixtures are integration-owned by Codex unless the active task explicitly assigns them otherwise. Claude Code may edit them only with named consumers, file scope, and acceptance checks. Commit a contract checkpoint before downstream work begins; the receiving agent must inspect the Git diff rather than rely on a conversation summary.

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
