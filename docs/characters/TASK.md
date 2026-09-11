# Jun and Rio DNA source sync

Active editor: Codex
Status: COMPLETE
Date: 2026-09-09

## Goal
Import the user-authored remote Jun and Rio DNA documents into the local production workspace.

## Constraints / Must Preserve
Preserve source text, candidate status, unresolved reference details, and all existing production changes.

## Must NOT Do
Do not invent identity details, approve references, generate media, or push private creative assets to the public remote.

## Plan and Progress
- Fast-forwarded D:/codex/XAI-Studio-Private to a9d4bbd2d9ae72641bea2e5539cc6822f2a1eef3.
- Copied docs/characters/jun.md and rio.md byte-for-byte into this workspace.
- Source: krchoi-X/XAI-Studio-Private, same paths and commit.
- Scope is original DNA document sync; no character.json conversion or Studio character registration performed.

## Next
The imported DNA documents are available locally. Canonical Character Manager registration remains a separate operation if needed.

## Blockers
None for document synchronization.

# Studio registration and OpenAI portraits — 2026-09-09
Active editor: Codex
Status: IN PROGRESS
Goal: Register ch-jun and ch-rio from imported DNA; generate five upper-body close-ups each using built-in OpenAI image generation and import/sync to Gallery.
Constraints: Preserve user-authored DNA, candidate status, all prior production records. Unspecified traits remain unresolved. No reference approvals or public publishing.
Scope: two canonical records and generated core/prompts, character index, ten images, importer manifests/session records, this task log.
Plan: Map existing user DNA to validated drafts; promote through Character Manager; generate one image per built-in call; inspect and import with exact prompts; sync and verify ten previews.
Progress: Source DNA and existing CLI/import contracts inspected. Use direct faithful source mapping for registration instead of asking a local LLM to redesign existing user-authored DNA.
Next: Register and generate.

## Completion — Studio registration and OpenAI portraits
Status: COMPLETE
- Registered ch-jun and ch-rio v1 as candidates through Character Manager save_draft/promote. All 11 canonical records pass validation; existing DNA hashes unchanged.
- Stable DNA hashes: Jun 1d0cf5d38778 (prefix), Rio 19c354bdc004 (prefix).
- Generated exactly 5 distinct 1024x1536 PNGs each with the ChatGPT built-in image tool. No API fallback or local renderer used.
- Each character's first generated portrait served as temporary runtime reference for its next four portraits; no canonical reference approval made. Rio earring side/shape remain unresolved in canonical DNA.
- Exact prompts and user wording: jun-closeups-manifest.json / rio-closeups-manifest.json; copied into importer provenance and per-file prompt records.
- Original images: D:/AI_Studio/library/characters/ch-jun/generations/GPT-20260909-jun-upper-body-closeups/outputs/gpt and equivalent ch-rio path.
- Sessions: GPT-20260909-jun-upper-body-closeups and GPT-20260909-rio-upper-body-closeups. Both completed, imported with needs_review initial state.
- POST /api/sync succeeded; GET character boards and assets report 5 images/1 session each. All 10 preview endpoints returned HTTP 200 with nonempty image data (gallery-verification.json).
- Gallery paths: /library/characters/ch-jun and /library/characters/ch-rio on the existing Studio server at http://127.0.0.1:8787.
Next: User can review/star/select preferred face candidates in the existing Gallery. No work remains for this request.
