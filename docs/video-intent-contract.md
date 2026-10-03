# Video Intent Contract

This guide defines the portable contract artifact used between an approved Storyboard Spec and model-specific video execution. It is the operational companion to [Intent-Preserving Storyboard-to-Video Methodology](intent-preserving-video-methodology.md).

## Lifecycle

```text
draft storyboard + draft contract
→ joint review
→ approved storyboard revision/hash + approved contract revision/hash
→ consumer acknowledgement
→ compiler intermediate + runtime prompt/control package
→ structural semantic check
→ renderer submission gate
→ human render review
→ segment sub-contract checks
```

The director authors the storyboard and contract together. Do not extract a supposedly authoritative contract later from prose without human review; that only moves reinterpretation to another hidden step.

## Minimum packet

```yaml
schema_version: 1
contract_id: intent_S07_v1
status: approved

source:
  storyboard_id: sb_reika_departure
  revision: 3
  sha256: <verified-storyboard-content-hash>

context:
  user_goal: Preserve the quiet departure rather than make it melodramatic.
  viewer_should_understand: Reika has decided to leave despite hesitation.
  viewer_should_feel: quiet finality, not reconciliation
  shot_purpose: hesitation -> brief connection -> departure
  rationale:
    delayed_gaze: Earlier lens contact removes the final emotional punctuation.
    static_camera: Pursuit would change a private observation into dramatic confrontation.

locked:
  ordered_events:
    - reach_door
    - pause
    - head_turn_only
    - brief_final_gaze
    - face_forward
    - exit
  gaze:
    before_final_moment: away_from_lens
    final_moment: brief_lens_contact
  screen_direction: toward_exit
  camera:
    movement: static
  final_state: exited_room
  omitted_events: [corridor_walk]
  forbidden_additions: [full_body_turn, object_pickup, return_to_room]

creative_envelope:
  level: L1
  allowed: [lens_family, light_softness, depth_of_field, foreground_layering]
  forbidden: [push_in, orbit, added_actor_action]

feasibility:
  decision: SHOW
  rationale: one actor, one location, one ordered action chain

unresolved: []
approval:
  approved_by: user
  approved_at: <timestamp>
```

The final machine schema may normalize IDs and timing anchors, but it must preserve context, locked meaning, allowed creativity, unresolved decisions and approval evidence as separate responsibilities.

The contract file does not contain its own SHA-256 because that would be self-referential. Consumers compute the exact file hash and store it in acknowledgements, compiler intermediates and semantic-check records.

## Consumer acknowledgement

Before compiling or revising, every consuming agent writes an acknowledgement beside the contract:

```yaml
agent: hermes
model: <selected-model>
accepted_contract_id: intent_S07_v1
accepted_contract_sha256: <verified-contract-hash>
locked_fields_understood: true
allowed_fields_understood: true
unresolved_fields: []
requested_change: null
```

If the agent cannot honor a lock, it sets `requested_change` and stops. It does not silently convert the lock into guidance.

## Compiler intermediate

The compiler preserves meaning in a structured form beside the renderer prompt:

```yaml
source_contract_id: intent_S07_v1
source_contract_sha256: <verified-contract-hash>
compiler: h3-contract-compiler
compiler_version: <version-or-commit>
target_model: minimax_h3_ref2va_pruned
ordered_events: [reach_door, pause, head_turn_only, brief_final_gaze, face_forward, exit]
gaze_phases: [away_from_lens, brief_final_lens_contact]
screen_direction: toward_exit
camera_operations: [static]
omitted_events: [corridor_walk]
final_state: exited_room
creative_choices:
  lens_family: normal_portrait
  light_softness: soft
```

Locked entries are copied or deterministically serialized. An LLM may propose values only for keys present in `creative_envelope.allowed`.

## Semantic-check record

```yaml
contract_id: intent_S07_v1
contract_sha256: <verified-contract-hash>
compiler_intermediate_sha256: <verified-ir-hash>
runtime_prompt_sha256: <verified-prompt-hash>
checker_version: <version-or-commit>
status: pass
hard_failures: []
warnings: []
checked_at: <timestamp>
```

Required deterministic checks:

- contract/storyboard revision and hashes match the approved artifacts;
- required events are present once and in order;
- no forbidden or unapproved narrative event is added;
- gaze phases, direction, camera locks, omissions and final state match;
- creative choices use only allow-listed keys;
- target compiler/model/version is recorded;
- prompt/check hashes match the submitted files;
- a check is invalidated whenever the contract, intermediate or prompt changes.

Run the maintained checker from the runtime repository:

```powershell
python tools/video_intent_contract.py `
  --contract <intent-contract.json> `
  --compiler-ir <compiler-ir.json> `
  --storyboard <approved-storyboard-file> `
  --prompt <runtime-prompt.txt> `
  --out <semantic-check.json>
```

Text lint may catch model vocabulary that contradicts a lock, such as `orbit` under a static camera contract or `occasionally glances` under a delayed-gaze contract. Lint is a backstop, not the primary semantic representation.

## Submission and override

A storyboard-derived job must not enter a renderer queue without a matching approved contract and passing check. The gate belongs at the shared renderer-job boundary so local and external backends receive the same protection.

An override requires:

- explicit human approval;
- actor and timestamp;
- reason and affected fields;
- prior contract ID/hash;
- new contract revision/hash when meaning changes;
- a new semantic check over the new compilation.

An agent cannot self-approve an override merely because a model is unlikely to follow the current contract.

## Render review and editing

Render review records both axes—Intent Fidelity and Cinematography Gain—and attributes defects to `storyboard`, `compiler`, `renderer`, or `edit`. Human review remains authoritative for moving-image meaning until verified automation exists.

Every selected Clypra interval records its source clip and time range, inherits the relevant events/states from the parent contract, and receives `pass`, `fail`, or `needs_human_review`. A segment that violates the shot's meaning is not accepted solely because it is visually strong.
