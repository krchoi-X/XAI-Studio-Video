"""Run Hermes storyboard authoring behind deterministic file and preflight gates."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from .storyboard_preflight import extract_source, validate_plan
    from .storyboard_revision import ROOT, sha256, validate_storyboard
except ImportError:  # Direct script execution from tools/.
    from storyboard_preflight import extract_source, validate_plan
    from storyboard_revision import ROOT, sha256, validate_storyboard


def _fingerprint(path: Path) -> str | None:
    return sha256(path) if path.is_file() else None


def evaluate_outputs(storyboard: Path, plan: Path) -> dict[str, Any]:
    lineage = validate_storyboard(storyboard)
    if not lineage["ok"]:
        return {"ready": False, "blocked": False, "repair_items": lineage["errors"], "lineage": lineage}
    try:
        preflight = validate_plan(plan)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"ready": False, "blocked": False, "repair_items": [f"preflight plan unreadable: {exc}"], "lineage": lineage}
    return {
        "ready": preflight["ready"],
        "blocked": bool(preflight["unresolved"]),
        "repair_items": preflight["repair_items"],
        "lineage": lineage,
        "preflight": preflight,
    }


def run_pipeline(
    *,
    source: Path,
    storyboard: Path,
    plan: Path,
    hermes_bin: str = "hermes",
    max_attempts: int = 2,
    timeout_seconds: int = 1200,
) -> dict[str, Any]:
    catalog = extract_source(source)
    if not catalog["scenes"]:
        return {"ready": False, "blocked": True, "attempts": 0, "repair_items": ["source has no machine-addressable scenes/actions; request a normalized writer input"]}
    baseline = {"storyboard": _fingerprint(storyboard), "plan": _fingerprint(plan)}
    repair_items: list[str] = []
    transcripts: list[str] = []
    for attempt in range(1, max_attempts + 1):
        task = {
            "source_path": source.relative_to(ROOT).as_posix(),
            "source_sha256": catalog["sha256"],
            "source_catalog": catalog["scenes"],
            "storyboard_output": storyboard.relative_to(ROOT).as_posix(),
            "preflight_plan_output": plan.relative_to(ROOT).as_posix(),
            "required_schema": "schemas/storyboard-preflight-plan-v1.schema.json",
            "repair_items": repair_items,
        }
        prompt = (
            "Use the active screenplay-to-storyboard skill. Write both requested output files; do not only print them. "
            "Map every supplied source event ID exactly once and in order. Copy exact dialogue and acknowledge every supplied constraint ID. "
            "Do not mark unresolved source contradictions as repaired. Stop before Intent Contract or rendering. "
            f"Machine task:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
        )
        completed = subprocess.run(
            [hermes_bin, "-z", prompt],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        transcripts.append(completed.stdout[-4000:])
        if completed.returncode != 0:
            repair_items = [f"Hermes process exited {completed.returncode}: {completed.stderr[-1000:]}"]
            continue
        current = {"storyboard": _fingerprint(storyboard), "plan": _fingerprint(plan)}
        if current == baseline or current["storyboard"] is None or current["plan"] is None:
            repair_items = ["Hermes reported completion but both output files were not created or changed"]
            continue
        report = evaluate_outputs(storyboard, plan)
        if report["ready"] or report["blocked"]:
            report.update({"attempts": attempt, "transcripts": transcripts})
            return report
        repair_items = report["repair_items"]
        baseline = current
    return {"ready": False, "blocked": False, "attempts": max_attempts, "repair_items": repair_items, "transcripts": transcripts}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--hermes-bin", default="hermes")
    parser.add_argument("--max-attempts", type=int, default=2, choices=range(1, 4))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    args = parser.parse_args()
    report = run_pipeline(
        source=args.source.resolve(),
        storyboard=args.storyboard.resolve(),
        plan=args.plan.resolve(),
        hermes_bin=args.hermes_bin,
        max_attempts=args.max_attempts,
        timeout_seconds=args.timeout_seconds,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ready"] else 2 if report["blocked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
