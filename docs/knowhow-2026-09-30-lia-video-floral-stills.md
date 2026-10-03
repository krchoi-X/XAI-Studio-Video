# Know-how — 2026-09-30 Lia beach video + floral stills + studio UX

Status: production notes (not a Spec).
Place: `D:\codex\XAI-studio\docs\knowhow-2026-09-30-lia-video-floral-stills.md`
Mirror: `D:\AI_Studio\docs\`
Related idea: `docs/meromero-paste-prompt-strip-override-IDEA.md`

---

## 1. Video — Lia beach vlog remake r2

### What went wrong (v1 → r2)

Original v1 Continuity FAIL (drivers that became r2 locks):

- FAIL-001 face-fill selfie CU open
- FAIL-008 portrait / pillarbox remap
- FAIL-003 sit reappear after stroll (ladder reset)
- Bracelet laterality unstable (user still saw LEFT after r2)

r2 Continuity still FAIL overall, but **user (v1-r2) said continuity improved**; remaining: bracelet still wrong on v1-r2; **story does not read as one cut-ladder** — feels like amateur clips concatenated.

### What we did

- Remake Spec + FG prompts: `SPEC-20260930-lia-beach-vlog-v{1,2,3}-r2.md`
- Writer: `write_r2_materials.py` → prompts `v1-A.txt`…`v1-D.txt` (bundle under remake writer / r2-bundle)
- Engine: WanGP `local-wangp-worker`, model `minimax_h3_ref2va_pruned`, prompt mode **FG**, enhancer off
- `requested_by: grok` (비서실장 relay of user GO — not Hermes still path)
- Locks in every pack prefix: RIGHT bracelet HARD ×3 thin knots, LEFT bare; Soft Soft half-body ×3 (sit/stand/walk) with face+RIGHT wrist; landscape 832×480 HARD; open MW/FS not CU; one-way ladder; ocean SCREEN-RIGHT; cast=1 friend OOF; phone only on call beat
- Packs A–D separate generations then hard-concat (~40.5 / 36.8 / 38.9s)
- **Standing rule:** long GPU remake / multi-pack / night batch only after **explicit user GO via 비서실장**. Do not auto-remake after Continuity FAIL/RCA.

### Why “concat of random clips” happened

Each pack is an independent MiniMax job. Phrases like “AFTER standing / AFTER stroll” are text only — **no temporal memory across packs**. Hard-cut concat cannot invent causal story continuity the model never saw.

### What to do next time (video)

1. Prefer **fewer packs / longer in-prompt multi-cut** when the story must feel like one vlog (see H3 prompt skill: in-prompt HARD CUTS inside one clip).
2. If multi-pack: design **overlap anchors** (same end pose of N = start pose of N+1) and accept concat limits; don’t expect ladder memory.
3. Bracelet: HARD text was not enough — **Soft Soft image must show the correct wrist**. If Soft Soft shows left or both, model follows the picture. Fix Soft Soft before another remake.
4. User sign-off on r2 v1: other continuity better; bracelet still open; story feel still weak — **no r3 until GO**.

### Paths

- Composites: `D:\AI_Studio\library\characters\ch-lia\generations\VLOG-20260930-064041-lia-beach-vlog-v{1,2,3}-r2\edit\`
- Prompt mirrors (box): `/workspace/lia-beach-remake/r2-bundle/prompts/v1-{A,B,C,D}.txt`
- Spec-diff tech line: landscape / RIGHT bracelet settings+Soft Soft / MW-FS / one-way ladder / teal cast=1 — **tech MATCHED; visual Continuity still FAIL**

---

## 2. Stills — floral sweater cheek-cup (4 characters)

### What went wrong

First pass (krea2×4, **no Soft Soft**): wardrobe + cheek-cup pose landed, but **all faces collapsed into one person**. Character DNA (Suan ribbon, Aoi hair, Reika face shape, Lia identity) was not in the request.

### What fixed it (user confirmed faces returned)

Second pass with **Soft Soft identity** + same Outfit HARD scene:

| Character | Session | Soft Soft used |
|---|---|---|
| ch-lee-suan | SCENE-20260930-125010-… | character-default (BATCH-004 gpt-image-09) |
| ch-mizuno-aoi | SCENE-20260930-125643-… | explicit BATCH-005 gpt-image-08 |
| ch-lia | SCENE-20260930-130200-… | character-default |
| ch-mizuki-reika | SCENE-20260930-130730-… | face-09-editorial-1 |

- Engine: **krea2** (not z-image for Soft Soft), actor **hermes**, `strict_translation`, count 4
- Outfit HARD: long floral lace sweater + earrings/ring/bracelet, coverage=clothed
- Pose: both palms cupping cheeks
- Prompt text: **scene-delta only** — strip SUBJECT/MAKEUP/HAIR/age locks so they don’t fight Soft Soft
- IDENTITY REF RULE: Soft Soft = face / body proportions / stable hair only; Outfit wins on clothes; don’t copy Soft Soft pose/lighting/wardrobe
- Ignore empty failed session `SCENE-20260930-125322` (GPU lock, 0 jpgs)
- Gap: Aoi & Reika still lack `reference_defaults.identity` in `character.json` — used last known masters. **Write those defaults** so the next job doesn’t guess.

Outputs under
`D:\AI_Studio\library\characters\<id>\generations\SCENE-20260930-12….…\outputs\krea2`

### Rule to keep

**Existing character still = Soft Soft (or face master) + Outfit/pose HARD. Never “prompt only” when identity must survive.**

---

## 3. Studio app — desired change

User paste pattern: long photo prompts (SHOT/CAMERA/SUBJECT/MAKEUP/HAIR/WARDROBE/POSE…). They should **paste as-is** and only name overrides:

- “pose only, jeans”
- “pose only, nude”
- or keep a named wardrobe

Internal pipeline (idea doc already drafted):

1. **meromero** strips all clothing/accessory lines (and face/hair/age when Soft Soft is on)
2. Keeps POSE (+ camera/light/mood)
3. Injects **only** the user’s Outfit override as HARD (`clothed` jeans, or `coverage=none`)
4. Attaches character **Soft Soft master** automatically from `character.json` identity default
5. **Hermes** `character_scene produce`

UX chips: character multi-select · override line · preview of stripped prompt · badge “Soft Soft on / wardrobe stripped”.

Full draft: `docs/meromero-paste-prompt-strip-override-IDEA.md`

Also: persist Soft Soft path on Aoi/Reika so the app doesn’t fall back to “last known”.

---

## 4. Ops

- One GPU job; Control Tower `running=0` before submit
- Remake / night / multi-pack video: **비서실장 GO only**
- Credit: still loops → Hermes; video WanGP path stays Contents Creator with GO gate
