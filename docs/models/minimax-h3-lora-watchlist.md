# MiniMax H3 LoRA Watchlist
Last updated: 2026-09-17

## Candidate: AfterMidnight-MiniMax-H3-NSFW

Source:
https://huggingface.co/SexGod1979/AfterMidnight-MiniMax-H3-NSFW

## Status

Experimental specialist candidate.

Do not treat this as the default H3 configuration.

## What it is

This repository is a MiniMax H3 add-on model candidate intended for Ref2VA-oriented workflows.

For this project, the main interest is **not primarily NSFW generation**. The useful research question is whether the LoRA improves difficult close-range human interaction and contact-heavy motion.

## Why it matters for this project

Potentially relevant difficult cases include:

- martial-arts blocking;
- wrist grabs / catches / turns;
- one person supporting another after loss of balance;
- pilates or posture correction;
- partner dance;
- close body interaction;
- physical-gag scenes that require two-person coordination.

These scenes are known to be difficult because the generator must preserve relative body positions, hand states, contact points, and action order over time.

## Hypothesis to test

The working hypothesis is:

> A contact/motion-specialized H3 LoRA may reduce failure rates in close-range multi-person motion compared with base H3 Ref2VA.

This is only a hypothesis. Do not promote the model to a production default without A/B evidence.

## Risks

Possible failure modes include:

- pose bias;
- overfitting to specific kinds of body interaction;
- overly intimate framing when not requested;
- reduced usefulness for ordinary daily motion;
- unwanted style bias;
- compatibility limits outside the workflow/mode for which the LoRA was trained.

## Recommended A/B test

Compare:

```text
A. Base H3 Ref2VA
B. Base H3 Ref2VA + AfterMidnight motion/contact-oriented variant
C. Optional alternate/softer variant if available
```

Keep as much as possible constant:

- character references;
- prompt;
- duration;
- seed where supported;
- sampler/scheduler settings appropriate for the LoRA;
- output resolution.

## Test scenes

### Test 1 — Martial arts contact

```text
one character reaches for the other's wrist
→ clear grip/contact
→ controlled turn / escape
→ both reset stance
```

### Test 2 — Pilates posture correction

```text
instructor approaches from the side
→ one hand supports pelvis
→ one hand guides shoulder alignment
→ student adjusts posture
→ corrected pose holds
→ instructor releases
```

### Test 3 — Support / catch

```text
one person loses balance
→ second person makes contact
→ supports torso/arm
→ both settle into a stable final pose
```

### Test 4 — Physical gag support

```text
comic trip or loss of balance
→ close-range recovery / catch
→ stable final state
```

## Evaluation criteria

Score or annotate:

- contact clarity;
- left/right hand consistency;
- contact-point stability;
- body-overlap readability;
- continuity of force / movement sequence;
- identity stability;
- prompt obedience;
- side effects / unwanted bias;
- regeneration rate needed to get one usable result.

## Promotion rule

Do not move this candidate from watchlist to recommended/default until it produces a repeatable improvement across at least several relevant contact-motion scenes.

If the result is useful only for a narrow class of interactions, keep it as a router-selectable specialist LoRA rather than a global default.

## Suggested tags

- `minimax-h3`
- `ref2va`
- `lora`
- `motion-specialist`
- `contact-motion`
- `experimental`
- `optional`

## Related pattern guidance

See:

`docs/director-memory/patterns/contact-motion-and-physical-gags.md`

The intended architecture is:

```text
problem pattern detected
→ Director Core / Skill Router selects contact-motion constraints
→ structured state-based storyboard
→ renderer compiler
→ optional specialist LoRA such as AfterMidnight
→ A/B evaluation
```
