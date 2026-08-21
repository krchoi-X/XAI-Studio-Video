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
- future local/open-weight video models

Adapters should be versioned because model behavior can change materially even when the product name stays the same.