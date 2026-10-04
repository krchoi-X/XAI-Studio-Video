# Hermes-compiled vs Claude-compiled: Lee Suan reference set

- Date: 2026-10-04
- Active editor: Claude Code (claude-opus-5-5), real actor `claude`; compiler under test: Hermes (local `meromero26b-a4b-hermes`)
- Status: DONE — comparison + two new pieces rendered, registered (needs_review); awaiting user viewing

## Goal

The user asked (2026-10-04 ~08:40 KST): register the overnight Lee Suan set in the Gallery, then have Hermes produce
the same four pieces so the two can be compared, and discuss both together afterwards. Question under test: does the
approved Intent Contract carry the director's intent to another agent without the conversation or Claude's prompts?

## Design (fixed before rendering)

- Same four pieces, same final storyboard revisions (B rev 3; A, C, D rev 4), same contracts' locked/context content,
  same clip modes (Ref2VA / FL2VA chain / C3 Ref2VA + previous frame), same reference image, settings and seeds as
  Claude's used takes.
- Hermes receives only: each clip's contract JSON, a factual world brief (place, props, wardrobe, camera position,
  clip mode, line text) and an H3 prompt-format guide. It does not receive Claude's prompts or storyboard prose. It
  writes one prompt file and one acknowledgement per clip.
- Gate: same pinned v1 checker as the overnight run (`2ebbb7e` snapshot). The committed v1.1 (`c66aaf0`) renders the
  prompt from contract-held prose, which would leave Hermes nothing to compile; it is a possible third arm later.
- One pass only; no retakes for either arm in the comparison (Claude's first pass = attempt-1 clips).
- Scoring: Claude scores both arms per clip on the same rubric (event presence/order, gaze phases, camera, final
  state, omissions; plus cinematography notes). Not blind; the user's viewing is the final judgement.
- Gallery: new sessions `VIDEO-20261004-*-suan-*-hermes`; intermediates written outside session folders (the Studio
  importer registers every mp4 in a manifest-less session, and a registered file must never change in place).
  Side-by-side comparison videos in `BATCH-20261004-suan-hermes-comparison`.

## Must NOT Do

No change to the overnight sessions' registered files, Gallery DB writes, DNA/approval changes, push, or edits to
Codex's methodology/tool files.

## Progress

- Overnight set registered by Studio sync (legacy manifest-less path; 55 assets incl. intermediates, restricted,
  needs review). Moving intermediates out broke registrations, so they were restored in place (sync back to 1785
  skipped, 0 errors). B final playback verified (Range 206, preview 200).

- Hermes compiled all 10 prompts (4 oneshot calls + 1 follow-up for the missing A3 acknowledgement); all passed the
  pinned gate unchanged. Compile observations (identity tags, C3 bound to Picture 2, D1 ordering) in
  `BATCH-20261004-suan-hermes-comparison/compile-review.md`. Workspaces: `D:/AI_Studio/reports/suan-hermes-compile-20261004/`.
- Rendering started 09:0x KST (B, A then C, D); Ollama model unloaded first.
- 11:36 all 10 Hermes-arm clips rendered (one pass); finals assembled; first-pass side-by-sides
  `BATCH-20261004-suan-hermes-comparison/compare-*-claude-vs-hermes.mp4`; per-clip scoring in `render-review.md`.
  Sync imported 18 assets (10 raw + 4 finals + 4 comparisons), no intermediates.
- First-pass intent score (Claude scoring, not blind): Claude arm 6/10 pass, 4 fail (A1, A3, C3, D1);
  Hermes arm 6/10 pass incl. warnings, 3 fail (A3 partial, C2 restored omission, D1) + B1 object-state error
  (antenna already up). Different failures: Hermes kept A1 order and C3 gaze; Claude kept C2 omission and object state.
- New pieces E 첫눈 / F 이거요 (Claude-directed, Hermes compile + operator): see
  `BATCH-20261004-suan-hermes-originals/` (spec_new.py, new_pipeline.py); compile instructions add explicit
  `<Subject 1>/<Picture 1>` and single-`<d>` rules learned from the comparison.

- E 첫눈 / F 이거요 (Claude-directed; Hermes compiled all 6 prompts and launched the render as operator):
  E1 failed staging (full-body wide, people inside cafe, snow invisible) -> E2 render cancelled, Hermes recompiled E1
  once from Claude's review notes -> pass. E2, E3, F1-3 pass with warnings (long lens contact in E3; F in profile;
  F3 eyes near-lens; mild identity drift on 3rd chained clips). Hermes's own model stayed resident after its
  operator call and was unloaded by Claude ~1 min into E1. Notes: `BATCH-20261004-suan-hermes-originals/notes.md`.
- Gallery: sync imported 9 more assets (E 4 raw + final, F 3 raw + final); E final playback verified (206).
- User review (2026-10-04 afternoon): Hermes clearly better on camera movement and on the rain-soaked look; both
  arms missed coat removal (storyboard omission), used a ramyeon-style pot instead of a ttukbaegi, and showed a
  duplicated spoon. Filed as 5 feedback records (`D:/AI_Studio/workspace/skill-feedback/open/skillfb-20261004T0653*`):
  everyday-realism check, prop/culture/count checklist, appearance state in Ref2VA subject definition, compiler
  freedom vs v1.1 template (hybrid proposal for Codex), explicit compiler-brief rules for Hermes.
- Gallery check: all 82 session videos registered; no sync run while Grok was rendering.

## Next

1. User watches: Claude finals (overnight), Hermes-arm finals, `compare-*` side-by-sides, E and F finals.
2. Decide what to keep; reject extra overnight intermediates in Review (no DB edits).
3. Possible third arm: v1.1 deterministic compile (`c66aaf0`) on the same contracts.
