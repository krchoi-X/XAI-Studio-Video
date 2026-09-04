# Current Task

Status: no active task recorded in this file yet.

This file is durable cross-agent state, not an end-of-session summary. The active coding agent must create or refresh it **before implementation begins** and keep it concise after meaningful milestones so another agent can recover even if the current session ends unexpectedly.

## Goal

Describe the concrete outcome of the current task.

## Constraints / Must Preserve

- List behavior, data, architecture boundaries, compatibility, or user decisions that must remain intact.

## Must NOT Do

- List explicitly out-of-scope changes.
- Avoid unrelated refactors.

## Expected Scope

- Likely files/directories:
- Expected change radius: small / medium / large
- Mechanically verifiable: yes / partial / no
- Diff-size expectation, if useful: use as a warning threshold, not an absolute hard limit.

## Plan

1. Inspect relevant code and Git state.
2. Implement the smallest coherent change.
3. Run deterministic verification first.
4. Update Progress / Next after meaningful milestones.

## Progress

- [ ] Not started

## Verification

- Tests:
- Typecheck:
- Lint:
- Build:
- Other:

## Next

Record the next concrete action another agent should take if this session ends now.

## Blockers / Uncertainties

Record only durable information that would prevent another agent from repeating failed work or misunderstanding the task.

## Relevant Files

- Add only the files that matter to recovering this task.

## Recovery Rule

If this file is stale, trust evidence in this order:

1. actual code and working tree;
2. Git status/log/diff;
3. deterministic verification results;
4. this file;
5. prior agent prose.

After two materially similar failed attempts, do not continue looping. Re-scope, diagnose, or escalate.
