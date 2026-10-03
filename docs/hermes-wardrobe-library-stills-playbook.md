# Hermes playbook — character wardrobe-library stills (Mira pattern)

Status: live pattern used 2026-09-28 on ArtXorn for `ch-mira`.
Purpose: fill a character's still library with diverse wardrobe / everyday full-body shots on **local WanGP Qwen Image 2.1**, without burning Grok/Contents Creator credits. **비서실장 reports results only.**

## 0. Hard gates (every character)

1. **Adult check FIRST** — read `character.json` (Private: `D:\codex\XAI-Studio-Private\characters\<id>\character.json` or resolved via `character_manager.character_record_path`).
   - Require explicit adult wording (e.g. `stable_dna.adult_age_range` like "young adult … early twenties", adult body proportions, graduate/job context).
   - If minor / ambiguous → **refuse** nude / swimsuit / underwear; report to 비서실장; do not generate those wardrobe classes.
2. **Preflight** (every run start / on GPU error):
   ```powershell
   cd D:\codex\XAI-studio
   D:\AI\WanGP\env_uv\Scripts\python.exe -m control_tower --check
   D:\AI\WanGP\env_uv\Scripts\python.exe tools\local_wangp.py doctor --wangp-root D:\AI\WanGP
   ```
   Gate: `running=0` `active=0`, doctor `ok: true`. **One GPU job at a time.** Idle WanGP Web UI (`wgp.py`) with VRAM≈0 is OK to leave; do not force-kill unless lock blocks and a real render holds VRAM.
3. **Gallery UI unfinished is not a blocker** — always save via character_scene default library path (below).

## 1. CLI / entrypoints

| Layer | Path / command | Role |
|---|---|---|
| Official still CLI | `D:\codex\XAI-studio\tools\character_scene.py produce` | Prepare + submit + wait |
| Engine | `--engines qwen21` → `qwen_image_21_uncensored_q4_k_m` | WanGP Qwen Image 2.1 |
| Sequential loop (this Mira job) | `D:\codex\XAI-studio\tmp\mira_qwen100_runner.py` | Loops items, logs jsonl, STOP_AT wall-clock |
| Monitor helper | `D:\codex\XAI-studio\tmp\mira_monitor.py` | Optional progress peek |
| Log | `D:\codex\XAI-studio\tmp\mira_qwen100_log.jsonl` | Per-item session_dir / counts |
| Hermes-native batch (preferred for next chars) | `tools\hermes_night_batch.py create --plan-file <plan.json>` | Sequential queue; **hardcodes `--actor hermes`** |

**Do not** invent alternate batch folders. **Do not** parallel WanGP.

### One-shot produce (building block)

```powershell
cd D:\codex\XAI-studio
D:\AI\WanGP\env_uv\Scripts\python.exe tools\character_scene.py produce `
  --character <character-id> `
  --engines qwen21 `
  --count 4 `
  --strategy strict_translation `
  --actor hermes `
  --constraints-json "{\"coverage\":\"none\",\"wardrobe\":\"none\"}" `
  --request "<verbatim English scene Prompt>"
```

- `count` 1–20 per engine (qwen21 renders **one image per WanGP batch and repeats** — still sequential under the hood).
- Prefer **subprocess list args** (Python) over PowerShell JSON quoting.
- Mira live run used `--actor grok` only because Contents Creator owned the mistargeted job; **Hermes future runs must use `--actor hermes`** (or night_batch which already sets hermes).

## 2. Scene plan shape + HARD wardrobe locks

**Mira live plan:** 25 primary scenes × `count=4` ≈ 100 images, then overflow scenes until wall-clock (user window). Same pattern for any character: N wardrobe buckets × M variants × count.

**Buckets used:** nude, swimsuit, underwear, dress, shorts/everyday, role (cafe / yoga / art-school).

### Encoding locks (critical — learn from Reika reference-clothes leak)

Pass **`--constraints-json`** (immutable), not Soft Outfit-only text:

| Intent | constraints-json | Request must also say |
|---|---|---|
| Nude | `{"coverage":"none","wardrobe":"none"}` | completely nude; no towels/robes/sheets/censor; barefoot unless stated |
| Clothed | `{"coverage":"clothed","wardrobe":"<exact outfit string matching request>"}` | explicit TOP / BOTTOM / FOOTWEAR; forbid extra layers / blazer invent |

Rules validated by `character_scene.validate_scene_spec`:
- `coverage` ∈ `user-specified` | `none` | `clothed`
- `coverage=none` **conflicts** with non-empty wardrobe → use wardrobe `"none"`
- Pipeline emits IMMUTABLE lines: "Coverage is none…" / "Wardrobe is immutable: …"

**Reference policy for wardrobe library fills:**

- Stable DNA is mandatory on every item. Confirm `prompt-trace.json` contains the resolved character record version/hash and compiled face/body/hair anchors; a character ID alone is insufficient.
- Do not use a broad auxiliary identity image whose clothing conflicts with the target wardrobe merely to increase diversity. The Reika face-reference blazer case showed clothing leakage from such a reference.
- This exception is only for **new-scene wardrobe-library generation**. If the operator says “transform this image,” the exact selected image is mandatory and must be hash-bound together with Stable DNA; use the reference-transformation path, not this diversity-batch recipe.
- A clean face/body master whose role and clothing risk were inspected may be used when the supported pipeline calls for it. Record that role and the accepted leakage risk rather than silently omitting the master.
- Strategy: `strict_translation`; do not soften or creatively rewrite the exact wardrobe lock.

### Request template (English, 3–6 sentences)

```
Photoreal live-action photograph of exactly one adult woman <Name>,
young adult …, full-body head-to-toe in frame.
No other people, no text overlays, no cartoon/anime, no plastic skin.
<location + pose + lighting>.
TOP: … BOTTOM: … FOOTWEAR: …   OR completely nude …
Do not invent extra layers, blazer, coat, or clothes copied from an auxiliary reference.
```

## 3. Output root

Always:

`D:\AI_Studio\library\characters\<character-id>\generations\SCENE-<stamp>-…\`

Per session: `outputs\`, `runs\`, `prompt.txt`, `batch.yaml`, `prompt-trace.json`, `request.txt`.
Gallery unfinished → ignore UI; files on disk are the deliverable.

## 4. Adult check + Soft + actor (summary)

| Check | Mira / pattern |
|---|---|
| Adult | Card `adult_age_range` young adult early twenties → nude/swim/UW allowed |
| Auxiliary identity reference | Omit only when its wardrobe would conflict; Stable DNA remains mandatory |
| Actor | Hermes jobs: `--actor hermes` or night_batch |
| requested_by | Flows from actor into run record |

## 5. How Hermes should run the NEXT character

**Preferred:** `hermes_night_batch` plan JSON (actor already `hermes`, sequential, GPU backoff).

Limits (code): max **48 items**, count **1–10** per item, max **240** generated images, engines `z-image|krea2|qwen21`. For Qwen-only wardrobe fill use `"engines": ["qwen21"]`.

```json
{
  "title": "<Char> wardrobe library fill qwen21",
  "source_request": "USER: diverse full-body stills …",
  "items": [
    {
      "character_id": "ch-example",
      "prompt": "<full request text as above>",
      "engines": ["qwen21"],
      "count": 4,
      "prompt_strategy": "strict_translation",
      "immutable_constraints": {"coverage": "none", "wardrobe": "none"},
      "scene_spec": {}
    },
    {
      "character_id": "ch-example",
      "prompt": "… charcoal one-piece … TOP/BOTTOM …",
      "engines": ["qwen21"],
      "count": 4,
      "prompt_strategy": "strict_translation",
      "immutable_constraints": {
        "coverage": "clothed",
        "wardrobe": "charcoal one-piece swimsuit"
      },
      "scene_spec": {}
    }
  ]
}
```

```powershell
cd D:\codex\XAI-studio
D:\AI\WanGP\env_uv\Scripts\python.exe tools\hermes_night_batch.py create --plan-file D:\codex\XAI-studio\tmp\<char>_wardrobe_plan.json
```

Queue root default: `D:\AI_Studio\workspace\hermes-night-batches\`. Only one active night batch.

**Fallback:** copy/adapt `tmp\mira_qwen100_runner.py` → set `CHARACTER`, `ACTOR="hermes"`, `ITEMS`, optional `STOP_AT`; run under WanGP python. Same produce CLI underneath.

For ~100 images: e.g. 25 items × count 4, or 48 items × count 2.

## 6. Files Hermes should read (already on ArtXorn)

| File | Use |
|---|---|
| `D:\codex\XAI-studio\tmp\mira_qwen100_runner.py` | **Canonical live recipe** — ITEMS list, constraints encoding, STOP_AT, produce argv |
| `D:\codex\XAI-studio\tmp\mira_qwen100_log.jsonl` | Example success lines (`session_dir`, `output_count`, `requested_by`) |
| `D:\codex\XAI-studio\tmp\mira_monitor.py` | Optional progress |
| This playbook | `D:\codex\XAI-studio\tmp\HERMES-wardrobe-library-stills-playbook.md` |
| Skills (Grok side; Hermes can mirror) | character_scene stills + wangp preflight + provenance |
| Prior Mira day-in-life prompts | `D:\AI_Studio\library\characters\ch-mira\generations\SCENE-20260919-*` (request/prompt-trace) — pose/everyday templates |
| Engine docs | `D:\codex\XAI-studio\docs\qwen-image-2.1-*.md` |

## 7. Completion report (to 비서실장 only)

- Adult check cite
- Engine `qwen21`
- Completed count vs target
- Absolute session dirs + per-session output counts
- Sample paths across wardrobe buckets
- Failures
- One Spec-diff line: wardrobe HARD + coverage locks; DNA version/hash; exact reference decision and role; actor hermes

## 8. Never

- Parallel WanGP / second produce while one runs
- Silent DNA edits
- A wardrobe-contaminated auxiliary identity reference on a diversity fill without an explicit accepted-risk note
- Treating “no auxiliary reference” as permission to omit Stable DNA
- Using the diversity-fill recipe when the request is to transform one exact image
- Outfit `[MUTABLE]` without a hard `coverage` / wardrobe lock (Reika leak)
- Switching engine to krea2/z-image if qwen21 fails without reporting
- Claiming done without files under `generations\...\outputs`
