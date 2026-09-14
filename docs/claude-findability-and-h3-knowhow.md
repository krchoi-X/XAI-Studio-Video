# What was hard to find, and what was learned — Claude Code, 2026-09-13/14

Two things the operator asked for: concrete feedback on why the repository's own guidance was hard to
reach, so the storage/repository reorganization can act on it; and the know-how from this run written down
so Hermes, Grok and a later session do not rediscover it.

Written after a run in which **three capabilities that were already documented or already installed went
unused for two days**, and the cost was real: roughly twenty wasted renders at eighteen minutes each.

---

## Part 1 — Why the guidance was not reached

### The evidence

`docs/` holds 37 markdown files and has **no index**. `AGENTS.md`'s routing table names ten documents.
The two that contained the answers to this run's central problems are not among them:

| Document | Lines | Live references from anywhere in the repo |
|---|---|---|
| `docs/vlog-production-orchestration.md` | 692 | **0** (only a task-archive snapshot and a `tmp/` backup) |
| `docs/toyxyz-h3-prompter-review.md` | 148 | **0** (same) |
| `docs/lia-vlog-pilot-01.md` | — | **0** |
| `docs/reference-driven-production-pipeline.md` | — | 1 |

`vlog-production-orchestration.md` §4-6 contains the shot-boundary policy this run needed. §4 says to use
multiple Look references together "only when the transformation itself matters inside the shot" — which is
exactly the technique the operator had to explain in chat on 2026-09-14 after a day of clips whose props
and hair changed between cuts.

`toyxyz-h3-prompter-review.md` states plainly that "later shot boundaries create cuts; image anchors inside
a shot are continuous states and do not create implicit cuts", and records MiniMax H3's `17k+5` frame grid
at 24 fps. Both were treated as unknowns during this run and one of them was re-derived experimentally.

### The specific problems

**1. The routing table routes by *task*, but this knowledge is organised by *research topic*.**
`AGENTS.md` sends "Video prompt design" to `docs/architecture.md` and `SKILL.md`. An agent asked to make a
vlog follows that row and never learns that a 692-line document about exactly this exists. The table is not
wrong; it is incomplete, and there is no way for a reader to notice the gap.

**2. Nothing distinguishes a settled finding from a proposal.** `toyxyz-h3-prompter-review.md` is titled as
an architecture *decision* about whether to fork a repository. Its verified facts about H3's shot semantics
are buried inside as supporting detail. A reader skimming titles has no reason to open it for H3 behaviour.

**3. Research notes and engine capability facts are mixed in one flat folder.** `wangp-models.md` says which
model *ids* exist, but not what any of them can do. The fact that `minimax_h3_ref2va_pruned` generates
synchronised speech with lip sync is in the model's own definition file under `D:\AI\WanGP\defaults\`, not
in this repository at all. Two days of clips were rendered asking for silence.

**4. There is no "what did we already try" record at the engine level.** Per-session READMEs hold results,
but they are scattered under `characters/<id>/02_generations/` and are not searchable by technique.

### What would fix it, in order of value

1. **`docs/README.md` as an index**, grouped by *when you need it*, with a one-line "what question this
   answers" per file. Cheap, and it alone would have prevented most of this.
2. **A `docs/engines/` area for capability facts** — one file per engine, stating what it can do, the exact
   prompt syntax for each capability, and what has been verified on this machine versus assumed. Generated
   `wangp-models.md` answers "does this id exist"; nothing answers "what can it do".
3. **Front-matter on each research doc**: `status: verified | proposal | superseded`, `answers:` one line,
   `verified_on:` date. Then a grep finds the right document without opening 37 files.
4. **Extend the `AGENTS.md` routing table rather than replace it** — it works, it is just missing rows.
   Adding "Vlog / multi-shot production" and "Engine capabilities" would have been enough here.
5. **A technique index** linking a technique to the sessions that tried it, so "has anyone tried multi-shot
   prompts" is one lookup instead of a directory crawl.

This is feedback, not an assignment: `docs/` and `AGENTS.md` are integration-owned.

---

## Part 2 — MiniMax H3 know-how, verified on this machine

Everything below was measured or read from the installed model definitions between 2026-09-12 and
2026-09-14, on an RTX 4070 Laptop with 8 GiB. Where something is inferred rather than tested, it says so.

### The two H3 variants here do different jobs

| model_type | What it takes | What it is for |
|---|---|---|
| `minimax_h3_ref2va_pruned` | `image_refs` (multiple `<Picture N>`) | identity from reference portraits |
| `minimax_h3_fl2va_pruned` | `image_prompt_type: "S"` + `image_start` (and `"SE"` + `image_end`) | continuing from an exact frame |

**Verified 2026-09-14:** FL2VA started from the previous clip's final frame produces a seam that is not
visible — same face, hair, clothing and background across the cut. This is the mechanism for continuity
*between* renders. Ref2VA cannot do it; prose asking for "the same basket" does not work and produced a
different basket every time across twenty clips.

### H3 generates speech and audio; it is not a silent model

The definition at `D:\AI\WanGP\defaults\minimax_h3_ref2va_pruned.json` describes it as
"Reference-to-Video-**and-Audio**" and carries a worked example with a lip-synced line:

```
... saying clearly (S1) <d>[English] Some journeys begin when the map runs out.</d>
overall_soundscape: <what the stereo track contains>
non_diegetic_music: <music, or None>
```

**Verified:** six of six spoken lines came back word-for-word under Whisper transcription, at −15 to −19 dB
mean, with visible mouth articulation. No TTS and no lip-sync model is involved — which matters because
none of InfiniteTalk, MultiTalk or S2V is installed here.

Clips whose prompt ended "a quiet neutral room tone and nothing else" measure −85 dB. The audio path was
working the whole time and was being asked for silence.

**Trap, verified:** prose *outside* the `<d>` tags can be spoken. A delivery instruction containing "never
announcing" produced the spoken words "You're announcing"; "I have stopped pretending" leaked as "Never
pretending". Keep direction outside `<d>` short, and avoid words that could pass as dialogue.

`<d>[Japanese]` is untested as of 2026-09-14.

### Shot boundaries inside one render

`docs/toyxyz-h3-prompter-review.md` records that later shot boundaries create cuts and that image anchors
inside a shot are continuous states that do not. The prompt format supports it directly — the
`retention_analysis` line reads `<Subject 1> (appears in [Shot 1])`, which only has meaning if a subject can
appear in a subset of several shots.

**Not yet verified on this machine.** Every clip rendered here so far used `[Shot 1]` alone.

The consequence, if it holds: state transitions that would break continuity — a wardrobe change, a hair
change, picking up a prop — belong *inside* one render, with the clip ending after the new state is stable.
Then the final frame feeds the next render through FL2VA. Continuity is then never the model's guess. This
is the operator's formulation and it matches `vlog-production-orchestration.md` §4-6.

### Framing is controlled by where the crop falls, not by shot-scale words

**Verified across two sessions.** "A steady medium shot holds her standing on the pavement, the street
receding softly behind her" produced a figure occupying a tenth of the frame, 47 px of face. "A steady
close-up holds her head and shoulders, cropped just below the collarbone" produced a close-up.

- Describe what fills the frame. Describing what is *behind* the subject invites a wide shot.
- "Steady" does not prevent camera movement: one shot travelled from full length to an extreme close-up.

### The identity score mostly measures face size

Measured across six shots of one short, then again across eighteen vlog clips:

| Face in frame | ArcFace vs the reference prototype |
|---|---|
| 375 px | 0.83-0.84 |
| 205 px | 0.82-0.84 |
| 106 px | 0.81-0.84 |
| 85 px | 0.60-0.77 |
| 47 px | 0.38-0.53 |

Ordering is by pixels, not by location: a new room at 107 px scores higher than the reference's own room at
85 px. **A low score on a wide shot is not drift and must not be reported as one.** Below roughly 150 px the
number is measuring the framing. This supersedes an earlier reading in this repository that attributed the
drop to leaving the reference's own room; that effect is real but smaller.

### Prompt budget is a real constraint

An identity anchor block of about ninety words was attached to all twenty vlog shots, against roughly
fifteen words of actual behaviour. The result was an average face doing very little — the operator's
"평균으로 회귀". Carrying the whole DNA into every shot is not free: it crowds out the specific.

### Operational facts

- **A resident Ollama model costs 7.5x on render speed** on an 8 GiB card. Unload before timing anything.
- **Heavy CPU work during an offloading render is worse**: one clip's step time went from 29 s to 36 min.
- **Modern Standby ignores "never sleep on AC".** This laptop has no S1/S2/S3 at all. Entry is triggered by
  the screen turning off (`SC_MONITORPOWER` in the System log), so the AC sleep timer being 0 does not help;
  the display timeout is effectively the sleep timeout. An overnight batch lost seven hours to this.
  `identity_batch.py` now requests `ES_SYSTEM_REQUIRED` for the life of the batch.
- **The GPU lock is exclusive and a submission against it fails rather than queues** — and the failure is
  written into the run record a second *after* `submit` returns successfully, so checking the submit call is
  not enough. Twenty shots were lost in six minutes to this before `identity_batch.py` learned to wait.
- **LoRA training is not possible here**: 8 GiB, and no kohya/sd-scripts, musubi-tuner, ai-toolkit,
  diffusion-pipe or OneTrainer installed; `bitsandbytes` absent. `tools/lora_dataset.py` produces a portable
  snapshot instead and records that training was not run.
- `video_length: 181` yields 175 frames at 24 fps (7.29 s). The `17k+5` grid in the toyxyz review is the
  likely reason; **untested** — 176 or 193 would be the values to try.

### Tools added for this work

`tools/identity_score.py`, `video_frame_harvest.py`, `turnaround_report.py`, `identity_set_builder.py`,
`reference_set_check.py`, `identity_batch.py`, `pairwise_preference.py`, `character_sheet.py`,
`lora_dataset.py`, `test_identity_score.py`. Thresholds and their evidence are in
`docs/identity-scoring-calibration.json`.
