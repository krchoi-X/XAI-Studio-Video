# Shared agent workflow

Accepted user direction: 2026-09-07. One project policy applies across agent hosts and their selected LLMs.

## Authority and entrypoints

[AGENTS.md](../AGENTS.md) is the shared operating policy. The applicable task supplies current intent and scope. [Artifact and review contract](artifact-and-review-contract.md) owns storage and presentation rules. Agent entrypoints are pointers and host-specific instructions only.

| Host / agent | Entry | Default responsibility |
|---|---|---|
| Codex | `AGENTS.md` | Repository integration and compatibility |
| Claude Code | `CLAUDE.md` → `AGENTS.md` | Bounded development; Control Tower exception retained |
| Grok Bot | `GROK.md` → `AGENTS.md` | Assigned development/import and explicit production trials |
| Hermes, with any installed LLM | `HERMES.md` → `AGENTS.md` plus selected skill | Production execution using configured tools |
| Other agents | Explicitly load `AGENTS.md` | Scope recorded in the applicable task |

These are defaults, not exclusive model capabilities. Current explicit assignments override defaults. [Role details](agent-development-production-roles.md) retains the Control Tower and Grok scope exceptions. A model change inside Hermes does not change ownership, artifact paths, permissions or workflow semantics.

A file named `GROK.md` or `HERMES.md` is not proof a host automatically loads it. For each installation, configure its supported startup/skill mechanism to load these entrypoints and required references. Resolve repository tools from the verified checkout, not the shell's starting directory or an installed skill directory. If packaging a skill copy, include its referenced files or provide a verified checkout path; record source revision (plus dirty patch/hash if applicable), installed location and verification date in that installation's deployment record. Never claim an installed copy was updated merely because this repository changed. Compare source and installed content before diagnosing inconsistent behavior.

## Work ownership and recovery

- Root task: one main objective and Active editor. Scoped package task: assigned files, its own Active editor, acceptance checks and link to root/assignment.
- Before a new root task, preserve the previous task in `docs/task-archive/` and retain open follow-ups in current priorities. Production jobs use existing job/run records instead of rewriting root TASK for every render.
- Only the scope's editor rewrites its plan. Other agents append a dated review/handoff note. Before taking over, inspect actual code, Git diff and verification; explicitly record the new editor. Never infer that all dirty files are yours.
- For cross-repository changes, record both repository roots, exact owned paths, producer/consumer changes, old fixture compatibility and checks in the relevant tasks. The shared contract checkpoint precedes downstream use; a patch and base revision suffice when a commit is unavailable.
- Completion is scoped: implementation complete, runtime verified, installed, and user reviewed are different facts. Record unverified portions explicitly.

A handoff contains goal, owner, scope, current state, evidence/check commands, remaining work, blockers and artifact/session IDs. Link durable records instead of requiring conversation reconstruction. Do not automatically send messages or launch another agent merely because a role table names it.

## Attribution and tool limits

Keep requester, executor/host, planner LLM, engine/provider and renderer model distinct. Persist them through existing supported fields and provenance records; unknown values remain unknown. Do not silently add required schema fields or assume UI readers consume new metadata.

`tools/character_scene.py --actor` accepts `codex`, `hermes`, `web`, `grok`, `claude`, `user`. Each caller must name its real actor; use web only through the app worker. For WanGP production, register the session with `tools/wangp_recorder.py session` and pass `--requested-by` to `tools/local_wangp.py submit`. Submit resolves the explicit flag, then `XAI_REQUESTED_BY`, then session records; absent information stays null. See [recording commands](wangp-recorder.md) and [Grok production instructions](grok-production-recording-note.md). External import retains its existing provenance contract.

## User-facing completion

Use the same short delivery pattern regardless of host: result/title; character + session/job IDs; verified web location or existing tab navigation; durable local record/output link; generation/import/sync/review state; unresolved verification. Prefer reusing an already open matching app/artifact tab when the host supports it. Never fabricate a deep link, open a new tab per output, or create an agent-specific Gallery destination.
