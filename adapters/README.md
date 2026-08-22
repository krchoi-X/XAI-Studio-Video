# Model Adapters

XAI-Studio-Video separates the model-agnostic Master Creative Spec from model-specific Runtime Prompts.

A Model Adapter is responsible for translating one into the other.

## Adapter responsibilities

For each target model/version, document:

1. What information the reference image/video already supplies.
2. How much visual description should remain in text.
3. How motion should be phrased.
4. Whether explicit timeline segments work reliably.
5. Whether negative prompts are supported or counterproductive.
6. Whether first/last frame or multiple keyframes are supported.
7. How camera motion is interpreted.
8. How identity preservation behaves under large motion.
9. Whether audio generation/synchronization is native.
10. Known failure modes and tested mitigations.
11. Which restrictions are technical/model requirements versus provider-specific service policy.

## Compilation rule

Do not blindly paste the entire Master Creative Spec into every model.

Example:

```text
Master Spec
- full character lock
- detailed visual look
- 5-stage shot graph
- micro motion
- ambient motion
- audio
- constraints

I2V Runtime Prompt
- motion sequence
- camera behavior
- settling rules
- identity-stability wording
- only visual details not already obvious from reference
```

## Policy separation rule

The canonical Storyboard Spec / Master Creative Spec should preserve the user's creative intent and should not be rewritten around the moderation behavior of one hosted provider.

Treat three classes of constraints separately:

```text
A. Creative / continuity constraints
   identity, composition, story state, anatomy, motion, lighting, tempo

B. Technical model constraints
   prompt length, reference limits, unsupported input combinations, resolution, context limits

C. Provider policy constraints
   restrictions imposed by a particular hosted service or API
```

Provider policy belongs in that provider's adapter, not in the canonical creative specification.

### Local / open-weight adapter rule

When compiling for a locally controlled or self-hosted open-weight model:

- do not automatically inherit provider-specific moderation wording from cloud adapters
- do not add generic conservative content restrictions that were not requested by the user and are not required for model stability
- do not sanitize ordinary creative details merely because another provider might reject them
- preserve the approved story, character, framing, emotion, wardrobe state, and scene intent as faithfully as the local model can support
- add negative prompts only when they solve a known generation failure, not as a hidden policy layer
- keep legal/rights/consent and adult-age metadata separate from visual-generation constraints when the project needs such metadata

The local adapter is still responsible for technical validity and for preserving the studio's production constraints. "No extra provider policy" does not mean "no constraints"; it means creative constraints remain creative, technical constraints remain technical, and service-policy constraints are not silently imported into self-hosted execution.

### Hosted-provider adapter rule

When a hosted provider requires restrictions, record them explicitly in that adapter as execution constraints. Do not back-propagate those restrictions into Character DNA, Storyboard Spec, or Master Creative Spec unless the user intentionally wants the underlying creative concept changed.

If a hosted renderer cannot execute an approved spec, prefer routing the job to another compatible renderer rather than mutating the canonical story solely to satisfy that provider.

See `docs/renderer-policy-separation.md`.

## Negative-to-positive conversion

Some engines respond better to desired-state wording than to long prohibition lists.

Master constraint:

```text
no excessive blinking
no identity drift
no strong artificial wind
```

Possible runtime conversion:

```text
stable facial identity throughout
one natural blink during the full clip
a very gentle coherent breeze moving only a few hair strands and nearby leaves
```

This conversion is for generation quality and controllability. It should not be used to inject unrelated provider-policy restrictions into a local adapter.

## Adapter maturity levels

- **L0 — Untested:** assumptions only.
- **L1 — Basic:** at least one successful generation.
- **L2 — Repeatable:** pattern succeeds across several scenes.
- **L3 — Character-safe:** tested with identity-sensitive I2V.
- **L4 — Production:** settings, failure modes, and regression examples documented.

## Planned adapters

- MiniMax H3
- Kling
- Veo
- Runway
- Z-Image / local open-weight image renderers
- future local/open-weight video models

Adapters should be versioned because model behavior can change materially even when the product name stays the same.
