# Changelog

## 0.3.0-draft — 2026-08-22

Promoted storyboarding from a video-specific reference trick into a medium-neutral creative intermediate representation.

### Added

- `skills/storyboard-director/SKILL.md` expanded into a medium-neutral directing skill
- `docs/storyboard-directing.md` rewritten around Storyboard Spec as the source of truth
- `docs/storyboard-rendering.md`
- `templates/storyboard-draft.md` expanded for video / graphic novel / comic / illustration-sequence targets
- Narrative Tempo Map separated from literal video duration
- attention-hold semantics: brief / normal / extended / dominant
- target-medium tempo translation:
  - video → duration, cut rhythm, slow motion, camera speed, silence/audio density
  - graphic novel/comic → panel size, panel density, silent panels, page turns, dialogue density, negative space
  - illustration sequence → ordering, focal hierarchy, hero-frame selection, visual pauses
- renderer-independent Storyboard Spec
- rough storyboard treated as disposable low-cost previsualization
- Storyboard Renderer Adapter concept
- separation of rough-board renderer and final high-quality renderer
- explicit local / ephemeral GPU pod / cloud renderer roles
- panel-by-panel high-quality rendering workflow for graphic novels and illustration sequences
- explicit rule that character identity should come from Character DNA / character references rather than from low-quality storyboard faces

### Design decisions

- Storyboarding is now a reusable **story / tempo / composition / emotion / continuity IR**, not merely an H3 input image.
- The rough storyboard image is not canonical; structured Storyboard Spec data is canonical.
- Storyboard design should begin with directorial interpretation, then Beat Sheet, Narrative Tempo Map, panel/shot specs, and user revision.
- The AI proposes `Draft 0`; the user remains the final director.
- Narrative tempo exists above the output medium and should be translated rather than discarded when moving between video and sequential static art.
- Cheap storyboard images should be used to decide expensive final images/video.
- Final rendering must remain replaceable across cloud services, local open-weight models, and ephemeral high-end GPU pods.
- Provider-specific prompt syntax, policy behavior, and aesthetics belong in adapters rather than canonical creative specs.
- Final panel/shot rendering should not re-search story decisions already approved in the storyboard stage.

### MiniMax H3 relevance

- MiniMax H3 remains an especially useful downstream video target because its official architecture supports text/image/video/audio context and H3-Context-IR performs instruction parsing, cross-modal association, temporal understanding, and complex logical reasoning.
- For H3 handoff, Character Reference, Storyboard Reference, and text timing/continuity responsibilities should be explicitly separated.
- Storyboard images should provide visual sequence/framing/blocking guidance while the approved Storyboard Spec carries timing, emotional emphasis, dialogue, continuity, and reference-role semantics.

### Learning / compute strategy

- Prefer story, storyboard, and image-design practice over repeated long video-generation search when video iteration is expensive.
- Use local LLMs as Assistant Directors for Draft 0 when adequate; use stronger cloud or pod LLMs for difficult interpretation, critique, or revision.
- Use low-cost/low-quality image generation for storyboard exploration and reserve high-quality image/video generation for approved survivors.

### Next candidates

- MiniMax H3 storyboard adapter
- renderer adapter examples for local / pod / cloud image models
- graphic-novel page-layout adapter
- character discovery vlog template using storyboard-first planning
- production-state-machine / approval-rate metrics
- action primitives derived only after repeated generation tests
- primitive metadata/schema format
- prompt/result experiment log
- identity consistency evaluation rubric

## 0.2.0-draft — 2026-08-22

Expanded the studio from motion control alone toward evidence-first reference analysis, bounded creative freedom, and reusable action-production grammar.

### Added

- Visual Responsibility model for assigning each prompt section a clear control role
- Action Skeleton as a causal action description before exact pose choreography
- Control Levels:
  - Hard Lock
  - Soft Guidance
  - Creative Freedom
- Controlled Randomness principle: lock direction and invariants without freezing low-risk micro-detail
- Evidence-first reference extraction
- Observation vs inference separation
- Reference State structure for pose, gaze, framing, lighting, spatial blocking, materials, and movable elements
- `docs/reference-extraction.md`
- Series Master → Variant workflow for expanding unusually successful results into reusable character/scene assets
- Entry-state / exit-state emphasis in Shot Graph
- accepted-work preservation and responsibility-layer debugging in architecture/template
- Series Master and approved-clip fields in the Master Creative Spec result log
- `docs/action-design.md`
- Action Grammar for connected combat/chase/sports/panic/dance motion rather than adjective-only prompting
- multi-agent interaction rules for simultaneous motion, spatial accountability, momentum, and avoiding artificial turn-taking
- Physics Lock structure:
  - Source / cause
  - Allowed manifestation
  - Forbidden manifestation
  - World reaction
- Reaction Evidence for proving force through dust, debris, clothing, hair, props, light, and camera response
- motivated Camera Imperfection: tracking lag, overshoot, whip-pan reacquisition, focus recovery, and impact-linked shake
- emotional continuity through spectacle
- optional micro-slow-motion emphasis as a localized readability tool
- action-specific evaluation fields in the Master Creative Spec

### Design decisions

- A prompt should be debuggable by responsibility layer rather than rewritten as one undifferentiated prose block.
- Exact pose choreography is optional; use an Action Skeleton unless contact geometry or silhouette truly requires precision.
- Generative randomness is not inherently a defect. Preserve bounded freedom where it can add natural variation.
- Reference reverse-engineering should describe visible effects and relationships, not invent exact equipment or hidden context.
- Strong generations can become Series Masters; future variants should preserve robust anchors while changing selected axes.
- Dense action should be written as connected causal grammar rather than a list of disconnected impressive moves.
- Stylized effects should obey simple visible physics rules when realism is intended.
- Environmental consequences are part of action readability, not decorative background motion.
- A camera may react imperfectly to extreme motion; motivated imperfection can increase live-action credibility.
- Character emotion is an invariant that must survive fast choreography.
- Long spectacular prompts are capability demonstrations until their patterns repeat reliably in production.
- External prompt methodologies are treated as candidate knowledge, not unquestioned rules. Concepts are promoted only after they prove useful in practical generation.

### Methodology sources reviewed

- Nuyoah knowledge-base updates on prompt responsibility, reference reverse-engineering, action-oriented prompting, controlled variation, and series-oriented prompt skills.
- A high-detail Seedance action prompt featuring continuous multi-agent martial-arts choreography, explicit physical-effect constraints, reaction evidence, timestamped beats, and reactive handheld camera behavior.
- Existing XAI-Studio-Video experiments on identity-first motion, Motion Budget, micro-motion, causal environmental motion, occlusion transitions, and model adapters.

## 0.1.0-draft — 2026-08-21

Initial working architecture created from accumulated AI video prompting experiments and prompt reverse-engineering notes.

### Added

- Character DNA
- Director Intent
- Visual DNA
- Shot Graph
- Camera DNA
- Motion DNA
- Motion Budget
- Micro Motion
- Ambient Motion Field
- Audio DNA
- Constraints
- Model Adapter concept
- Master Creative Spec vs Runtime Prompt separation
- Dynamic vs Stillness primitive families
- identity-first priority hierarchy
- negative-to-positive constraint conversion
- reusable Master Creative Spec template
- `Quiet Eye-Contact Hold` stillness primitive
- `Occlusion Roll Reveal` dynamic primitive
- `Summer_Garden_EyeContact_v1` reference example

### Design decisions

- A video prompt is treated as a temporal production specification, not merely prose.
- DNA represents invariants; Shot Graph and Motion represent transformations.
- Identity preservation outranks aesthetic spectacle when they conflict.
- Stillness is an explicit controllable state, not an absence of prompting.
- Environmental micro-motion should be causal and coherent.
- Large transitions may be hidden behind motivated occlusion.
- Model-specific Runtime Prompts are compiled from a model-agnostic Master Spec.