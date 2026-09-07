# external_media_import

Import external images (PNG/JPEG/WebP) and videos (MP4/WebM) into the Studio library and generation-record layout used by `import_batch` / `POST /api/sync`.

This package **copies** originals (never deletes or overwrites sources), preserves SHA-256 and prompts in provenance, defaults review to `needs_review`, and publishes `batch.yaml` **atomically last** after all copies succeed.

Studio Gallery video playback is a **separate phase** — this package only prepares on-disk contracts.

## Install / run

No install required. From `D:\codex\XAI-studio`:

```powershell
cd D:\codex\XAI-studio
python -m external_media_import --help
```

Requires: Python 3.11+, Pillow, `ffprobe` on PATH (for video). Optional: Studio running for `--sync-url`.

## Default ops paths

| Role | Default |
|---|---|
| library-root | `D:\AI_Studio\library\characters` |
| record-root | `D:\codex\XAI-studio\characters\<character-id>\02_generations` |

Output layout:

```text
<record-root>/<session-id>/
  batch.yaml                 # published LAST
  prompt.txt
  import-provenance.json

<library-root>/<character-id>/generations/<session-id>/outputs/<engine>/
  <files>
```

Studio treats the first path element under `outputs/` as `engine` (e.g. `gpt`, `krea2`, `z-image`).

## Manifest shape

JSON object with `items` (also accepts `images` / `files` / `media`):

```json
{
  "engine": "gpt",
  "provider": "OpenAI",
  "model": "GPT built-in image generation",
  "items": [
    {
      "file": "shot-01.png",
      "source": "D:\\inbox\\shot-01.png",
      "prompt": "exact prompt text",
      "references": ["D:\\refs\\face.png"],
      "user_request": "optional user wording",
      "created_at": "2026-09-06T12:00:00+09:00",
      "engine": "gpt",
      "provider": "OpenAI",
      "model": "optional-override"
    }
  ]
}
```

Relative `source` / `file` values resolve under `--source-dir` / `--allowed-source-root`. Paths escaping allowed roots (`..`, absolute outside, symlink escape) are rejected.

When items have **different prompts**, the tool does **not** invent one fake session prompt. It writes file-tagged sections into `prompt.txt` and keeps full per-item prompts in `import-provenance.json` (`prompt_strategy=provenance`). Prefer separate `--session-id` runs when you want item-level sessions.

Visibility comes from `--visibility` / input only — never lifted based on engine name. Review defaults to `needs_review` (no invented favorites / star / base-face approval).

## Commands

### dry-run / plan (default safe mode)

Reports missing / invalid / path_rejected / duplicate / conflict / planned copies. **Writes nothing.**

```powershell
cd D:\codex\XAI-studio

python -m external_media_import dry-run `
  --manifest D:\codex\XAI-studio\external_media_import\tests\fixtures\manifest.json `
  --source-dir D:\codex\XAI-studio\external_media_import\tests\fixtures `
  --allowed-source-root D:\codex\XAI-studio\external_media_import\tests\fixtures `
  --character-id ch-mizuki-reika `
  --session-id IMPORT-20260907-fixture-dry `
  --title "Fixture dry-run (do not apply to live gallery)" `
  --engine gpt `
  --provider OpenAI `
  --model fixture-model `
  --library-root D:\AI_Studio\library\characters `
  --record-root D:\codex\XAI-studio\characters\ch-mizuki-reika\02_generations `
  --visibility standard
```

`plan` is an alias for `dry-run`. Add `--json` for machine-readable output.

### apply

Copies originals into the library tree, writes `prompt.txt` + `import-provenance.json`, then publishes `batch.yaml` last. Same batch + file + hash = no-op. Same dest name + different hash = **conflict** (no silent overwrite).

```powershell
# Example against a disposable test character folder (recommended first):
python -m external_media_import apply `
  --manifest D:\codex\XAI-studio\external_media_import\tests\fixtures\manifest.json `
  --source-dir D:\codex\XAI-studio\external_media_import\tests\fixtures `
  --allowed-source-root D:\codex\XAI-studio\external_media_import\tests\fixtures `
  --character-id ch-import-fixture `
  --session-id IMPORT-20260907-fixture-apply `
  --title "Fixture apply" `
  --engine gpt `
  --library-root D:\AI_Studio\library\characters `
  --record-root D:\codex\XAI-studio\characters\ch-import-fixture\02_generations `
  --visibility standard
```

Optional Studio sync after a successful publish:

```powershell
python -m external_media_import apply ... --sync-url http://127.0.0.1:8787/api/sync
```

Exit codes:

| Code | Meaning |
|---|---|
| 0 | OK |
| 1 | dry-run found blockers |
| 2 | plan/validation blockers (apply refused) |
| 3 | copy failure (batch.yaml not published) |
| 4 | sync-only refused (copies incomplete) |
| 5 | **sync failure** after successful copies — retry sync-only |

### resume

Same as `apply`: unfinished copies continue; hash-equal destinations are no-ops. Does not re-copy identical content.

```powershell
python -m external_media_import resume `
  --manifest D:\codex\XAI-studio\external_media_import\tests\fixtures\manifest.json `
  --source-dir D:\codex\XAI-studio\external_media_import\tests\fixtures `
  --allowed-source-root D:\codex\XAI-studio\external_media_import\tests\fixtures `
  --character-id ch-import-fixture `
  --session-id IMPORT-20260907-fixture-apply `
  --title "Fixture apply" `
  --engine gpt `
  --library-root D:\AI_Studio\library\characters `
  --record-root D:\codex\XAI-studio\characters\ch-import-fixture\02_generations
```

### sync-only retry

When copies + `batch.yaml` already succeeded but Studio sync failed:

```powershell
python -m external_media_import apply `
  --sync-only `
  --sync-url http://127.0.0.1:8787/api/sync `
  --manifest D:\codex\XAI-studio\external_media_import\tests\fixtures\manifest.json `
  --allowed-source-root D:\codex\XAI-studio\external_media_import\tests\fixtures `
  --character-id ch-import-fixture `
  --session-id IMPORT-20260907-fixture-apply `
  --title "Fixture apply" `
  --engine gpt `
  --library-root D:\AI_Studio\library\characters `
  --record-root D:\codex\XAI-studio\characters\ch-import-fixture\02_generations
```

Sync-only refuses to run if hashes are not already present (will not re-copy).

## Source folder without manifest

```powershell
python -m external_media_import dry-run `
  --source-dir D:\inbox\reika-batch `
  --allowed-source-root D:\inbox\reika-batch `
  --character-id ch-mizuki-reika `
  --session-id GPT-20260907-inbox `
  --title "Inbox import" `
  --engine gpt `
  --prompt-file D:\inbox\reika-batch\prompt.txt
```

## Tests

```powershell
cd D:\codex\XAI-studio
python -m pytest external_media_import/tests -q
```

Fixtures under `tests/fixtures/` include tiny PNG/JPEG/WebP plus silent MP4/WebM. Unit tests mock missing `ffprobe` where needed.

## Notes for Studio phase

- Package-side video thumbnails are **not** written into the Studio preview cache here (Studio importer owns preview generation).
- Current Studio `MEDIA_TYPES` is image-only — video files land on disk but will be skipped by today's `import_batch` until the Studio phase extends probe/playback.
- Do not feed video into image-only reference/variation paths.
