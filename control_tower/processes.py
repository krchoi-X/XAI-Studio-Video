"""Process observatory: classify local processes into known actors and measure activity honestly.

Activity is *inferred* from CPU time deltas between scans. It is never presented as progress.
"""
from __future__ import annotations

import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

try:
    import psutil
except ImportError:  # pragma: no cover - psutil is present in the target venv
    psutil = None  # type: ignore[assignment]

from .util import iso_now

# Agents shown in the AGENTS / PROCESSES section, in display order.
AGENT_ORDER = ["claude", "codex", "hermes", "wangp", "comfyui", "gallery", "ollama", "xai-tools"]
AGENT_LABELS = {
    "claude": "Claude Code",
    "codex": "Codex",
    "hermes": "Hermes",
    "wangp": "WanGP",
    "comfyui": "ComfyUI",
    "gallery": "Gallery (Prompt Studio)",
    "ollama": "Ollama",
    "xai-tools": "XAI tools",
}
# Kinds whose presence on the GPU means "AI workload", as opposed to a desktop app touching the GPU.
AI_RUNTIME_KINDS = {"wangp-worker", "wangp-webui", "wangp", "comfyui", "ollama", "python", "xai-tool", "hermes-agent"}
ACTIVE_CPU_PERCENT = 1.0  # percent of the whole machine (all cores = 100)
IDLE_GRACE_SECONDS = 45.0


@dataclass
class ProcessInfo:
    pid: int
    ppid: int | None
    name: str
    kind: str
    agent: str | None
    label: str
    exe: str | None = None
    cmdline: str | None = None
    cwd: str | None = None
    created_at: str | None = None
    elapsed_seconds: float | None = None
    cpu_percent: float = 0.0
    memory_rss_mb: float | None = None
    on_gpu: bool = False
    gpu_memory_mib: float | None = None
    active: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentState:
    agent: str
    label: str
    state: str  # working | idle | offline
    process_count: int = 0
    cpu_percent: float = 0.0
    on_gpu: bool = False
    active_since: str | None = None
    last_active_at: str | None = None
    oldest_started_at: str | None = None
    pids: list[int] = field(default_factory=list)
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProcessSnapshot:
    processes: list[ProcessInfo]
    agents: list[AgentState]
    scanned_at: str = field(default_factory=iso_now)
    total_processes: int = 0
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "scanned_at": self.scanned_at,
            "total_processes": self.total_processes,
            "error": self.error,
            "processes": [p.to_dict() for p in self.processes],
            "agents": [a.to_dict() for a in self.agents],
        }


def _lower(value: str | None) -> str:
    return (value or "").replace("/", "\\").lower()


def classify(name: str | None, cmdline: str | None, exe: str | None = None, cwd: str | None = None,
             wangp_root: str | None = r"D:\AI\WanGP") -> tuple[str, str | None, str]:
    """Return (kind, agent, label). Pure function so it can be unit tested without psutil."""
    n = _lower(name)
    c = _lower(cmdline)
    e = _lower(exe)
    w = _lower(cwd)
    root = _lower(wangp_root)
    is_python = n.startswith("python") or "\\python.exe" in c[:200] or "\\python3" in c[:200]

    if "control_tower" in c:
        return "control-tower", None, "Control Tower (this service)"
    if n == "claude.exe":
        if "claude-code" in e or "claude-code" in c or "--output-format" in c:
            return "claude-code", "claude", "Claude Code session"
        if "--type=" in c:
            return "claude-desktop-helper", "claude", "Claude desktop helper"
        return "claude-desktop", "claude", "Claude desktop app"
    if n in {"codex.exe", "codex-code-mode-host.exe"} or (n == "codex" and "codex" in e):
        return "codex-cli", "codex", "Codex app-server" if "app-server" in c else "Codex"
    if "openai.codex" in e or "openai.codex" in c:
        if "--type=" in c:
            return "codex-desktop-helper", "codex", "Codex desktop helper"
        return "codex-desktop", "codex", "Codex desktop app"
    if n.startswith("chatgpt"):
        return "chatgpt-desktop", None, "ChatGPT desktop app"
    if "local_wangp.py" in c and " worker" in c:
        return "wangp-worker", "wangp", "WanGP local worker (XAI)"
    if "wgp.py" in c:
        return "wangp-webui", "wangp", "WanGP Web UI"
    if "comfyui" in c and ("main.py" in c or "comfy" in n):
        return "comfyui", "comfyui", "ComfyUI"
    if n in {"ollama.exe", "ollama app.exe", "ollama"}:
        return "ollama", "ollama", "Ollama server" if "serve" in c else "Ollama app"
    if "ollama" in n and "runner" in c:
        return "ollama", "ollama", "Ollama model runner"
    if "personal-prompt-studio" in c or "personal-prompt-studio" in e:
        if "web_generation_worker" in c or "idea_production_worker" in c:
            return "xai-tool", "xai-tools", "Web generation worker"
        if "uvicorn" in c:
            return "gallery", "gallery", "Gallery API (uvicorn)"
        if "public-site" in c:
            return "gallery", "gallery", "Gallery public site"
        if "public-publisher" in c:
            return "gallery", "gallery", "Gallery publisher"
        return "gallery", "gallery", "Gallery process"
    if "xai-studio\\tools\\" in c:
        script = None
        for token in c.split():
            if "xai-studio\\tools\\" in token and token.endswith(".py"):
                script = token.rsplit("\\", 1)[-1]
                break
        return "xai-tool", "xai-tools", f"XAI tool {script}" if script else "XAI tool"
    if "hermes_cli" in c or ("hermes-agent" in c and is_python):
        return "hermes-agent", "hermes", "Hermes agent server" if "serve" in c else "Hermes agent"
    if n == "hermes.exe":
        if "--type=" in c:
            return "hermes-desktop-helper", "hermes", "Hermes desktop helper"
        return "hermes-desktop", "hermes", "Hermes desktop app"
    if is_python and root and (root in c or root in e or (w and w.startswith(root))):
        return "wangp", "wangp", "WanGP Python process"
    if is_python:
        return "python", None, "Python process"
    if n in {"node.exe", "node", "node_repl.exe"}:
        return "node", None, "Node process"
    return "other", None, name or "process"


def _normalize_cpu(raw: float) -> float:
    count = os.cpu_count() or 1
    return raw / count


class ProcessObserver:
    """Scans processes with psutil, keeps per-process handles so CPU deltas are meaningful."""

    def __init__(self, wangp_root: str | None = r"D:\AI\WanGP") -> None:
        self.wangp_root = wangp_root
        self._agent_active_since: dict[str, str] = {}
        self._agent_last_active: dict[str, float] = {}
        self._agent_last_active_iso: dict[str, str] = {}

    # ------------------------------------------------------------------ raw collection
    def _iter_raw(self) -> Iterable[dict[str, Any]]:
        if psutil is None:
            return []
        rows: list[dict[str, Any]] = []
        # psutil.process_iter caches Process instances per (pid, create_time), so cpu_percent(None)
        # measures the delta since the previous scan on the same instance.
        for proc in psutil.process_iter(["pid", "ppid", "name", "exe", "cmdline", "create_time", "memory_info"]):
            info = proc.info
            pid = info.get("pid")
            if pid is None:
                continue
            try:
                cpu = proc.cpu_percent(None)
            except (psutil.Error, OSError):
                cpu = 0.0
            cmd = info.get("cmdline")
            rows.append({
                "pid": pid,
                "ppid": info.get("ppid"),
                "name": info.get("name") or "",
                "exe": info.get("exe"),
                "cmdline": " ".join(cmd) if isinstance(cmd, list) else (cmd or None),
                "create_time": info.get("create_time"),
                "rss": getattr(info.get("memory_info"), "rss", None),
                "cpu": cpu,
                "_proc": proc,
            })
        return rows

    def _cwd(self, row: dict[str, Any]) -> str | None:
        proc = row.get("_proc")
        if proc is None:
            return None
        try:
            return proc.cwd()
        except Exception:
            return None

    # ------------------------------------------------------------------ snapshot
    def scan(self, gpu_pids: dict[int, float | None] | None = None, rows: Iterable[dict[str, Any]] | None = None,
             now: float | None = None) -> ProcessSnapshot:
        gpu_pids = gpu_pids or {}
        now = now if now is not None else time.time()
        try:
            raw = list(rows) if rows is not None else list(self._iter_raw())
        except Exception as exc:  # psutil failures must not kill the monitor
            return ProcessSnapshot(processes=[], agents=self._agent_states({}, now), error=str(exc))

        by_pid: dict[int, dict[str, Any]] = {r["pid"]: r for r in raw}
        classified: dict[int, tuple[str, str | None, str]] = {}
        for r in raw:
            kind, agent, label = classify(r.get("name"), r.get("cmdline"), r.get("exe"), None, self.wangp_root)
            if kind == "python" and rows is None:
                cwd = self._cwd(r)
                if cwd:
                    kind, agent, label = classify(r.get("name"), r.get("cmdline"), r.get("exe"), cwd, self.wangp_root)
                    r["cwd"] = cwd
            classified[r["pid"]] = (kind, agent, label)

        # Fold unclassified descendants into their nearest classified ancestor's agent (max 4 levels).
        def inherit(pid: int) -> str | None:
            seen = 0
            cur = by_pid.get(pid)
            while cur is not None and seen < 4:
                ppid = cur.get("ppid")
                parent = by_pid.get(ppid) if ppid else None
                if parent is None:
                    return None
                pk = classified.get(parent["pid"])
                if pk and pk[1]:
                    return pk[1]
                cur = parent
                seen += 1
            return None

        processes: list[ProcessInfo] = []
        agent_cpu: dict[str, float] = {}
        agent_pids: dict[str, list[int]] = {}
        agent_gpu: dict[str, bool] = {}
        agent_oldest: dict[str, float] = {}
        for r in raw:
            pid = r["pid"]
            kind, agent, label = classified[pid]
            if agent is None and kind in {"other", "node", "python"}:
                inherited = inherit(pid)
                if inherited:
                    agent = inherited
            cpu = _normalize_cpu(float(r.get("cpu") or 0.0))
            on_gpu = pid in gpu_pids
            if agent:
                agent_cpu[agent] = agent_cpu.get(agent, 0.0) + cpu
                agent_pids.setdefault(agent, []).append(pid)
                # a desktop helper idling on the GPU (e.g. an on-device model utility) is not 'working'
                agent_gpu[agent] = agent_gpu.get(agent, False) or (on_gpu and kind in AI_RUNTIME_KINDS)
                ct = r.get("create_time")
                if ct:
                    agent_oldest[agent] = min(agent_oldest.get(agent, ct), ct)
            interesting = kind not in {"other", "node"} or on_gpu or (agent is not None and cpu >= ACTIVE_CPU_PERCENT)
            if kind.endswith("-helper") and not on_gpu and cpu < ACTIVE_CPU_PERCENT:
                interesting = False
            if not interesting:
                continue
            ct = r.get("create_time")
            created_iso = datetime.fromtimestamp(ct, tz=timezone.utc).isoformat(timespec="seconds") if ct else None
            cmd = r.get("cmdline") or None
            processes.append(ProcessInfo(
                pid=pid, ppid=r.get("ppid"), name=r.get("name") or "", kind=kind, agent=agent, label=label,
                exe=r.get("exe"), cmdline=cmd[:300] if cmd else None, cwd=r.get("cwd"),
                created_at=created_iso, elapsed_seconds=max(0.0, now - ct) if ct else None,
                cpu_percent=round(cpu, 1), memory_rss_mb=round(r["rss"] / 1048576, 1) if r.get("rss") else None,
                on_gpu=on_gpu, gpu_memory_mib=gpu_pids.get(pid) if on_gpu else None,
                active=cpu >= ACTIVE_CPU_PERCENT,
            ))
        processes.sort(key=lambda p: (0 if p.on_gpu else 1, -(p.cpu_percent), p.pid))
        agents = self._agent_states(
            {a: {"cpu": agent_cpu.get(a, 0.0), "pids": agent_pids.get(a, []), "gpu": agent_gpu.get(a, False),
                 "oldest": agent_oldest.get(a)} for a in set(agent_pids)},
            now,
        )
        return ProcessSnapshot(processes=processes, agents=agents, total_processes=len(raw))

    def _agent_states(self, seen: dict[str, dict[str, Any]], now: float) -> list[AgentState]:
        states: list[AgentState] = []
        order = list(AGENT_ORDER) + [a for a in seen if a not in AGENT_ORDER]
        for agent in order:
            label = AGENT_LABELS.get(agent, agent)
            data = seen.get(agent)
            if not data:
                self._agent_active_since.pop(agent, None)
                states.append(AgentState(agent=agent, label=label, state="offline"))
                continue
            cpu = data["cpu"]
            working = cpu >= ACTIVE_CPU_PERCENT or data["gpu"]
            if working:
                self._agent_last_active[agent] = now
                self._agent_last_active_iso[agent] = datetime.fromtimestamp(now, tz=timezone.utc).isoformat(timespec="seconds")
                self._agent_active_since.setdefault(agent, self._agent_last_active_iso[agent])
                state = "working"
            else:
                last = self._agent_last_active.get(agent)
                if last is not None and now - last <= IDLE_GRACE_SECONDS:
                    state = "working"  # brief pauses between tool calls are still one working stretch
                else:
                    self._agent_active_since.pop(agent, None)
                    state = "idle"
            oldest = data.get("oldest")
            states.append(AgentState(
                agent=agent, label=label, state=state, process_count=len(data["pids"]), cpu_percent=round(cpu, 1),
                on_gpu=data["gpu"], active_since=self._agent_active_since.get(agent),
                last_active_at=self._agent_last_active_iso.get(agent),
                oldest_started_at=datetime.fromtimestamp(oldest, tz=timezone.utc).isoformat(timespec="seconds") if oldest else None,
                pids=sorted(data["pids"])[:20],
                note="activity inferred from CPU/GPU use, not a progress measure",
            ))
        return states
