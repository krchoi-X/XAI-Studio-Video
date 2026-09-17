# Codex Handoff — Contact Motion / Physical Gag Routing
Last updated: 2026-09-17

## Purpose

When implementing the Director Core / Skill Router, treat `contact_motion` and `physical_gag` as first-class specialist pattern families.

These scenes should not be handled as generic action, generic vlog, or generic comedy because they require explicit tracking of multi-person physical relationships over time.

## Route when relevant

Use this route for scenes such as:

- martial arts / sparring;
- wrist grabs, catches, turns, controlled force transfer;
- pilates or posture correction;
- partner dance / body guidance;
- one person catching or supporting another;
- trip-and-recover comedy;
- impossible everyday physical gags involving props or food.

## Required constraint skills

Prefer selective loading of:

- `multi_actor_blocking`
- `hand_state_continuity`
- `contact_point_continuity`
- `prop_state_choreography`
- `action_decomposition`
- `spatial_continuity`
- `locked_end_state`
- `reaction_timing`
- `stylized_physics_lock` when the gag intentionally violates normal physics

Do not load unrelated travel, dance, vlog, or cinematic reference packs unless they are independently justified by the episode.

## State-based representation

For difficult physical interaction, the internal storyboard should represent:

```text
initial state
→ preparation
→ contact established
→ core movement / force transfer
→ resulting state
→ release / settle
```

Where useful, add fields such as:

```yaml
left_hand_state:
right_hand_state:
contact_points:
prop_owner:
prop_location:
physical_connection:
locked_end_state:
micro_beats:
```

Prefer one clear state transition per shot or beat.

## Renderer / LoRA watch candidate

Record the following as an optional specialist candidate, not a default:

- `AfterMidnight-MiniMax-H3-NSFW`
- Source: https://huggingface.co/SexGod1979/AfterMidnight-MiniMax-H3-NSFW

Project interest is primarily whether it improves **contact-heavy human motion**, not its NSFW label.

Potential A/B targets:

- martial-arts wrist contact;
- pilates posture correction;
- partner guidance;
- support/catch motion;
- close-range physical gag recovery.

Do not assume it improves general motion. Promote it only after repeatable A/B evidence against base H3 Ref2VA.

See:

- `docs/director-memory/patterns/contact-motion-and-physical-gags.md`
- `docs/models/minimax-h3-lora-watchlist.md`

## Implementation rule

The correct architecture is:

```text
scene classification
→ selective skill routing
→ structured state-based storyboard
→ renderer-specific prompt compilation
→ optional specialist LoRA
→ A/B evaluation
→ record real success/failure evidence
```

Do not make the LoRA, a giant freeform prompt, or any one example the canonical directing representation.
