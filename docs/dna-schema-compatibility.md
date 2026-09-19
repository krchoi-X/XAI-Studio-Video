# Stable DNA: two body schemas, one reader

Status: implemented 2026-09-19 by Claude Code
Scope: `tools/character_manager.py` only. No record was rewritten and no hash changed.

## Why this exists

A new character, `ch-mira`, arrived from the remote in a different Stable DNA shape and
failed validation with nine errors. The rest of the roster is written the old way. Rather
than convert twelve records to match one, the reader was widened to accept both, so Mira is
usable today and the full schema decision can be made deliberately later.

## The two shapes

| | anatomical (12 characters) | compact (`ch-mira`) |
|---|---|---|
| `body` | `height_impression, limb_proportions, shoulders, torso, bust, waist, pelvis_hips, lower_body, body_hair` | `overall, neck, shoulders, athleticism, proportions` |
| `face` | 6 fields | 6 + `profile` |
| `distinctive_marks` | present | absent |
| `recognition_anchors` | present | absent |
| extra | — | `beauty_direction`, and top-level `role_modes`, `hidden_identity`, `flexible_variables`, `forbidden_drift` |

A record is `anatomical` when all nine anatomical fields are filled, `compact` when
`overall`, `proportions` and `shoulders` are, and `unknown` otherwise. `unknown` is refused,
and the error names what is missing from each shape rather than assuming which was intended.

## What changed

- `body_shape(body)` reports which schema a record uses.
- `validate()` accepts either. `distinctive_marks` stays **required** on an anatomical record,
  where it has always been required, and is not required on a compact one, which has no field
  for it. Nothing was relaxed backwards.
- `warnings_for(record)` is new: valid records that give something up say so, rather than
  passing silently. Mira reports two — no `distinctive_marks`, and a compact body.
- `body_sentence()` and `body_lines()` render either shape. An anatomical record renders with
  its original phrasing, character for character, so the twelve keep sending the identical
  prompt. Anything else renders from whatever fields it carries, which also means a field
  added later reaches the prompt instead of validating and then vanishing — the failure that
  cost `ch-lia` its `nose_profile` and `chin_profile` on 2026-09-11.

`tools/character_sheet.py` already tolerated both and already knew `profile`; it needed nothing.

## What was deliberately not done

- **No record was converted.** Collapsing nine anatomical fields into `proportions` is a
  judgement about how a character should look, not a format conversion. The old wording is
  mostly pushback against an image model's defaults — "bust: not a defining identity trait",
  "waist: without exaggerated glamour shaping", "body_hair: not an identity-defining feature" —
  so each slot is a place to say no to a specific drift. Folding them loses that pressure, and
  whoever folds them is rewriting twelve characters' appearance.
- **No hash changed.** `stable_dna_sha256` is computed over the whole `stable_dna` block, and
  92 recorded sessions embed one. Touching a single field name would orphan all of them.
- **The new top-level blocks are not read yet.** `role_modes`, `hidden_identity`,
  `flexible_variables` and `forbidden_drift` are stored and ignored. `forbidden_drift` in
  particular overlaps something the code currently hardcodes — `validate_scene_spec` refuses
  `face`, `body` and `skin` for every character alike — and moving that into the record is a
  real improvement, but it is a design change, not a compatibility fix.

## Verified

- Every one of the twelve existing characters produces a **byte-identical** base prompt, core
  document and stable hash before and after. Checked by importing both module versions and
  comparing all three outputs for all twelve.
- `character_manager.py doctor` reports OK for all thirteen, Mira included.
- 17 new tests in `tests/test_dna_schema_compatibility.py`, covering shape detection, both
  shapes validating, `distinctive_marks` still required where it was, a half-written body being
  refused with both shapes' missing fields named, the warnings, both renderers, and a field
  nobody hardcoded still reaching the prompt. The live records are asserted to validate and to
  still be anatomical, so a record turning compact later is noticed rather than absorbed.
- `tests/test_character_manager.py::test_missing_body_field_is_rejected` was asserting the old
  error string. It now asserts the intent — an incomplete body is refused and names the field
  it lost — which is what the test was for.

## Open, for the full schema decision

1. What the intended schema actually is. Mira is one sample, not a specification.
2. Whether `distinctive_marks` and `recognition_anchors` return to it. Recommended: yes. They
   are what pins identity across generations, and reaching no prompt at all was treated as a
   bug and fixed on purpose.
3. Whether the anti-drift wording survives a body collapse, and where it goes if so.
4. How the 92 recorded sessions relate to new hashes: leave historical hashes as they are,
   keep an old-to-new map, or bump each character's `version` and preserve the old DNA under
   `history/`. The repository already keeps `history/<sha>/` directories, so the third fits
   what is there.
