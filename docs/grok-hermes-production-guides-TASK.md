# Scoped task — Grok/Hermes production and incident guides

Active editor: Codex
Status: COMPLETE
Date: 2026-09-30

## Goal

Create durable, low-cost operating guidance for character/video generation performed through Grok Bot or Hermes, and define how production problems are recorded for later Codex/Claude consultation without relying on chat history.

## Scope

- `docs/grok-hermes-production-playbook.md`
- `docs/production-incident-and-agent-consultation.md`
- `docs/production-incidents/TEMPLATE.md`
- `docs/production-incidents/2026-09-29-reika-suan-morning-care-identity-and-props.md`
- `docs/production-incidents/2026-09-30-lia-beach-vlog-r2-reference-and-continuity.md`
- discovery links in `GROK.md` and `HERMES.md`

## Constraints / Must Preserve

- Existing Library session paths, run records, character IDs, DNA approval state and generated media.
- Existing requester/executor/engine/model meanings; do not invent a required provenance field.
- Explicit user GO for long, multi-pack, night-batch or remake generation.
- Current shared authority, production-skill-maintenance feedback flow and human review gates.

## Must NOT Do

- No GPU generation, rerender, media move/delete, DNA edit, shared-skill edit, deployment, push or publication.
- Do not rewrite the root `TASK.md` or unrelated dirty work.
- Do not promote one engine observation into a universal rule.

## Plan

1. Convert the Reika/Suan and Lia production evidence into a reusable preflight/review playbook.
2. Define the durable storage split between Library session evidence, repository incident reports and Private shared-skill feedback.
3. Add a copyable incident template and link both guides from the Grok/Hermes entrypoints.
4. Verify links, required sections, whitespace and owned-file diff.

## Progress

- Read current governance, production roles, artifact contract, shared workflow and the catalog-resolved `production-skill-maintenance` skill plus its evidence reference.
- Reconstructed the recent production failures from exact prompts, settings, references, provenance and continuity reports.
- Added the Grok/Hermes production playbook, incident/consultation guide and copyable incident template.
- Recorded the Reika/Suan and Lia r2 cases as review-ready incident reports linked to their immutable Library evidence.
- Linked the guides from both host entrypoints without changing production schemas or shared skills.

## Next

Use the playbook for the next delegated production run. Create a new incident from the template only when a new problem occurs; submit shared-skill feedback after the affected catalog skill/source is identified. No render is authorized by this task.

## Verification

- All relative Markdown link targets in the six new/updated guide files exist.
- The template and both incident reports contain every required evidence, decision, question and verification section.
- `git diff --check -- GROK.md HERMES.md` passed; only existing line-ending conversion warnings were reported.
- Existing unrelated working-tree changes were left untouched.

## Contract impact

Documentation only. Producers and persisted session schemas do not change. The guides point existing consumers to existing session records and `shared_skill_feedback.py`; rollback is removal of these new documents and entrypoint links.
