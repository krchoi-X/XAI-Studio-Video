# Lia identity lock — single-axis validation batch

Master reference (runtime input; not an approved canonical reference yet):
`D:\AI_Studio\library\characters\ch-lia\imports\inbox\GPT\ChatGPT Image 2026년 9월 4일 오후 10_31_54.png`

Operator picked candidate #4 on 2026-09-07 from `D:\AI_Studio\reports\lia-identity-candidates`.

## The failure being measured

Reported symptom: a face the operator likes appears, then the next image is a generic "AI beauty" face; changing the angle or the clothes produces a different person or that same generic face.

That is the model falling back to its beauty prior whenever it is given latitude, not seed noise. The written DNA cannot prevent it, because every trait in the DNA (large soft eyes, clear pale skin, slim oval face, small refined nose) also describes the prior. `docs/character-face-discovery-workflow.md` already named this as the character *separability* problem.

## Design

Each shot changes exactly one axis and pins everything else to the reference, so a broken face identifies the axis that broke it. Every prompt carries an anti-prior instruction stated positively, because this model runs at guidance 0 where negative prompts have no effect.

| id | axis under test |
|---|---|
| ax-00-rebuild-same | baseline: does the face survive a pass through the model with nothing asked |
| ax-01-wardrobe-only | the clothes axis the operator reported as a failure |
| ax-02-turn-45-only | the angle axis at 45 degrees, with nothing else changed |
| ax-03-profile-90-a | the full profile, seed A |
| ax-04-profile-90-b | the same profile request, seed B: if A and B disagree the profile is being invented |
| ax-05-hair-ponytail-only | the hair axis |
| ax-06-neutral-studio | three axes at once: the neutral master, and how much latitude costs |

Engine `krea2_turbo_edit` at 768x1024, 8 steps, guidance 0, one image per shot, no retries.
Outputs: `D:\AI_Studio\library\characters\ch-lia\generations\IDENTITY-20260907-211003-lia-master-lock\outputs\krea2-edit`

## What each outcome means

- `ax-00` already drifting: the turbo edit path cannot hold this face at all; go to Krea2 RAW (20 steps, guidance 2, negative prompts effective) or to the video route.
- `ax-01`/`ax-05` fine but `ax-02`+ drifting: only rotation breaks it; the video turnaround is the answer.
- `ax-03` and `ax-04` disagreeing with each other: the profile is being invented per seed and must instead be established once, by video or by choosing one and making it canon.
