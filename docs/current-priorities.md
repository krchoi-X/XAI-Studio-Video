# Current Priorities — XAI-Studio-Video

Updated: 2026-08-25

## P0 — Codex-controlled Hermes Character Manager

- Source: GitHub issue #2
- Status: `IN PROGRESS` — schema, deterministic control CLI, tablet review/generation, Prompt Trace, Hermes skill, and Jung Hae-won/Harim migrations implemented
- Next action: operate and refine the Hermes night-batch loop, then add automatic first-pass curation and tablet batch controls

The current user-directed priority is practical Hermes delegation: structured batches, local sequential generation, durable outputs, tablet review, and feedback-driven DNA proposals. Repository validation, Stable DNA hashing, Scene Spec precedence, promotion rules, and indexing remain deterministic and Codex-controlled. See `docs/character-manager.md`.

This file is the project-local execution handoff. It should reflect what is most useful to do next, not everything that is technically interesting.

## Operating principle

The current bottleneck is not lack of architecture ideas. Too many parallel tracks have accumulated while local generation is too slow for casual practice and RunPod/Vast lifecycle operation is still not routine. Character DNA is also not yet mature enough to justify treating it as a prerequisite for making content.

For now, use **one planned main task + one lightweight content lane**:

1. Main task: make one cloud 5090 production path repeatable from start to finish.
2. Content lane: when spare time appears, make something small with the current tools instead of opening a new infrastructure/design project.

Do not promote a new research/architecture item to P0 unless it directly blocks the main task.

## P0 — Build operational fluency with one repeatable RunPod 5090 content loop

- Priority: `P0`
- Status: `READY`
- Owner: `Codex + Manual`

### Context

The user can already provision and use RunPod/Vast, but the sequence is not yet familiar enough to feel effortless. As a result, each cloud session carries setup friction and the user falls back to the local RTX 4070, where H3/video generation is too slow for casual creative practice.

At the same time, the project has accumulated many worthwhile tracks: Character DNA, H3 adapters, toyxyz patterns, WanGP, Render Broker, Vast/RunPod automation, upscale, multiple model experiments, and UI ideas. Continuing to expand all of them now increases coordination cost without increasing the number of finished pieces.

RunPod is the first provider to practice because the user already has an account, balance, prior Pod experience, and a network volume. Vast remains a later portability target, not a simultaneous learning task.

### Priority rationale

This outranks `h3_intent` schema work and additional renderer architecture because the practical bottleneck is **getting from an idea to a finished artifact without setup hesitation**.

A perfect cloud abstraction is less valuable right now than being able to repeat the same known path reliably. Once the user has a stable operational loop, automation and provider abstraction can be added based on observed friction rather than anticipated friction.

### Success criterion

Demonstrate the same basic cycle repeatedly with a known workflow:

1. choose the known RunPod template / GPU / network volume;
2. deploy the Pod;
3. verify the expected workspace, models, and UI/endpoint;
4. run one predetermined small content job;
5. save the exact prompt/settings and resulting artifact;
6. copy/register the result in durable local/Drive storage;
7. verify the result is recoverable outside the Pod;
8. terminate the Pod cleanly and confirm no unintended billable compute remains.

The first goal is not maximum image/video quality. The goal is that the lifecycle becomes boring and predictable.

### Depends on

- Existing RunPod account and network volume.
- One known-good generation workflow already present or easy to restore.

### Blocks

- confident 5090 experimentation;
- casual content production without falling back to the slow 4070;
- later automation of provisioning/cleanup;
- meaningful RunPod-vs-Vast comparison based on actual repeated use.

### Codex next action

Reduce the current RunPod path to a **single operator runbook/checklist** using the existing repo assets. Reuse the existing Render Broker / GPU worker work where it helps, but do not make automation a prerequisite.

The runbook must state:

- what template/environment to choose;
- what persistent storage to attach;
- where models/workspace/results live;
- how to verify readiness;
- the exact minimal test job;
- where the result is copied or registered;
- how to verify billing/cleanup before ending the session;
- what to do when the desired 5090 is unavailable.

Prefer a manual-but-repeatable checklist first. Automate only steps that prove annoying across repeated real sessions.

### Not now

Do **not** make the following prerequisites for this P0:

- completing Character DNA;
- implementing a new H3 timeline UI;
- implementing `h3_intent` schema;
- supporting both RunPod and Vast at once;
- full Render Broker auto-provisioning;
- perfect one-click orchestration;
- testing every H3 checkpoint/LoRA/upscaler.

## Lightweight content lane — make small finished things with current capability

This is deliberately **not another engineering project**.

When the user has a spare creative window, use an existing acceptable character/reference image and a known workflow to make a small finished artifact: a short everyday clip, simple visual gag, mood shot, micro-vlog beat, or other low-dependency piece.

Rules:

- Character DNA completion is not required.
- Do not redesign the pipeline before creating the piece.
- Prefer one character, one location, one beat, one short clip.
- Reuse existing references/prompts/workflows.
- If the result is good, keep it as content even if the underlying system is imperfect.
- If it fails, record only the failure that is likely to recur; do not turn every failure into a new architecture project.

After several real pieces exist, use their repeated failures to decide what Character DNA or workflow automation actually needs to solve.

## Completed / deferred architecture work

### toyxyz MiniMax-H3-prompter review — COMPLETE

Static review is complete in `docs/toyxyz-h3-prompter-review.md` with decision `borrow-pattern-only`. Keep the result as reference; it is no longer the active P0.

### `h3_intent` adapter schema — DEFERRED

This remains a sensible next architecture step after the operational loop is routine, but it does not currently block making content.

### Vast provider routine — DEFERRED

Practice Vast after the RunPod lifecycle is familiar enough that the comparison is between two known workflows rather than two sources of friction.

## Handoff maintenance rule

When priorities change, keep this document deliberately short and execution-oriented. Broad research history belongs in `personal-ai-knowledge`; this file should answer only: **what is the one planned task now, why is it first, and what should not distract from it**.
