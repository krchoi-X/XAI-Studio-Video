# Storyboard Director Memory

## Purpose

This directory is the shared directing-memory layer for character-driven short-form video production.

It exists because model conversations are ephemeral. Claude, Grok, Hermes, Codex, ChatGPT, or another model may each improve inside one session, yet the next model can repeat the same directing mistakes. This layer turns those lessons into durable production knowledge without forcing every episode into the same style.

The goal is **not** to make every model produce identical storyboards. The goal is to make every model:

1. know important prior failures;
2. know the user's demonstrated visual preferences;
3. know useful directing patterns and alternatives;
4. know what production tools are actually available;
5. propose a small number of distinct, producible storyboard candidates;
6. preserve room for creative variation.

## Scope

This layer sits between character identity and renderer-specific prompting.

```text
Character DNA / Episode brief
        ↓
Director Memory
  - principles
  - opening families
  - failure lessons
  - approved examples
        ↓
Capability Registry
        ↓
Independent storyboard exploration
        ↓
2–3 candidate storyboards
        ↓
Human selection / revision
        ↓
Renderer-specific compilation
        ↓
WanGP / H3 / image generation / editing
        ↓
Result review
        ↓
Memory update
```

Character DNA answers **who the character is**. Director Memory answers **how this episode might be shown**. Renderer skills answer **how to express the chosen storyboard to a specific model or tool**.

Do not move temporary events, one-off gags, camera choices, shot orders, or editing tricks into Character DNA unless they become true recurring canon.

## Files

- `principles.md` — stable directing rules and decision process.
- `opening-patterns.md` — reusable opening families and when they fit.
- `failures.md` — failure lessons and anti-patterns. These are warnings, not universal bans.
- `capabilities.md` — current production capabilities and constraints. Keep factual and date-sensitive.
- `approved-storyboards.md` — selected storyboard examples and why the user approved them.
- `candidate-template.md` — required output structure for storyboard proposals.

## Required use by an AI director

Before proposing a character-driven vlog or short:

1. Read the character's current canonical record from the configured shared character source.
2. Read the current episode brief.
3. Read `principles.md`, relevant entries in `failures.md`, and relevant patterns in `opening-patterns.md`.
4. Read `capabilities.md`; do not invent unavailable production features.
5. If approved examples exist for the same character or episode type, read only the most relevant examples. Learn the principle, not the literal shot order.
6. Produce **at least two meaningfully different candidates** unless the user explicitly asks for one.
7. Make one candidate production-safe and one candidate more exploratory when appropriate.
8. State whether each proposal is primarily `long_take`, `multi_cut`, or `hybrid`.
9. Include a production route for each candidate: still generation needs, reference needs, motion/control needs, and likely renderer path.
10. Do not render or execute until the selection/approval contract for the active workflow allows it.

## Independence rule

When multiple models are asked to ideate, they should explore independently before seeing each other's candidate storyboards. Shared memory should contain durable lessons, not the other model's fresh answer. This reduces anchoring and preserves stylistic diversity.

Suggested role bias, not a hard assignment:

- Claude: subtle continuity, psychology, environmental storytelling.
- Grok: contemporary visual ideas, unusual but plausible openings, internet-native references.
- Hermes/local model: systematic, production-safe, constraint-aware permutations.
- ChatGPT/Codex planning: structural comparison, synthesis, production compilation, durable documentation.

The host/executor and the selected LLM are separate identities. Record the real actor/model where the project workflow supports it.

## Memory rule

A failure lesson must not automatically become a hard creative prohibition.

Bad transformation:

> Failure: one vlog opened with an unhelpful face-filling selfie. Rule: never start a vlog with a close-up.

Correct transformation:

> Failure: when the brief only said "vlog introduction", the model defaulted to a generic handheld face-filling selfie that hid the space and body language. Future directors must choose the opening strategy deliberately and specify camera support, subject scale, and reveal logic. A close-up remains valid when intentionally selected.

Store **why** something failed and what alternatives exist.

## Production-first principle

The storyboard is not merely prose. It must be executable enough that another agent can turn it into stills and video without reconstructing the director's intent from conversation history.

At minimum, every shot or beat should specify:

- narrative purpose / hook;
- subject scale;
- camera position/support;
- character or object position;
- action beat;
- environment or spatial anchor;
- transition or handoff;
- continuity state that must persist;
- whether the beat is suitable for one continuous clip or should be separated.

For H3-style production, also preserve useful concepts such as spatial anchors, pose/expression path, camera behavior, continuity handoff, and explicit reference bindings when relevant.

## Update policy

Update this directory after real production evidence, not after every speculative idea.

Add or revise memory when at least one of these is true:

- the same failure happens more than once;
- the user explicitly identifies a preference or rejection reason;
- a storyboard is selected and successfully produced;
- a renderer limitation materially changes what is feasible;
- a new capability becomes reliably available in the actual production environment.

Avoid cosmetic rule growth. Prefer a few strong, evidence-backed lessons over a large handbook of imagined constraints.
