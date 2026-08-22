# Renderer Policy Separation

## Purpose

XAI-Studio should keep creative intent independent from the moderation behavior of any single hosted image or video provider.

The studio may use cloud services, local GPUs, or ephemeral self-hosted pods. Those execution targets can impose different technical and service constraints. The canonical story and character assets should not become permanently shaped by one provider's restrictions.

## Three constraint classes

### 1. Creative / production constraints

Examples:
- character identity
- continuity
- anatomy
- composition
- story state
- emotional tone
- camera behavior
- tempo
- lighting
- wardrobe / prop state

These belong in Character DNA, Storyboard Spec, Master Creative Spec, or other canonical production documents.

### 2. Technical constraints

Examples:
- supported resolution
- prompt length
- reference-image count
- unsupported input combinations
- VRAM limits
- duration limits
- model-specific negative-prompt behavior

These belong in the renderer/model adapter.

### 3. Hosted-provider policy constraints

These are service-specific execution rules imposed by a particular hosted product or API.

They belong only in that hosted provider's adapter or execution notes.

Do not rewrite the canonical story or Character DNA merely because one hosted provider cannot render it.

## Local / self-hosted default

For a locally controlled or self-hosted open-weight renderer, the adapter should compile the approved creative specification with minimum distortion.

Default behavior:

```text
approved creative spec
→ preserve creative intent
→ apply only required technical/model transformations
→ render locally
```

Do not silently copy cloud-provider moderation phrases, generic conservative negative prompts, or service-specific content restrictions into the local runtime prompt.

Negative prompts should exist because they fix generation failures such as:
- identity drift
- extra limbs
- background morphing
- unwanted beauty filtering
- excessive motion
- bad text

They should not become an implicit second policy system.

## Renderer routing

If one hosted renderer rejects or cannot execute an approved creative specification:

```text
Approved Spec
   ├─ Provider A: incompatible
   ├─ Provider B: compatible
   └─ Local / Pod renderer: compatible
```

Prefer changing the renderer before changing the underlying story.

This makes renderer choice an execution decision rather than a creative-authority decision.

## Adult-oriented projects

When a project is explicitly intended for adult audiences, keep project-level eligibility metadata separate from visual constraints.

Examples of metadata that may be useful in the project record:
- fictional / synthetic character status
- all depicted characters are adults
- rights / source provenance for reference assets
- consent or release information when real-person source material is involved

These records are project governance metadata. They should not automatically alter lighting, framing, expression, costume, story, or other creative fields unless the production itself requires it.

## Guiding principle

**Canonical creative assets describe what the work is. Adapters describe how a particular renderer can execute it. Provider policy must not silently become creative canon.**
