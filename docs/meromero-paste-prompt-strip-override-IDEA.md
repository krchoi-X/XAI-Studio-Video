# IDEA: meromero paste-prompt strip + outfit override

Status: draft idea only (not implemented)
Owner intent: 2026-09-30 — paste full photo-style prompts; keep only what the user names; Hermes produces.
Actors: **meromero** (decompose / rewrite) → **Hermes** (`character_scene produce`)
Related: Modular Photo Prompt Architect, IDENTITY REF RULE, Outfit+[COVERAGE] HARD, Soft Soft identity-only.

---

## Problem

Many reference→prompt dumps look like SHOT / CAMERA / SUBJECT / MAKEUP / HAIR / WARDROBE / POSE / LIGHT / ….
Users want to **copy-paste as-is**, then say only:

- “pose only, jeans”
- “pose only, nude”
- “same pose, floral sweater” (or pick Soft character)

Today, leaving SUBJECT/MAKEUP/HAIR/WARDROBE in the prompt fights Soft DNA and imports the ref’s clothes/face.

---

## Product rule (one sentence)

**Paste = raw inspiration. User override lines = sole clothing authority. Soft/DNA = face/body/hair only. Everything else (esp. wardrobe) is stripped unless the user re-adds it.**

---

## Studio webapp UX (minimal)

1. **Paste box** — full multiline prompt (no required format).
2. **Character** — Soft picker (single or multi: 이수안 / 아오이 / 리아 / 레이카…).
3. **Override line** (required for wardrobe change) — free text or chips, e.g.
   - `복장: 청바지 + 흰 티 | coverage: clothed`
   - `복장: none | coverage: none` (nude)
   - `복장: (원문 WARDROBE 유지)` — opt-in; default is **strip**
4. **Keep toggles** (defaults):
   - ✅ POSE
   - ✅ CAMERA / LIGHT / COLOR / TEXTURE / MOOD / AVOID (scene grammar)
   - ❌ SUBJECT / MAKEUP / HAIR / age-ethnicity locks (when Soft present)
   - ❌ WARDROBE / accessories / jewelry (unless override says keep or re-specifies)
5. **Preview panel** — meromero output: Scene-delta prompt + Outfit HARD block + IDENTITY REF RULE badge.
6. **Run** — Hermes `produce` with `--constraints-json` / immutable Outfit; actor `hermes`.

Default when Soft is attached: **strip clothing from paste**; never invent Soft clothing.

---

## meromero pipeline (logical steps)

```
input:  pasted_prompt, soft_character?, user_overrides
out:    scene_prompt, outfit_block, coverage, identity_ref_rule, warnings[]
```

1. **Segment** — detect labeled sections (WARDROBE, POSE, SUBJECT, …) *or* unlabelled clothing/pose phrases.
2. **Strip clothing** — remove / neutralize:
   - garments, fabrics, hems, lace, knit, jeans, dress, bikini, nude, topless, …
   - accessories that are “worn” (earrings, rings, bracelets, bags, shoes) unless override keeps accessories
   - coverage implications (“hinting S-line sweater”)
3. **Strip identity collisions** when Soft present:
   - age, ethnicity, face shape, eye color, makeup recipe, hairstyle length/color/part
   - keep only expression/gaze if user asked “expression from paste”
4. **Keep pose** — palms, weight, turn, head tilt, hand–face contact, etc.
5. **Inject Outfit HARD** from overrides only:
   - jeans example → Outfit Block + `coverage: clothed`
   - nude → `coverage: none` + HARD do-not-add-clothing
6. **Emit IDENTITY REF RULE** always when Soft:
   Soft = face / body proportions / stable hair only; never imports clothes / pose / lighting / environment / accessories. Outfit+[COVERAGE] wins on wardrobe.
7. **Warnings** — “stripped N wardrobe phrases”; “Soft on → face/hair lines dropped”; “override empty → no clothes specified (refuse or ask)” for clothed scenes.

Refuse produce if Soft+clothed scene and override wardrobe is empty (except explicit “keep paste wardrobe”).

---

## Hermes produce contract

```powershell
cd D:\codex\XAI-studio
python tools\character_scene.py produce `
  --character <id> `
  --request "<meromero scene_prompt>" `
  --engines krea2 `
  --count <n> `
  --strategy strict_translation `
  --actor hermes `
  # + immutable_constraints / --constraints-json for Outfit + coverage
```

- Preflight: Control Tower `running=0` + `local_wangp doctor`.
- Multi-character: same scene_prompt + same Outfit HARD; sequential jobs (one GPU).
- Soft Soft: prefer `krea2` (and `qwen21` if bake-off); avoid z-image for Soft Soft unless user asks.

---

## Examples

### A — Pose keep, jeans

Paste: full floral-sweater cheek-cup prompt.
Override: `청바지, 흰 크롭티 | clothed`
Result: POSE+CAMERA+LIGHT… kept; sweater/earrings/ring stripped; Outfit = jeans + white crop; Soft = 이수안 face/hair only.

### B — Pose keep, nude

Override: `none | coverage none`
Result: all wardrobe/accessories stripped; HARD no clothing; Soft must be scene-matched nude/neutral Soft when available.

### C — Multi-character same scene

Characters: ch-lee-suan, ch-mizuno-aoi, ch-lia, ch-mizuki-reika
Same meromero output ×4 Soft; Hermes sequential produce.

---

## Non-goals (this idea)

- Editing Stable DNA / Character Sheet from paste
- Auto-starting remake after Continuity FAIL (still needs 비서실장 GO)
- Replacing Modular Photo Prompt Architect — this is the **ingest front-door** that feeds it

---

## Open questions

1. Accessories: always strip with wardrobe, or separate “keep jewelry” chip?
2. Expression/makeup: strip always with Soft, or optional “keep gaze/expression from paste”?
3. meromero model/host: studio API vs local CLI first?
4. Gallery: show side-by-side paste vs stripped preview before Run?

---

## Suggested next implementation slice

1. CLI: `tools/meromero_paste_strip.py` — stdin paste + `--override` → stdout scene + constraints JSON.
2. Wire Studio still page: Paste + Override + Character → preview → Hermes produce.
3. Golden tests: floral→jeans, floral→nude, Soft-on face strip, empty override refuse.

Path: `docs/meromero-paste-prompt-strip-override-IDEA.md` (this file).
