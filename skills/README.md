# Specialized Skill Router

Use the root `SKILL.md` for the general XAI-Studio-Video production framework. Load specialized skills only when the task requires them.

## Available skills

### `storyboard-director`

Path: `skills/storyboard-director/SKILL.md`

Use when a rough story or scene idea must become a director-style Storyboard Spec before expensive image/video generation.

It owns:

- interpretation of dramatic intent
- Beat Sheet creation
- Narrative Tempo Map creation
- emotional hold / reveal / acceleration decisions
- shot or panel scale decisions
- emotional pacing
- annotated panel/shot planning
- rough storyboard rendering prompt creation
- iterative revision with the user
- medium-neutral Storyboard Spec maintenance
- handoff to video, graphic-novel/comic, or illustration workflows

Read together with:

- `docs/storyboard-directing.md`
- `docs/storyboard-rendering.md`
- `templates/storyboard-draft.md`

Do not load this skill for a simple single-shot prompt that does not need story, sequencing, or pacing design.

## Routing principle

```text
rough story / scene idea
→ storyboard-director
→ Storyboard Spec Draft 0
→ user revision
→ Approved Storyboard Spec
        ├─ video flow → root XAI-Studio-Video → model adapter
        ├─ graphic-novel/comic flow → panel/layout adapter → image renderer
        └─ illustration-sequence flow → selected-frame renderer
```

The Storyboard Spec is the source of truth. Rough storyboard images are replaceable visualization artifacts.

The storyboard skill plans **story, time, attention, emotion, composition, and continuity**. Downstream skills remain responsible for medium-specific motion, identity enforcement, rendering, model adapters, recovery, and evaluation.