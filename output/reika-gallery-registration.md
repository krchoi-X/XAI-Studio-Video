# Reika gallery registration — 2026-09-06

Completed by Codex at user request. Existing Studio batch import contract was reused; no application code or schema changes.

- GPT base candidates: 10 images.
- GPT face 06 / 09: editorial 3 and smile 3 each, 12 images.
- Existing Krea2 and Z-Image sessions: 5 images each, retained unchanged.
- Added five GPT session records under characters/ch-mizuki-reika/02_generations/GPT-20260906-*.
- GPT media copied non-destructively into D:/AI_Studio/library/characters/ch-mizuki-reika/generations.
- Source paths, content hashes, prompts and reference-image paths retained in import-provenance.json beside each batch.yaml.
- /api/sync imported 22 images; repeated sync imported 0.
- Character asset API returns gpt=22, krea2=5, z-image=5; all 32 preview GET requests return HTTP 200.
- Gallery: http://127.0.0.1:8787/library/characters/ch-mizuki-reika
- Existing restricted visibility of local engine sessions is preserved. Use the existing restricted-media toggle to show them.

Repeat registration with output/register-reika-gpt-gallery.py, then POST /api/sync. Candidate approvals and favorites remain user-controlled.
