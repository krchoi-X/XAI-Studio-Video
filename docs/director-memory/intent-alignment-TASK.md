# Storyboard intent-alignment method

Active editor: Codex / GPT-6 Astra
Status: COMPLETE
Date: 2026-09-16

## Goal

Define a shared directing method in which rough visual storyboards help the user and AI discover and align an incompletely expressed intent, then compile the approved intent into engine-specific image/video inputs without losing story, interest, continuity or coherence.

## Scope

- `docs/director-memory/intent-alignment-method.md`
- `docs/director-memory/README.md`
- `docs/director-memory/visual-language-pipeline.md`
- `docs/director-memory/candidate-template.md`
- `AGENTS.md`, `HERMES.md`, and `skills/README.md` routing
- host-aware renderer selection in the public method and canonical rendering reference
- `D:/codex/XAI-Studio-Private/shared-skills/storyboard-director/SKILL.md`
- `D:/codex/XAI-Studio-Private/shared-skills/storyboard-director/references/visual-intent-alignment.md`
- the matching Private scoped task record

## Must preserve

- The primary objective is a high-quality result faithful to the user's intent. Multi-agent reuse and shared learning are subordinate.
- Storyboard images are review instruments; the approved Storyboard Spec remains the durable source of intent.
- Existing Character DNA, artifact, Gallery, renderer, requester and v1 idea-to-production contracts remain unchanged.
- Preserve unrelated staged public changes and the existing Private shared-skill lifecycle work.

## Must not do

- No renderer/schema/worker change, generation, service restart, installation rewrite, push or publication.
- Do not claim a storyboard sheet alone communicates exact timing, motion, continuity or reference roles to every engine.
- Do not require film terminology from the user or force multiple candidates when one interpretation is already sufficiently clear.

## Plan and verification

1. Add a concise public method document and route it from Director Memory.
2. Add the executable method to the canonical shared `storyboard-director` skill with one focused reference and route every supported host through it.
3. Validate the shared skill, catalog resolution, links and diffs.

## Contract impact

Producer: any AI director using the catalog-resolved `storyboard-director` skill. Consumers: the user during visual alignment and any later Claude, Grok, Hermes or Codex session compiling the approved spec. This is an instruction-only refinement: existing persisted schemas and records remain valid. Rollback removes the new reference and skill sections and unlinks the public method document.

## Progress

Added the public visual-intent alignment method, aligned Director Memory candidate guidance, and routed all supported hosts to the catalog-resolved `storyboard-director` skill. The method now prioritizes result quality, treats rough boards as visual hypotheses, records approval against the Storyboard Spec, and requires engine-specific compilation rather than assuming a contact sheet is sufficient.

Verification:

- canonical shared skill passed `quick_validate.py` in UTF-8 mode;
- runtime resolver returned the Private canonical `storyboard-director/SKILL.md`;
- Claude/Grok shared policy, Hermes entrypoint and the project skill router point to the shared storyboard flow;
- required reference files exist;
- `git diff --check` passed in both repositories;
- no generation, schema/worker change, service restart, deployment, push or publication occurred.

## Next

Use the method on one real video idea. The active agent should select its strongest appropriate renderer—native image generation or the approved local route—then preserve the approved Storyboard Spec across production. Feed only evidence from that real run into shared-skill maintenance.

Follow-up verification:

- canonical skill validation passed after adding host-aware renderer selection;
- Codex/GPT Image, available Grok image generation, and Claude/Hermes local Krea 2 or Z-Image are documented as current examples rather than permanent assignments;
- the instructions require runtime capability inspection, real executor/provider attribution and an explicit handoff when no renderer is callable;
- both repository diff checks passed.
