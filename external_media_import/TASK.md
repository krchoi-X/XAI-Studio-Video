# Task — external_media_import (Gallery image+video ingest)

Owner / Active editor: Grok Bot (Coder)
Integration owner: Codex
Status: PACKAGE COMPLETE + Studio video Gallery integration implemented (2026-09-07 JST)
Started: 2026-09-06 (Asia/Tokyo)
Authority: `docs/grok-bot-handoff.md` Task A (overrides root Control Tower TASK.md for this package only)

Do **not** replace or rewrite root `D:\codex\XAI-studio\TASK.md` (Control Tower v0.1 COMPLETE).
This file is the durable state for the bounded `external_media_import/**` package plus the explicitly assigned Studio video-extension files.

## Goal

Build a reusable CLI package `python -m external_media_import` that imports externally produced stills and videos (GPT / Grok / Krea / Z-Image / etc.) into the existing Studio Gallery contract:

1. Copy originals non-destructively into the library tree.
2. Write discoverable generation records (`batch.yaml`, `prompt.txt`, `import-provenance.json`).
3. Optionally call `POST /api/sync` so Studio indexes them.
4. Extend Studio importer + Gallery so videos are first-class (probe, thumbnail, list badge, immersive `<video>` playback with Range), without breaking image review/favorite/reference flows.

v1 media: PNG/JPEG/WebP images; MP4 (H.264/AAC or silent) and WebM (VP9/Opus or silent) video. Other containers/codecs: preserve original, surface unsupported playback reason — no silent remux/overwrite.

## Constraints / Must Preserve

- Existing image batch layout and `import_batch` / `sync_character_repo` / `POST /api/sync` entry points.
- Asset IDs derived from `sha256(root_id:relative)` — re-import of same relative path is skip/no-op.
- Existing review decisions, favorites, restricted visibility, and image reference/variation paths.
- Original media bytes and content hashes; video thumbnails are separate derived files (preview cache), never rewritten originals.
- Default review state `needs_review`; never invent user approvals/favorites.
- Visibility only from explicit input (or preserve existing); never clear restricted flags.
- Path confinement: input paths must stay under an allowed source root; reject `..` / symlink escape.
- Default mode is dry-run (report only). apply copies; never move/delete sources.
- Same destination filename with different hash = hard conflict (no quiet overwrite, no silent rename-into-duplicate).
- Package does **not** write the Studio SQLite DB directly; Gallery indexing goes through sync/`import_batch`.
- Dirty/unrelated working-tree files owned by other agents stay untouched.
- Operational defaults on this PC:
  - library-root: `D:\AI_Studio\library\characters`
  - record-root: `D:\codex\XAI-studio\characters\<character-id>\02_generations`

## Must NOT Do

- Do not replace root XAI-studio `TASK.md` or rewrite Control Tower docs as this task.
- Do not run Task B (new image generation experiments).
- Do not edit `tools/`, `control_tower/`, root launch scripts, package manifests, or DB migrations unless Codex explicitly expands scope.
- Do not invent model versions/seeds when unknown; record as unknown/missing.
- Do not merge distinct per-item prompts into one fake shared prompt in the detail UI (session prompt vs per-item provenance).
- Do not publish half-written batches: write media + provenance first; publish `batch.yaml` last.
- Do not accept arbitrary filesystem paths from the playback API — resolve by asset id through `asset_roots`.
- Do not auto-play video with sound; use `<video controls playsinline preload="metadata">`.
- Do not treat `output/register-reika-gpt-gallery.py` as the general tool — it is a one-off reference only.
- Do not push to production `main` without explicit approval.

## Investigation findings (2026-09-06 JST)

### Paths

| Path | Status |
|---|---|
| `D:\codex\XAI-studio` | EXISTS |
| `D:\codex\personal-prompt-studio\personal-prompt-studio` | EXISTS |
| `D:\AI_Studio\library` | EXISTS (characters include `ch-mizuki-reika` + GPT sessions) |
| `external_media_import/` | MISSING before this TASK.md (package not created yet) |

### Reference materials

- `output/register-reika-gpt-gallery.py` — EXISTS (one-off GPT register; copy2 + batch.yaml JSON + provenance + library outputs/gpt)
- `output/reika-gallery-registration.md` — EXISTS (22 GPT images synced; 32 previews 200)
- `output/reika-gpt-expression-study-20260906/manifest.json` — EXISTS
- `characters/ch-mizuki-reika/02_generations/GPT-20260906-*/batch.yaml` — 5 matches:
  - `GPT-20260906-reika-base-candidates`
  - `GPT-20260906-reika-face-06-editorial`
  - `GPT-20260906-reika-face-06-smile`
  - `GPT-20260906-reika-face-09-editorial`
  - `GPT-20260906-reika-face-09-smile`
- Note: these `batch.yaml` files contain **JSON** (yaml.safe_load still accepts them).

### Studio importer (current)

Key APIs in `backend/app/importer.py`:

- `MEDIA_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}` — **images only**
- `_sha256(path: Path) -> str`
- `_preview(source: Path, destination: Path) -> None` — PIL RGB thumbnail → webp
- `import_batch(database: Database, batch_root: Path, preview_root: Path) -> tuple[str, int, int]` — walks `asset_root` / `outputs`, skips unknown suffixes, opens every accepted file with PIL, engine = first relative path part
- `import_external_candidates(database: Database, manifest_path: Path, preview_root: Path) -> tuple[str, int, int]` — inbox JSON, read-only over source files, still image-only + PIL
- `sync_character_repo(database: Database, repo_root: Path, preview_root: Path) -> dict[str, int]` — characters/*/02_generations/*/batch.yaml when outputs exist
- helpers: `_batch_outputs_exist`, `import_character_record`, `import_haewon`, `_canonical_prompt_text`, `_frontmatter`

### Studio APIs / schemas / Gallery

- `POST /api/sync` → `sync_character_repo` + legacy batches + external inbox `_import-batch.json`
- `GET /api/characters/{id}/assets`, `GET /api/assets/{id}`, `GET /api/assets/{id}/preview` (webp FileResponse only)
- **No** original-media / playback / Range endpoint yet — required for video
- `schemas.Asset`: has `media_type`, `byte_size`, `preview_url`; **no** duration / width / height / playback_url yet
- Frontend `shared/types.ts` `Asset` currently **omits** `media_type` / `byte_size` (backend already returns them) — Gallery cards/viewer use `<img src={previewUrl}>` only
- Reference transformation path rejects non-image suffixes (keep that; do not feed video into image transform)

### Tooling / git

- `ffprobe` **available** on PATH: FFmpeg 8.1.1 full build (WinGet Gyan.FFmpeg)
- XAI-studio git: dirty/untracked owned by others (Control Tower leftovers, Lia/Aoi scenes, `docs/grok-bot-handoff.md`, `output/`, `characters/ch-mizuki-reika/`, etc.) — **do not touch/commit those**
- personal-prompt-studio git: dirty `public-publisher/curation/*.json` — **do not touch**

## Output layout contract (target)

```text
<record-root>/<session-id>/
  batch.yaml
  prompt.txt
  import-provenance.json

<library-root>/<character-id>/generations/<session-id>/outputs/
  <engine>/image-or-video-files
```

`batch.yaml` session fields: id, character_id, title, asset_root, visibility, status, prompt_file.
jobs/engines: provider/model + output_dir whose leaf folder name matches engine directory under outputs.

## Recommended CLI sketch

```text
python -m external_media_import --help

python -m external_media_import plan|dry-run \
  --manifest PATH | --source-dir PATH \
  --character-id ch-... \
  --session-id SESSION \
  --title "..." \
  --engine gpt|krea2|z-image|<name> \
  --library-root D:\AI_Studio\library\characters \
  --record-root D:\codex\XAI-studio\characters\<id>\02_generations \
  [--visibility standard|restricted] \
  [--provider ...] [--model ...] \
  [--allowed-source-root PATH ...]

python -m external_media_import apply   # same args; copies + writes records; batch.yaml last
python -m external_media_import resume  # continue after interrupt; hash-equal no-op
python -m external_media_import apply ... --sync-url http://127.0.0.1:8787/api/sync
```

Manifest item fields (when known): source path, engine/provider/model, prompt text, reference file/id, user request, optional created_at.
Report: accepted / invalid / duplicate / conflict / planned copy+record paths.
Distinguish media-copy failure vs sync failure; sync retry must not re-copy identical hashes.

## Plan

1. [x] Investigate paths, references, importer, APIs, Gallery, git, ffprobe; write this TASK.md; append Studio TASK note.
2. [x] Scaffold `external_media_import/` package: `__main__.py`, CLI, path guards, SHA-256, dry-run planner, apply/resume, provenance + batch.yaml writer, README with real commands.
3. [x] Studio `importer.py`: extend MEDIA_TYPES; branch image (PIL) vs video (ffprobe); video preview/thumbnail into existing preview cache; keep external_candidates compatible.
4. [x] Studio `main.py`: asset playback endpoint by id (Range/206), optional playback_url on Asset/AssetDetail; keep preview for thumbnails.
5. [x] `schemas.py` + frontend `types.ts` / `api.ts`: additive optional fields (`duration_seconds`, `width`, `height`, `playback_url`, ensure `media_type` on FE Asset).
6. [x] Gallery: card badge + duration; ImmersiveAssetViewer `<video controls playsinline preload="metadata">`; preserve image review/favorite; block video from image-only transform handoffs.
7. [x] Tests/fixtures: 3 images + 1 MP4 + 1 WebM mixed prompts; dry-run/apply/idempotent re-apply; escape/conflict/corrupt; preview+playback; old image fixture still imports.
8. [ ] Contract checkpoint + isolated branch/patch for Codex integration review. No Task B.

## Progress

- [x] Path existence confirmed (XAI-studio, personal-prompt-studio, AI_Studio/library).
- [x] Reference materials inventoried; `external_media_import/` did not exist prior to this note.
- [x] Importer/API/schema/Gallery gaps documented (image-only MEDIA_TYPES/PIL; no playback route; FE Asset lacks media_type).
- [x] ffprobe on PATH confirmed.
- [x] Git dirty files noted; left untouched.
- [x] Package implementation (`python -m external_media_import` dry-run|plan|apply|resume)
  - Modules: `__init__`, `__main__`, `cli`, `models`, `paths`, `hashutil`, `probe`, `planner`, `apply`, `sync_client`
  - README with default ops paths + real command examples
  - Path safety (abs/.. /symlink escape), SHA-256, conflict vs duplicate, atomic batch.yaml last
  - Per-item prompts via provenance + file-tagged prompt.txt (no fake mashed session prompt)
  - Optional `--sync-url` / `--sync-only` (exit 5 = sync failure after successful copies)
  - PNG/JPEG/WebP + MP4/WebM; ffprobe for video
- [x] Package tests + fixture dry-run (2026-09-07 JST): 18 passed; dry-run planned 5 (3 images + mp4 + webm)
- [x] Studio video extensions
- [x] Studio verification via pytest/httpx (import_batch video, poster, Range/206); live Gallery player on tablet still pending

## Next

1. Operator/desktop+tablet smoke: open a synced video in Gallery immersive viewer; confirm controls, no autoplay audio, seek via Range.
2. Optional: dry-run/apply a real GPT/Krea inbox batch with this CLI (still no Task B paid generation).
3. Contract checkpoint + isolated branch/patch for Codex integration review (coordinator).

## Blockers / Uncertainties

- Live Studio browser playback on tablet remains unverified until a local Studio session is available; mark live playback unverified rather than claiming full integration done.
- Frontend `Asset` type currently drops backend `media_type` — must plumb through or video branching in UI will be guesswork by extension (avoid guessing; use API fields).
- Whether preview thumbnail for video should be mid-frame vs first-frame: prefer earliest extractable frame that ffprobe/ffmpeg can grab; document choice.
- Concurrent Studio TASK Active editor was Codex (supervisor task COMPLETE); video-import scope appended below — coordinate before overlapping Studio file edits.

## Contract impact

- **Producers:** `external_media_import` CLI (new); Studio `importer.import_batch` / `import_external_candidates` / `sync_character_repo`; optional sync caller.
- **Consumers:** `POST /api/sync`; asset list/detail/preview/(new) playback APIs; Gallery cards + ImmersiveAssetViewer; image reference/variation paths (must keep rejecting non-images).
- **Persisted shapes:** existing image `batch.yaml` + asset rows preserved; additive optional video metadata in `normalized_json` (duration_seconds, width, height, codec, frame_rate, has_audio, mime) and optional Asset response fields; no DB migration required if metadata stays in JSON + existing `media_type` column.
- **Old fixtures:** retain GPT Reika image batches as regression; add mixed image+video fixture under package tests.
- **Compatibility:** expand/read-old-and-new; unknown media_type clients keep working for images; video-aware clients use new fields.
- **Rollback:** disable new import CLI / video preview branch; originals + provenance remain on disk; image gallery continues.
- **Verification:** handoff checklist (dry-run, hash equality, idempotent re-apply, rejection cases, sync-retry without recopy, import_batch on fixtures, counts/engines/preview 200, Range/206 + player, desktop+tablet smoke, no Task B generation).

## Files expected next (edit list)

### New (XAI-studio, owned here)

- `external_media_import/__init__.py`
- `external_media_import/__main__.py`
- `external_media_import/cli.py`
- `external_media_import/planner.py` (dry-run plan / conflicts / path guards)
- `external_media_import/apply.py` (copy, hash, provenance, atomic batch.yaml publish)
- `external_media_import/probe.py` (ffprobe wrapper used by package reports; Studio may share logic or re-probe)
- `external_media_import/README.md`
- `external_media_import/tests/**` + fixtures (3 images, 1 mp4, 1 webm)
- this `TASK.md`

### Studio (assigned by handoff — coordinate with Codex)

- `backend/app/importer.py`
- `backend/app/main.py` (playback + Asset field plumbing)
- `backend/app/schemas.py`
- `frontend/src/shared/types.ts`
- `frontend/src/shared/api.ts`
- `frontend/src/apps/gallery/**` (AssetCard, ImmersiveAssetViewer, model/tests as needed)
- `backend/tests/**` related fixtures

### Out of scope unless Codex expands

- `tools/**`, `control_tower/**`, root launchers, DB migrations, Task B generation
