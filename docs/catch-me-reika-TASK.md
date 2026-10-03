# "잡아봐" (Catch Me) — Reika 개정판 콘티

- Date opened: 2026-10-03
- Active editor: none (completed scope)
- Status: COMPLETE — Storyboard Draft 2 delivered. A later, separate remake produced five clips; those clips remain `needs_review` and are recorded in `catch-me-reika-remake-NOTES.md`.
- Deliverable: [storyboard-draft-catch-me-reika.md](storyboard-draft-catch-me-reika.md)

## Goal

The user asked (2026-10-03) for a revised storyboard of Muse's `scenario-catch-me.md` (origin/main commit `026c716`, not
merged into this checkout): a cozy home, the door opens onto a living-room sofa, a short stay at the living-room window,
then flight to the bathroom; things that could break continuity must change at cuts, so cut there; the character becomes
Mizuki Reika (Muse had no local information); the method is adapted to MiniMax H3. The long-term goal is to produce the
whole piece; this task is the storyboard only.

## Constraints / Must Preserve

- Stable DNA of `ch-mizuki-reika` is read-only. Hair damp, bare-faced look and at-home wardrobe are Scene Deltas.
- The identity reference is the user-selected default `face-09-editorial-1.png` (candidate character, not Gallery-approved).
- Apply FAIL-009..015 (`docs/director-memory/failures.md`) and Muse's four renderability questions as gates.
- Muse's original document and its remote commit stay unchanged.

## Must NOT Do

- No render, GPU job, session registration, reference preparation or Character record edit in this task.
- No runtime prompt compile yet; the storyboard names the H3 packaging, not final prompts.

## Contract impact

None. Documentation only.

## Verification

Links resolve; `git diff --check`; every shot has a start/end state and the continuity sheet covers layout, direction,
state, cause, time and object appearance.

## Progress

- 2026-10-03: Draft 1 written, then strengthened to Draft 2 at the user's request: reaction design (visible behaviors,
  gaze table with four lens contacts, camera reactions), 18-item production risk register with evidence labels, sample
  acceptance checklist, fallback ladder. Seated start posture changed to reduce the riskiest motion. The user said a
  separate version of this story will be produced by other means; this document covers the clothed version only.
- 2026-10-03: The clothed storyboard scope was closed. A distinct remake storyboard and five resulting clip records were
  added later; that work does not retroactively change this task's constraints or approval state.

## Next

Human review of the five remake clips recorded in `catch-me-reika-remake-NOTES.md`. Any regeneration must use the
intent-preserving methodology and pass its contract gate; this completed storyboard task should not be reopened.
