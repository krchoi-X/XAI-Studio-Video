"""CLI for external_media_import."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .apply import apply_plan
from .models import ItemStatus
from .planner import build_plan
from .sync_client import post_sync

DEFAULT_LIBRARY_ROOT = r"D:\AI_Studio\library\characters"


def _default_record_root(character_id: str) -> str:
    return rf"D:\codex\XAI-studio\characters\{character_id}\02_generations"


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    # --manifest and --source-dir may be combined (manifest paths resolve under source-dir).
    parser.add_argument("--manifest", type=str, default=None, help="JSON manifest of items to import")
    parser.add_argument(
        "--source-dir",
        type=str,
        default=None,
        help="Folder of PNG/JPEG/WebP/MP4/WebM (also resolves relative manifest paths)",
    )
    parser.add_argument("--character-id", required=True, help="e.g. ch-mizuki-reika")
    parser.add_argument("--session-id", required=True, help="Batch/session id (folder name)")
    parser.add_argument("--title", required=True, help="Human-readable session title")
    parser.add_argument(
        "--engine",
        required=True,
        help="Engine folder under outputs/ (Studio uses first path element as engine)",
    )
    parser.add_argument(
        "--library-root",
        default=DEFAULT_LIBRARY_ROOT,
        help=f"Default: {DEFAULT_LIBRARY_ROOT}",
    )
    parser.add_argument(
        "--record-root",
        default=None,
        help="Default: D:\\codex\\XAI-studio\\characters\\<character-id>\\02_generations",
    )
    parser.add_argument(
        "--visibility",
        default="standard",
        choices=["standard", "restricted"],
        help="Taken from input only; never lifted based on engine name",
    )
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--allowed-source-root",
        action="append",
        default=[],
        dest="allowed_source_roots",
        help="Repeatable. Paths outside these roots are rejected.",
    )
    parser.add_argument(
        "--prompt-file",
        default=None,
        help="Optional shared prompt text file (only applied to items lacking prompt)",
    )
    parser.add_argument(
        "--prompt-strategy",
        choices=["auto", "shared", "provenance", "split"],
        default="auto",
        help="How to record prompts when items differ (default auto→provenance if multiple)",
    )
    parser.add_argument("--no-probe", action="store_true", help="Skip media probe (tests only)")
    parser.add_argument("--ffprobe", default=None, help="ffprobe binary path override")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Print machine-readable JSON report",
    )
    parser.add_argument(
        "--sync-url",
        default=None,
        help="Optional POST target (e.g. http://127.0.0.1:8787/api/sync)",
    )
    parser.add_argument(
        "--sync-only",
        action="store_true",
        help="Only POST sync-url; do not copy (requires existing matching files + batch.yaml)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="external_media_import",
        description=(
            "Import external images/videos into Studio library + generation records. "
            "Default mode is dry-run (plan): report only, write nothing."
        ),
    )
    parser.add_argument("--version", action="version", version="external_media_import 0.1.0")

    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in [
        ("dry-run", "Plan only: report missing/invalid/dupe/conflicts/planned paths; write nothing"),
        ("plan", "Alias for dry-run"),
        ("apply", "Copy originals, write provenance/prompt, publish batch.yaml last; optional sync"),
        ("resume", "Continue after interrupt (hash-equal destinations are no-ops)"),
    ]:
        p = sub.add_parser(name, help=help_text)
        _add_common_args(p)

    return parser


def _plan_kwargs(args: argparse.Namespace) -> dict:
    record_root = args.record_root or _default_record_root(args.character_id)
    shared_prompt = None
    if args.prompt_file:
        shared_prompt = Path(args.prompt_file).read_text(encoding="utf-8")

    if not args.manifest and not args.source_dir:
        raise SystemExit("error: provide --manifest and/or --source-dir")

    return dict(
        character_id=args.character_id,
        session_id=args.session_id,
        title=args.title,
        engine=args.engine,
        library_root=Path(args.library_root),
        record_root=Path(record_root),
        visibility=args.visibility,
        provider=args.provider,
        model=args.model,
        manifest_path=Path(args.manifest) if args.manifest else None,
        source_dir=Path(args.source_dir) if args.source_dir else None,
        allowed_source_roots=[Path(p) for p in args.allowed_source_roots] or None,
        shared_prompt=shared_prompt,
        prompt_strategy=args.prompt_strategy,
        probe=not args.no_probe,
        ffprobe_bin=args.ffprobe,
    )


def _print_human_plan(plan) -> None:
    counts = plan.counts()
    print(f"session: {plan.session_id}")
    print(f"character: {plan.character_id}")
    print(f"engine: {plan.engine}")
    print(f"visibility: {plan.visibility}")
    print(f"prompt_strategy: {plan.prompt_strategy}")
    print(f"record_dir: {plan.record_dir}")
    print(f"outputs_dir: {plan.outputs_dir}")
    print(f"asset_root: {plan.asset_root}")
    print(f"counts: {counts}")
    for w in plan.warnings:
        print(f"WARNING: {w}")
    for e in plan.errors:
        print(f"ERROR: {e}")
    for item in plan.items:
        status = item.status.value if isinstance(item.status, ItemStatus) else item.status
        extra = ""
        if item.probe and item.probe.kind in {"image", "video"}:
            dims = ""
            if item.probe.width and item.probe.height:
                dims = f" {item.probe.width}x{item.probe.height}"
            dur = f" {item.probe.duration_seconds:.2f}s" if item.probe.duration_seconds else ""
            extra = f" [{item.probe.kind}/{item.probe.mime}{dims}{dur}]"
        print(f"  [{status}] {item.dest_name} <- {item.resolved_source or item.source_path}{extra}")
        if item.message:
            print(f"           {item.message}")
        if item.dest_path and status in {"planned", "duplicate", "conflict"}:
            print(f"           -> {item.dest_path}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    command = args.command
    if command == "plan":
        command = "dry-run"

    try:
        kwargs = _plan_kwargs(args)
    except SystemExit as exc:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # sync-only path
    if getattr(args, "sync_only", False):
        if not args.sync_url:
            print("error: --sync-only requires --sync-url", file=sys.stderr)
            return 2
        plan = build_plan(**kwargs)
        # Require all items already present with matching hash
        not_ready = [
            i
            for i in plan.items
            if i.status != ItemStatus.DUPLICATE
        ]
        if not_ready or plan.errors:
            print(
                "error: sync-only refused — media copy not complete "
                f"(non-duplicate items: {len(not_ready)}). Fix copies first; sync failure != copy failure.",
                file=sys.stderr,
            )
            if args.as_json:
                print(json.dumps({"sync_attempted": False, "plan": plan.to_dict()}, ensure_ascii=False, indent=2))
            else:
                _print_human_plan(plan)
            return 4
        batch = Path(plan.record_dir) / "batch.yaml"
        if not batch.is_file():
            print("error: sync-only refused — batch.yaml missing (publish apply first)", file=sys.stderr)
            return 4
        sync = post_sync(args.sync_url)
        if args.as_json:
            print(
                json.dumps(
                    {
                        "sync_attempted": True,
                        "sync_ok": sync.ok,
                        "sync_message": sync.message,
                        "sync_status_code": sync.status_code,
                        "sync_body": sync.body,
                        "plan": plan.to_dict(),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            print(f"sync_ok={sync.ok} status={sync.status_code} {sync.message}")
        return 0 if sync.ok else 5  # 5 = sync failure (copies already OK)

    plan = build_plan(**kwargs)

    if command == "dry-run":
        if args.as_json:
            print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2))
        else:
            _print_human_plan(plan)
            print("(dry-run: no files written)")
        return 1 if plan.has_blocking_errors() else 0

    # apply / resume (resume == apply with hash-equal no-ops)
    result = apply_plan(plan)

    # Optional sync after successful publish
    if args.sync_url and result.batch_published and result.exit_code == 0:
        sync = post_sync(args.sync_url)
        result.sync_attempted = True
        result.sync_ok = sync.ok
        result.sync_message = sync.message
        if not sync.ok:
            # Distinguish sync failure from copy failure
            result.exit_code = 5
            result.sync_message = (
                f"{sync.message} — copies and batch.yaml succeeded; "
                "retry with --sync-only --sync-url ... (will not re-copy identical hashes)"
            )

    if args.as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_human_plan(result.plan)
        print(
            f"apply: copied={result.copied} noop={result.noop} failed={result.failed} "
            f"records={result.records_written} batch_published={result.batch_published}"
        )
        if result.sync_attempted:
            print(f"sync: ok={result.sync_ok} {result.sync_message}")

    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
