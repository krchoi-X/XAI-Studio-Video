# Changelog

## 0.2.0-draft — 2026-08-22

Expanded the studio from motion control alone toward evidence-first reference analysis and bounded creative freedom.

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

### Design decisions

- A prompt should be debuggable by responsibility layer rather than rewritten as one undifferentiated prose block.
- Exact pose choreography is optional; use an Action Skeleton unless contact geometry or silhouette truly requires precision.
- Generative randomness is not inherently a defect. Preserve bounded freedom where it can add natural variation.
- Reference reverse-engineering should describe visible effects and relationships, not invent exact equipment or hidden context.
- Strong generations can become Series Masters; future variants should preserve robust anchors while changing selected axes.
- External prompt methodologies are treated as candidate knowledge, not unquestioned rules. Concepts are promoted only after they prove useful in practical generation.

### Methodology sources reviewed

- Nuyoah knowledge-base updates on prompt responsibility, reference reverse-engineering, action-oriented prompting, controlled variation, and series-oriented prompt skills.
- Existing XAI-Studio-Video experiments on identity-first motion, Motion Budget, micro-motion, causal environmental motion, occlusion transitions, and model adapters.

### Next candidates

- MiniMax H3 adapter
- Seedance action adapter / action grammar notes
- Kling adapter
- Veo adapter
- Runway adapter
- character discovery vlog template
- production-state-machine / approval-rate metrics
- action physics primitives
- primitive metadata/schema format
- prompt/result experiment log
- identity consistency evaluation rubric
- keyframe planning grammar
- motion primitive tagging/index
- reference-image / Character DNA integration with future XAI-Studio-Image work

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

### Next candidates

- MiniMax H3 adapter
- Kling adapter
- Veo adapter
- Runway adapter
- primitive metadata/schema format
- prompt/result experiment log
- identity consistency evaluation rubric
- keyframe planning grammar
- motion primitive tagging/index
- reference-image / Character DNA integration with future XAI-Studio-Image work