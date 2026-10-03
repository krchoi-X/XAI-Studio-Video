# Hermes GPU handoff

Status: COMPLETE
Active editor: Codex

## Goal

Make Hermes autonomously alternate between its local planning LLM and WanGP renderers on the single 8 GB GPU. Hermes must be able to finish and persist a prompt, unload Huihui/Meromero, verify usable VRAM, keep Windows awake, run the renderer to a terminal state, and only then resume LLM work.

## Constraints / Must Preserve

- Preserve existing prompt, reference, Recorder, Gallery and session contracts.
- Preserve all unrelated working-tree changes, especially the active production-plan additions in `tools/local_wangp.py` and `HERMES.md`.
- Use supported Ollama and llama.cpp router APIs; never expose or persist the Hermes router API key.
- Keep old asynchronous CLI behavior unless Hermes explicitly selects the blocking handoff option.
- Verification is deterministic and uses fake HTTP/process responses; no GPU render or service restart.

## Must NOT Do

- Do not kill Hermes, Ollama, WanGP or GPU processes.
- Do not change character DNA, media, model choice, prompts, Windows global power settings or update policy.
- Do not claim that a file lock can prevent an unrelated process from allocating VRAM.

## Plan

1. Add a standard-library GPU handoff helper for Ollama/llama.cpp unload, NVIDIA telemetry verification and a process-scoped Windows sleep guard.
2. Make Hermes-attributed WanGP workers perform that handoff before importing/initializing WanGP and record the evidence in `run.json`.
3. Add a blocking `local_wangp submit --wait` route and a foreground Hermes night-batch route so Hermes does not reload its LLM while rendering.
4. Update Hermes instructions and add deterministic tests.

## Contract impact

Producers are Hermes commands invoking `local_wangp.py submit` or `hermes_night_batch.py create`; consumers are the detached WanGP worker, Recorder run records and Hermes itself. Existing submissions remain asynchronous. `submit --wait` adds a backward-compatible blocking response containing the terminal run record; Hermes-attributed workers add `gpu_handoff` evidence to `run.json`. Night-batch `create --wait` runs the existing durable queue in the foreground. Old records remain readable. Rollback removes the new flags/helper and optional record field. Tests cover router/Ollama unload, VRAM gates, terminal waiting and foreground routing without loading a model.

## Progress

- Confirmed the current VRAM release path only unloads Ollama, while Hermes's llama.cpp Huihui worker remains loaded.
- Confirmed `local_wangp submit` is detached, so Hermes can resume and reload an LLM while the renderer is active.
- Added `tools/gpu_runtime.py`: it discovers Hermes's ephemeral router credential in memory, unloads every non-unloaded llama.cpp worker plus all Ollama residents, polls NVIDIA telemetry, fails closed below 6144 MiB free VRAM, and provides a process-scoped Windows sleep guard.
- Hermes-attributed `local_wangp` workers now perform the strict handoff before importing WanGP and persist `gpu_handoff` plus `power_guard` evidence in `run.json`.
- Added `local_wangp submit --wait` and `hermes_night_batch create --wait`; Hermes instructions make the blocking form mandatory so its next inference turn cannot overlap the renderer.
- Read-only live parsing confirmed this PC's router reports Huihui as loaded and NVIDIA telemetry is readable. No model was unloaded and no renderer was started during verification.
- Verification: `D:/codex/personal-prompt-studio/personal-prompt-studio/backend/.venv/Scripts/python.exe`, cwd `D:/codex/XAI-studio`, `PYTHONPATH=tools;C:/Users/krcho/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages`; focused pytest selection (`tests/test_gpu_runtime.py`, `tools/test_local_wangp.py`, `tests/test_hermes_night_batch.py`, `tools/test_requester_provenance.py`) passed **48 tests** in 7.50 s. `py_compile` passed four changed modules and `git diff --check` passed (only existing CRLF warnings).

## Next

On the next authorized Hermes production request, use the documented foreground/blocking command. The resulting `run.json.gpu_handoff` is the live acceptance evidence; no test render was spent for this implementation.

## Blockers / uncertainties

The repository cannot force arbitrary non-Hermes applications to honor a shared GPU lease. The safety guarantee therefore covers Hermes-attributed production and aborts before renderer initialization when the local LLM cannot be released or VRAM cannot be verified.
