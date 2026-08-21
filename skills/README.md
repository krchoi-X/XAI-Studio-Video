# Specialized Skill Router

Use the root `SKILL.md` for the general XAI-Studio-Video production framework. Load specialized skills only when the task requires them.

## Available skills

### `storyboard-director`

Path: `skills/storyboard-director/SKILL.md`

Use when a rough idea must become a director-style storyboard draft before video generation.

It owns:

- interpretation of dramatic intent
- Beat Sheet creation
- Tempo Map creation
- long-hold / slow-motion decisions
- shot scale and camera-energy decisions
- emotional pacing
- annotated panel planning
- storyboard-image prompt creation
- iterative revision with the user
- handoff of approved storyboard timing to video-model prompts

Read together with:

- `docs/storyboard-directing.md`
- `templates/storyboard-draft.md`

Do not load this skill for a simple single-shot prompt that does not need storyboarding or pacing design.

## Routing principle

```text
rough story / scene idea
→ storyboard-director
→ approved storyboard draft
→ root XAI-Studio-Video production flow
→ model adapter
→ runtime prompt
```

The storyboard skill plans **time, attention, emotion, and shot structure**. The general video skill remains responsible for full production constraints, identity, motion, references, adapters, generation, recovery, and evaluation.