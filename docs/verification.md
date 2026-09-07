# Verification by change scope

Read this for implementation, not for every content request. Record exact interpreter, working directory, command, counts/failures and unverified scope in the applicable task. Never call a subset the whole repository suite.

## XAI-studio Python

This repository contains both unittest classes and pytest functions, including external importer tests. `unittest discover` alone is not full coverage; installing pytest does not make unittest discover pytest functions.

Use the project's selected Python environment. Inspect imports and tool requirements for the affected subsystem before setup. Root dependency packaging is not yet centralized: pytest, PyYAML, Pillow and jsonschema are relevant to core/import tests; Control Tower additionally uses fastapi, uvicorn, sse-starlette, psutil, pydantic and httpx. This list is guidance, not a lockfile. Record missing dependencies as environment gaps, not passing tests. Studio declares its own dependencies in `backend/pyproject.toml`.

From the XAI-studio root, a broad explicit regression selection is:

```powershell
python -m pytest tests external_media_import/tests tools/test_wangp_recorder.py tools/test_local_wangp.py tools/test_requester_provenance.py tools/test_reference_variation_worker.py infra/gpu-worker/test_provision.py
```

`tests/test_control_tower_*.py` are inside `tests` above. `tools/test_requester_provenance.py` starts a real detached
worker against a fake WanGP root (no GPU, no model); it needs the interpreter to reach `tools/` on `PYTHONPATH`.

Inspect collection with the same selection plus `--collect-only -q` if coverage is uncertain. Select only affected files for bounded changes; full runtime/GPU/provider execution is not implied by passing these tests. Check module resolution points into the intended checkout if multiple copies exist.

## Control Tower service changes

Unit tests do not cover the service lifecycle. After changing `control_tower/*.ps1` or the server entry point,
verify by running it: `control_tower\start.ps1` (idempotent), `GET /api/health` on 127.0.0.1, kill the server process
and confirm the supervisor restarts it, then `schtasks /Run /TN "XAI Control Tower"` for the logon path. Do not test
the guard with a port listener check alone: `tailscale serve` also listens on 8790 to proxy the tablet.

## Studio changes

Follow Studio `AGENTS.md`. From its `backend/` directory, verify `import app.main; print(app.main.__file__)` resolves into the intended checkout, then use `python -m pytest` with the affected test scope. Backend dev dependencies are declared in `pyproject.toml` (`.[dev]` when setting up that environment).

From `frontend/`, existing scripts are `npm test`, `npm run lint`, and `npm run build` (TypeScript plus Vite). Run checks appropriate to the changed UI/contracts. Review/import changes must preserve old image fixtures and review/favorite state; video changes also need probe/poster/playback/Range tests. UI claims need actual desktop/tablet browser verification, not just unit tests.

## Documentation-only changes

Check referenced files, actual CLI options and path/route contracts; inspect diffs for unintended edits and run `git diff --check`. No new implementation-mirroring tests or full renderer suite are needed. Distinguish policy documented, code implemented, installed copy updated, runtime verified and user reviewed in the final report.
