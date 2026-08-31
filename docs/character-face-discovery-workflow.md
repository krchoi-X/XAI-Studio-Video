# Character Face Discovery Workflow

Status: proposed / P0 input  
Updated: 2026-08-31

## Why this workflow exists

The current character-building process starts from written DNA, then generates full portraits and body references.

That approach exposed a practical failure mode:

- multiple characters were described differently in text,
- yet image models often converged on similar East Asian beauty priors,
- some outputs looked different, but it was unclear whether the difference came from prompt semantics, seed variation, or random sampling,
- the result was a growing set of characters that were conceptually distinct in text but insufficiently separated visually.

The problem is therefore not just character consistency.

It is **character separability**.

The system must first discover visually distinct faces, then build body, hair, styling, and video identity around the chosen face.

## New operating principle

Use a **face-first discovery pipeline**:

```
Face Discovery
→ Character Separation
→ Master Face Selection
→ Body / Hair / Style Expansion
→ Character Sheet
→ Video Reference Pack
```

Do not spend effort finalizing body DNA, outfit systems, or video prompts until a visually distinct face has been selected.

## Role of prompt vs seed

Treat seed as an experimental variable, not as character identity.

Recommended interpretation:

- Prompt: defines the broad facial / aesthetic region to explore.
- Seed: samples variation within that region.
- Reference image: becomes the actual visual anchor after selection.

When testing prompt changes, lock seed where supported.
When discovering candidate faces, vary seed broadly.
After a master face is selected, prioritize reference-based generation over seed reuse.

## Discovery batch design

Do not generate 100 near-identical images from one prompt.

Use multiple deliberately separated face directions.

Recommended initial batch per character:

- 4 face-direction prompts
- 8 images per direction
- 32 images per character

If diversity is insufficient, expand only the underexplored directions.

The goal is not maximum beauty.
The goal is:

1. memorability,
2. separability from existing characters,
3. realism,
4. reference usefulness,
5. potential for later full-body / video expansion.

## Shared generation constraints

For fair comparison, keep scene variables nearly constant:

- chest-up or shoulders-up framing
- bright white / warm-neutral background
- soft even studio light
- natural makeup
- simple dark hair
- no strong accessories
- neutral or faintly smiling expression
- 50–85mm portrait look where controllable

Hair signatures should be minimized during the first face-discovery pass.
Strong hairstyle anchors are added after the face is selected.

## Jung Hae-won discovery target

### Separation anchors

Jung Hae-won should read as:

- quiet
- restrained
- realistic
- introspective
- softly refined
- less sharp and less fashion-forward than Harim

### Face-direction prompts

#### HAEWON-A — Baseline

```text
Create a photorealistic face-exploration portrait of Jung Hae-won, a young adult Korean woman in her early 20s.

Jung Hae-won has a slightly elongated oval face, soft pale skin, calm dark-brown eyes, naturally shaped dark eyebrows, a delicate jawline, a refined but understated nose, and natural lips with restrained softness. Her beauty should feel believable, understated, and quietly memorable rather than glamorous.

Show a chest-up portrait in a minimal bright neutral studio with soft even lighting. Use a 50–85mm portrait-photography look. She has straight dark hair worn simply, natural makeup, and a calm neutral expression or a very faint restrained smile. Her gaze is direct or near-direct, but gentle and introspective.

This image is for face discovery. Emphasize a quiet, realistic, introspective identity. Avoid strong cat-like sharpness, exaggerated glamour, overly full lips, heavy makeup, doll-like skin, or influencer styling.
```

#### HAEWON-B — Softer / rounder

```text
Create a photorealistic face-exploration portrait of Jung Hae-won, a young adult Korean woman in her early 20s.

This variation should preserve her quiet, understated identity, but make her face slightly softer and gentler. Use a softly elongated oval face with mild cheek softness, calm dark-brown eyes, natural eyebrows, a modest straight nose, and soft natural lips. She should look realistic, gentle, and quietly attractive.

Use a chest-up portrait in a clean neutral studio with soft even lighting, minimal styling, natural makeup, and simple straight dark hair. Expression is neutral to faintly warm, never bright or performative.

Focus on subtle realism and emotional restraint. Avoid sharp feline features, strong glamour, excessive symmetry, plastic skin, or overly fashionable styling.
```

#### HAEWON-C — Longer / more refined

```text
Create a photorealistic face-exploration portrait of Jung Hae-won, a young adult Korean woman in her early 20s.

This variation should make her face slightly longer and more refined while preserving her quiet personality. Use a slightly elongated oval face, clean jawline, calm eyes, soft straight brows, understated nose, and restrained natural lips. She should look calm, thoughtful, and a little more elegant, but never cold or severe.

Show a chest-up portrait in a bright neutral studio under soft artificial lighting. Keep styling minimal, hair simple, expression calm, and proportions realistic.

Avoid sharp cat-like intensity, dramatic cheek contouring, glamorous makeup, doll-like perfection, or celebrity-like stylization.
```

#### HAEWON-D — More memorable but still restrained

```text
Create a photorealistic face-exploration portrait of Jung Hae-won, a young adult Korean woman in her early 20s.

This variation should keep her understated identity but slightly increase facial memorability. Use a slightly elongated oval face, clearer eyebrow definition, calm dark-brown eyes, a refined straight nose, softly defined lips, and a delicate but readable jawline. She should still look realistic and reserved, not flashy.

Use a chest-up studio portrait with a clean bright background, soft even lighting, natural skin texture, simple straight dark hair, and minimal makeup. Expression should be restrained and composed.

Avoid making her glamorous, seductive, strongly feline, or aggressively fashion-oriented.
```

## Harim discovery target

### Separation anchors

Harim should read as:

- cool
- chic
- slightly cat-like
- visually cleaner and sharper than Hae-won
- small-face impression
- stronger eyebrow / eye-shape recognition
- more urban and slightly aloof

### Face-direction prompts

#### HARIM-A — Baseline

```text
Create a photorealistic face-exploration portrait of Harim, a young adult Korean woman in her early 20s.

Harim has a small slightly elongated oval face, defined dark eyebrows, almond-shaped dark-brown eyes with subtly upturned outer corners, a refined straight nose, a small mouth with softly full lips, and a slim clean jawline. Her beauty should feel cool, elegant, realistic, and slightly cat-like, with a calm and quietly striking presence.

Show a chest-up portrait in a minimal bright neutral studio with soft even lighting. Use a 50–85mm portrait-photography look. Keep styling simple: natural makeup, near-black straight hair, no strong accessories, and a neutral or very faint restrained smile. Her gaze should be direct or near-direct, calm and a little aloof.

This image is for face discovery. Emphasize a chic, memorable face that is distinct from softer and more introspective characters. Avoid exaggerated glamour, overly sharp feline styling, influencer makeup, plastic skin, or doll-like proportions.
```

#### HARIM-B — Eye / eyebrow emphasis

```text
Create a photorealistic face-exploration portrait of Harim, a young adult Korean woman in her early 20s.

This variation should emphasize Harim’s eye area more strongly while preserving realism. Use defined dark eyebrows, almond-shaped eyes with subtly raised outer corners, and a calm, chic, slightly cool expression. Her face is small and slightly elongated, with a refined straight nose, a small mouth, softly full lips, and a clean jawline.

Use a chest-up portrait in a bright neutral studio with soft even lighting, natural skin texture, minimal styling, and simple near-black hair. Makeup remains natural and restrained.

Avoid heavy eyeliner glamour, extreme cat-eye sharpness, exaggerated sexiness, doll-like skin, or overly large eyes.
```

#### HARIM-C — Stronger nose / jaw structure

```text
Create a photorealistic face-exploration portrait of Harim, a young adult Korean woman in her early 20s.

This variation should make Harim slightly more structured and refined. Use a small elongated face, clearly shaped dark eyebrows, slightly upturned almond eyes, a refined straight nose with a clear bridge, a small mouth with softly full lips, and a slim sharp-clean jawline. She should look elegant, cool, and stylish, but still believable.

Show a chest-up studio portrait with a soft bright neutral background, even lighting, and realistic skin texture. Keep hair simple, makeup light, and the expression neutral to faintly restrained.

Avoid over-glamorization, harsh contouring, celebrity imitation, or overly angular unnatural facial structure.
```

#### HARIM-D — Softer Harim

```text
Create a photorealistic face-exploration portrait of Harim, a young adult Korean woman in her early 20s.

This variation should preserve Harim’s slightly cat-like identity but soften it a little. Use defined brows, almond-shaped eyes with only a subtle upward tilt, a refined nose, a small mouth, softly full lips, and a clean feminine jawline. Her face remains small and slightly elongated, and her expression is calm, cool, and quietly elegant rather than severe.

Use a chest-up portrait in a clean bright studio under soft lighting. Keep styling minimal and realistic, with near-black straight hair and natural makeup.

Avoid making her too cute, too round-faced, too glamorous, or too similar to a gentle introspective type.
```

## Review taxonomy

The web app should support at least these face-discovery states:

- `face-exploration`
- `face-candidate`
- `master-face`
- `alternate-face`
- `rejected-overlap`

Recommended evaluation fields:

- separation
- memorability
- realism
- expandability
- stability_guess
- reviewer_note

The most important field is **separation**.

A beautiful face that overlaps too strongly with an existing character should be rejected.

## Hermes execution target

This workflow is intended to be executed through **Hermes + local LLM**.

Codex should not be used repeatedly to generate face prompts or manually create batches.

Codex should instead make Hermes able to run this workflow reliably.

### Local image engines

Initial execution targets:

- local Krea installation
- local Z-Image installation

Hermes should be able to:

1. read the current character DNA and face-discovery definitions,
2. select a discovery prompt,
3. submit batch generation to the requested local engine,
4. generate the requested count,
5. save outputs into the correct character/session folder,
6. record prompt, model/engine, seed if available, timestamp, and face-direction ID,
7. register outputs so the web app can review them,
8. preserve existing character files,
9. report the generated batch.

### Suggested session structure

```
characters/<character>/02_generations/
  YYYY-MM-DD_face-discovery_<engine>_<direction>/
    prompt.md
    metadata.json
    review.md
    images/
```

### Suggested metadata

```json
{
  "character": "harim",
  "character_version": "0.2",
  "phase": "face-discovery",
  "direction": "HARIM-B",
  "engine": "z-image",
  "count": 8,
  "seeds": [],
  "status": "unreviewed"
}
```

## Codex responsibility

Codex owns the control plane.

Codex should:

- inspect how the local Krea and Z-Image installations are invoked,
- expose those execution paths to Hermes safely,
- create or refine a Hermes skill / command for face discovery,
- ensure batch outputs are written into the canonical character structure,
- ensure metadata is generated consistently,
- ensure the web app can ingest the generated batch,
- avoid spending Codex credit on repetitive image-generation orchestration.

A successful end state is that the operator can issue a simple Hermes request such as:

```
하림 HARIM-B 얼굴 탐색을 Z-Image로 8장 생성해.
```

and Hermes performs the full generation + storage + registration workflow under Codex-defined rules.

## Decision rationale for Codex

This workflow is being introduced because text-first character DNA alone did not create sufficient visual separation between multiple characters.

The system therefore changes from:

```
Text DNA first
→ generate full character
→ hope identities separate
```

to:

```
structured face exploration
→ human selection
→ master visual anchor
→ body/hair/style expansion
→ character sheet
→ video
```

This is an intentional architectural change, not a temporary prompt experiment.

The purpose is to reduce wasted generation, reduce character overlap, improve later image/video consistency, and move repetitive generation work from Codex to Hermes + local inference.
