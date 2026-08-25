# toyxyz MiniMax-H3-prompter architecture decision

**Status:** P0 static review complete

**Reviewed:** 2026-08-25

**Upstream:** `toyxyz/ComfyUI_toyxyz_test_nodes` at `9c86150264e5675710897074c5100551e2240cbc`

## Decision

Choose **borrow-pattern-only**, with an optional later runtime trial of the unmodified node behind an adapter boundary.

Do not fork it now, do not vendor the repository, and do not build a competing H3 timeline UI yet. First use its proven project schema, validation boundaries, frame-grid logic, reference routing, and tests to define a smaller renderer-neutral H3 intent contract for XAI-Studio-Video. Hermes remains the authoring agent and the Recorder remains the run-history authority.

This decision supersedes the earlier review of the separately supplied `Ultra MiniMax H3 Prompt V3.50` ZIP. That package is related research, but it is not the P0 GitHub implementation named by `docs/current-priorities.md`.

## Verified architecture

### Shot and timeline schema

- Frontend state is serialized as one versioned `project_data` JSON document.
- A project contains an overall request, constraints, requested duration, ordered shots, references, model choice, enhancement flags, and the last successful enhanced prompt.
- Each current shot is deliberately small: stable ID, duration, and one unified natural-language `visual_action` field.
- Older separate dialogue, visible-text, sound, camera, and transition fields are migrated into `visual_action` during normalization.
- Shot durations are fitted to the requested duration and the output is aligned to MiniMax H3's 24 fps `17k+5` frame grid.
- Later shot boundaries create cuts; image anchors inside a shot are continuous states and do not create implicit cuts.

This is simpler than XAI-Studio's Master Creative Spec. It is best treated as a renderer-side projection of Shot Graph, Camera DNA, Motion DNA, Audio DNA, and constraints—not as their replacement.

### Reference asset schema

Each reference records:

- stable ID and media type
- semantic role
- optional `@alias`
- strength for subject images
- uploaded-file identity
- source duration and trim start
- target timeline placement or exact frame index
- user description for applicable video/audio relationships

Supported roles are intentionally bounded:

- image: first frame, last frame, exact frame, subject identity
- video: editing, continuation, motion, camera, cuts/rhythm, or no preset
- audio: full/partial signal copy, voice/delivery, dialogue/lyrics, sound/ambience, music/rhythm, or no preset

References are numbered independently by media type and emitted in downstream slot order. The implementation validates per-type and total limits. This is a strong candidate for our adapter contract, but XAI-Studio should retain its richer evidence/intent distinction: observed source facts and requested target treatment must not collapse into one description.

### H3 mode routing

`AUTO` resolves only exact layouts:

- no references → T2VA
- one first-frame image → I2VA
- first-frame then last-frame images → FL2VA
- one last-frame image → L2VA
- every other reference layout → REF2VA

Explicit mode selection remains available, and validation rejects incompatible required anchors. This exact-layout rule is worth borrowing because it does not silently ignore extra or reversed references.

### Prompt compiler and constraint layers

The backend performs distinct stages even though they live in one Python module:

1. normalize/migrate versioned project JSON
2. resolve mode and align duration
3. validate aliases, durations, roles, counts, and mode contracts
4. compile a deterministic raw project plan
5. construct mode-specific LLM/system prompts from JSON configuration
6. optionally analyze visual references and expand with Qwen3.8-27B + Vision, or use the lighter H3 rewriter for non-REF2VA modes
7. normalize and semantically validate the generated H3 prompt
8. expose prompt, aligned length, and ordered media outputs

Notable constraints cover action progression, hand/object/contact continuity, observable locomotion, endpoint alignment, reference-medium/style authority, dialogue preservation, speaker IDs, audio routing, and refusal to invent unsupported reference facts.

### Outputs and downstream interface

The ComfyUI node exposes:

- latest successful generated prompt
- aligned frame count
- ordered image outputs plus exact frame indices
- trimmed/resampled video outputs
- trimmed audio outputs

The last successful prompt is preserved while the user edits inputs and is replaced only after successful generation. That transactional behavior should be borrowed by Recorder: a failed compile or render must create a failure event without overwriting the last accepted artifact.

### Separation and coupling

There is a useful serialized boundary: the JS editor owns `project_data`; Python re-normalizes and validates it authoritatively. System prompts are external JSON files and the tests exercise migrations, routing, compiler semantics, frontend behavior, enhancement, and media output.

However, runtime concerns remain highly coupled:

- the 2,047-line frontend is a custom one-node editor
- the 4,337-line backend combines schema migration, validation, prompt compilation, LLM server/model download, Vision analysis, upload resolution, ffmpeg processing, media trimming, API routes, and ComfyUI node execution
- the node returns fixed maximum media slots using flexible output types
- selected Qwen/LightX2V model IDs and llama.cpp execution are embedded in the implementation

This is effective as a self-contained ComfyUI tool but does not match XAI-Studio's desired separation between model-agnostic creative truth, Hermes compilation, Recorder history, and interchangeable local/pod render adapters.

## Option comparison

| Option | Maintenance burden | Upstream coupling | Duplicate code avoided | Storyboard / VIDEO-DNA compatibility |
| --- | --- | --- | --- | --- |
| `reuse` unmodified behind an adapter | Medium; upstream updates and ComfyUI compatibility still need tracking | High at the UI/project/model-execution layer | High for H3 UI, compiler, reference handling, and local enhancement | Medium. Master Spec must be projected into its compact shot JSON, and Recorder must wrap it externally. |
| `fork/adapt` | Very high; a large JS/Python surface plus GPL-3.0 fork maintenance | Medium-high | Initially high, but divergence quickly creates duplicated maintenance | Medium-high only after significant decomposition; not justified before runtime evidence. |
| `borrow-pattern-only` | Low to medium; implement only the stable contracts we need | Low | Medium; avoids repeating discovered schema/routing mistakes but not implementation work | High. Hermes, Master Spec, VIDEO-DNA, Recorder, and provider-neutral adapters remain authoritative. |

## Patterns to borrow

1. Versioned H3 intent JSON with explicit migrations.
2. Exact-layout Auto mode routing plus explicit override and validation.
3. `asset + role + strength + timeline placement`, extended locally with separate source evidence and target instruction.
4. Deterministic `17k+5` alignment and explicit requested-versus-effective duration.
5. Shot boundaries separated from in-shot frame anchors.
6. Stable last-successful-prompt semantics.
7. Prompt/system rules in versioned configuration rather than UI code.
8. Normalization, blocking validation, deterministic compilation, optional LLM expansion, and post-expansion semantic validation as separate stages.
9. Upstream tests as a behavioral checklist for our adapter, particularly mode routing, alias boundaries, reference order, duration fitting, dialogue preservation, reference overreach, and physical continuity.

## Do not copy into the canonical architecture

- the monolithic ComfyUI editor as the only source of project truth
- automatic model downloading as part of prompt compilation
- fixed Qwen3.8 or LightX2V model choices in the Master Spec
- transient visual analysis mixed with durable user intent
- fixed maximum output sockets as the cross-provider render contract
- browser state or ComfyUI workflow state as the run-history database

## Next implementation decision

The next step is not another H3 UI. Define a small `h3_intent` adapter schema and map one existing Master Creative Spec into it. Then compare:

1. our deterministic compiler output,
2. toyxyz's raw compiler output, and
3. toyxyz's optional enhanced output.

Use the same 12-second, multi-shot, two-character case with at least one image reference and preserved dialogue. Record prompt differences and one real render result before deciding whether an unmodified toyxyz runtime adapter is worth maintaining.

## Verification performed

- Inspected the upstream Python node/compiler, JS editor, both system-prompt JSON files, README, GPL-3.0 license, and test suite at the pinned commit.
- Ran all 138 upstream unit tests in the available bundled Python environment.
- 128 tests passed.
- 10 media-output tests could not run because that isolated Python environment lacks `torch`; all reported errors were `ModuleNotFoundError: torch`, not assertion failures.
- No model was downloaded, no ComfyUI node was installed, and no runtime integration was performed.
