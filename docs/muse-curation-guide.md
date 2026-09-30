# Muse Guide — Reference Analysis and Knowledge Curation

Audience: Muse / Somni  
Status: active  
Updated: 2026-09-30

## Mission

Continue analyzing strong AI-video references, but shift the priority from
**collecting more techniques** to **validating, merging, scoping, and strengthening the existing knowledge base**.

Current authorities:
- `reference-state-analyses.md` — evidence corpus
- `directing-technique-db.md` — T-techniques
- `prompt-craft-db.md` — P-techniques

The current corpus is large enough that uncontrolled taxonomy growth is now a bigger
risk than missing one speculative technique.

## Evidence-first rule

Keep these labels explicit:

- `prompt-derived`
- `author-described`
- `frame-derived`
- `inference`

Never silently promote inference into the production spec.

If a claim is based only on a creator's wording, keep it separate from what can actually
be verified in frames.

## Before creating a new T/P item

For every new reference, answer in this order:

1. Which existing T-items explain it?
2. Which existing P-items explain it?
3. Does this add independent evidence to an existing item?
4. Does it reveal a boundary/exception to an existing item?
5. Is the behavior model-specific rather than general?
6. Only if none of the above: is a new T/P item justified?

Prefer:
**reinforce → merge → scope → model-tag → new ID**

## What to extract from every useful reference

### A. Visible/directing problem

State the actual production problem:
- spatial continuity
- identity continuity
- difficult contact
- state transition
- pacing
- action readability
- emotional eyeline
- camera motivation
- object continuity
- etc.

### B. Technique used

Record the smallest technique set that explains the solution.

Avoid treating every stylistic flourish as a new technique.

### C. Evidence type

Mark exactly where the claim comes from.

### D. Failure avoided or observed

If the creator describes failed attempts or the video visibly breaks, capture the failure
as evidence. Failures are valuable for scope boundaries.

### E. Cross-model generality

Add an explicit judgment field:

```text
cross_model_generality:
  HIGH / MEDIUM / LOW / UNKNOWN
```

Guidance:
- classical film/editing grammar → usually higher generality
- prompt syntax hack → often lower
- renderer-specific behavior → LOW unless independently replicated

### F. Evidence strength

Keep star notation if useful, but also state:

```text
evidence_strength:
  HIGH / MEDIUM / LOW
```

Do not conflate number of examples with generality.

## Renderer capability findings

When a finding says more about a renderer than about directing, do not create a timeless
T/P rule.

Record it as capability evidence with:
- model
- version/date
- task
- input mode
- observed success/failure
- source reference
- confidence

Examples:
- absolute timestamps drift
- ordered beats survive
- contact is unstable
- cinematography terminology is understood
- multi-character identity degrades

These findings should later feed model profiles/adapters.

## Renderability Boundary Principle

When the model struggles with an intermediate state, classify it:

- DIRECT — render the full transition
- PARTIAL — render only reliable portions
- HIDE — place unreliable state change behind cut/occlusion
- CONSEQUENCE_ONLY — omit cause and show evidence/result

Use this lens when reviewing:
T-01 / T-04 / T-08 / T-10 / T-37.

Do not assume "more detailed prompting" is always the right fix.

## Distinguish four promotion targets

When a new insight is valuable, tag its likely destination:

```text
promotion_target:
  PRIMITIVE
  DIRECTOR_RECIPE
  COMPILER_POLICY
  PRODUCTION_STATE
  MODEL_CAPABILITY
  EVIDENCE_ONLY
```

Examples:

- pan/dolly/rack focus → PRIMITIVE
- ellipsis cut + audio bridge → DIRECTOR_RECIPE
- Trace-first → COMPILER_POLICY
- prop state ledger → PRODUCTION_STATE
- "model X ignores absolute seconds" → MODEL_CAPABILITY

## Do not duplicate private runtime data

The private `video-motion` YAML library is the machine-readable execution layer.
Muse should not copy that library into public docs.

Muse's role is evidence and curation.
Codex/runtime tooling decides whether a validated item is promoted into executable YAML.

## Preferred analysis footer

For each new reference, append a compact promotion summary:

```yaml
knowledge_update:
  existing_T: [T-..]
  existing_P: [P-..]
  evidence_strength: MEDIUM
  cross_model_generality: HIGH
  promotion_target: DIRECTOR_RECIPE
  action: strengthen_existing
  notes: "..."
```

Allowed `action` values:
- `strengthen_existing`
- `scope_existing`
- `merge_candidate`
- `model_capability_only`
- `new_candidate`
- `evidence_only`

## New-ID threshold

A new T/P ID should meet all of these:

1. cannot be expressed cleanly as an existing technique/variant,
2. solves a distinct production problem,
3. has observable evidence,
4. has a reusable formulation,
5. is not merely one renderer's temporary quirk.

Single-example discoveries may still be recorded, but default to `new_candidate` rather
than immediate canonization unless the distinction is structurally important.

## Review cadence

Every 10–15 additional references, perform a consolidation pass:
- duplicate T/P candidates
- stale renderer assumptions
- low-value one-off entries
- stronger evidence for existing rules
- scope changes
- model-specific findings needing adapter/profile updates

## Output style

Keep the current evidence-first structure.
Do not turn the analysis corpus into tutorials or marketing copy.
Concrete frame/prompt observations matter more than elegant interpretation.

The best new analysis is not the one that produces the most new techniques.
It is the one that makes the existing system more reliable.
