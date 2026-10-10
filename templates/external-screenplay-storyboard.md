---
schema_version: 1
artifact_type: screenplay_storyboard
storyboard_id: sb_<SCENARIO-ID>_<lineage>
revision: 1
status: draft
source_scenario:
  path: scenarios/<SCENARIO-ID>-<slug>.md
  scenario_id: <SCENARIO-ID>
  revision: 1
  sha256: <source-file-sha256>
parent_storyboard: null
author:
  actor: hermes
  model: <selected-model>
created_at: <ISO-8601 timestamp>
---

# <Title> — Hermes Production Storyboard

## Source and review state

- Source scenario:
- Source revision:
- Storyboard revision:
- Status: Draft 0
- Optional world/lore files:
- Optional production brief:
- Production scope: full / partial / teaser
- Included source scenes/beats:
- Intentionally unproduced scenes/beats:
- Selected directing skill/reference IDs:
- Assumptions:
- Unresolved questions:

## Story locks

| Lock ID | Source scene/locator | Locked meaning | Why it matters |
|---|---|---|---|
| L01 | | | |

Include event order, causality, who knows what and when, ending, dialogue, mandatory information and prohibited reveals.

## Staging proposals and ambiguities

| Item ID | Source scene/locator | Source wording or summary | Classification | Hermes treatment |
|---|---|---|---|---|
| ST01 | | | staging_proposal / ambiguous | retain / restage / ask |

## Scene analysis

### Scene <source scene ID>

- Dramatic purpose:
- Entry state:
- Ordered events:
- Exit state:
- Character motivation and emotional change:
- What the viewer must understand by the end:
- Visual evidence required:
- Story locks used:
- Source contradiction or uncertainty:
- Directing strategy:

## Shot plan

### Shot <SHOT-ID>

- Source mapping: `<scene ID>/<beat or source locator>`
- Expected duration or relative weight:
- Narrative purpose:
- What the viewer must understand by the end:
- Screen start state:
- Location and camera setup:
- Framing and information scale:
- Ordered visible actions:
  1.
- Dialogue, sound and silence:
- Screen end state:
- Link to next shot:
- Emotion and directing intent:
- Story locks carried:
- Must not show:
- Production difficulty:
- Allowed alternative staging:
- Required references and their roles:
- Clean start/end keyframes required:
- Critical-information preview stills: reveal / reaction cause / new-element source / none
- Preflight: pass / revise / blocked

## Continuity and production preflight

| Shot | Legibility | Cause | Source | Space/setup | Contradiction | In-range scope | Action fit | Lock protection | Result |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Reference and keyframe plan

| Shot/setup or information moment | Target aspect | Identity reference role | Location/prop role | Preview purpose | Start/key information/end frame | Re-anchor note |
|---|---|---|---|---|---|---|
| | | | | setup / reveal / cause / source / continuity | | |

Exact approved paths and hashes are added later to the production plan. Do not invent unresolved asset paths here.

## Hermes staging change log

| Change ID | Source locator | Affected shots | Category | Before | After | Lock preserved | Rationale |
|---|---|---|---|---|---|---|---|
| C01 | | | legibility / cause-shot / source-clarification / feasibility / continuity / contradiction-fix / scope-coverage | | | yes / no | |

If `Lock preserved` is `no`, the storyboard remains blocked until the user approves a scenario or lock revision.

## Scenario change proposals

| Proposal ID | Source scene | Problem | Proposed scenario change | Effect on intent | Approval required |
|---|---|---|---|---|---|
| | | | | | yes |

Do not silently apply these proposals to the storyboard.

## Writer-facing feedback summary

Write this so the user can pass it directly to the external writer.

| Request ID | Source scene/lock | Problem visible in production planning | What Hermes needs clarified or revised | Why staging alone cannot solve it |
|---|---|---|---|---|
| W01 | | | | |

## Source-to-shot coverage

| Source scene/beat/lock | Covered by shot(s) | Status | Notes |
|---|---|---|---|
| | | covered / blocked / missing | |

List source beats outside a declared partial/teaser production range as `intentionally_unproduced`, not `missing`.

## Render-review attribution handoff

If a later render review assigns the top-level defect owner `storyboard`, it must also record:

- subtype: `source_scenario` or `hermes_staging`;
- source scene/locator when subtype is `source_scenario`;
- Hermes staging change-log ID when subtype is `hermes_staging`.

## Review state

- Accepted shots:
- Shots to revise:
- Blocked story-lock decisions:
- Preflight result:
- Ready for joint Storyboard + Intent Contract approval: no

The adjacent `<storyboard-name>.preflight.json` is mandatory. Markdown self-assessment is advisory; only `tools/storyboard_preflight.py validate` may report deterministic readiness.
