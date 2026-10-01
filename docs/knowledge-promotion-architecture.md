# Video Knowledge Promotion Architecture

Status: active design note  
Updated: 2026-09-30

## Purpose

This document defines how reference analysis, directing knowledge, prompt-craft rules,
machine-readable motion primitives, model capability knowledge, and local agent skills
fit together without becoming duplicate sources of truth.

The current evidence corpus and derived DBs are:

- `docs/reference-state-analyses.md` — evidence corpus, currently 68 analyses.
- `docs/directing-technique-db.md` — directing/editing knowledge, currently T-01~T-37.
- `docs/prompt-craft-db.md` — prompt/compiler knowledge, currently P-01~P-30.

The private repository also contains a machine-readable execution layer:

`XAI-Studio-Private/XAI-Studio/personal-prompt-studio/library/video-motion/`

## Canonical knowledge flow

```text
Reference / observed output / authored prompt
                 ↓
       Evidence corpus
 reference-state-analyses.md
                 ↓
     Curated directing knowledge
 directing-technique-db.md
                 ↓
       Prompt/compiler knowledge
    prompt-craft-db.md
                 ↓
     Production compiler policies
                 ↓
 Machine-readable motion primitives
  private video-motion/*.yaml
                 ↓
       Model capability profile
                 ↓
          Model adapter
                 ↓
 H3 / LTX / Seedance / Veo / future renderers
```

The arrows are promotion/compilation relationships, not copy relationships.
Do not duplicate the same rule as competing prose in multiple files.

## Layer responsibilities

### 1. Evidence corpus

`reference-state-analyses.md` is the source-evidence archive.

Keep these evidence labels distinct:

- `prompt-derived`
- `author-described`
- `frame-derived`
- `inference`

Inference may explain why something appears to work but must not silently become a
production rule. A production rule should have an explicit evidence path.

### 2. Directing DB

`directing-technique-db.md` answers:

> What should the director show, omit, hide, imply, or transition?

Examples:
- ellipsis cut
- occlusion wipe
- eyeline match
- causal camera reaction
- motion budget
- state changes off-screen

These are directing/editing patterns. They should not all become YAML primitives.

### 3. Prompt Craft DB

`prompt-craft-db.md` answers:

> How should an orchestration agent express the intended result to a generation model?

Examples:
- trace-first physics writing
- state transition chain
- positive locks
- capability-calibrated language
- model adapters
- prop state ledger

Many P-items are compiler policies, not visual primitives.

### 4. Machine-readable motion library

The private `video-motion` library stores reusable atomic or near-atomic execution units:

- camera motion
- transition motion
- timing
- physical follow-through / inertia

A term is promoted here only if an orchestration agent benefits from selecting it as a
stable semantic unit and expanding it into observable model-facing motion.

## Promotion classification

Every T/P item considered for runtime use must first be classified as one of:

### A. Primitive

A reusable atomic or near-atomic unit that can be selected and parameterized.

Examples:
- pan
- dolly
- orbit
- whip pan
- rack focus
- easing
- camera settling

Destination:
`video-motion/*.yaml`

### B. Director recipe

A composition of multiple primitives or editing choices used to solve a scene problem.

Examples:
- ellipsis cut + audio bridge
- occlusion wipe around a difficult state transition
- END BEFORE IMPACT

Destination:
keep in `directing-technique-db.md`; optionally add a machine-readable recipe later.

### C. Compiler policy

A rule for how an agent writes or compiles prompts.

Examples:
- P-06 Trace-first
- P-13 capability-calibrated language
- P-14 positive locks
- P-26 model adapter

Destination:
local/agent skill instructions and prompt compiler policy.

### D. Production state system

A rule that requires persistent structured state across shots rather than wording alone.

Examples:
- P-29 injury/damage state lock
- P-30 prop state ledger

Destination:
Studio state schema / Shot Graph / continuity state store.

### E. Model capability fact

A renderer-dependent observation that can change over time.

Examples:
- a model follows ordered beats better than absolute time
- a model fails particular contact transitions
- a model understands a given cinematography term reliably

Destination:
model capability profile, with evidence date and source.

Do not freeze renderer limitations into timeless canonical directing rules.

## Renderability Boundary Principle

The current corpus contains several related techniques:
T-01, T-04, T-08, T-10, and T-37.

Treat them as instances of a higher-order decision:

```text
If a causal intermediate state is unreliable to render,
do not keep adding prompt detail indefinitely.

Classify the transition as:
A. Render directly
B. Render partially
C. Hide behind cut/occlusion
D. Infer from consequence only
```

This is the preferred decision path for difficult:
- dressing / undressing transitions
- hand-object contact
- door crossing
- object extraction / insertion
- vehicle entry / exit
- hairstyle state changes
- wet/dry state changes
- crowd rearrangement
- complex prop handoffs

The point is not to avoid complexity universally. The point is to spend renderer
capability only where the visible intermediate state has story value.

## Time-dependent capability rules

Do not encode current renderer weaknesses as permanent truth.

Prefer:

```yaml
renderability:
  current_risk: HIGH
  preferred_strategy: conceal_or_cut
  evidence_date: 2026-09
  tested_models:
    - model_name
```

The same applies to timing syntax such as percentage phases versus absolute seconds.
Those belong in model capability profiles and adapters.

## Confidence should be two-dimensional

The existing star score is useful as an evidence-count shorthand, but runtime promotion
should distinguish:

```text
Evidence Strength:
  HIGH / MEDIUM / LOW

Cross-Model Generality:
  HIGH / MEDIUM / LOW / UNKNOWN
```

A classical continuity rule may have high generality even with few corpus examples.
A renderer-specific prompting trick may have many examples but low cross-model generality.

## Promotion rule for new findings

For every newly analyzed reference, decide in this order:

1. Is it already explained by an existing T/P item?
2. Does it strengthen evidence for an existing item?
3. Does it narrow or expand an existing item's scope?
4. Is it model-specific capability evidence?
5. Only then: is a new technique ID actually required?

Default preference:
**strengthen / merge / scope-tag before creating a new ID.**

The corpus has reached the point where uncontrolled taxonomy growth is more dangerous
than missing one speculative technique.

## Runtime architecture target

```text
User intent
  ↓
Director reasoning
  ↓
Shot / continuity state
  ↓
Prompt-craft compiler policies
  ↓
Motion primitives
  ↓
Model capability profile
  ↓
Model adapter
  ↓
Final renderer prompt
```

The user should not need to memorize cinematography terms or prompting hacks.
The orchestration layer owns that translation.
