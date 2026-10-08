# Hermes Autonomous Director — Decision Policy (Proposal)

- Date: 2026-10-08
- Status: PROPOSAL / guidance only; not installed, not runtime-tested, no schema/queue/permissions changed
- Example input: **"1900년대 초 등대지기의 일상을 영상으로 만들어줘."**
- Owner of creative input: user. Default production director/operator: Hermes. Frontier models: guidance authors and optional escalation consultants.
- Related: `AGENTS.md`, `HERMES.md`, `docs/hermes-autonomous-pipeline-TASK.md`, `docs/director-memory/autonomous-video-quality-guide.md`, `docs/creative-treatment-production-storyboard-role-split-PROPOSAL.md`, `docs/directing-technique-db.md`, `docs/prompt-craft-db.md`, `scenarios/LH-001-the-last-light-of-day.md`.

## Mission / Non-goals

The user supplies a short natural-language creative idea. Hermes should independently determine what facts to check, which techniques to retrieve, which references to prepare, how to storyboard, when to split or omit motion, what to render and how to review/repair. The end-state is **Hermes + MiniMax/local tools, without routine Claude, Grok, ChatGPT or Codex calls**.

This document is **not** an authorization for unlimited spending, rendering, GitHub pushes, public publication, schema changes or bypassing existing Studio user GO gates. Existing active assignments and code contracts remain authoritative. Do not create a second orchestrator if `adaptive-video-production` already handles a stage.

## Small-input execution policy

On receiving an idea, preserve the exact request; infer the least assumption-heavy feasible story. Produce three fields before elaborating:

```yaml
viewer_should_understand:
viewer_should_feel:
must_remain_true:
```

Use one central event and visible payoff. Avoid manufacturing emergencies to give a routine activity artificial drama. Before images/prompts, validate causal and state continuity, e.g. an unlit lighthouse must not be emitting its working beam before the keeper lights it.

Do not demand technical directing input from the user. Offer normal approval/GO gates only where the actual workflow requires them.

## Decision router (IF / THEN)

| Situation | Autonomous decision | Evidence / result |
|---|---|---|
| Story depends on date, place, technology, craft or profession | Research only the uncertainties that change visible actions or objects; prefer primary museum, historic or technical references; mark unverified details explicitly | Small fact sheet with source and confidence |
| Already-known place/technology with no material uncertainty | Reuse verified local notes rather than browsing by habit | Linked note and date |
| Plot is thin | Add one motivated activity and modest consequence; keep ordinary stories ordinary | Minimal story treatment |
| Existing reference or successful exact prompt fits the shot | Reuse it unchanged as baseline; alter one responsibility layer at a time | Provenance, prompt/version |
| Identity, wardrobe, prop or location consistency matters | Locate or produce authoritative masters by role; avoid recursive derivation and contradictory multi-reference packets | Reference manifest |
| A shot requires multiple distinct viewpoints/actions | Split into generated shots; keep edit clip/beat separate from renderer shot | Shot/clip mapping |
| Fragile hand-object contact, mechanism or state change | Classify DIRECT / PARTIAL / HIDE / CONSEQUENCE_ONLY; choose cut, bridge, insert, or result-only when better | Technique choice and tradeoff |
| A specific motion/transition technique is needed | Search directing DB by **problem**, read candidate constraints/evidence, pick the smallest technique that preserves meaning | Technique ID and predicted failure |
| Image/video prompt assembly | Compile from approved visible-world packet, not from concatenating full DNA, storyboard and style prose. Preserve exact successful prompts where applicable | Versioned prompt and references |
| Output fails | Diagnose references/contradictions → packaging → spatial/causal state → prompt compilation → model limitation. Repair only failed layer/clip, retain accepted clips | Observed failure and correction |
| Two materially similar failures | Stop repeated renders; diagnose, choose different technique or reduced shot complexity; optional bounded frontier escalation if allowed | Incident packet |
| Video appears complete | Inspect moving video and sound, boundary frames, timeline causality, identity and physical state; assemble with existing tools; do not claim pass based on stills only | QA record, assembled movie |
| Completion | Preserve source request, versions, models/settings, prompts, assets, failure/retry count, duration/cost when observable, explicit user acceptance | Reproducible production record |

## Selective research and skill loading

Do **not** load all technique DBs, failure corpora or long conversation history on each run. Route each uncertainty to the smallest relevant document or skill; link back to evidence. Read specialized references only for a visible failure risk. When new information contradicts established masters, preserve approved masters and ask for approval only if changing canonical assets is essential.

Hermes has on-demand skills; implementation must use the currently installed skills and verified checkout, not assume repository edits update a deployed skill. Verify actual installed state.

## Bounded production loop

1. **Intent pass**: classify genre, era, one central event, viewer outcome and immutable user requirements.
2. **Research pass**: answer only scene-critical factual uncertainties. Separate historical certainty from fictional choices.
3. **Story pass**: produce minimal treatment, beat order and emotional tempo. For a routine story, prefer observation → daily task → visible result → afterglow.
4. **Production pass**: construct clip/shot boundaries based on coherent camera/temporal state; maintain location/prop/light ledger.
5. **Reference pass**: authoritative identity/environment/prop masters; shot-specific role binding.
6. **Technique pass**: route render-risk to existing technique/prompt DB, choose DIRECT/PARTIAL/HIDE/CONSEQUENCE_ONLY and document why.
7. **Execution pass**: use Hermes as sole normal submitter through existing WanGP session/queue/recording and GPU locking; honor GO gates and requested engine. Renderer IDs/settings from installed tools, never guesses.
8. **Independent QA pass**: inspect moving outputs, sound and edit seams; preserve accepted shots; repair narrowly.
9. **Learning pass**: record observed results, not only preferred theory; promote a rule after repeated success or clear failure evidence. Mark one-off observations experimental.

### Autonomy ladder for Lighthouse Golden Reference

- **A: Reference reproduction** — Hermes is given the approved LH-001 story and independently makes production decisions; outside LLM only reviews defects when needed.
- **B: Independent production** — Hermes runs without outside LLM intervention after normal user GO approvals, using project skills/DBs.
- **C: Independent new story** — from a new one-line idea, Hermes performs research, treatment, shot planning, render, QC and targeted repair.

Compare **narrative/visual quality, contract fidelity, intervention count, render retries, time and known cost**. Do not declare full autonomous creativity proven by reproducing a prewritten storyboard.

## Lighthouse example: autonomous decisions expected

User input: "1900년대 초 등대지기의 일상을 영상으로 만들어줘."

- Historical lookup: time of lighting, portable vs fixed source, Fresnel lens/clockwork/weights. Avoid falsely assuming lenses were rotated by hand continuously; specific details may vary by station.
- Narrative: ordinary evening lighting routine, not invented rescue, sabotage or storm.
- Causal state: lamp OFF before lighting, ON after; track separate portable lantern.
- Difficult motion: split cranking, ignition, clockwork and lens rotation; preserve fixed burner versus rotating lens where historically chosen.
- Sound: waves, boots, glass, gears and logbook form continuity bridges, with minimal dialogue.
- Cinematic quality: warm-to-cool natural timeline and material consistency, not arbitrary camera spectacle.
- Acceptance: story reads without explanation; same keeper/setting; visible cause-effect; plausible equipment; complete video with review record.

## Methodology change and role-boundary decision

Prior role-split proposal treated frontier models as the default Creative Treatment authors and Hermes as production storyboard writer. **New evidence**: the Muse-produced lighthouse film from a refined 14-clip storyboard was reported as convincingly successful; frontier credits are constrained and user explicitly targets Hermes-only autonomy. Therefore allow Hermes to own **both treatment and storyboard**, optionally consulting frontier models for high-impact uncertainties. This is a **proposed default**, not a claim that unassisted Hermes quality is already proven.

Existing active schema/versioned contracts, assigned editors and GO stages override this proposal. Codex/Claude should integrate with the already available `adaptive-video-production`, `director_skill_router` and validation tools rather than implementing a second competing controller.

## Validation before promotion

- Dry-run: one-sentence LH-001 idea without supplying v3 shot list; inspect research choices, story/shot structure and technical decisions.
- Compare with Golden Reference and current production records; label actual Muse outputs and settings as **unverified in this proposal** until linked with exact session artifacts.
- Verify required assets and approval gates using existing registry.
- Record failure examples for wrong historical facts, invented crisis, contradictory OFF/ON lighting, source/rotating lens confusion, unnecessary frontier consultation, over-rendering and silent retries.
- Promote only independently tested improvements to deployed Hermes skill and project guidance through designated integration owner.
