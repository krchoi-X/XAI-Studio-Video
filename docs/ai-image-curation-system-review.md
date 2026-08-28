# AI Image Curation System Review

Updated: 2026-08-28

Status: `DEFERRED — REVIEW BEFORE IMPLEMENTATION`

This note records the product direction reached after testing Eagle and
FrameWire against the Jung Hae-won image-review workflow. It is a decision
record, not approval to begin implementation today.

## Problem

Increasing image-generation volume creates a creative-memory bottleneck:

```text
generate many images
→ forget which faces and compositions worked
→ lose the prompt, model, seed, and source-image relationship
→ repeat experiments
→ struggle to assemble character masters and LoRA datasets
```

The desired system must support three distinct kinds of work:

1. rapidly reducing hundreds or thousands of outputs to a small candidate set
2. studying those candidates and using their lineage to make better images
3. preserving approved assets for later video, comic, LoRA, and other projects

Trying to put all three activities into one dense asset-management screen makes
the first task too slow and the later tasks too shallow.

## Evidence from tool tests

### Eagle

Strengths observed:

- excellent thumbnail browsing and folder navigation
- tags, notes, ratings, filters, and smart-library concepts
- suitable as a general visual asset manager

Limitations observed with the actual test images:

- Chroma exposed a readable prompt through `ImageDescription`.
- Some JPEG files exposed only `[Unicode encoded text]` in `UserComment`.
- GPT Image, Grok, Krea, z-image, and other web-model outputs did not produce a
  unified prompt/model/seed view.
- Stable Diffusion metadata plugins are mainly designed around A1111 and
  ComfyUI conventions.
- EXIF plugins show raw camera/file metadata but do not normalize AI-generation
  lineage.
- Rating and note workflows were less discoverable than a phone-gallery
  interaction model.

Decision: do not purchase or adopt Eagle on the assumption that existing
plugins solve heterogeneous AI metadata. Eagle remains a possible general
library, but it is not the core solution demonstrated by this test.

### FrameWire

Strengths observed:

- local-first folder access in the inspected version
- visual placement of references, prompts, scenes, notes, and relationships
- useful for planning with a small, already selected set of assets

Limitations observed:

- not optimized for rapidly reviewing hundreds of images
- no native rating/triage workflow
- no automatic normalization of prompt/model/seed metadata
- canvas placement adds friction during first-pass selection

Decision: FrameWire is a planning-board reference, not the primary review or
curation application.

### FrameWire privacy inspection

The inspected version did not contain `fetch`, `XMLHttpRequest`, beacon,
WebSocket, analytics, Firebase, Supabase, or similar upload code. It used local
folder read access, IndexedDB, and localStorage. Normal web requests still go to
Netlify when the page loads, and a future deployed version could change.

If FrameWire is used later, connect only a dedicated folder containing copies,
not a broad archive or production root.

## Product direction

The desired experience is closer to a custom Google Photos or Samsung Gallery
than to a traditional DAM or node canvas.

Use one local system with three purpose-specific surfaces:

```text
generation output folders
        ↓
1. REVIEW — fast touch-first triage
        ↓
2. WORKBENCH — analysis, lineage, and improvement
        ↓
3. LIBRARY — approved durable assets
        ↓
video / comic / LoRA / project exports
```

These should initially be three routes or modes backed by one database, not
three unrelated programs that copy files between themselves.

Suggested routes:

```text
/review
/workbench
/library
```

## Stage 1 — Review

Goal: decide whether an image deserves more attention without forcing detailed
metadata entry.

Primary device: Galaxy phone or tablet on the local network.

Core interaction:

- swipe left/right: previous or next image
- pinch/double-tap: inspect face, eyes, hands, skin, and artifacts
- swipe up or a large positive gesture: shortlist
- swipe down or a large negative gesture: reject
- star: favorite/master potential
- hold: multi-select
- undo the last decision
- optionally compare two to four images
- hide controls for an unobstructed full-screen view

Minimal states:

```text
NEW → SHORTLISTED
   ↘ HOLD
   ↘ REJECTED
```

Prompt editing, detailed tagging, and long comments should not interrupt this
stage.

## Stage 2 — Workbench

Goal: understand why shortlisted images work, preserve how they were made, and
turn that knowledge into the next generation.

Capabilities:

- show only shortlisted images
- compare two or four candidates
- normalized prompt/model/seed/generator metadata
- retain raw metadata beside normalized fields
- clearly show `not provided` instead of inventing missing values
- copy and revise prompts
- comments and structured review dimensions
- mark Face Master, Base Image, Body Master, Outfit Master, or LoRA Candidate
- link reference, source, derivative, and variant images
- build the next generation recipe from selected assets
- show later results beside their parents

Required lineage relationships include:

```text
derived_from
variation_of
used_as_reference
trained_in_lora
generated_with_lora
used_in_project
```

This lineage is more important than storing prompt text alone. It must answer:

- Which source image produced this result?
- Which prompt/model/settings were used?
- Which successful result became a new character master?
- Which images trained a specific LoRA version?
- Which later images were generated with that LoRA?

## Stage 3 — Library

Goal: preserve only approved, reusable assets and expose them to later
production work.

Example organization:

```text
Jung Hae-won
├─ Character Masters
│  ├─ Face
│  ├─ Body
│  ├─ Hairstyle
│  └─ Expressions
├─ LoRA
│  ├─ Training v1
│  ├─ Training v2
│  └─ Test Results
├─ Outfits
├─ Locations
├─ Comic Assets
└─ Video Assets
```

Approved assets should retain:

- character and asset role
- approval and rating state
- prompt, model, seed, generator, and creation time when available
- source and derivative relationships
- LoRA version and dataset membership
- projects in which the asset was used
- provenance and usage-right notes

Downstream export should copy only deliberately selected files and include a
machine-readable manifest so video, comic, and LoRA workflows do not lose
context.

## Reuse versus custom implementation

### Reuse open-source components

- PhotoSwipe or a comparable permissive touch viewer for pan, pinch zoom, and
  image navigation
- libvips/Sharp for thumbnails and image transforms
- a virtualized grid component for large libraries
- ExifTool for EXIF, XMP, IPTC, PNG text chunks, JPEG comments, dimensions, and
  general file metadata
- SQLite for local durable state
- existing local web/PWA, authentication, and API libraries
- filesystem watchers and hashing libraries for indexing and deduplication
- AI Toolkit, OneTrainer, or another existing trainer for LoRA execution

### Build directly

- Samsung Gallery/Google Photos-inspired review gestures and decision flow
- review state machine and undo history
- generator-specific metadata adapters for Chroma, GPT Image, Grok, Krea,
  z-image, ComfyUI, A1111, and future sources
- canonical AI-generation metadata schema
- comparison and structured critique workbench
- image lineage and generation-recipe graph
- Base Image, Character Master, and LoRA Candidate workflows
- LoRA dataset validation, captions, manifests, and exports
- downstream video/comic project export manifests

### Use existing applications selectively

- Immich: candidate for the final approved library, mobile browsing, external
  read-only libraries, search, albums, API, and XMP integration; do not fork it
  as the initial review/workbench implementation without a new comparison.
- Aves and Fossify Gallery: interaction references for Android gallery UX; not
  the shared PC/tablet database foundation.
- PiGallery2: possible reference for lightweight read-only folder browsing.
- FrameWire: possible reference for visual lineage/planning with a small set.
- Eagle: optional general asset manager only if its independent library
  strengths justify purchase; do not depend on current plugins for cross-model
  AI metadata.

## Proposed technical shape

```text
Windows PC
├─ original output folders (read-only to the application)
├─ indexer and thumbnail cache
├─ generator metadata adapters
├─ SQLite creative-memory database
├─ local API and PWA server
└─ explicit export folders
        ↑
        │ local Wi-Fi only by default
        ↓
Galaxy phone / tablet
├─ /review
├─ /workbench
└─ /library
```

Do not store image binaries in SQLite. Store stable asset IDs, hashes, paths,
metadata, decisions, relationships, and export history. Preserve originals and
write derived records to the local database or sidecars.

## Privacy and safety requirements

- no outbound image or metadata transfer by default
- original folders mounted or opened read-only
- local-network access only unless the user explicitly enables remote access
- explicit device enrollment or authentication
- delete in the UI means a reversible review state unless the user explicitly
  requests filesystem deletion
- local thumbnail and metadata processing
- external AI analysis disabled by default and separately authorized
- visible audit history for export, metadata edits, and dataset membership

## Implementation order when resumed

1. Re-evaluate current open-source candidates and licenses before adoption.
2. Define the canonical asset, review-state, metadata, and lineage schemas.
3. Index one existing Jung Hae-won output folder read-only.
4. Build thumbnails and the touch-first `/review` route.
5. Validate the workflow on an actual Galaxy tablet.
6. Add undo, shortlist, hold, reject, and favorite states.
7. Implement metadata adapters against the known test set.
8. Build comparison, comments, and role assignment in `/workbench`.
9. Add lineage and generation-recipe records.
10. Add LoRA dataset validation and manifest export.
11. Decide whether `/library` remains native or exports approved assets to
    Immich.
12. Add video and comic project handoff manifests.

## Deferred decisions

Revisit these before implementation:

- custom lightweight PWA versus adapting a small permissive gallery codebase
- whether Immich should be only a final library or also provide selected APIs
- exact canonical storage: SQLite-only metadata versus SQLite plus JSON/XMP
  sidecars
- gesture vocabulary after testing on a Galaxy tablet
- how to recover generation lineage when source services omit metadata
- whether local semantic similarity is needed in the first release

## Current decision

Do not implement today. Preserve this document as the basis for a later review.

When work resumes, begin with the schema and a minimal touch-first review
prototype. Do not start by forking Immich, purchasing Eagle, or extending
FrameWire. The primary product value is the combination of effortless triage,
heterogeneous AI metadata normalization, and durable creative lineage.
