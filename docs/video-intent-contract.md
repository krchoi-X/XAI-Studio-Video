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

The Production Director authors the storyboard, contract, v2 `prompt_segments`, and any required engine prompt profile together. In the default local role split this author is Hermes. Do not extract a supposedly authoritative contract later from prose without human review; that only moves reinterpretation to another hidden step. Optional frontier Creative Treatment is upstream context, not a substitute for this joint production approval.

## Minimum packet

```yaml
schema_version: 2
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
  prompt_segments:
    subject_definition: One woman at the door, carrying nothing.
    scene_definition: A quiet room with the exit visible.
    event_lines:
      reach_door: She reaches the door.
      pause: She pauses.
      head_turn_only: She turns only her head.
      brief_final_gaze: Only at the final moment, she briefly looks into the lens.
      face_forward: She faces forward again.
      exit: She exits the room.
    gaze_line: Before the final moment she looks away; lens contact occurs only at the end.
    direction_line: She moves toward the exit throughout.
    camera_line: Static camera; no push-in and no orbit.
    final_state_line: She has exited the room.
    omission_line: Do not show a corridor walk, object pickup, full-body turn, or return.
  engine_prompt_profiles:
    h3_ref2va_v1:
      subject_definitions: <Subject 1> is the woman in <Picture 1>, preserving her exact identity and appearance.
      summary: Place <Subject 1> in the approved departure scene.
      retention_analysis: '<Subject 1> (appears in [Shot 1]): fully_preserved - identity and wardrobe remain unchanged.'
      detailed_description: '[Shot 1] A {{lens_family}} view. She reaches the door. She pauses. ...'
      overall_soundscape: Quiet room tone, footsteps, and one door sound; no speech.
      non_diegetic_music: None.

creative_envelope:
  level: L1
  allowed: [lens_family, light_softness, depth_of_field, foreground_layering]
  allowed_values:
    lens_family: [normal_portrait, short_telephoto]
    light_softness: [soft, diffused]
    depth_of_field: [moderate, shallow]
    foreground_layering: [none, subtle_doorframe]
  forbidden: [push_in, orbit, added_actor_action]

feasibility:
  decision: SHOW
  rationale: one actor, one location, one ordered action chain

unresolved: []
approval:
  approved_by: user
  approved_at: <timestamp>
```

Schema v2 is the required format for new work because it adds deterministic prompt segments and enumerated creative values. Schema v1 remains readable for historical records but does not prove prompt meaning and must not be used for a new faithful-execution claim.

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
prompt_template_version: h3-ref2va-v1
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

Locked entries, including director-approved prompt prose and engine profile, are copied exactly. An LLM may select only values listed under the matching `creative_envelope.allowed_values` key. The versioned engine adapter renders the complete prompt; there is no free-text post-processing stage.

`intent-prompt-v1` is a generic adapter, not valid H3 renderer syntax. Exact H3 Ref2VA targets require `h3-ref2va-v1` and its six approved sections; exact H3 FL2VA targets require `h3-fl2va-v1` and its three approved sections. The compiled H3 prompt omits management metadata such as target model, template ID, hashes, and creative-choice field names. Those stay in the compiler intermediate and semantic-check record. Audio and music remain explicit approved fields. Every ordered event line must occur exactly once and in order inside `detailed_description` or `integrated_multimodal_description`.

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
- creative choices use only allow-listed keys and enumerated values;
- every ordered event has exactly one approved prompt line;
- the runtime prompt exactly equals the versioned deterministic rendering;
- target compiler/model/version is recorded;
- prompt/check hashes match the submitted files;
- a check is invalidated whenever the contract, intermediate or prompt changes.

Run the maintained checker from the runtime repository:

```powershell
python tools/video_intent_contract.py `
  --contract <intent-contract.json> `
  --compiler-ir <compiler-ir.json> `
  --storyboard <approved-storyboard-file> `
  --render-prompt <runtime-prompt.txt> `
  --out <semantic-check.json>
```

Use `--prompt` instead of `--render-prompt` only to verify an already generated file. Substring lint is not an enforcement mechanism: it produces false positives for phrases such as “no push-in” and misses synonyms such as “dolly toward.” Exact template equality and enumerated creative values replace that ambiguity.

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

Render review records both axes—Intent Fidelity and Cinematography Gain—and attributes defects to `storyboard`, `compiler`, `renderer`, or `edit`. For an external-scenario workflow, a `storyboard` defect also records subtype `source_scenario` or `hermes_staging` and cites the source locator or Hermes staging change-log ID. This preserves the established top-level vocabulary while keeping writer and director evaluation separate. Human review remains authoritative for moving-image meaning until verified automation exists.

Every selected Clypra interval records its source clip and time range, inherits the relevant events/states from the parent contract, and receives `pass`, `fail`, or `needs_human_review`. A segment that violates the shot's meaning is not accepted solely because it is visually strong.
