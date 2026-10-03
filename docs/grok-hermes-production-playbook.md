# Grok/Hermes character image/video production playbook

Use this when routine or credit-sensitive image/video production is delegated to Grok Bot or Hermes. It is an operator checklist, not permission to generate. The current user request and explicit GO gates still control spending and rerenders.

Canonical policy remains [AGENTS.md](../AGENTS.md), [artifact and review contract](artifact-and-review-contract.md), the host entrypoint, and the catalog-resolved production skill. If this playbook conflicts with those sources, follow the current authority and record the conflict.

## 1. Role and attribution

Keep these facts separate:

| Fact | Meaning | Example |
|---|---|---|
| requester | actor that submitted or relayed the production request | `grok` or `hermes` |
| executor | process that performed the render | `local-wangp-worker` |
| engine | rendering system/provider | `WanGP` |
| model | exact installed model/checkpoint ID | `minimax_h3_ref2va_pruned` |
| planning/review model | model that wrote or reviewed the plan | record in a production note when supported |

Do not put `hermes` into `requested_by` merely because Hermes orchestrated a request from Grok, or put `grok` into `executor` when the local worker rendered it. If the current schema has no orchestration field, state the relay in `Spec.md` or a production note without changing the meaning of existing fields.

Before the first WanGP submission, register the session with `tools/wangp_recorder.py session`. Store the exact user request, not a reconstructed intention. Submit runs below that session's `runs/` directory and close the session as `completed` or `failed`. See [WanGP recorder](wangp-recorder.md) and [Grok recording note](grok-production-recording-note.md).

For new character-video or multi-pack production, create an approved
`shot-production-plan-v2.json` (start from
[`lia-pack-contract-v2.json`](../tests/fixtures/shot-production-plan/lia-pack-contract-v2.json)), validate it, then
register it with the session:

```powershell
python tools/shot_production_plan.py validate --plan <session>/shot-production-plan-v2.json --json
python tools/wangp_recorder.py session --session-dir <session> --requested-by hermes `
  --engine WanGP --model minimax_h3_ref2va_pruned --character-id ch-lia `
  --title "<short title>" --user-request "<exact request>" --status running `
  --production-plan <session>/shot-production-plan-v2.json
```

The v2 file is the execution contract, not an informal note. Each chunk gets a unique `prompt_id`, its exact ordered
reference packet, forbidden earlier-state tags and cast IDs. Each character contract freezes the canonical record
path, version, Stable-DNA hash and literal mandatory prompt terms. A later pack uses an accepted boundary frame and
must not keep an earlier sit/pose reference unless that state is intentionally required.

## 2. Resolve current authority before writing prompts

1. Run the workspace governance initialization required by the host entrypoint.
2. Resolve characters and shared skills through the active shared-resource catalog.
3. Read the current canonical character record, not a copied legacy snapshot.
4. Freeze the skill source and character DNA used for the run. Do not edit either halfway through production.
5. Record in the session Spec or production note:
   - canonical character ID for every cast member;
   - character record path, version and Stable DNA hash;
   - selected identity/body/wardrobe/pose references and their roles;
   - reference source paths and hashes when the producer does not snapshot them automatically;
   - exact engine/model and prompt mode.

`character_id` alone is not proof that Stable DNA reached the renderer. Before submitting, inspect the final prompt and settings that the engine will actually receive.

## 3. Build an identity contract per character

For each cast member, make a compact table before writing the shot prompt.

| Field | Required content |
|---|---|
| identity source | character ID, DNA version/hash, selected face master |
| mandatory recognition anchors | features that must remain visible and stable |
| bounded state | allowed hair state, wardrobe, age/presentation and scene-specific changes |
| prohibited substitutions | another cast member's face, clothes, accessories or body reference |
| reference roles | face, body, wardrobe, pose, scene, first frame, last frame |
| visibility risk | whether the shot can actually show a small anchor such as a bracelet |

Then check the compiled prompt against the table. A mandatory recognition anchor must not be downgraded to vague wording or contradicted by a scene line.

Example: Suan's rounded updo and large black-and-white ribbon are identity anchors. A line such as `natural morning hair Soft` conflicts with that contract unless the user explicitly selected a different bounded hair state. Lia's three thin red-and-blue bracelets belong on her anatomical right wrist; a reference showing them on the other wrist contradicts the text lock.

Written DNA and pixel identity are complementary:

- Text defines the invariant and tells the renderer how references should be interpreted.
- A face/body master supplies the visual identity that prose alone cannot pin.
- A pose or wardrobe reference must not silently become the identity master.
- Scene overrides may change allowed bounded state, but do not edit canonical DNA.

### Still-image rule: DNA is mandatory even when the task looks simple

This rule applies to ordinary character stills, wardrobe-library fills, and image-to-image edits—not only video.

- Resolve the canonical character record for every still request and compile the actual Stable DNA text into the final engine prompt. A `character_id`, filename, or conversational mention of the character is not a substitute.
- Record the character record path, version, Stable-DNA hash, and the exact compiled prompt in the prompt trace. If the trace cannot prove that DNA reached the renderer, stop before spending credits.
- Treat collected wardrobe, pose, camera, and scene prose as a **Scene Delta**. It may be long and may override only the requested mutable fields; it never replaces or paraphrases away Stable DNA.
- Do not silently shorten a long prompt to fit a chat box. Preserve the verbatim request in durable input and use typed operation fields or an attached prompt file when the host supports them.

There are two different still workflows:

1. **New scene from character DNA**: Stable DNA is mandatory. Add only references whose visual role is needed, and record any deliberate decision not to use a pixel master.
2. **“Transform this image” / “이 이미지에서 변형”**: both Stable DNA **and the exact selected source image** are mandatory. Bind the source path, asset ID, role, byte count, and SHA-256. Do not fall back to text-to-image or swap in the newest face image.

Before submission, read the final compiled prompt—not only the user's input—and verify this order: exact selected source contract, canonical Stable DNA, requested Scene Delta, explicit operations, then preservation locks. A pose or outfit paragraph must never be interpreted as the character definition.

## 4. Inspect reference pixels, not filenames

Before spending GPU time, visually inspect every selected reference.

### Required checks

- Correct person and intended character role.
- Anatomical left/right, not screen-left/screen-right or a filename claim.
- Mandatory accessories are present on the correct side.
- Face, body and hair match the intended character state.
- Wardrobe/reference leakage is explicitly accepted or excluded.
- Native composition matches the target shot.
- No black bars, blurred side-fill or portrait-centered layout masquerading as a landscape reference.
- Resolution and crop preserve the needed face, hands and identity anchors.

Padding a portrait image to `832x480` changes the file dimensions, not its visual grammar. H3 may still reproduce a portrait crop, face-fill close-up or pillarbox. For a landscape medium/wide shot, prefer a landscape-native keyframe with the character at the intended scale and screen position.

For laterality-sensitive details, store a short human-readable note such as `subject anatomical RIGHT wrist verified; viewer-left in frontal view`. If orientation is ambiguous, do not claim it is verified.

## 5. Give each shot only the references it needs

Do not pass one large reference bundle to every independent pack.

- An establishing sit pack may use the sit keyframe.
- A later standing/walking pack should normally omit the sit reference.
- A face close-up may use a face master, but a medium/wide opening should use a medium/wide identity keyframe.
- Keep cast references role-separated so one character's wardrobe or face does not leak onto another.
- Prefer the smallest coherent packet that preserves identity and the current shot state.

If the model has a reference-count or role limitation, record the tradeoff. Do not silently drop an identity anchor.

## 5A. Convert the creative specification into the target model's runtime prompt

Keep two durable artifacts:

1. **Master creative specification:** the story, tone, witnessed action, inferred interval, initial/result states, camera intent, identity/prop locks and audio intent.
2. **Runtime prompt package:** the target-specific prompt text, settings, reference order, duration/window schedule and renderer-job boundaries actually submitted.

A Seedance-derived structure such as `GLOBAL STYLE / FIRST FRAME / SHOT BREAKDOWN / CAMERA / AUDIO / EXCLUSIONS` is allowed in the master specification. It is not a universal renderer grammar. Grok must not label that document “H3 ready” without compiling it, and Hermes must not submit it to H3 merely because it contains `[Shot N]`, timestamps or `HARD CUT`.

Use this handoff block in the Spec or production note:

```text
MASTER SPEC
source/revision: ...
viewer must witness: ...
viewer may infer: ...
strategy: witnessed long take | elliptical setup→result | hybrid

TARGET ADAPTER
engine/model: ...
input mode: ...
prompt processing: FG | PW | provider-specific mode
duration / expected internal windows: ...
enhancer: on | off
package: single-window | verified in-render cuts | separate jobs | scheduled windows
reference roles in actual slot order: ...
dialogue/audio syntax: ...

EXECUTION CHECK
compiled runtime prompt path/hash: ...
settings path/hash: ...
boundaries represented as: in-window cut | overlap | new shot | separate job
sample gate: required | waived by explicit user instruction
```

### MiniMax H3 / WanGP profile

- Official base H3 generation is 4–15 seconds. Longer WanGP output is a sliding-window extension and needs an explicit packaging decision.
- Ref2VA runtime prompts use, in order: `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music`.
- Define reference roles with `<Subject N>`, `<Picture N>`, `<Video N>` and `<Audio N>` as applicable. Keep stable speaker IDs; exact speech belongs inside `<d>[Language] ...</d>`.
- With `prompt_enhancer=false`, the submitted text must already use the selected H3 structure. A Seedance-style brief is not silently translated.
- With enhancement enabled, preserve and inspect the compiled result. The enhancer cannot decide whether the story should be a long take or an ellipsis, and it cannot repair contradictory reference pixels.
- `FG` is one coherent prompt contract. It does not schedule a different story section for each internal sliding window.
- `PW` is the WanGP per-window contract. Blank lines separate complete window prompts; keep the six Ref2VA sections together without internal blank lines. Each window restarts at `[Shot 1]` and time zero, and picture numbers are remapped for that window.
- Use `[/overlap=...]` for a continuing shot and `[/new_shot]` for a hard cut between generated windows. A timed `[Shot N]` is a cut inside one window; it is not the same boundary.

Evidence scope: H3 duration and prompt structure come from the [official MiniMax H3 repository](https://github.com/MiniMax-AI/MiniMax-H3) and its linked base/full-reference writing guides. `FG`/`PW`, paragraph separation, local timeline reset, overlap and `[/new_shot]` behavior come from the installed WanGP `models/minimax_h3/prompt_enhancer.py` and the [upstream implementation](https://github.com/deepbeepmeep/Wan2GP/blob/main/models/minimax_h3/prompt_enhancer.py). The 30-second failure is local evidence documented in [the 2026-10-01 night-batch incident](production-incidents/2026-10-01-night-batch-home-cvstore-prompt-vs-actual.md). Keep these claims scoped to the named model/runtime versions.

For a first H3 attempt, prefer a representative single-window clip that tests the hardest identity, action, framing and dialogue requirement. If the intended finished piece is longer, success in that sample approves the visual approach, not a monolithic 30-second prompt. Repackage the remaining story deliberately.

### Grok planning responsibility

Grok preserves the model-neutral intent and produces a target-adapter handoff. It must identify which actions remain continuous, which middle interval is deliberately omitted, and which boundaries need actual independent renderer state. Public Seedance, H3, Veo/Flow or creator examples are evidence for their stated model/version only; do not transfer their limits or syntax without adapter evidence.

### Hermes submission responsibility

Hermes compares the handoff block against the exact prompt and settings files. Stop before GPU submission when the target model, prompt mode, enhancer state, expected windows, reference order, dialogue syntax or job boundaries disagree. Do not “repair” a mismatch by quietly changing the story, adding generic negative prompts, or enabling an enhancer without recording the new compiled prompt.

### Example: the convenience-store scene

The same premise can produce different valid packages:

- **Witnessed 10-second long take:** choose one action whose continuity matters—such as entering, approaching the counter and reacting to what is there. Use one H3 single-window prompt, one motivated camera path and a settling payoff. Remove secondary count changes or extra dialogue that do not fit the time.
- **Elliptical setup → result:** Job A clearly shows four gimbap rolls and the character's intention. Cut before the routine or difficult purchase/repacking action. Job B opens on the same character, wardrobe and location anchors but unmistakably reveals seven rolls in the bag and the consequence. The omitted middle is not described as something either renderer must perform.
- **Long continuous version:** use it only if the audience needs to witness the entire causal performance. If WanGP must cross H3 windows, use an explicit `PW` schedule with complete per-window prompts and overlap anchors; otherwise split at a motivated editorial boundary.

Do not encode all three approaches at once as one 30-second `FG` prompt with many timestamps, cut commands, prop counts, exact dialogue and prohibitions. Choose the audience experience first, then compile only that package.

## 6. Treat independent packs as independent jobs

Text such as `AFTER standing` does not give Pack B access to Pack A's actual result. Hard-cut concatenation cannot create causal continuity that was never supplied to the next job.

### Decide what the audience witnesses

Do not equate good directing with either “always use a long take” or “always split into short packs.” Before packaging, answer:

1. What must the audience watch continuously for the emotion, causality, geography or fairness of the story to work?
2. What can be omitted because a precise setup and result let the audience imagine the middle more effectively?

Choose one:

- **Witnessed long take:** keep causally connected performance in one editorial shot. Direct one smooth motivated camera path that follows or reveals the important action and settles on the payoff. Several internal beats may remain inside this shot.
- **Elliptical setup → result:** make a setup shot that clearly shows intention and before-state, then a real cut, then a result shot that clearly shows changed state and consequence. Do not describe the omitted choreography as an action the renderer must still perform.
- **Hybrid:** hold the meaningful performance in a smooth long take, cut on a gesture, occlusion, exit, sound, glance or object match, then reveal the consequence separately.

Use existing storyboard/plan purpose and transition fields to record this compact decision; do not invent unsupported schema keys:

```text
viewer must witness: ...
viewer may infer: ...
strategy: witnessed long take | elliptical setup→result | hybrid
setup exit state: ...
deliberately omitted interval: ...
result entry state: ...
carried anchors / deliberate changes: ...
```

An ellipsis is legible only when the before-state and after-state share enough anchors to imply one intended event. A long take is useful only when its duration and camera movement carry meaning; generic drifting or orbiting is not a substitute for direction.

When the piece must feel like one story, choose one of these approaches:

1. A short in-prompt cut ladder only when comparable evidence exists for the same engine/model family, prompt mode, duration regime and cut structure, and the job stays inside one verified generation window.
2. First/last-frame or explicit boundary-frame workflows when supported.
3. An overlap anchor: the accepted end pose/frame of Pack N becomes the starting state for Pack N+1.
4. Independent editorial shots whose discontinuity is intentional and hidden by a motivated cut.

### A requested cut must become the right kind of boundary

`HARD CUT`, `[Shot N]`, timestamps and a prop ledger are prompt text, not independent renderer state. They can direct a compact montage, but they do not guarantee that a long job will execute each beat once or that a later sliding window will continue at the next line.

Current MiniMax H3 evidence is deliberately narrow:

- Repeated success: three `[Shot N]` sections and two measured cuts in one 181-frame, approximately 7.3-second render when the prompt named every boundary and ended the cut list with `only, and nowhere else`.
- Repeated failure: the 2026-09-30 night batch placed six or seven timed beats into one 720-frame job. All four jobs used two 481-frame sliding windows; story order, dialogue and prop state failed, and the convenience-store result visibly and audibly restarted near the approximately 20-second window boundary.

Do not extrapolate the short result to a 30-second multi-window story. Default to separate renderer jobs plus edit assembly when exact prop/hand/cast state, exact dialogue timing, several locations, or a difficult hidden transition matters. If cuts were requested because the model cannot perform an action reliably, put that action change between the actual jobs; do not ask the same render to perform it and merely add the words `HARD CUT`.

For multi-pack work, define at every boundary:

- ending pose/action and prop state;
- starting pose/action and prop state;
- screen direction and environment axis;
- wardrobe/accessory state;
- which frame or image carries the boundary.

Do not reuse earlier-state references in later packs merely because they depict the correct character.

## 7. Low-cost preflight before a batch

Before a long, night, multi-pack or remake batch:

1. Confirm explicit user GO.
2. Confirm the GPU queue is available and the intended model ID is installed.
3. Validate session provenance and exact prompt/settings files.
4. Check every cast member's mandatory anchors in the final prompt.
5. Visually check all references, especially laterality and composition.
6. Verify that each pack has only its required references.
7. Generate one representative sample pack when the user has not explicitly required an all-at-once run.
8. Review that sample for identity, visible and container aspect, framing, cut order, dialogue placement and state continuity before spending the rest of the batch.
9. Stop the remaining batch if requested and actual dimensions disagree, if a window boundary restarts/reorders the prompt, or if the sample replaces ordered beats with a thematic montage.

Do not automatically rerender after a failed review. Preserve the failure, write the smallest proposed correction and wait for user approval when the run requires a GO gate.

For a registered v2 session, `local_wangp.py submit` performs items 3–6 as a hard gate before it creates the run.
The semantic pixel review still belongs to the named reviewer: code verifies the declaration, file hash and physical
dimensions, not whether a pictured wrist is truly anatomical right or whether a landscape canvas merely contains
blurred portrait padding.

After two materially similar failures, stop repeating the same approach. Create an incident report and request Codex/Claude review.

## 8. Post-run review

Review generation, import/sync and human acceptance as separate states. For video, inspect both container metadata and visible content; `832x480` metadata does not prove full-frame landscape content.

Minimum review:

- identity and mandatory recognition anchors for every cast member;
- cast count and role separation;
- native visible aspect/framing, not only container dimensions;
- wardrobe, props and left/right continuity;
- pack boundary state and story order;
- unintended close-up or slideshow inserts;
- output paths, run IDs and checksums;
- whether the result is only completed, needs review, accepted or rejected.

Classify findings using the shared maintenance levels:

- `candidate`: one observation or one model/run;
- `repeated`: reproduced in comparable runs;
- `verified`: deterministic contract fact or controlled durable comparison.

Keep engine-specific observations engine-specific.

## 9. Lessons from the September 2026 runs

These are scoped production findings, not universal renderer laws.

- Reika/Suan: canonical Suan DNA required the updo/ribbon, but a later runtime prompt replaced it with vague natural morning hair. The ribbon then appeared only in a later pack. This was a prompt-compilation conflict, not evidence that the canonical DNA was wrong.
- Lia r2: files named `rightwrist` visually showed the bracelets on the apparent anatomical left wrist. Repeating `RIGHT HARD` in text did not repair contradictory pixels.
- Lia r2: portrait images padded into landscape canvases continued to encourage portrait remaps, close-up openings and pillarbox content.
- Lia multi-pack: all packs received sit, stand and walk references, so later packs retained a visual invitation to reset to sitting.
- Independent H3 jobs did not remember the previous pack. Hard concatenation improved duration, not causal continuity.
- 2026-10-01 night batch: putting six or seven `HARD CUT` beats into one 720-frame H3 Ref2VA job did not create a deterministic edited story. The jobs crossed the 481-frame sliding-window limit; the approximately 20-second continuation repeated/reordered prompt material, and one landscape request returned a portrait result. Preserve short in-render cut evidence, but compile long or state-sensitive cuts as separate jobs and stop after a representative failure.

The detailed local case note is [Lia beach video and floral stills know-how](knowhow-2026-09-30-lia-video-floral-stills.md). Durable consultation summaries are the [Reika/Suan incident](production-incidents/2026-09-29-reika-suan-morning-care-identity-and-props.md) and [Lia r2 incident](production-incidents/2026-09-30-lia-beach-vlog-r2-reference-and-continuity.md). Treat them as scoped evidence; use this playbook for the reusable operating rules.

## 10. Escalation packet

When asking Codex or Claude to help, do not send only “the face changed” or the full chat transcript. Create a production incident report using [the consultation guide](production-incident-and-agent-consultation.md) and [template](production-incidents/TEMPLATE.md), then provide its path and specify whether the request is review-only or authorizes a bounded change.
