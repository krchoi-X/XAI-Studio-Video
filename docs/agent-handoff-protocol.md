# Credit-Aware Cross-Agent Handoff Protocol

## Purpose

This repository may be edited by more than one coding agent, especially Codex and Claude Code. The goal is **not** to build another model router or orchestration application. The goal is to make agent switching cheap, predictable, and recoverable using artifacts the repository already has: files, Git history, and deterministic verification.

The design is optimized for a solo developer using subscription-based coding tools where usage/credit limits may be reached unexpectedly.

## The problem this solves

A naive workflow looks like this:

```text
User -> Codex conversation -> manual handoff prompt -> Claude Code
```

This is fragile because the Codex session may become unavailable before it can prepare the handoff. It also makes the user responsible for remembering and copying architecture context, implementation status, failed attempts, and next steps.

A second naive solution is to add an API-based model router or another orchestration tool. That can solve prompt routing, but it adds installation, maintenance, credentials, and potentially separate API billing. For this project that complexity is not justified yet.

The preferred model is therefore:

```text
                 Repository
              /      |       \
          AGENTS.md TASK.md   Git
              \      |       /
               Codex <-> Claude Code
```

The repository is the shared memory. Model conversations are temporary execution contexts.

## Core principle: durable state before graceful shutdown

Do not design around a graceful end-of-session event.

Credit limits, crashes, lost sessions, machine restarts, or tool failures can interrupt work without giving the active agent a chance to summarize. Therefore a final handoff step cannot be a required part of correctness.

Instead:

1. task intent is written before coding starts;
2. durable progress is checkpointed during meaningful milestones;
3. the next agent reconstructs reality from code and Git;
4. stale prose never overrides current implementation evidence.

This is the same resilience principle used in fault-tolerant systems: recovery state must exist before failure occurs.

## Shared artifacts and responsibilities

### `AGENTS.md` — durable operating policy

Contains rules that should remain valid across many tasks:

- repository role and architecture boundaries;
- startup read order;
- cross-agent recovery protocol;
- scope discipline;
- deterministic verification preference;
- retry limits;
- project-specific routing rules.

It should remain compact enough to function as a map, not become a complete encyclopedia of the project.

### `CLAUDE.md` — compatibility shim, not a second policy

Claude Code uses `CLAUDE.md`, while Codex naturally consumes `AGENTS.md`. Maintaining two independent instruction sets creates documentation drift.

Therefore `CLAUDE.md` imports and points to `AGENTS.md`. Claude-specific notes should remain minimal.

### `TASK.md` — current intent and recovery hint

`TASK.md` is created or refreshed **before implementation**. It is not a post-session report.

It should answer only the questions another agent needs to recover quickly:

- What outcome are we trying to achieve?
- What must remain unchanged?
- What is explicitly out of scope?
- What was the planned approach?
- What has actually been completed?
- What verification has run?
- What is the next concrete step?
- What failed approach or blocker should not be rediscovered from scratch?

Do not store long chain-of-thought or conversational narrative. The goal is durable operational context with low token cost.

### Git — actual handoff medium

Git, not model prose, is the authoritative record of implementation progress.

When taking over work, inspect:

```bash
git status
git log --oneline --decorate -n 20
git diff
git diff <base>...HEAD
```

Use coherent commits/checkpoints where practical. A future agent should be able to answer "what changed?" without the previous model being present.

## Evidence priority

When sources disagree, use this order:

1. actual code and working tree;
2. Git history and diff;
3. deterministic test/build/type information;
4. `TASK.md`;
5. previous model prose or chat summary.

The reason is simple: task notes can become stale while code continues to change. Documentation exists to explain intent, not to rewrite reality.

## Credit-aware verification

The system should not spend a second model call to verify facts a deterministic tool can settle.

Default path:

```text
Executor
   |
   v
Tests / typecheck / lint / build
   |
   +-- PASS and change is well-scoped --> Done
   |
   +-- Ambiguous / architectural risk --> LLM review or escalation
```

Use a second strong model when machine verification cannot judge the important part of correctness, for example:

- architecture boundary changes;
- large change radius;
- visually or semantically subtle behavior with weak tests;
- unclear legacy dependencies;
- repeated failures indicating the current approach is wrong.

This keeps the Planner/Reviewer concept available without paying for it on every task.

## Routing principle

Do not route only by subjective "difficulty". Prefer these dimensions:

1. **Change radius** — how much of the repository can be affected?
2. **Mechanical verifiability** — will tests/typecheck/build reliably expose failure?
3. **Architecture impact** — does the task change a durable boundary or hard-to-reverse decision?
4. **Retry cost** — will a weak first attempt likely cost more than starting with a stronger executor?

Example matrix:

| Change radius | Mechanically verifiable | Preferred handling |
|---|---|---|
| Small | High | cheaper/faster capable executor is reasonable |
| Small | Low | stronger executor; avoid silent failure |
| Large | High | strong executor + deterministic verification |
| Large | Low | planner + strong executor + selective LLM review |

The project currently does **not** require an API model router or a new local orchestration application to apply this principle.

## Retry budget

Repeated agent loops can consume more subscription credit than using a stronger model once.

Rule:

- one failed attempt may be corrected normally;
- after two materially similar failed attempts, stop repeating the approach;
- diagnose, split the task, reduce scope, or escalate.

The objective is not to maximize autonomous retries. The objective is to maximize useful progress per unit of credit and attention.

## Scope guardrails

`TASK.md` may include:

- expected directories/files;
- explicitly forbidden areas;
- expected change radius;
- approximate diff-size warning threshold.

These are guardrails, not arbitrary hard limits. For example, exceeding an expected 500-line diff should trigger inspection for generated/formatting/unrelated changes rather than automatic rejection.

## Example: Codex stops unexpectedly

Assume Codex was implementing a generation queue and the subscription limit is reached without warning.

Claude Code should not require a handcrafted handoff prompt from Codex.

It should:

1. read `AGENTS.md`;
2. read `TASK.md`;
3. inspect `git status`, `git log`, and the current diff;
4. run or inspect the recorded deterministic checks;
5. identify the gap between current implementation and task goal;
6. update stale task notes if necessary;
7. continue from repository evidence.

The user should not have to reconstruct the previous Codex conversation.

## Why no additional orchestrator yet

A dedicated CLI orchestrator may become useful if agent switching becomes frequent enough that session launching and routing themselves dominate the workflow. That is not the current baseline.

Adding another application today would introduce:

- installation/update overhead;
- another configuration surface;
- additional failure modes;
- possible authentication complexity;
- temptation to automate model routing before enough real task data exists.

The minimal protocol solves the highest-value problem first: **safe state transfer without prompt copying and without relying on graceful session termination.**

## Future evolution

Only add more infrastructure when repeated real usage demonstrates a need. Possible later additions include:

- task-specific branch/worktree automation;
- automatic task snapshot generation from Git state;
- subscription/quota-aware CLI routing;
- execution metrics by model (attempts, success, review rejection, credit use);
- selective planner/reviewer escalation.

These should remain optional layers around the repository protocol, not prerequisites for basic handoff.

## Summary for coding agents

If you are Codex or Claude Code working in this repository:

- Assume your session can disappear at any time.
- Do not keep critical task state only in conversation memory.
- Write the task intent before coding.
- Leave small, durable checkpoints while working.
- Use Git and code as the source of truth.
- Prefer deterministic verification over another expensive LLM pass.
- Keep handoff notes concise.
- After two similar failed attempts, stop looping and change strategy.
- Make it possible for another capable agent to continue without asking the user to manually translate your session.
