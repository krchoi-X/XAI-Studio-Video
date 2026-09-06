# XAI Control Tower — Local Job Observability

Status: **Design reference / future implementation**  
Updated: 2026-09-06  
Implementation owner: **Claude Code**  
Repository/design record owner: **Codex**

## 1. Purpose

Build a small local-first web application that answers one operational question:

> What is the RTX 4070 workstation doing right now, who started the work, how far has it progressed, when is it likely to finish, and what did it produce?

The user normally accesses the workstation remotely from a tablet through Tailscale. Work may have been started by different actors and tools:

- Claude Code
- Codex
- Hermes
- WanGP
- another local web app
- Python / batch scripts
- manual terminal execution

The Control Tower is therefore not a generation UI and not an agent router. It is an **observability and job-status layer for the local AI workstation**.

## 2. Scope boundary

### Current target

```text
Machine      Windows RTX 4070 workstation
Access       Tailscale
User model   Single user
Storage      Local SQLite
Primary UI   Tablet-friendly web dashboard
```

### Explicitly out of scope for the first implementation

- Runpod / Vast / Packet or other remote GPU orchestration
- public Internet hosting
- multi-user authentication
- distributed queues
- cloud worker scheduling
- speculative abstractions added only for future cloud support

Remote GPU support may be added much later if the local design proves useful. The first implementation should remain small and local.

## 3. Architectural principle

Do not make every tool integrate directly with the UI.

Run a small local monitor service on the 4070 PC and normalize observed work into a canonical `Job` model.

```text
Tablet / phone
      │
   Tailscale
      │
Control Tower Web UI
      │
 HTTP / SSE / WebSocket
      │
Local Monitor Service
      │
 ┌────┼───────────────┐
 │    │               │
GPU  WanGP       local processes
 │    │               │
NVML API/events   Claude/Codex/Hermes/Python
```

The monitor service observes and records work. It does not need to become the universal executor.

## 4. Canonical Job model

A job must distinguish **who requested the work** from **what actually executed it**.

Example:

```json
{
  "job_id": "job_20260906_00142",
  "title": "Lia beach vlog #014",
  "requested_by": "hermes",
  "executor": "wangp",
  "engine": "hunyuanvideo",
  "status": "running",
  "phase": "inference",
  "created_at": "...",
  "started_at": "...",
  "updated_at": "...",
  "progress": {
    "type": "step",
    "current": 31,
    "total": 42,
    "percent": 73.8
  },
  "eta_seconds": 423,
  "outputs": [],
  "parent_job_id": null
}
```

These fields are conceptually different:

```text
requested_by = webapp
executor     = Hermes
engine       = WanGP
model        = Hunyuan / H3 / other
```

or:

```text
requested_by = Codex
executor     = Python batch
engine       = ComfyUI
model        = Krea2
```

This separation is required because the initiator, orchestrator, runtime and model may all differ.

## 5. Progress must be honest

Do not invent percentage bars for tools that do not expose measurable progress.

Recommended progress types:

```text
exact     explicit percentage from runtime
step      N / total steps or N / total items
phase     planning / implementation / testing / review
activity  process alive + recent activity
unknown   running but progress cannot be estimated
```

Examples:

### WanGP / image-video inference

```text
73%
31 / 42 steps
ETA 7 min
```

### Batch generation

```text
17 / 30 images
56%
```

### Claude Code / Codex

```text
ACTIVE
running 18m
last activity 14s ago
current phase: testing
```

### Unknown process

```text
RUNNING
elapsed 22m
ETA unavailable
```

The UI should explicitly distinguish measured progress from inferred activity.

## 6. ETA strategy

When a runtime exposes steps, estimate remaining time from recent observed step durations rather than a hard-coded model estimate.

Conceptually:

```text
ETA ≈ remaining_steps × smoothed_recent_step_time + learned_finish_overhead
```

Persist local timing history so the estimate gradually becomes specific to this workstation and configuration.

Useful dimensions may later include:

- model / workflow
- resolution
- frame count
- step count
- GPU
- upscale stage

Do not over-engineer this in v0.1. A simple moving average is sufficient initially.

## 7. Host observability

The first useful version should work even before any tool-specific integration.

Use NVIDIA NVML or an equivalent reliable local interface to collect:

- GPU utilization
- VRAM used / total
- temperature
- power
- active GPU processes
- process IDs

Typical dashboard state:

```text
RTX 4070
GPU 96%
VRAM 7.4 / 8 GB
TEMP 72 C

python.exe
PID 28141
runtime 00:32:18
```

This host-level layer is the foundation for detecting work started outside the Control Tower.

## 8. Unknown / untracked workload detection

This is a first-class feature, not an edge case.

If the Job database says nothing is running but GPU/process telemetry shows a significant workload, display:

```text
Untracked workload detected
GPU 98%
python.exe
PID 17421
runtime 12m
```

Attempt only lightweight identification using:

- executable
- command line
- working directory
- known port
- known parent process

Example:

```text
Likely: WanGP
Working dir: D:\AI\WanGP
```

Do not pretend certainty if identification is heuristic.

## 9. Tool adapters

Keep the adapter contract intentionally small.

Conceptual interface:

```python
class JobAdapter:
    def discover_jobs(self): ...
    def get_status(self, job): ...
    def get_progress(self, job): ...
    def get_outputs(self, job): ...
```

Initial adapters:

```text
System/NVML adapter
GenericProcess adapter
WanGP adapter
Manual/registered Job adapter
```

Possible later adapters:

```text
Hermes
ComfyUI
Claude Code task events
Codex task events
```

Do not add provider abstractions solely because Runpod may exist later.

## 10. Claude Code and Codex observation

Coding agents do not naturally expose a truthful numeric completion percentage.

Initial observation should therefore be process/activity based:

```text
Claude Code
PID 29412
cwd D:\XAI-Control-Tower
elapsed 41m
last file change 12s ago
```

A later voluntary event protocol may add phases such as:

```text
planning
implementing
testing
reviewing
done
```

The shared `TASK.md` / handoff protocol can supply coarse phase state when appropriate, but the Control Tower must not derive fake exact percentages from prose plans.

## 11. Result presentation

Completed jobs should show useful artifacts rather than only `Completed`.

### Image work

```text
Completed
20 images
38m 12s
[thumb] [thumb] [thumb]
Open in Gallery
```

### Video work

```text
Completed
3 clips
1h 13m
preview / open result
```

### Coding work

```text
Completed
files changed: 14
tests: 37 passed / 0 failed
commit: <sha>
```

The Control Tower is the bridge from **execution status** to **result inspection**, while the Gallery remains the primary long-term media curation interface.

## 12. Recommended tablet dashboard

The home page should answer the operational state within a few seconds.

```text
XAI CONTROL TOWER                 4070 ●

GPU 96%   VRAM 7.4/8G   72 C

RUNNING
Lia Beach Vlog #14
WanGP · H3
██████████████░░ 73%
Step 31/42 · ETA 7 min
[Preview]
Started by Hermes

AGENTS / PROCESSES
Claude    ● Working 12m
Codex     ○ Idle
Hermes    ● Working 38m
WanGP     ● GPU

QUEUE
1. Hae-won upscale ×12
2. Lia reference ×20
3. vlog upscale ×3

RECENT RESULTS
...
```

Prefer SSE or WebSocket updates rather than page polling when useful, but choose the simplest implementation that works reliably on the local network.

## 13. Relationship to existing XAI Studio services

Keep service responsibilities separate.

```text
Gallery
  → inspect and curate media results

Creator / Production UI
  → request work

Control Tower
  → observe work

Character Studio
  → manage character DNA / canon
```

A future top-level portal may surface a small status widget:

```text
GPU 93%
Running Jobs 2
Next ETA 18m
```

Clicking that widget can open Control Tower. Services remain separate even if the experience becomes integrated.

## 14. Implementation ownership

### Claude Code — primary implementation owner

For this project Claude Code should lead:

- repository/code exploration
- implementation architecture within this bounded scope
- FastAPI or equivalent local backend
- GPU telemetry
- process discovery
- WanGP adapter
- SQLite persistence
- tablet UI
- tests and debugging

Reason: Codex credits are currently a practical continuity constraint. This is a bounded subsystem that Claude can own end to end without requiring Codex for every development step.

### Codex — documentation / integration / review owner

Codex should continue to manage:

- canonical repository documentation
- architecture records
- compatibility with wider XAI Studio contracts
- cross-repository implications
- occasional review when credits are available

This is a project-specific ownership choice and does not require redefining the global development role split for every repository task.

### Hermes — observed production worker

Hermes may start or orchestrate production jobs, but it is not the Control Tower implementation owner.

## 15. Handoff discipline

Claude should maintain enough state that Codex can later inspect or continue without reconstructing the entire session.

Use the existing repository handoff conventions. For this project, record at minimum:

```text
Owner
Status
Completed
Current
Next
Decisions
Acceptance criteria
Relevant files
```

Example:

```text
Owner: Claude Code
Status: implementing

Completed:
- GPU collector
- process discovery
- API schema

Current:
- WanGP adapter

Next:
- running-job tablet card

Decisions:
- SQLite WAL
- SSE for live status
```

Do not overwrite an unrelated active `TASK.md` merely to reserve this future project. Move it into the active task slot only when implementation actually begins.

## 16. Recommended implementation milestones

### M0 — Host Monitor

Deliver:

- PC online state
- GPU utilization
- VRAM
- temperature
- power
- GPU process list

This should already be useful by itself.

### M1 — Process Observatory

Recognize or classify:

- Claude Code
- Codex
- Hermes
- WanGP
- Python / batch processes
- unknown GPU workload

Show elapsed time and recent activity when measurable.

### M2 — Job Model + WanGP

Add:

- canonical Job schema
- requester / executor distinction
- status
- progress type
- progress
- ETA
- preview
- outputs
- basic history

### M3 — Tablet UI

Primary sections:

```text
NOW RUNNING
GPU
AGENTS / PROCESSES
QUEUE
RECENT RESULTS
```

Declare v0.1 complete at this point.

## 17. Explicitly defer after v0.1

Do not let the first implementation expand into all of the following:

- job creation from the Control Tower
- remote kill/restart for every process
- sophisticated notification infrastructure
- distributed workers
- Runpod/Vast integration
- full Prometheus/Grafana/OpenTelemetry stack
- public authentication
- multi-user RBAC
- universal agent routing

Add these only in response to demonstrated need.

## 18. Future direction

If local use proves valuable, the same conceptual model can later observe a remote worker:

```text
Local Monitor Agent ─┐
                     ├─ Control Tower
Remote Monitor Agent ┘
        │
     Runpod pod
```

This is intentionally a future possibility, not a current implementation requirement.

## 19. Core design decision

The durable abstraction is not "GPU monitoring". It is:

> **A canonical Job/Activity view across heterogeneous local AI tools, backed by truthful progress semantics and host-level observation.**

Recommended first path:

```text
NVML / host telemetry
→ generic process observation
→ canonical Job model
→ WanGP detailed integration
→ tablet dashboard
```

This sequence provides immediate utility and avoids coupling the project to hypothetical cloud infrastructure before the local workflow is proven.
