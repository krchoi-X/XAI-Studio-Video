# Task: Gallery-integrated Character Compiler

## Why this task exists
The user wants character creation to stop being a long manual preparation loop. Once the user defines a character and explicitly approves one face as the **Master Face**, the Studio should automatically build the reusable identity references needed for later image/video production.

The inspiration is the staged ShoeCatch canvas pattern (reference → face → makeup/hair → comp card → outfit → editorial), but this Studio needs a stronger **persistent fictional identity** layer.

## Product decision
This belongs in the existing **Gallery / Character Manager** experience rather than becoming another standalone tool or repository.

Human decisions should be concentrated at two gates:
1. **Master Face approval** — user selects “this is the character”.
2. **Master Character Pack approval** — user checks the automatically generated identity pack before it becomes canonical.

Everything between those gates should be automatable.

## Proposed pipeline
```text
Character idea / existing Character DNA
        ↓
Character DNA + Face DNA + Skin Baseline
        ↓
candidate faces
        ↓
[HUMAN GATE 1] Master Face approved
        ↓
neutralized master reference
        ↓
multi-angle face generation
  front / left 30 / right 30 / left profile / right profile
        ↓
identity QA + candidate ranking
        ↓
body references
  front / 3/4 / side / back
        ↓
identity + proportion QA
        ↓
Master Character Sheet / Character Pack
        ↓
[HUMAN GATE 2] approve / reject individual views
        ↓
canonical Gallery character assets
```

## Canonical data separation
Do not collapse everything into one prompt.

- **Character DNA**: age, stature/proportions, overall presence, persistent non-face identity.
- **Face DNA**: facial geometry and relative landmarks.
- **Skin Baseline**: pores, microtexture, tonal variation, baseline complexion and physically plausible surface response.
- **Master Face**: visual identity anchor selected by the user.
- **Master Character Pack**: reviewed multi-view evidence.
- **Scene state**: hair, makeup, expression, outfit, pose, lighting, camera and environment. These remain variable and must not silently mutate canonical DNA.

A rendered “sheet” is a human-friendly view of the underlying references, not the only source asset.

## Suggested character asset shape
```text
characters/<character-id>/
  dna/
    character.md
    face.md
    skin.md
  master/
    face.png
  face/
    front.png
    left30.png
    right30.png
    left90.png
    right90.png
  body/
    front.png
    three-quarter.png
    side.png
    back.png
  sheets/
    face-sheet.png
    body-sheet.png
    master-sheet.png
  manifest.json
```

Adapt this to the repository's existing character schema rather than creating a parallel incompatible hierarchy.

## Gallery UX target
From an existing character card:
- show current Master Face;
- action such as **Build Character Pack**;
- generation progress by required view;
- thumbnails for candidates and selected references;
- identity/quality warning rather than silent promotion;
- approve/reject/regenerate per view;
- final **Approve Character Pack** action;
- subsequent scene generation can request the minimum appropriate references from this pack.

Do not require the user to hand-write prompts for every angle.

## Model/renderer strategy — deliberately unresolved
Do **not** hard-code the feature to Krea2, Qwen Image 2.1, or another model yet.

Build the workflow around an adapter contract so engines can be A/B tested. The current Qwen Image 2.1 identity pilot is directly relevant and should be reused rather than duplicated. Krea2 remains a candidate/baseline. Future ComfyUI identity adapters, FaceID/IP-Adapter-like approaches, or other edit/reference models may become better choices.

The first implementation should prove the workflow with whichever already-integrated renderer provides the best controllable reference-bound experiment. Record:
- identity preservation across angle;
- anatomy/proportion stability;
- skin/face beautification drift;
- latency;
- VRAM/runtime cost;
- manual rejection rate.

Model selection is an empirical decision made during implementation, not an architectural dependency.

## QA rules
- A generated view must never become canonical solely because generation succeeded.
- Automatic similarity scores may rank/filter candidates but are not the final authority.
- Reject obvious identity drift (eye geometry, brow-eye spacing, nose, mouth, jaw/chin, face length/width).
- Lighting and makeup may change surface appearance but must not be treated as permission to change anatomy.
- Avoid recursive derivation where a drifted generated angle becomes the sole parent for later views. Keep the approved Master Face / reviewed masters in the reference chain.
- Preserve provenance: renderer/model, workflow/adapter version, seed/settings where available, source master(s), generation timestamp and approval status.

## MVP
Use one existing character (Reika is a useful stress case) and implement:
1. Master Face input/selection from Gallery.
2. 5 face views.
3. Review UI with approve/reject/regenerate.
4. Master face sheet.
5. Persist reviewed assets + provenance.
6. Verify that downstream Gallery/character retrieval can use them.

Body views and automatic similarity ranking may follow immediately after the face MVP if the architecture supports them cleanly.

## Out of scope for first pass
- Character LoRA training by default.
- Automatic canonical promotion without human approval.
- Large hair/makeup/outfit variation libraries.
- Video generation.
- Making one renderer permanent before A/B evidence.
- New standalone repository or duplicated character database.

## Codex review / implementation request
Codex should first inspect the existing Gallery, Character Manager, character schema, reference-driven production pipeline, and the current Qwen Image 2.1 identity pilot. Then:
1. map this task onto the existing architecture;
2. identify the smallest Gallery integration point;
3. propose the renderer adapter interface and provenance fields;
4. implement the smallest end-to-end Master Face → reviewed multi-angle pack path;
5. add scoped verification;
6. update current priorities only according to the repository's one-active-P0 policy.

The key product principle is: **the user creates the character and chooses the face; the Studio compiles that decision into reusable identity evidence.**
