# Intent-Preserving Storyboard-to-Video Methodology

Status: canonical runtime methodology for new storyboard-derived video work. Enforcement revision: v1.2; new artifact schema: v2 (v1 remains readable only).

## Why this exists

Recent production showed that an acceptable storyboard can still produce a weak video when a downstream agent rewrites the shot while preparing a model prompt. The prompt may sound polished while changing the gaze timing, screen direction, action order, omission, camera behavior, blocking, or final emotional state that made the storyboard work.

The correction is not a larger universal prompt. It is a separation of authority:

```text
user goal
→ director and approved Storyboard Spec
→ Intent Contract
→ bounded cinematography
→ model-specific compiler
→ structural semantic check
→ renderer
→ human render review
→ contract-checked segment assembly
```

Before approval, creative exploration is encouraged. After approval, narrative meaning is closed by default.

For complex work, an optional Frontier Creative Treatment may precede the storyboard. It frames story and reference grammar but is not render approval. Hermes is the default local Production Director: it drafts the Production Storyboard, Intent Contract, and engine-ready prompt segments. The user approves those production artifacts together before compilation. See [Creative Treatment and Production Role Sidecars](creative-treatment-contract.md).

## Authority and scope

The approved Storyboard Spec defines the scene. The Intent Contract carries the subset that downstream work must preserve. A runtime prompt is a disposable model-specific compilation artifact; it is never the directing source of truth.

This methodology applies to new video work derived from an approved storyboard, regardless of whether Codex, Claude, Grok, Muse/Somni, Hermes/Meromero, or another agent performs a stage. Agent identity does not change the contract.

Free prompt experiments that are not storyboard-derived remain possible, but they must not be presented as faithful execution of an approved storyboard.

## Roles

### Director

Creates the storyboard and Intent Contract together. The director decides narrative purpose, action order, what the audience witnesses or infers, gaze and direction semantics, entry/exit state, final beat, and feasibility strategy. Approval covers both artifacts and one exact revision/hash pair.

In the default treatment-backed flow, Hermes is this Production Director. ChatGPT, Claude, Codex, or Grok may author the optional Creative Treatment, but treatment authorship does not grant authority to approve or silently rewrite the Production Storyboard.

### Cinematographer

Improves expression only inside the contract's allow-list. Lens family, light, depth, texture, foreground layering, and limited framing refinement are typical safe freedoms. Camera movement, actor action, gaze, blocking, and temporal order are locked unless explicitly allowed.

### Model compiler

Translates the approved contract and allowed cinematography into the target model's syntax and controls. It may choose supported reference/control mechanisms but may not redesign the shot. Locked values remain structured in a compiler intermediate beside the prose prompt.

Hermes authors model-neutral `prompt_segments` and any required engine prompt profile while the production packet is still a draft. Once the user approves the packet, neither Hermes nor a frontier model may paraphrase those locked segments. Subsequent compilation selects only approved values and applies the versioned engine adapter. The structured contract/IR is not itself renderer prose.

### Verifier

Compares the contract to the compiler intermediate before render and attributes post-render failures to `storyboard`, `compiler`, `renderer`, or `edit`. Aesthetic quality does not excuse low intent fidelity.

The normal first-line render reviewer is a separate Hermes pass with an independent context. Reusing the authoring context and merely asking it to “look again” does not count as independent review.

### Editor

May mine usable micro-shots, but every selected segment inherits the applicable portion of its parent contract. Editing cannot turn an attractive intent violation into an accepted result.

## Intent Contract

Every approved video shot must carry a self-contained packet sufficient for an agent with no originating conversation history. The required artifact shape, lifecycle and checks are defined in [Video Intent Contract](video-intent-contract.md).

The packet includes:

- user-visible goal, viewer understanding/feeling, shot purpose, and short rationale;
- Storyboard Spec ID, revision, and verified content hash;
- ordered required events and entry/exit states;
- gaze, direction, blocking, camera, omission, and final-state locks;
- explicit creative-envelope allow-list and named level;
- feasibility decision and rationale;
- unresolved decisions that no agent may answer silently;
- compiler/model/version provenance and semantic-check evidence;
- consumer acknowledgement of the locked, allowed, and unresolved sets.

Background must be bounded. Include why a decision matters to execution, not the whole research archive.

## Creative levels

Creative levels are named allow-list presets, not permission to improvise everything not prohibited.

| Level | Allowed by default | Still locked unless explicitly added |
|---|---|---|
| L0 Literal | no additions | all camera, action, gaze and visual changes |
| L1 Cinematography Enhancement | lens family, light quality, depth of field, texture, foreground/background separation, small framing refinement | camera movement, actor action, gaze, blocking, event order |
| L2 Interpretive Cinematography | L1 plus explicitly named parallax, rack focus, camera lag or visual motif | narrative action, gaze meaning, direction, omissions, final state |

Re-direction is not a creative level. It requires returning to the director and approving a new storyboard/contract revision.

Silence is not permission. Per-shot `allowed` and `forbidden` lists override the preset only when explicitly recorded.

## Feasibility vocabulary

Choose feasibility before prompt compilation:

- `SHOW`: render the required event directly.
- `SPLIT`: divide it into simpler approved shots or chunks without changing editorial meaning.
- `IMPLY`: show cause or consequence so the audience infers the event.
- `OMIT`: deliberately remove a nonessential event from the screen.
- `INSERT`: use a detail, reaction, establishing, or bridge shot.
- `CONTROL`: use an approved first/last frame, pose, trajectory, reference or other control modality.

An event hidden behind a cut or occlusion is represented as `IMPLY`, `OMIT`, or `SPLIT` according to what the audience receives; it is not a separate feasibility decision.

`REGENERATE` is a retry policy, not a directing strategy. Do not solve feasibility by making the prompt longer.

## Timing

Record semantic order and relative position by default:

```text
private gaze
→ required action
→ brief lens connection only at the end
```

Add exact seconds or a tolerance only when dialogue, music, a cut point, or another timing fact is itself a director invariant. The compiler may map relative anchors to backend timing, but it may not replace them with a different sequence.

## Contract enforcement

For storyboard-derived work, apply all of these layers:

1. Closed structured packet with required fields, stable IDs, controlled vocabulary and source hashes.
2. Deny-by-default changes to narrative action, gaze, direction, blocking, camera motion, omission and final state.
3. Locked structured compiler intermediate. The contract carries director-approved prompt segments plus an engine-specific prompt profile when the renderer has a required grammar. A versioned adapter renders them without LLM paraphrase.
4. Creative slots accept only values explicitly enumerated in `allowed_values`; the final runtime prompt must exactly equal the deterministic rendering of the contract and those values. Renderer prompts contain renderer-facing content only, never contract IDs, hashes, target-model labels, template IDs, or creative-choice bookkeeping.
5. Deterministic structural checks for event coverage/order, direction, gaze phase, camera locks, omissions and final state.
6. Advisory semantic review only for nuance that cannot be settled mechanically.
7. Submission gate requiring a matching approved contract and passing check before a storyboard-derived renderer job. Registering a new approved production plan through the maintained recorder enables this gate even if an agent omits the methodology flag; pre-existing legacy records are not silently reclassified.
8. Explicit human-approved, versioned and audited override when meaning must change.
9. Human post-render review and failure attribution.
10. Parent-contract inheritance and recheck for selected editing segments.

Hard failures include a stale or mismatched hash, missing or reordered required action, changed gaze/direction, restored omitted event, forbidden camera/action, wrong final state, or missing/failed semantic check. Ambiguous performance nuance and cinematography gain remain warnings or human-review decisions.

Documentation is not proof that a runtime gate exists. A renderer path may enforce the gate natively or through the maintained pre-submit checker. Until native integration exists, the executing agent must run `tools/video_intent_contract.py` immediately before submission, attach its passing record to the run, and submit the exact hash-matched prompt. A prompt-only handoff without that evidence is noncompliant and must stop.

### Engine-specific adapters

`intent-prompt-v1` is the generic adapter and is not a universal model prompt. Exact MiniMax H3 targets reject it:

- Ref2VA requires `h3-ref2va-v1`, which emits only `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, and `non_diegetic_music`, in that order.
- FL2VA requires `h3-fl2va-v1`, which emits only `integrated_multimodal_description`, `overall_soundscape`, and `non_diegetic_music`, in that order.

The H3 narrative section must contain every approved event line exactly once and in order. Audio and music are first-class approved fields. Engine profiles may contain deterministic `{{creative_key}}` slots, but the slot set must exactly match the selected allow-listed values. Unit tests prove structural preservation, not output quality; the first production still needs a controlled same-seed comparison or an explicitly approved pilot before any quality claim.

## Known-good prompts and reference studies

Keep the existing prompt and video-analysis library, but use it differently:

- extract reusable temporal and cinematographic patterns;
- preserve verified event structure instead of paraphrasing for elegance;
- bind every pattern to the tested model, version, mode and control method;
- substitute only compatible semantic slots;
- never let a successful example override the current contract.

## Evaluation

Judge two axes independently:

- **Intent Fidelity:** required actions, order, gaze, direction, blocking, omission, final state and narrative function.
- **Cinematography Gain:** composition, lens, lighting, depth, texture, atmosphere and permitted camera language.

A beautiful result with low Intent Fidelity fails. The target is high Intent Fidelity with positive Cinematography Gain.

## Migration precedence

Until every older guide is reconciled, these rules apply immediately:

1. Approved storyboard meaning and its contract outrank downstream prompt prose.
2. Omitted events remain omitted.
3. Narrative action, gaze, direction, blocking, camera motion and final state are closed unless explicitly allowed.
4. A model guide compiles the contract; it does not re-direct it.
5. Feasibility changes return upstream for a new revision.
6. Storyboard-derived rendering stops when contract/check evidence is missing or failed.

Existing camera, motion, continuity, character, reference and model-specific knowledge remains valid where it does not conflict with these rules.

## Guiding statement

**The director decides meaning; the cinematographer improves permitted expression; the compiler translates; the verifier guards the contract; the renderer executes; the editor preserves only compliant segments.**
