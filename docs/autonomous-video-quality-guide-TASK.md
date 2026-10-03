# Autonomous video quality guide

- Date: 2026-10-03
- Active editor: Codex
- Status: COMPLETE — documentation integrated; production effectiveness awaits a controlled pilot

## Goal

Distill Muse's directing failures and Claude's Hermes production failures into one compact guide that Claude,
Muse/Somni, and Hermes/Meromero can find and apply. The guide should help Hermes choose and package an ordinary
vlog autonomously so the result is pleasant and coherent, not merely schema-valid.

## Scope

- Add `docs/director-memory/autonomous-video-quality-guide.md`.
- Link it from `AGENTS.md`, `HERMES.md`, `docs/director-memory/README.md`, and `docs/muse-curation-guide.md`.
- Do not edit Claude's active autonomous-pipeline task or its append-only failure entries.

## Constraints / Must Preserve

- Failure records remain evidence, not universal bans.
- Keep observation, hypothesis, repeated pattern, and verified behavior distinct.
- Preserve Character DNA, approval gates, renderer contracts, queues, and provenance rules.
- Optimize the local Meromero path for bounded context and machine-checkable decisions.

## Must NOT Do

- No renderer run, GPU use, schema change, runtime change, deployment, push, or publication.
- No promise that a written guide alone can guarantee the user's taste.
- No automatic retry loop or prompt-lock accumulation after a failure.

## Plan

1. Write a compact autonomous decision procedure and default ordinary-vlog recipe.
2. Add discoverable links for all agents, Hermes, and Muse.
3. Check links, diff, whitespace, and shared-policy consistency.

## Contract impact

Documentation-only. Producers and validators are unchanged. Consumers are human/LLM production agents reading
the repository entrypoints and Director Memory. Rollback removes the guide and four links. Verification is link
resolution plus diff/whitespace inspection; no production claim is made until a later controlled pilot.

## Progress

- Reviewed Muse's failure DB, Claude's Hermes findings and production incident lessons.
- Confirmed the existing Director Memory is the detailed knowledge layer and Hermes/Meromero should receive a
  compact bounded procedure rather than the entire corpus.
- Added the autonomous quality guide with an ordinary-vlog default, bounded planning passes, clip/continuity and
  reference checks, renderability choices, independent review, failure-triage order, and taste-learning rules.
- Linked the guide from the shared agent table, Hermes entrypoint, Director Memory index, and Muse curation guide.
- Preserved Claude's active autonomous-pipeline task and append-only failure changes without editing them.

## Next

Use the guide in one bounded Hermes/Meromero pilot after the existing user approval gate. Compare the finished video
against the intended feeling, spatial/causal continuity, state continuity, and naturalness; record acceptance or
rejection evidence before promoting any candidate default into a validator or renderer adapter.

## Verification

- `git diff --check`: passed; only repository line-ending notices were emitted.
- All four entrypoints contain the guide reference, and the guide plus its three principal evidence sources resolve.
- Documentation inspection confirmed no schema, runtime, renderer, queue, character, or approval contract changed.
