# Specialized Skill Router

Specialized definitions resolve through `python tools/shared_resources.py --skill <name>` when shared authority is active. Read the returned source and its adjacent references. Project entrypoints are adapters; edit the shared source. Runtime tools, schemas and application contracts remain dependencies in this checkout.

Use the root `SKILL.md` for the general XAI-Studio-Video production framework. Load specialized skills only when the task requires them.

## Available skills

### `idea-to-production`

Path: `skills/idea-to-production/SKILL.md`

Use when a natural-language content idea should become 2–3 directing alternatives, an explicitly chosen low-cost sample, and then a reviewed final render. It owns the durable v1 contract flow and Prompt Trace, but never edits Character DNA or resolves an asset ID by guessing a filesystem path.

Use `storyboard-director` alone when the user only wants story, beat, pacing, or shot design without starting a production request. Use `idea-to-production` when those choices must continue through sample and final production.

### `screenplay-to-storyboard`

Path: `skills/screenplay-to-storyboard/SKILL.md`

Use when an external writer has already supplied a screenplay or scenario and Hermes must convert one exact source revision into a separately versioned production storyboard. It separates story locks from staging proposals, records staging changes, runs pre-render checks, and preserves source/parent hashes. It stops before Intent Contract compilation or rendering.

### `storyboard-director`

Path: `skills/storyboard-director/SKILL.md`

Use when a rough or incompletely expressed idea must be aligned visually with the user and become an approved director-style Storyboard Spec before expensive image/video generation.

It owns:

- interpretation of dramatic intent
- Beat Sheet creation
- Narrative Tempo Map creation
- emotional hold / reveal / acceleration decisions
- shot or panel scale decisions
- emotional pacing
- annotated panel/shot planning
- rough storyboard rendering prompt creation
- visual intent comparison without requiring film terminology from the user
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
→ one or two low-cost visual hypotheses when useful
→ Storyboard Spec Draft 0 + user visual revision
→ Approved Storyboard Spec
        ├─ video flow → root XAI-Studio-Video → model adapter
        ├─ graphic-novel/comic flow → panel/layout adapter → image renderer
        └─ illustration-sequence flow → selected-frame renderer
```

For an executable production request:

```text
natural-language production idea
→ idea-to-production
→ 2–3 storyboard candidates
→ explicit user choice
→ low-cost sample
→ per-shot review
→ final render
```

For an external writer scenario:

```text
versioned scenario source
→ screenplay-to-storyboard
→ Hermes Storyboard Draft 0 + preflight + change log
→ user review
→ approved Storyboard Spec + Intent Contract
→ storyboard-cutboard and renderer adapter
```

The Storyboard Spec is the source of truth. Rough storyboard images are replaceable visualization artifacts.

The storyboard skill plans **story, time, attention, emotion, composition, and continuity**. Downstream skills remain responsible for medium-specific motion, identity enforcement, rendering, model adapters, recovery, and evaluation.
