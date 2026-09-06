"""`python -m control_tower` — run the local Control Tower server."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .config import Config


def build_parser() -> argparse.ArgumentParser:
    cfg = Config.from_env()
    parser = argparse.ArgumentParser(prog="control_tower", description="XAI Control Tower — local job observability")
    parser.add_argument("--host", default=cfg.host, help="bind address (default 0.0.0.0 so the tailnet can reach it)")
    parser.add_argument("--port", type=int, default=cfg.port)
    parser.add_argument("--db", default=str(cfg.db_path), help="SQLite file for snapshots/timing history")
    parser.add_argument("--scan-root", action="append", help="directory tree containing */runs/*/run.json (repeatable)")
    parser.add_argument("--night-batch-root", default=str(cfg.night_batch_root))
    parser.add_argument("--web-job-root", action="append", help="Gallery generation-jobs directory (repeatable)")
    parser.add_argument("--gallery-url", default=cfg.gallery_url, help="link target for 'Open in Gallery'")
    parser.add_argument("--wangp-root", default=str(cfg.wangp_root))
    parser.add_argument("--host-interval", type=float, default=cfg.host_interval)
    parser.add_argument("--job-interval", type=float, default=cfg.job_interval)
    parser.add_argument("--log-level", default="info")
    parser.add_argument("--check", action="store_true", help="sample once, print a summary, and exit without serving")
    return parser


def config_from_args(args: argparse.Namespace) -> Config:
    cfg = Config.from_env()
    cfg.host = args.host
    cfg.port = args.port
    cfg.db_path = Path(args.db)
    if args.scan_root:
        cfg.scan_roots = [Path(p) for p in args.scan_root]
    cfg.night_batch_root = Path(args.night_batch_root)
    if args.web_job_root:
        cfg.web_job_roots = [Path(p) for p in args.web_job_root]
    cfg.gallery_url = args.gallery_url
    cfg.wangp_root = Path(args.wangp_root)
    cfg.host_interval = args.host_interval
    cfg.job_interval = args.job_interval
    return cfg


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = config_from_args(args)
    if args.check:
        from .monitor import MonitorService

        service = MonitorService(cfg)
        service.tick(force=True)
        view = service.overview()
        host = view["host"]
        gpu = host["gpus"][0] if host.get("gpus") else None
        print(f"GPU: {gpu['name']} util={gpu['utilization_percent']}% vram={gpu['memory_used_mib']}/{gpu['memory_total_mib']} MiB temp={gpu['temperature_c']}C" if gpu else f"GPU unavailable: {host.get('error')}")
        print("Agents: " + ", ".join(f"{a['label']}={a['state']}" for a in view["processes"]["agents"]))
        print(f"Jobs: total={view['counts']['jobs_total']} active={view['counts']['active']} running={view['counts']['running']} queue={view['counts']['queue']}")
        for job in view["running"]:
            print(f"  RUNNING {job['title']} [{job['progress']['label']}] eta={job['eta_seconds']} ({job['eta_basis']})")
        for item in view["untracked"]:
            print(f"  UNTRACKED pid={item['pid']} likely={item['likely']} reason={item['reason']}")
        print(f"Recent: {len(view['recent'])} · DB rows={view['counts']['history_rows']} · db={cfg.db_path}")
        service.db.close()
        return 0
    import uvicorn

    from .app import create_app

    app = create_app(cfg)
    print(f"XAI Control Tower on http://{cfg.host}:{cfg.port}/  (db: {cfg.db_path})", file=sys.stderr)
    uvicorn.run(app, host=cfg.host, port=cfg.port, log_level=args.log_level, access_log=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
