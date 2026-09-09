from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DB_PATH = Path(r"D:\AI_Studio\control-tower\control_tower.sqlite3")
# Producers choose their own --runs-root, so scan every place runs actually land: character sessions,
# the repository-root `runs/` Hermes uses for non-character projects, and the character-lab experiments.
DEFAULT_SCAN_ROOTS = [REPO_ROOT / "characters", REPO_ROOT / "runs", REPO_ROOT / "examples"]
DEFAULT_NIGHT_BATCH_ROOT = Path(r"D:\AI_Studio\workspace\hermes-night-batches")
DEFAULT_WEB_JOB_ROOTS = [
    Path.home() / "PersonalPromptStudio" / "workspace" / "generation-jobs",
    Path(r"D:\codex\personal-prompt-studio\personal-prompt-studio\data\workspace\generation-jobs"),
]
DEFAULT_WANGP_ROOT = Path(r"D:\AI\WanGP")


@dataclass
class Config:
    host: str = "0.0.0.0"
    port: int = 8790
    db_path: Path = DEFAULT_DB_PATH
    scan_roots: list[Path] = field(default_factory=lambda: list(DEFAULT_SCAN_ROOTS))
    night_batch_root: Path = DEFAULT_NIGHT_BATCH_ROOT
    web_job_roots: list[Path] = field(default_factory=lambda: list(DEFAULT_WEB_JOB_ROOTS))
    wangp_root: Path = DEFAULT_WANGP_ROOT
    gallery_url: str = "http://127.0.0.1:8787/"  # used when the dashboard is opened on this PC
    gallery_port: int = 8787
    # Used when the dashboard is opened from the tailnet. Detected from `tailscale serve status` at startup
    # unless set explicitly, so the tablet's Open Gallery link does not point at this PC's loopback.
    gallery_tailnet_url: str | None = None
    host_interval: float = 2.0
    job_interval: float = 5.0
    process_interval: float = 3.0
    untracked_gpu_util_threshold: float = 25.0
    recent_limit: int = 12
    history_days: int = 30
    nvidia_smi: str = "nvidia-smi"
    machine_label: str = "RTX 4070"

    @classmethod
    def from_env(cls) -> "Config":
        cfg = cls()
        if os.environ.get("XAI_CT_DB"):
            cfg.db_path = Path(os.environ["XAI_CT_DB"])
        if os.environ.get("XAI_CT_GALLERY_URL"):
            cfg.gallery_url = os.environ["XAI_CT_GALLERY_URL"]
        if os.environ.get("XAI_CT_GALLERY_TAILNET_URL"):
            cfg.gallery_tailnet_url = os.environ["XAI_CT_GALLERY_TAILNET_URL"]
        if os.environ.get("XAI_CT_SCAN_ROOTS"):
            cfg.scan_roots = [Path(p) for p in os.environ["XAI_CT_SCAN_ROOTS"].split(os.pathsep) if p]
        return cfg
