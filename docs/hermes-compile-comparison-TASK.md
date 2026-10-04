# Hermes-compiled vs Claude-compiled: Lee Suan reference set

- Date: 2026-10-04
- Active editor: Claude Code (claude-opus-5-5), real actor `claude`; compiler under test: Hermes (local `meromero26b-a4b-hermes`)
- Status: ACTIVE

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

## Next

Build Hermes workspaces → Hermes compile → gate check → render 10 clips → assemble → score → comparison videos → sync.
