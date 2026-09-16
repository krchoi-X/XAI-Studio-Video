# Prompt Compiler Principles for Video Generation

## Purpose

This document records prompt-compilation principles for the Director / Storyboard pipeline. It is intended for Codex, Claude Code, Hermes, Grok, and any future implementation agent that needs to compile an approved visual plan into renderer-specific video prompts.

These are **compiler policies**, not universal creative rules. The canonical storyboard should remain renderer-neutral and structured; only the final renderer layer should lower that structure into the form preferred by the selected video engine.

## Core distinction: planning language vs renderer language

Do not design the project around a single giant natural-language prompt.

Upstream planning should remain structured:

```text
Episode brief
→ visual-language interpretation
→ skill routing
→ storyboard candidate
→ continuity / physical-state design
→ renderer-specific prompt compile
```

The final video prompt is a compiled artifact. It is not the canonical source of truth.

## 1. Signal-density principle

Prefer information that produces observable visual consequences.

High-value prompt information includes:

- subject identity and visible appearance;
- spatial relationships;
- action order;
- physical contact and support states;
- camera position / operator / motion;
- lens or field-of-view only when materially useful;
- lighting direction and source;
- depth-of-field behavior;
- continuity state carried from adjacent shots;
- timing or action phases when the renderer benefits from them.

Low-value or weakly grounded wording includes long stacks of abstract adjectives such as:

- cinematic;
- amazing;
- stunning;
- masterpiece;
- hyper-realistic, when not backed by concrete visual evidence.

Do not ban such words categorically. Prefer concrete visual instructions whenever they communicate the intent more precisely.

### Positive physical state over negative lists

Long negative lists consume context and often fail to explain what the correct state should be.

Prefer:

```text
steady handheld movement following real footsteps
```

over:

```text
no shake, no jitter, no glitch
```

Prefer:

```text
her right hand supports the cup from below while her fingers remain clearly visible around the side
```

over:

```text
no bad hands, no extra fingers, no warped grip
```

Use negative constraints when the renderer has a documented negative-prompt channel or when a repeated failure cannot be expressed clearly as a positive state. Negative prompts are not forbidden; they should be purposeful and compact.

## 2. Multi-pass processing

Do not ask one model call to simultaneously invent story intent, solve blocking, reason about physics, choose camera grammar, and compress everything into a renderer prompt unless the task is trivial.

Preferred logical passes:

```text
Pass A — Intent / directing
What must the viewer understand or feel?

Pass B — Spatial / physical design
Where is everything? What contacts, supports, transfers, or moves?

Pass C — Shot construction
Framing, camera role, action chain, continuity, transition.

Pass D — Renderer lowering
Compile only the information the target engine needs in the syntax/verbosity it handles well.
```

These passes may be separate model calls, separate deterministic transforms, or a single internal pipeline. The logical separation matters more than the implementation count.

## 3. Renderer-specific lowering

Different video engines may prefer different prompt shapes and densities.

Do not hard-code one universal final format.

Each renderer profile should eventually be able to describe at least:

```yaml
renderer_id: example
final_prompt_shape: paragraph   # paragraph | structured | hybrid
negative_policy: compact        # none | compact | dedicated_field
preferred_length_words: [80, 130]
phase_chain_support: medium      # low | medium | high
camera_spec_tolerance: medium
continuity_detail_tolerance: high
notes: []
```

The numeric length ranges are **starting heuristics**, not standards.

Useful initial categories for experimentation may be:

- short-form engines: roughly 40–80 words;
- balanced engines: roughly 80–130 words;
- detail-tolerant engines: roughly 150–250 words.

Codex must not encode these as universal truths. They should live in engine profiles and be revised from actual production results.

## 4. Natural-language paragraph lowering

Some video models may respond better to a continuous natural-language paragraph than to explicit labels such as `[Camera]`, `[Scene]`, or `[Subject]`.

Treat this as an **engine capability / formatting preference**, not a global rule.

Recommended architecture:

```text
structured storyboard / shot state
        ↓
renderer compiler
        ↓
continuous paragraph, structured block, or hybrid form
```

Do not destroy upstream structure just because the final renderer prompt is a paragraph.

A claim that brackets or labels universally "break latent-space projection" should not be treated as established fact. Evaluate prompt shape empirically per renderer.

## 5. Physical-state compilation

When interaction matters, compile actions as observable state transitions rather than vague verbs.

Example:

```text
reach
→ contact
→ support
→ release
```

is preferable to simply:

```text
handoff
```

when the visual result depends on hand/object continuity.

Likewise, actions with several meaningful phases may be expressed as a compact three-stage chain if the selected engine handles phased motion well.

Avoid packing multiple unrelated actions into one short clip merely because the text can describe them.

## 6. Global invariants vs shot-specific variation

Preserve stable global state strongly while allowing shot grammar to vary.

Typical global invariants:

- character identity;
- wardrobe / hairstyle when continuity requires them;
- key prop ownership/state;
- baseline visual texture;
- location-specific continuity facts.

Typical shot-specific variables:

- framing;
- camera operator;
- camera height / angle;
- movement;
- focus behavior;
- transition;
- shot rhythm;
- local action.

Do not confuse consistency with sameness. The point is to keep the world coherent while allowing visual variety.

## 7. Exception scoping

When a shot or sequence intentionally differs from the baseline, make the scope explicit and restore the baseline afterward.

Example:

```text
Shots 7–9 use DV-style texture.
Shot 10 returns to the baseline phone-video texture.
```

This helps prevent a local stylistic exception from leaking into later shots.

## 8. What the compiler should preserve from the storyboard

The renderer prompt should be derived from, not replace, the approved storyboard.

At minimum preserve relevant parts of:

- framing;
- camera role/operator;
- camera behavior;
- dominant action;
- physical interaction state when needed;
- continuity anchor;
- duration / beat timing;
- transition / handoff;
- renderer-specific references or controls.

Do not inject unrelated style references just because they exist in the reference library.

## 9. Validation and experimentation policy

Before adopting a compiler rule as default:

1. identify which renderer it is intended for;
2. test it on a small repeatable fixture;
3. compare against the current baseline;
4. record whether the improvement concerns motion, continuity, visual fidelity, prompt obedience, or some other axis;
5. promote only repeatable improvements into the renderer profile.

Do not promote a single successful viral/example prompt into a universal compiler rule.

## 10. Guidance for Codex implementation

The first implementation should be small.

Recommended minimal additions:

- a renderer profile schema;
- a prompt compiler that accepts the existing structured storyboard/shot representation;
- a positive-description-first transformation policy;
- optional compact negative constraints;
- configurable final prompt shape;
- configurable target verbosity range;
- tests that show the same storyboard can compile differently for at least two renderer profiles.

Do not add a second orchestration system, vector database, or large prompt-DSL solely for this feature.

## Evidence / confidence notes

- **Strong principle:** multi-pass planning before renderer execution.
- **Strong principle:** prefer observable physical/visual states over vague adjectives.
- **Strong practical heuristic:** long negative lists are usually lower-value than precise positive states.
- **Engine-dependent heuristic:** continuous paragraph vs structured syntax.
- **Engine-dependent heuristic:** target word-count ranges.

Treat engine-dependent items as profiles to be measured, not doctrine.

## Summary for future agents

The project should think structurally and render adaptively:

```text
structured intent
→ structured visual plan
→ selected skills
→ approved storyboard
→ renderer profile
→ compact engine-specific prompt
```

The goal is not the longest or most "cinematic" prompt. The goal is the **highest useful signal density for the selected renderer while preserving the approved visual plan**.
