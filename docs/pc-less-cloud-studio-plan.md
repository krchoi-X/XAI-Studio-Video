# PC-less Cloud Studio — Architecture Plan

Updated: 2026-09-18

Status: `PLAN — design under discussion, not an implementation order`

Supersedes the compute-only framing in [cloud GPU automation plan](cloud-gpu-automation-plan.md),
which assumed the workstation stays on as the control plane. Related: [render broker](render-broker.md),
[Control Tower v0.1](control-tower-v0.1.md).

## 1. The new premise

The RTX 4070 workstation is **off**. It is not a tier in the system, not a fallback, and
not the home of any durable state. The user works from a phone and a tablet.

Everything the workstation used to provide must come from somewhere else:

| Was on the PC | Must now come from |
|---|---|
| Git checkout of this repo and the Studio source | remote GitHub / the private snapshot repo |
| Character sheets, references — session **inputs** | Google Drive, already backed up by a separate batch |
| WanGP + weights | pod, fetched per session |
| Studio / Gallery web app (port 8787) | pod, **starting empty** |
| Control Tower dashboard (port 8790) | pod |
| Tailscale node the tablet connected to | pod, joined as an ephemeral node |
| The thing that could call the RunPod API | see §2 |

**The pod does not restore the workstation's library.** Material produced before this session is
reviewed directly in Drive; it never needs to enter a pod. The Gallery in the pod exists to show
**what this session just generated**, so the user can judge and select while it runs. State flows
one way in each direction:

```text
Drive --(inputs: character sheets, references)--> pod
pod   --(outputs: this session's media + records)--> Drive
```

There is no bidirectional state sync, no database to migrate, no cross-session lock, and nothing
on the powered-off workstation is on the critical path.

## 2. The structural problem: nothing is left to start the pod

**[Premise re-examination]** The natural design is "the web app lives in the pod." But the
web app is also how the user would ask for a pod. With the PC off, there is no process
anywhere that can call the RunPod API, so the session can never begin.

Something must be always-on. That is exactly the standing cost that already burned a month of
storage charges, so the always-on tier has a hard requirement: **near-zero cost, and never a GPU.**

Candidates for the launcher:

| Option | Standing cost | From a phone | Verdict |
|---|---|---|---|
| RunPod web console, by hand | 0 | yes | works today, no automation, easy to forget teardown |
| **GitHub Actions `workflow_dispatch`** | 0 (free minutes) | yes, GitHub mobile or browser | secrets built in, repo is already the durable state |
| Cloudflare Worker / Vercel function | ~0 | yes | another surface to build and secure |
| Tiny always-on VPS | ~$4–5/mo | yes | reintroduces the forgotten-resource failure |

An agent host — a Claude Code cloud session, or Grok Bot — is also a launcher, and a more
convenient one: the user already talks to it from the phone, so there is no workflow form to
fill in and the agent can diagnose a failed boot instead of only reporting it. Two conditions
apply before it can work, both one-time environment configuration:

- the RunPod key must be an **environment-level variable**, because a session's own environment
  does not persist between sessions;
- the environment's **network policy must allow `api.runpod.io`**. It is blocked by default —
  a session in this environment reached that wall while researching this plan.

An agent session is not always-on, though, so it cannot be the safety net.

**Recommendation: do not couple the launcher to one host.** Keep launching as a small script in
this repository that takes a session manifest. A Claude or Grok session runs it from the phone,
a GitHub Action runs it on a schedule, and the user can run it by hand. Then put only the
*unattended* duties — the daily orphan sweep — on the most boring scheduler available, which is
an Actions cron. Convenience on top, dull reliability underneath.

## 3. Target architecture

```text
ALWAYS ON — free, no GPU
  GitHub          repo = control plane: code, prompts, run records, session state
  GitHub Actions  launcher, teardown, daily orphan sweep; holds all secrets
  Google Drive    durable media library, Gallery database snapshot, optional weight cache
  Tailscale       identity/network fabric the phone and tablet are already on

EPHEMERAL — only while a session runs
  RunPod pod (5090 or better)
    boot:  clone repo(s) -> join tailnet -> restore state from Drive -> fetch weight profile
    serve: WanGP (BF16, high-VRAM profile) + Studio web app + Control Tower
    work:  phone/tablet drives it over the tailnet
    end:   upload media to Drive -> push records to GitHub -> self-terminate
```

The rule in `render-broker.md` — keep the control plane outside disposable GPU instances — is
preserved and in fact strengthened. The control plane simply moves from a single powered-on PC
to GitHub plus Drive, neither of which can be left running by accident.

## 4. Session flow

The user's flow, with the parts that need a decision filled in:

```text
1. command          user states the job from the phone
                    a launcher (agent session, Action, or by hand) runs the repo's
                    launch script with a session manifest and creates the pod

2. environment      pod boots the pinned image (WanGP runtime already inside)
                    fetches only the weight profile this command needs

3. inputs + UI      mounts Drive, pulls character sheets and references
                    starts the Gallery web service with an EMPTY library
                    starts Control Tower

4. network          joins the tailnet as an ephemeral tagged node

5. execute          the command runs, driven either from outside (agent session)
                    or by an LLM inside the pod -- see 4.2

6. review           user watches results appear in the Gallery from the phone,
                    selects and judges while the session is still live
                    new media syncs to Drive continuously, not only at the end

7. teardown         final export verified, then the pod terminates itself
```

Steps 2-4 run **in parallel**, not in sequence. Tailscale and the Gallery are up in well under
two minutes; weights keep downloading in the background. The user can be looking at the
dashboard long before the video model is resident. Serialising these would mean paying 5090
rates to watch a progress bar.

### 4.1 Boot time is the real cost problem

Nothing in this flow is expensive except waiting. A rough budget, all of it billed at GPU rate:

```text
image pull          runtime image, tens of GB, per machine unless cached
weight profile      video models are large; the dominant term
LLM weights         only if an in-pod LLM is used -- see 4.2
Drive inputs        character sheets and references; negligible
services up         seconds
```

This is what a network volume actually solves — and it is the honest counter-argument to
deleting it. The month of wasted storage was caused by a **forgotten** volume, not by a wrong
idea. With an automated launcher, an in-pod idle timeout and a daily sweep, forgetting is much
less likely, so a small volume holding only the active weight profile may become defensible
again.

Do not re-add it on that reasoning alone. Measure first: record image-pull and weight-download
seconds for the first few real sessions, then decide with numbers. Until then, parallel boot and
per-command weight selection are free and should be done regardless.

### 4.2 An in-pod LLM competes with the renderer for VRAM

**[Premise re-examination]** "Install an LLM too" reads as a small step, but on one GPU it is not.
A 5090 has 32 GB and a video model will want most of it. An 8B model co-resident costs roughly a
third of that; anything larger does not fit alongside generation at all. Loading both means
either smaller batches, lower resolution, or swapping weights in and out between every step.

Three options, and they are genuinely different systems:

| Where the driving LLM runs | VRAM cost | Works unattended | Notes |
|---|---|---|---|
| Outside the pod (agent session, or an API call from the pod) | none | yes, while the session lives | default; costs tokens, not VRAM |
| In the pod, on CPU/RAM | none on GPU | yes | slow, fine for prompt compilation and metadata |
| In the pod, on the GPU | large | yes | only worth it if the LLM work is heavy and generation is not concurrent |

**Recommendation: keep the driving LLM outside the pod by default.** The pod is rented for its
GPU; spending that GPU on token generation is the expensive way to do the cheap part. Add a
CPU-hosted small model in the pod only if the session must keep deciding things with nobody
connected.

### 4.3 Continuous sync is what makes automatic teardown safe

Uploading at teardown only is fragile, and it also makes aggressive timeouts frightening — nobody
wants a 20-minute idle timeout if losing the session means losing the work. Sync new media to
Drive continuously and both problems disappear together: a crash costs minutes, and the idle
timeout becomes safe to set short. The verified final export stays as the teardown gate.

Outputs must use the existing importer and Gallery contracts (`batch.yaml`, provenance records,
`POST /api/sync`) so the Drive tree matches every other route, per `AGENTS.md`.

## 5. Access and authentication

**[Premise re-examination]** RunPod exposes a pod's HTTP ports at public
`https://{podId}-{port}.proxy.runpod.net` hostnames. Neither the WanGP UI nor Studio has
authentication — on the PC, Tailscale provided it implicitly by never leaving the tailnet.
Publishing those ports would put an unauthenticated GPU and the user's media library on the
open internet, discoverable by anyone scanning that domain.

**Strong recommendation: the pod joins the tailnet instead of publishing proxy ports.** [principle]
Supply an **ephemeral, tagged, pre-authorized** Tailscale auth key as a pod secret. The pod
appears as a tailnet node, the phone and tablet already trust that tailnet, nothing is exposed
publicly, and an ephemeral node is removed automatically when the pod dies.

Approving each pod interactively from the phone (`tailscale up`, click the printed URL) also
works and needs no stored secret, but the GPU bills for every minute the pod waits for that
click, and it makes an unattended night batch impossible. Generate a reusable ephemeral tagged
key **once** instead: the approval still happens exactly once, at key creation, and every later
session joins with no interaction. Keep interactive `tailscale up` only as the fallback for the
first manual test.

This also preserves existing work: `control_tower/tailscale.py` already discovers the tailnet
origin serving a local port, so the dashboard's URL handling needs no redesign. Only the
hard-coded Windows paths change, and Control Tower already accepts `--scan-root`,
`--night-batch-root`, `--web-job-root`, `--db` and environment overrides for all of them.

Do not expose the RunPod proxy ports as a shortcut, and do not put a password form in front of
WanGP as a substitute.

## 6. State: what lives where

```text
GitHub (small, versioned, canonical)
  prompts, character records, run records and events, session manifests,
  the pod's published tailnet URL for the current session

Google Drive (large, durable, not versioned)
  media library, Gallery database snapshot, exported finals,
  optionally a weight cache if measurement shows it beats fetching upstream

Pod (disposable)
  weights, scratch, logs, running services
```

**Database handling.** The Gallery SQLite file must be **downloaded at session start and
uploaded at session end**, not mounted from Drive. A network-mounted SQLite file risks lock
corruption. This makes concurrent sessions unsafe, so the run record must hold a session lock
and the launcher must refuse a second session while one is live.

**Sync during the session, not only at the end.** Uploading to Drive just before teardown is
correct but insufficient: an unexpected pod loss — host failure, crash, provider reclaim — leaves
nothing uploaded at all. Sync new media incrementally every few minutes so a crash costs minutes
rather than the whole session, and keep the verified final export as the teardown gate.

**Irreplaceable assets** — self-trained LoRAs, curated reference sets — live in Drive and in
Git, never only in a pod or on a provider volume.

## 7. Cost safety without a watcher

With the PC off, nothing outside the pod is continuously watching it. Cost control therefore has
to be inside the pod, plus a cheap external sweep:

1. **Idle timeout inside the pod.** No queued or running job for N minutes → export, verify, self-terminate.
2. **Hard max runtime.** An absolute ceiling regardless of activity.
3. **Export-verified teardown.** Terminate only after uploads are checksum-verified; if verification
   fails, stop and raise instead of destroying, per the Vast runbook.
4. **Daily Actions cron sweep.** Reuses `provision.py list-active`, which already exits non-zero when
   a query fails so an unreachable provider is never read as "nothing is billing".
5. **No standing provider volume by default.** The month of storage charges is the evidence.

## 8. What this changes in the existing repo

- `docs/render-broker.md`: control plane is GitHub + Drive, not the workstation. Local WanGP becomes
  an optional route that is simply unavailable while the PC is off, not the fallback.
- `docs/control-tower-v0.1.md`: Control Tower must run in the pod; paths come from configuration,
  and its Tailscale discovery keeps working unchanged.
- `infra/gpu-worker/`: the worker image must also carry the repos, Tailscale, Drive sync and the
  self-terminating supervisor — it is no longer only a WanGP runtime.
- `infra/gpu-worker/config.example.json`: profile `WANGP_PROFILE: "4"` is the low-VRAM setting
  inherited from 8 GB local thinking. A 5090-class pod should use a high-VRAM profile and BF16
  weights, not the INT8/quanto files the workstation uses. Verify profile semantics against the
  pinned WanGP commit before changing it.
- `personal-prompt-studio` is a **separate repository** and is not in this session's scope. Running
  Studio in the pod requires a decision about how that repo and its data directory are provisioned.

## 9. Open decisions

1. Whether the pod clones `XAI-Studio-Private` (which carries both source snapshots) or the public
   repository plus a Studio source bundle. The private repo is the simpler single source.
2. Whether weights come from upstream or a Drive cache — measure both before deciding.
3. How the pod's tailnet URL reaches the phone: a run-record commit, a push notification, or a fixed
   tailnet hostname per session tag.
4. Whether the launcher also offers a cheap CPU-only pod profile for review-only sessions where no
   GPU is needed.
5. Whether GPU tier is chosen by the user at launch or by an ordered availability list.

## 10. Build order once this is agreed

Deliberately smallest-first, and teardown before launch:

```text
0. ONE-TIME, PC MUST BE ON: migrate the media library and review database to Drive
1. pod-side self-terminate supervisor (idle + max runtime + verified export)
2. Actions workflow: teardown + daily orphan sweep, using list-active
3. Actions workflow: launch, with secrets and a session lock
4. worker image: repo clone, tailnet join, Drive sync, high-VRAM WanGP profile
5. Control Tower in the pod, paths from configuration
6. Studio in the pod, after its repository provisioning is decided
```

Nothing in this order is implemented yet. `provision.py list-active` is the only piece already
built, and step 2 reuses it as-is.
