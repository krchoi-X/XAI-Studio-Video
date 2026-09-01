# Precedence and Modes

Reference for `skills/idea-to-production/SKILL.md`.

## The ladder

```text
1  explicit user constraints     request.constraints  →  renderer job immutable_constraints
2  stable Character DNA          characters/<id>/character.json, read-only
3  scene requirements            what this shot must show for the beat to read
4  style enrichment              mood, lens, grade, palette
5  optional creative detail      texture, background business, props of convenience
```

Rules:

1. A lower level never overwrites a higher one.
2. When a lower level must be dropped to satisfy a higher one, drop it and record the drop. Do not keep contradictory text in the prompt hoping the model resolves it.
3. Level 1 beating level 2 is normal and expected. It suppresses that DNA field for one run; it never edits the character record.
4. Level 1 conflicting with level 1 has no tie-break and is a structured failure.
5. Levels 4 and 5 exist only in `creative_expansion`. In `strict_translation` they are empty; in `exact` they do not run at all.

This ladder matches `docs/idea-to-production-contracts.md` rule 2 and the `precedence` array already written by `tools/character_scene.py` into `prompt-trace.json`. Keep them consistent.

## Suppression, not mutation

When level 1 wins over level 2:

- omit the superseded Stable DNA sentence from the compiled prompt for this run;
- list the DNA field name in `prompt_trace.suppressed_stable_dna_fields`;
- record which constraint caused it in `prompt_trace.after_constraint_validation`;
- leave `characters/<id>/character.json` untouched.

`suppressed_stable_dna_fields` holds Stable DNA field names (`hair`, `wardrobe`, `skin`, ...), not constraint keys and not prose.

## Worked conflict — resolvable

Request:

```json
{"constraints": {"hair": "short blunt bob just below the jaw; no hair below the shoulders"}}
```

`ch-harim` Stable DNA says near-black long hair reaching around mid-back with a default high ponytail.

Resolution: the constraint wins. The DNA `hair` sentence is omitted from the compiled prompt, `suppressed_stable_dna_fields` becomes `["hair"]`, and every other identity field (face, eyes, jaw, proportions) still applies. The run proceeds normally to `needs_user_choice`.

A resolvable conflict is not an error. Do not surface it as one, and do not ask the user to confirm something the ladder already answers.

## Worked conflict — unresolvable

Request:

```json
{"constraints": {"coverage": "clothed", "wardrobe": "no clothing"}}
```

Both are level 1. The ladder cannot rank them, and choosing either silently would misrepresent the user's instruction. Emit:

```json
{
  "status": "failed",
  "storyboards": [],
  "errors": [{
    "code": "constraint_conflict_unresolvable",
    "message": "Explicit constraints 'coverage' and 'wardrobe' contradict each other and share the highest precedence level. Revise one of them.",
    "field": "constraints.wardrobe"
  }]
}
```

Name both constraints in the message and point `field` at one of them. Do not pick a winner, do not average them, and do not drop to a "safe" default.

## Modes

### `exact`

The user's text is the product. Never add, remove, reorder, translate, soften, or spell-correct it.

- `candidate_count` is clamped to one storyboard containing one shot.
- That shot's `description` is the `idea` string, character for character.
- No DNA merge prose, no scene enrichment, no negative-constraint block.
- A durable request and a full Prompt Trace are still produced. Contract rule 3 makes this mandatory, so `exact` is never a reason to skip the audit trail.
- `after_scene_style_expansion` is `null`.

If Stable DNA and the exact text disagree, the exact text wins and the DNA fields it displaces are still listed in `suppressed_stable_dna_fields`. If a reference cannot be resolved, `exact` fails like any other mode — it does not bypass adapter resolution.

### `strict_translation`

Restructure into a compiled prompt without introducing content. Identity merge runs; enrichment does not. Use for wardrobe, coverage, continuity, and identity-consistency work where new invented detail is a defect.

`after_scene_style_expansion` is `null` here too. The difference from `exact` is that DNA merge and structure are allowed, so `after_character_dna_merge` differs from `raw_user_prompt`.

### `creative_expansion`

The default. Adds pose, lens, lighting, location texture, and mood that do not conflict with levels 1–3. Enrichment is always droppable: if any addition would contradict a constraint or DNA, drop the addition, not the constraint.

`after_scene_style_expansion` is a non-null string and is normally what `final_prompt_sent_to_image_engine` is derived from.

## Mode is carried, not re-decided

`request.mode` → `renderer_job.prompt_strategy`, same value, both stages. A sample and its final render share a strategy. If the user wants a different strategy after review, that is a new request, not a mutated one.
