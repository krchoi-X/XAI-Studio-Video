"""Safe handoff between Hermes local LLMs and local GPU renderers.

The API key in Hermes's runtime descriptor is used in memory only.  Reports returned
by this module deliberately contain model ids and telemetry, never credentials.
"""
from __future__ import annotations

import ctypes
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable


HERMES_DESCRIPTOR = Path.home() / "AppData/Local/hermes/runtimes/llamacpp/server.json"
OLLAMA_PS = "http://127.0.0.1:11434/api/ps"
OLLAMA_GENERATE = "http://127.0.0.1:11434/api/generate"
DEFAULT_MIN_FREE_MB = 6144
DEFAULT_MAX_GPU_UTILIZATION = 20


def _read_json(request: str | urllib.request.Request, *, timeout: float = 10) -> Any:
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def _post_json(url: str, value: dict[str, Any], *, headers: dict[str, str] | None = None,
               timeout: float = 60) -> Any:
    all_headers = {"Content-Type": "application/json", **(headers or {})}
    request = urllib.request.Request(
        url, data=json.dumps(value).encode("utf-8"), headers=all_headers, method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
    return json.loads(body) if body else None


def _hermes_config(descriptor: Path = HERMES_DESCRIPTOR) -> tuple[str, str] | None:
    try:
        value = json.loads(descriptor.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    base_url = str(value.get("base_url") or "").strip().rstrip("/")
    api_key = str(value.get("api_key") or "").strip()
    return (base_url, api_key) if base_url and api_key else None


def _model_status(model: dict[str, Any]) -> str:
    value = model.get("status")
    if isinstance(value, dict):
        value = value.get("value")
    return str(value or "").strip().lower()


def hermes_loaded_models(descriptor: Path = HERMES_DESCRIPTOR) -> list[str]:
    config = _hermes_config(descriptor)
    if config is None:
        return []
    base_url, api_key = config
    request = urllib.request.Request(
        base_url + "/models", headers={"Authorization": "Bearer " + api_key},
    )
    value = _read_json(request)
    if isinstance(value, dict):
        value = value.get("data", value.get("models", []))
    if not isinstance(value, list):
        raise RuntimeError("Hermes /models returned an unexpected response")
    return [
        str(model.get("id") or model.get("model") or model.get("name"))
        for model in value
        if isinstance(model, dict) and _model_status(model) != "unloaded"
        and (model.get("id") or model.get("model") or model.get("name"))
    ]


def unload_hermes_models(descriptor: Path = HERMES_DESCRIPTOR) -> list[str]:
    config = _hermes_config(descriptor)
    if config is None:
        return []
    base_url, api_key = config
    loaded = hermes_loaded_models(descriptor)
    headers = {"Authorization": "Bearer " + api_key}
    for model in loaded:
        _post_json(base_url + "/models/unload", {"model": model}, headers=headers)
    return loaded


def ollama_loaded_models() -> list[str]:
    value = _read_json(OLLAMA_PS)
    models = value.get("models", []) if isinstance(value, dict) else []
    return [str(model.get("name")) for model in models if isinstance(model, dict) and model.get("name")]


def unload_ollama_models() -> list[str]:
    loaded = ollama_loaded_models()
    for model in loaded:
        _post_json(OLLAMA_GENERATE, {"model": model, "keep_alive": 0, "stream": False})
    return loaded


def nvidia_telemetry(*, run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> dict[str, int]:
    completed = run(
        ["nvidia-smi", "--query-gpu=memory.total,memory.used,memory.free,utilization.gpu",
         "--format=csv,noheader,nounits"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15, check=False,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        raise RuntimeError("nvidia-smi telemetry is unavailable")
    fields = [part.strip() for part in completed.stdout.splitlines()[0].split(",")]
    if len(fields) != 4:
        raise RuntimeError("nvidia-smi returned unexpected telemetry")
    total, used, free, utilization = (int(float(value)) for value in fields)
    return {"total_mb": total, "used_mb": used, "free_mb": free, "utilization_percent": utilization}


def release_local_llms() -> dict[str, Any]:
    """Ask both supported local runtimes to unload, without treating absence as failure."""
    report: dict[str, Any] = {"hermes_unloaded": [], "ollama_unloaded": [], "errors": []}
    for key, operation in (("hermes_unloaded", unload_hermes_models),
                           ("ollama_unloaded", unload_ollama_models)):
        try:
            report[key] = operation()
        except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
            report["errors"].append(f"{key}: {type(exc).__name__}: {exc}")
    return report


def prepare_renderer_gpu(*, timeout_seconds: float = 120, poll_seconds: float = 2,
                         min_free_mb: int | None = None,
                         max_utilization: int = DEFAULT_MAX_GPU_UTILIZATION,
                         sleep: Callable[[float], None] = time.sleep,
                         telemetry: Callable[[], dict[str, int]] = nvidia_telemetry) -> dict[str, Any]:
    """Unload local LLMs and fail closed unless the card is demonstrably ready."""
    required_free = min_free_mb if min_free_mb is not None else int(
        os.environ.get("XAI_GPU_HANDOFF_MIN_FREE_MB", DEFAULT_MIN_FREE_MB)
    )
    deadline = time.monotonic() + timeout_seconds
    unloaded_hermes: list[str] = []
    unloaded_ollama: list[str] = []
    errors: list[str] = []
    last: dict[str, int] | None = None
    while True:
        released = release_local_llms()
        unloaded_hermes.extend(model for model in released["hermes_unloaded"] if model not in unloaded_hermes)
        unloaded_ollama.extend(model for model in released["ollama_unloaded"] if model not in unloaded_ollama)
        errors.extend(error for error in released["errors"] if error not in errors)
        hermes_verify_error = None
        try:
            hermes_resident = hermes_loaded_models()
        except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
            hermes_resident = []
            hermes_verify_error = f"hermes verify: {type(exc).__name__}: {exc}"
            if hermes_verify_error not in errors:
                errors.append(hermes_verify_error)
        try:
            ollama_resident = ollama_loaded_models()
        except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
            ollama_resident = []
            message = f"ollama verify: {type(exc).__name__}: {exc}"
            if message not in errors:
                errors.append(message)
        last = telemetry()
        ready = (
            hermes_verify_error is None and not hermes_resident and not ollama_resident
            and last["free_mb"] >= required_free
            and last["utilization_percent"] <= max_utilization
        )
        if ready:
            return {
                "status": "ready", "hermes_unloaded": unloaded_hermes,
                "ollama_unloaded": unloaded_ollama, "telemetry": last,
                "minimum_free_mb": required_free, "errors": errors,
            }
        if time.monotonic() >= deadline:
            raise RuntimeError(
                "GPU handoff failed: "
                f"Hermes resident={hermes_resident}, Ollama resident={ollama_resident}, "
                f"telemetry={last}, required_free_mb={required_free}, errors={errors}"
            )
        sleep(poll_seconds)


class WindowsSleepGuard:
    """Process-lifetime rendering guard; does not change the user's power plan."""

    def __init__(self) -> None:
        self.status = "not Windows; no sleep request made"
        self._active = False

    def __enter__(self) -> "WindowsSleepGuard":
        if os.name != "nt":
            return self
        kernel32 = ctypes.windll.kernel32
        result = kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000040)
        if not result:
            result = kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
        if not result:
            raise RuntimeError("Windows refused the renderer sleep-prevention request")
        self._active = True
        self.status = "sleep suppressed for renderer lifetime"
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._active:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
            self._active = False
