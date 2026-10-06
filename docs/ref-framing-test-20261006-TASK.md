# Reference face-size vs seated head crop — controlled test (2026-10-06 night)

- Active editor: Claude Code (claude-opus-5-5), real actor `claude`; Hermes compiles prompts for new routines.
- Status: ACTIVE
- User request (2026-10-06 ~23:xx): "진행해줘. 자야할 시간이라 끝나면 비슷한 패턴으로 다른 캐릭터로 2개쯤 더 만들어서 가설을 검증해봐"
  — run the identity-reference test proposed in Grok's record, then verify on two more characters.

## Hypothesis (from Grok's 2026-10-06 record, sharpened)

Seated-line c3 head cropping depends on the identity reference. Measured face height / 480 px of the references used:
Noa 0.67 (head kept) vs Suan 0.37-0.40 and Lia 0.34-0.46 (head cropped). H: a reference whose face fills ~0.65 of the
frame keeps the whole head in the seated c3; ~0.40 crops it. Alternative: c3 inherits the scale of Picture 2 (the
previous clip's last frame).

## Design

- References: `ch-lee-suan/generations/BATCH-20261006-ref-framing-test/make_refs.py` builds loose (face 0.40) and tight
  (face 0.65) 832x480 refs from each character's default identity image with one rule (scale + pad; same face centre);
  measured fractions in `refs/refs-manifest.json`.
- Part A (existing scenes, only image_refs[0] and seed vary; prompt, contract, Picture 2 unchanged):
  Suan v5 c3, Noa v1 c3 (reverse test: loose), Lia v1 c3; two seeds for Suan and Noa.
- Part B (new characters, same routine pattern as Grok's Noa/Lia, Hermes-compiled): Reika (gyoza) and Jun (kimchi
  fried rice): c1 Ref2VA, c2 FL2VA, c3 rendered twice with the same seed and Picture 2 — loose vs tight.
- Measure: YuNet face detection at 2 fps on every c3 — face-top / frame-height, frames with the face cut at the top;
  plus Claude's frame review. Approval delegated as before; renders one at a time; intermediates outside sessions.

## Must NOT Do

No DNA or approval changes, no Codex-owned file edits, no direct DB writes, no push.

## Progress
