# Character record contract

The machine-readable contract is `schemas/character-v1.schema.json`. The deterministic validator and renderer live in `tools/character_manager.py`.

Stable DNA includes adult age range, visual background, face, hair, skin, full-body proportions, body-hair continuity, distinctive marks, and recognition anchors. Its canonical JSON is SHA-256 hashed. A mismatch or unapproved replacement is identity drift.

Scene Delta includes pose, expression, outfit, camera, lens, lighting, location, action, and scene styling. Store it with a generation/scene record, never by mutating Stable DNA.

Status progression is `draft → candidate → approved`; `deprecated` preserves history. New local-LLM output starts as draft and promotion changes it to candidate. Only human review should mark a character or reference approved.

The app may cache records by ID and use `characters/index.json` for discovery. It must not treat a display name, file path, or database row as the canonical identity.
