# Production Capability Registry

> Snapshot date: 2026-09-16
>
> This file is a directing aid, not the canonical source for model installation state. Verify the current repo/runtime before execution. Update this file only when a capability is reliably available or materially constrained in actual production.

## Purpose

A good storyboard should be imaginative **and executable**. Directors should know what tools can currently support the idea, but they must not turn current tool limits into permanent aesthetic rules.

## Current production orientation

### WanGP

Role:
- primary local video-generation interface;
- preferred over hand-building ComfyUI graphs for routine production;
- renderer entry point for available video model modes.

Directing implications:
- storyboard candidates should identify whether a shot is best attempted as direct generation, I2V/reference-driven generation, control/motion-driven generation, or a separately generated clip;
- do not assume every backend mode exists merely because H3 or another model theoretically supports it; verify current WanGP model types and adapters before execution;
- when a shot depends on a specific movement, consult available motion/reference assets instead of relying only on prose.

Canonical runtime/model details:
- `docs/wangp-models.md`
- `docs/wangp-recorder.md`
- current adapters/runtime state

### MiniMax H3 family

Role:
- important character/video renderer for reference-driven and controlled motion workflows;
- useful for short clips, reference-based identity, control/motion experiments, and chained/continued production where supported by the active runtime.

Directing implications:
- preserve explicit spatial anchors and continuity handoffs;
- distinguish a still/reference anchor from the storyboard itself: the reference protects appearance/state, while the storyboard owns shot order, action, reveal logic, camera behavior, and handoff;
- avoid placing too many unrelated actions into one clip merely because a model can generate several seconds;
- when continuity risk rises, consider splitting the action and using a deliberate handoff anchor.

Before execution, verify:
- active H3 mode in WanGP;
- reference limits and supported input types;
- control/motion availability;
- current licensing/usage constraints for the actual deployment context.

### Krea 2 / local image generation

Role:
- current high-value source for realistic stills, first frames, visual exploration, and character/environment plates where the active local setup supports it.

Directing implications:
- use still generation when framing, subject scale, environment layout, wardrobe, or opening reveal is uncertain;
- prefer generating a small set of purposeful storyboard frames over a large pile of near-duplicates;
- a still is a composition decision, not proof that the resulting video motion will work.

### Character references / canonical identity

Role:
- identity should come from the maintained Character Manager/shared character source, not from an improvised prompt copied from an old conversation.

Directing implications:
- do not modify Character DNA to solve a one-off shot problem;
- state which reference is identity authority and which references are pose/composition/style/motion aids;
- if identity and directing requirements conflict, surface the trade-off rather than silently weakening identity.

Canonical source:
- shared Character Manager resolver and `skills/character-manager/SKILL.md` entrypoint.

### Motion/reference asset library

Role:
- reusable movement, pose, blocking, and camera-motion references for shots where prose alone is unreliable.

Current maturity:
- architecture/reference workflow exists or is planned; availability of indexed assets must be checked before relying on it.

Directing implications:
- specify the desired motion semantically (`walk into frame and sit`, `casual turn`, `dance phrase`, etc.);
- do not hard-code local absolute paths into storyboard memory;
- if no suitable motion reference exists, label the shot as prose-driven or propose a lower-risk construction.

### Upscaling / finishing

Role:
- final-master finishing after the underlying shot is approved.

Directing implication:
- never design around the hope that upscaling will rescue bad identity, composition, anatomy, or motion;
- upscale approved material, not rejected candidates.

## Capability decision checklist

For each candidate storyboard, answer briefly:

1. **Identity source** — what canonical reference protects the character?
2. **Composition source** — direct prompt, still board, or existing reference?
3. **Motion source** — prose only, motion reference, control video, or continuation?
4. **Clip structure** — one long take, multiple independent clips, or hybrid?
5. **Continuity handoff** — how is state preserved between clips?
6. **Audio** — generated with video, separate dialogue/TTS, ambience, or none?
7. **Risk** — what is most likely to fail?
8. **Fallback** — how can the same directing idea be simplified without losing its point?

## Rule for new tools

Do not add a newly discovered model/tool to the active production path merely because it looks promising.

Default sequence:

```text
public research / watch note
→ small isolated test
→ proven useful capability
→ registry update
→ production use
```

This protects the directing layer from constantly moving infrastructure targets.
