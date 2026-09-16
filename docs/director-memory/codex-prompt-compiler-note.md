# Codex Note — Renderer Prompt Compiler

Read this together with `codex-pipeline-handoff.md` and `prompt-compiler-principles.md` before implementing the Director / Storyboard pipeline's renderer-specific prompt stage.

## Why this note exists

Recent prompt-guide review reinforced several useful ideas, but some claims were too absolute. Codex should implement the useful structure without hard-coding unverified folklore.

## Required interpretation

1. **Signal density** — prioritize observable visual/physical states over vague adjectives and long negative lists.
2. **Positive state first** — express what the correct grip, camera behavior, spatial relation, or motion should be. Use negative constraints only when they add value or the renderer exposes a dedicated negative channel.
3. **Multi-pass logic** — keep intent/directing, spatial/physical design, shot construction, and renderer lowering logically separate.
4. **Renderer-specific lowering** — do not assume one prompt shape or one word-count range is optimal for every engine.
5. **Structured upstream, adaptive downstream** — keep storyboard/state structured, then compile to paragraph/structured/hybrid syntax according to the renderer profile.
6. **Treat word counts as heuristics** — ranges such as 40–80, 80–130, and 150–250 words are starting presets for experiments, not universal standards.
7. **Do not encode claims such as 'brackets break latent space' as facts** — test prompt formatting per engine.
8. **Preserve physical state transitions** for interactions: reach → contact → support → release when that sequence matters visually.
9. **Preserve global continuity, vary shot grammar** — identity/wardrobe/props/world state remain stable while framing/operator/motion/focus/transition can vary.
10. **Scope exceptions explicitly** and restore baseline styling after a local exception.

## Minimal implementation target

The renderer profile should eventually be able to express fields similar to:

```yaml
renderer_id: minimax_h3
final_prompt_shape: paragraph
negative_policy: compact
preferred_length_words: [80, 130]
phase_chain_support: medium
camera_spec_tolerance: medium
continuity_detail_tolerance: high
```

These values are examples only; verify them against actual runtime behavior before treating them as defaults.

The compiler should accept the approved structured storyboard and produce engine-specific output without mutating the canonical storyboard.

## Tests worth having

- same storyboard compiled through two different renderer profiles yields meaningfully different prompt shape/verbosity;
- long negative-list input is reduced to positive observable state plus only essential negatives;
- physical interaction state survives compilation;
- a local style exception is bounded and baseline restoration is explicit;
- compiler never loads unrelated directing references merely because they exist in the library.

## Scope guard

Do not turn this into a prompt DSL project. Start with a small profile schema and deterministic/templated compiler behavior around the existing storyboard representation. Expand only after real WanGP/H3 production reveals repeatable failure modes.
