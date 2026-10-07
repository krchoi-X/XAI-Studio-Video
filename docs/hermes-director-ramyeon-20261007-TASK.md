# Hermes as Production Director again — Lia 라면 with time ellipsis (2026-10-07)

Active editor: Claude (actor `claude`, model claude-opus-5-5). Scope: one experimental production; no methodology,
schema, shared-skill or Codex-owned tool edits.

## Goal

User (2026-10-07): the methodology says frontier agents (Claude/Codex/Grok) write only the upper-level plan and Hermes
writes the detailed storyboard, but the 10-06 routines (Grok) and the 10-06 night reftest (Claude) had the frontier
agent write the whole storyboard and used Hermes only as a per-clip compiler. Also: cooking is compressed into one
7-second clip (ramyeon done in seconds) although the guidance already has ellipsis cuts (T-01, storyboard-cutboard).
"지금은 어떻게 해야 잘 나오는지를 알아보는 단계야. 진행해봐" — results decide later methodology changes.

Run the documented flow: Claude writes only the Creative Treatment → Hermes (Production Director) writes the
Production Storyboard incl. the cut plan, then one packet file per clip → structural validation → delegated approval
(Claude review, return items, no rewriting) → deterministic contracts/IR → semantic check → render → review.

Test questions: (1) given the cut/ellipsis guidance as input, does Hermes plan a time-passage cut by itself?
(2) does Hermes-as-director keep the strengths the user liked (camera, story) with the round-2 checklist and this
week's failure lessons? (3) object/utensil duplication and skipped start poses.

## Constraints / Must preserve
- Lia identity/wardrobe/kitchen facts from Grok's lia-kitchen-routine spec (r2); identity ref
  `ch-lia/generations/BATCH-20261006-lia-kitchen-routine/refs/identity-front-832x480.png` (sha 729bc8db…).
- One spoken line 맛있겠다. (Korean). 16:9, title card, burned subtitle as before. Renders one at a time, detached.
- Treatment must not prescribe clip count or shots; Hermes decides (cap 5 clips).
- Record real roles: treatment_author claude, storyboard/prompt author hermes, approval delegated.

## Must NOT do
No DNA/approval changes, no direct Gallery DB writes, no push, no edits to Codex-owned methodology/tools, no Claude
rewriting of Hermes's words (return items only; phrase-level fixes only if Hermes fails twice, logged).

## Plan
1. Batch `ch-lia/generations/BATCH-20261007-lia-ramyeon-hermes-director/` (`hdir.py` adapted from the 10-04
   `newflow.py`); authoring folder `D:/AI_Studio/reports/lia-ramyeon-hermes-director-20261007/`.
2. Inputs for Hermes: treatment, characters, PACKET-FORMAT, CHECKLIST (round-2 + this week's lessons), h3-guide,
   CUT-PLANNING (T-01 ellipsis, storyboard-cutboard boundary rules, real-time vs clip-length check).
3. Hermes call 1: storyboard.md (cut plan). Claude review → return items if needed. Calls 2..N: one cN.json each.
4. validate → build → render (detached) → finish → sheets → Claude review + YuNet head metric → Gallery sync.

## Progress
- 10:35 task recorded. Inputs written (treatment without clip count; CUT-PLANNING from T-01/T-30/storyboard-cutboard/
  xai-shot-menu + real-time check; CHECKLIST round-2 + this week's lessons; Lia h3-guide; hdir.py from newflow.py).
- 11:0x Hermes storyboard v0 (253 s): did its own time check (noodles ~4 min > 7 s clip) and planned an ELLIPSIS
  c1 noodles in → c2 cooked; 4 clips (ref, ref_cont, ref_cont, ref). Defects: invented a pot lid without placing it,
  cut plan vs c2 text disagreed (window/clock glance), no face in c1/c2, chopsticks source/exit missing.
- Revise 1 (128 s) fixed part; revise 2 (82 s) resolved lid/one-action but wrote the file in its read-tool view
  ('N|' prefixes, literal backslash-n) and gave c3 three held objects. Retry limit reached: format-only repair (word-identical,
  checked) + remaining items moved into `approval-review.md` conditions for the per-clip files (no Claude rewording).
- Hermes per-clip files c1..c4 running.

## Next
Validate c1..c4 (max 2 fix rounds), build, render detached, finish, review.
