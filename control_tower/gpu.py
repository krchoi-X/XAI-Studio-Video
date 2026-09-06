"""Host GPU telemetry via `nvidia-smi` CSV queries.

pynvml is not installed in the local interpreter, and per-process VRAM is not exposed on Windows WDDM
anyway, so the CLI is the pragmatic, dependency-free source. Every sample is either measured or absent;
this module never fabricates zeros when the tool fails.
"""
from __future__ import annotations

import subprocess
from dataclasses import asdict, dataclass, field
from typing import Any

from .util import iso_now

GPU_FIELDS = [
    "index",
    "name",
    "driver_version",
    "utilization.gpu",
    "utilization.memory",
    "memory.used",
    "memory.total",
    "temperature.gpu",
    "power.draw",
    "power.limit",
    "clocks.sm",
    "pstate",
]
APP_FIELDS = ["gpu_uuid", "pid", "process_name", "used_memory"]


@dataclass
class GpuProcess:
    pid: int
    name: str
    used_memory_mib: float | None = None


@dataclass
class GpuSample:
    index: int
    name: str
    driver_version: str | None
    utilization_percent: float | None
    memory_utilization_percent: float | None
    memory_used_mib: float | None
    memory_total_mib: float | None
    temperature_c: float | None
    power_draw_w: float | None
    power_limit_w: float | None
    sm_clock_mhz: float | None
    pstate: str | None
    processes: list[GpuProcess] = field(default_factory=list)
    sampled_at: str = field(default_factory=iso_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class HostSample:
    ok: bool
    gpus: list[GpuSample]
    error: str | None = None
    sampled_at: str = field(default_factory=iso_now)

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "error": self.error, "sampled_at": self.sampled_at, "gpus": [g.to_dict() for g in self.gpus]}


def _num(value: str) -> float | None:
    text = value.strip()
    if not text or text.startswith("[") or text.lower() in {"n/a", "not supported", "insufficient permissions"}:
        return None
    for suffix in (" MiB", " W", " MHz", " %", "%"):
        if text.endswith(suffix):
            text = text[: -len(suffix)]
    try:
        return float(text)
    except ValueError:
        return None


def _text(value: str) -> str | None:
    text = value.strip()
    if not text or text.startswith("["):
        return None
    return text


def parse_gpu_csv(output: str) -> list[GpuSample]:
    samples: list[GpuSample] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < len(GPU_FIELDS):
            continue
        idx = _num(parts[0])
        samples.append(
            GpuSample(
                index=int(idx) if idx is not None else len(samples),
                name=parts[1],
                driver_version=_text(parts[2]),
                utilization_percent=_num(parts[3]),
                memory_utilization_percent=_num(parts[4]),
                memory_used_mib=_num(parts[5]),
                memory_total_mib=_num(parts[6]),
                temperature_c=_num(parts[7]),
                power_draw_w=_num(parts[8]),
                power_limit_w=_num(parts[9]),
                sm_clock_mhz=_num(parts[10]),
                pstate=_text(parts[11]),
            )
        )
    return samples


def parse_apps_csv(output: str) -> list[GpuProcess]:
    processes: list[GpuProcess] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        # process_name may itself contain commas only in pathological cases; split from the right.
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < len(APP_FIELDS):
            continue
        pid = _num(parts[1])
        if pid is None:
            continue
        name = ",".join(parts[2:-1]).strip()
        processes.append(GpuProcess(pid=int(pid), name=name, used_memory_mib=_num(parts[-1])))
    return processes


class NvidiaSmiCollector:
    def __init__(self, executable: str = "nvidia-smi", timeout: float = 5.0) -> None:
        self.executable = executable
        self.timeout = timeout

    def _run(self, args: list[str]) -> str:
        result = subprocess.run(
            [self.executable, *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout,
            check=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode != 0:
            raise RuntimeError((result.stderr or result.stdout or f"nvidia-smi exit {result.returncode}").strip())
        return result.stdout

    def sample(self) -> HostSample:
        try:
            gpu_out = self._run(["--query-gpu=" + ",".join(GPU_FIELDS), "--format=csv,noheader"])
            gpus = parse_gpu_csv(gpu_out)
            if not gpus:
                return HostSample(ok=False, gpus=[], error="nvidia-smi returned no GPU rows")
            try:
                apps_out = self._run(["--query-compute-apps=" + ",".join(APP_FIELDS), "--format=csv,noheader"])
                procs = parse_apps_csv(apps_out)
            except (RuntimeError, OSError, subprocess.TimeoutExpired):
                procs = []
            # Single-GPU workstation: attribute all compute apps to GPU 0 (the apps query does not
            # reliably map uuid -> index without a second query).
            if gpus:
                gpus[0].processes = procs
            return HostSample(ok=True, gpus=gpus)
        except FileNotFoundError:
            return HostSample(ok=False, gpus=[], error=f"{self.executable} not found on PATH")
        except subprocess.TimeoutExpired:
            return HostSample(ok=False, gpus=[], error="nvidia-smi timed out")
        except (RuntimeError, OSError) as exc:
            return HostSample(ok=False, gpus=[], error=str(exc))
