# AGENTS.md — XAI-Studio-Video

## Repository role

This repository is the implementation workspace for the user's AI video prompt/storyboard/workflow project.

The broader research and decision history lives separately in the private repository `krchoi-X/personal-ai-knowledge`. A Codex or Claude Code session attached to this repository may not have that repository or the original ChatGPT conversation in context.

## Shared authority and startup

These instructions apply equally to Codex, Claude Code, Grok Bot, Hermes, and any LLM running inside those hosts. The host/executor and its selected LLM are different identities. Agent-specific entrypoints only route here; they must not maintain independent project policy.

Read `AGENTS.md`, the applicable `TASK.md`, and inspect Git status/diff before implementation. Use `docs/current-priorities.md` when choosing work; a direct current user objective overrides stale task/priority notes. Code and tests establish what exists, while the user's objective establishes what should change.

Read additional documents only for the work involved:

| Work | Read |
|---|---|
| Agent setup, ownership or handoff | [Shared agent workflow](docs/shared-agent-workflow.md) |
| Producing, importing, presenting or locating results | [Artifact and review contract](docs/artifact-and-review-contract.md) |
| Code changes and verification | [Verification](docs/verification.md) and relevant subsystem architecture |
| Video prompt design | `docs/architecture.md`, `SKILL.md` |
| Character identity or local still generation | `skills/character-manager/SKILL.md` |
| Idea/storyboard/sample/final workflow | `skills/idea-to-production/SKILL.md` |
| External media importer assignment | `docs/grok-bot-handoff.md`, `external_media_import/TASK.md` |
| Control Tower | `docs/control-tower-v0.1.md`, scoped task and ownership exception |
| Studio UI/integration | Studio `AGENTS.md`, `DESIGN.md`, architecture and navigation plan |

Before implementation, record intent in the applicable task document. Read-only reviews need not replace an active task. Root `TASK.md` tracks the main task; assigned packages keep their scoped `TASK.md`. Each active scope names one Active editor. Preserve other scopes and append handoff notes instead of rewriting another editor's plan. Archive completed root notes before replacing them; link open follow-ups.

## Durable cross-agent handoff protocol

This repository is intentionally designed so work can move between development and production agents without relying on either model's conversation history or on a final handoff message.

Why this exists:
- subscription/credit limits can be reached without a useful warning;
- an agent may disappear before it can summarize its work;
- copying prompts manually between agents is error-prone and wastes context;
- the repository, not an agent conversation, must be the durable shared state.

Therefore:

### Before modifying code for a new task

1. Read this file and the applicable root or scoped `TASK.md`.
2. Inspect the relevant code and Git state.
3. Create or refresh that task record with Active editor, scope, and at minimum:
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

Files outside a bounded package are not ownerless. Shared schemas, migrations, CLI entry points, package/build configuration, root launch scripts, architecture documents, and cross-module fixtures are integration-owned by Codex unless the active task explicitly assigns them otherwise. Any assigned agent may edit them with named consumers, file scope, and acceptance checks; the current explicit assignment overrides default ownership. Before downstream work, preserve a reviewable contract checkpoint (commit when available, otherwise an exact diff/patch and base revision). The receiving agent must inspect it rather than rely on a conversation summary. This rule does not itself authorize publishing or pushing changes.

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

## Production request routing

Use [the shared routing and artifact contract](docs/artifact-and-review-contract.md) for every agent. An explicitly requested external engine takes precedence over the local default. Local existing-character still requests use `tools/character_scene.py produce`; read the Character Manager skill first. External image/video results enter through the existing importer and Gallery contracts. Do not invent a parallel gallery or per-agent output hierarchy.

When the request is clear, execute within its authorized scope without asking the user to restate it. Preserve the exact request, canonical DNA, and existing review/visibility decisions. A pasted identity prompt is runtime input unless a canonical edit is explicitly requested. Report meaningful DNA differences without silently changing the character.

Record the real requesting actor, executor and model/provider separately where supported. The local scene CLI accepts `codex`, `hermes`, `web`, `grok`, `claude`, `user`; use your real actor and use `web` only through its worker. Register WanGP sessions with `wangp_recorder.py session` and pass `--requested-by` on submit as documented in `docs/wangp-recorder.md`. Never impersonate another agent or invent unsupported CLI values. See the shared workflow for supported-host delegation and production recording rules.
