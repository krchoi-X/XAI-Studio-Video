# Changelog

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