# Production incident and Codex/Claude consultation guide

Use this guide when Grok, Hermes or a human operator encounters a character, continuity, prompt, renderer or recording problem that may need Codex/Claude analysis. The goal is to make collaboration possible from durable evidence without reconstructing a chat.

## 1. Store each kind of information in its owning place

| Information | Durable location | Rule |
|---|---|---|
| exact prompts, settings, references, runs, output links | the existing Library/session directory returned by the producer | Keep originals and failed runs; do not create a second media tree |
| session attribution and status | `session-provenance.json` and run records | Keep requester, executor, engine and model distinct |
| shot plan and current production decision | session `Spec.md`, storyboard or generation packet | Record what was approved and what remains held |
| one problem needing cross-agent analysis | `docs/production-incidents/YYYY-MM-DD-<session-id>-<short-issue>.md` | Link evidence; do not copy large media into Git |
| repeatable shared-skill issue or technique | Private authority through `tools/shared_skill_feedback.py` | Feedback proposes learning; it does not edit a skill automatically |
| one character's anatomy or identity correction | character evidence/DNA proposal workflow | Never silently edit Stable DNA from a production incident |
| code/schema/API fix | a scoped `TASK.md` in the owning implementation repository | Name Active editor, consumers, compatibility, checks and rollback |

The repository incident report is the consultation index. It must link to the actual session evidence rather than duplicate or move it.

## 2. When to create an incident report

Create one when any of these is true:

- a mandatory identity anchor is missing, swapped or assigned to the wrong character;
- left/right, wardrobe, cast, aspect, prop or story-state continuity fails;
- two comparable attempts fail for the same reason;
- the prompt says one thing but the selected references say another;
- a run cannot be reproduced because DNA, skill, requester or reference provenance is unclear;
- fixing the issue may change a shared skill, adapter, schema or character record;
- another agent must review before more credits are spent.

A single obvious operator typo can stay in the session note if corrected before generation. Once it affected an output, keep the evidence and record it.

## 3. Required incident content

Start from [the template](production-incidents/TEMPLATE.md). At minimum include:

1. Status, date, author and requested reviewer.
2. Exact session ID and absolute session path.
3. The user request and approval/GO state.
4. Attribution: requester, orchestration/relay note if known, executor, engine and model.
5. Every cast character's canonical ID, DNA source, version/hash, whether the literal DNA text appears in the final
   renderer prompt, and selected reference roles/hashes. For “transform this image,” identify the exact selected
   source rather than writing only “master used.”
6. Expected behavior stated as observable acceptance criteria.
7. Observed behavior with timestamps, pack/shot IDs and affected run IDs.
8. Direct evidence links: prompt lines, settings, reference images, review file and output path.
9. Evidence level: `candidate`, `repeated` or `verified`.
10. Facts separated from hypotheses.
11. Changes already attempted and their results.
12. Current safety/approval state: held, review-only, allowed to edit, or user-approved rerender.
13. Exact questions for Codex/Claude.
14. Smallest proposed correction and a verification method that avoids unnecessary generation.

Do not label an inference as an engine fact. For example, “portrait-padded refs caused pillarbox” is a hypothesis until comparison or repeated evidence supports it; “the selected file contains black side bars” is directly verifiable.

## 4. Evidence rules

Prefer evidence in this order:

1. Exact run and artifact records.
2. Final engine prompt/settings and reference bytes.
3. Human or deterministic review with timestamps/frames.
4. Code/configuration and Git revision.
5. Agent explanation.
6. Chat recollection.

Use absolute paths for local evidence. Include hashes when identity or input bytes matter. Link only the relevant files and timestamps instead of dumping entire logs into the report.

Preserve contradictory evidence. If one variant succeeds and two fail, report all three; do not rewrite the rule as universally successful or broken.

## 5. Requesting Codex or Claude review

Send the incident path and a bounded request, for example:

> Review only. Read `docs/production-incidents/2026-09-30-...md`, identify whether the fault belongs to prompt compilation, reference selection, the H3 adapter or character data, and recommend the smallest fix. Do not rerender or edit canonical DNA.

Or, when edits are authorized:

> Implement the accepted fix described in the incident. First create or update the owning scoped TASK, preserve existing sessions, and run the listed deterministic checks. Do not generate media.

State explicitly whether the reviewer may:

- only diagnose;
- edit a session prompt for a future approved run;
- modify implementation code;
- propose but not apply DNA changes;
- edit a canonical shared skill;
- run a sample generation.

Silence does not authorize rerendering, Stable DNA changes, publication, deployment or pushing Git changes.

## 6. Shared-skill feedback

When the incident suggests reusable production learning, submit a structured record to the active Private authority after the run is stopped or completed. Example shape:

```powershell
python D:\codex\XAI-Studio-Private\tools\shared_skill_feedback.py submit `
  --workspace D:\AI_Studio\workspace.yaml `
  --skill <catalog-skill-name> `
  --actor grok `
  --kind production-failure `
  --scope "MiniMax H3 Ref2VA landscape multi-pack" `
  --confidence candidate `
  --summary "Short problem statement" `
  --observed "What the durable evidence shows" `
  --proposed-change "Smallest proposed instruction or adapter correction" `
  --evidence "Absolute incident/session/review path"
```

Use the real actor. Choose `candidate`, `repeated` or `verified` conservatively. A feedback submission does not authorize editing the shared skill; an Active editor and bounded shared-skill task are still required.

List open feedback before proposing a duplicate:

```powershell
python D:\codex\XAI-Studio-Private\tools\shared_skill_feedback.py list `
  --workspace D:\AI_Studio\workspace.yaml
```

## 7. Closing an incident

An incident can be marked:

- `OPEN`: evidence captured, decision pending;
- `REVIEWED`: diagnosis agreed, no implementation yet;
- `FIX PLANNED`: bounded owner/scope/checks assigned;
- `FIXED — UNVERIFIED`: deterministic edit complete, production proof pending;
- `VERIFIED`: acceptance checks or approved comparison passed;
- `WONT FIX / SCOPED`: intentionally accepted or narrowed, with reason;
- `SUPERSEDED`: replaced by a linked incident without deleting the old evidence.

Record the final disposition, changed files/commits, checks, any later production evidence and remaining uncertainty. Do not delete failed outputs or rewrite their historical prompt/settings.
