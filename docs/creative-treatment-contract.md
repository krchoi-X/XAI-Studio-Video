# Creative Treatment and Production Role Sidecars

Status: optional contract boundary for complex, reference-heavy, continuity-sensitive, or story-driven production. Simple work may start with Hermes directly from the user's idea.

## Authority boundary

The Creative Treatment frames the story; it is not a production storyboard, renderer prompt, or render GO.

```text
User idea
→ optional Frontier Creative Treatment
→ Hermes Production Storyboard + Intent Contract + prompt_segments and required engine-profile drafts
→ user jointly approves the production artifacts and visible production details
→ Hermes selects approved engine values
→ deterministic compile/check
→ Hermes Runtime
→ local renderer
→ independent-context Hermes review
```

For clearly adult fictional characters, mature production details may be chosen at the Hermes production stage only when they are visible in the Production Storyboard and Intent Contract and included in the user's final production approval. Never hide such details in a handoff to evade another provider's policy.

## Creative Treatment v1

Schema: `schemas/creative-treatment-v1.schema.json`.

It records the premise, audience understanding and feeling, story arc, important visual moments and objects, extracted reference grammar, known failures, production risks, Hermes's creative freedom, boundaries, author/model, and a treatment-only approval. `approval.scope` is deliberately fixed to `creative_direction_only_not_render_go`.

`status: approved` means the direction may advance to production design. It does not approve the resulting shots or prompts.

## Production Role Attribution v1

Schema: `schemas/production-role-attribution-v1.schema.json`.

It separates treatment author/model, storyboard author/model, prompt author/model, submitter/runtime, renderer, first reviewer, and the exact user-approved production artifacts and hashes.

For the treatment-backed default flow, storyboard author, prompt author, and submitter are Hermes. The treatment author may be ChatGPT, Claude, Codex, Grok, or another explicitly recorded agent. The first reviewer is a separate Hermes pass with `independent_context: true`.

At minimum, `production_approval.approved_artifacts` binds the exact approved production-plan path and hash. Per-shot Intent Contracts and approved prompt-segment artifacts should be added before their renderer submissions. `mature_details_reviewed` records whether the user-facing production review included those details; it is not permission to invent them.

## Validation and registration

```powershell
python tools/creative_treatment.py `
  --treatment <session>/creative-treatment.json `
  --roles <session>/production-role-attribution.json

python tools/wangp_recorder.py session `
  --session-dir <session> `
  --requested-by user `
  --executor hermes-runtime `
  --production-plan <session>/shot-production-plan-v2.json `
  --creative-treatment <session>/creative-treatment.json `
  --role-attribution <session>/production-role-attribution.json
```

Registration rejects draft or invalid treatments, missing sidecars, non-Hermes production authors in the treatment-backed default path, or an approval record that does not match the exact production-plan path and hash. Renderer-specific grammar remains a compiler-adapter responsibility: H3 Ref2VA and FL2VA use their native approved engine profiles, not the generic contract/debug representation. Existing sessions without these sidecars remain valid.

## Review boundary

The first review inspects moving video, critical frames, clip boundaries, audio/dialogue, identity, wardrobe, props, state persistence, everyday realism, cultural prop identity, and object counts. Failure attribution remains `storyboard | compiler | renderer | edit`.

Two materially similar failures or an ambiguous repair returns to a frontier consultant. The consultant diagnoses; Hermes applies the production revision after any required user reapproval.
