#!/usr/bin/env python3
"""List the WanGP `model_type` values this workstation can actually run.

WanGP takes its `model_type` from the file names in `<wangp>/defaults` and `<wangp>/finetunes`. A definition
existing there does not mean the weights are on disk, and several definitions borrow another model's weights or
need extra module/LoRA files. Guessing an id fails in WanGP validation before any GPU work starts, which is what
`Unknown model type minimax_h3` was.

    python tools/wangp_models.py                      usable model types
    python tools/wangp_models.py --all                include ones whose weights are missing
    python tools/wangp_models.py --json               machine-readable
    python tools/wangp_models.py --check <model_type> exit 0 when it is usable, 2 otherwise
    python tools/wangp_models.py --write              regenerate docs/wangp-models.md

Read-only over the WanGP installation.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WANGP_ROOT = Path(r"D:\AI\WanGP")
DEFAULT_DOC = REPO_ROOT / "docs" / "wangp-models.md"
WEIGHT_SUFFIXES = {".safetensors", ".gguf", ".pt", ".ckpt"}


def load_definitions(wangp_root: Path) -> dict[str, dict[str, Any]]:
    """Every model_type WanGP knows, from both the shipped defaults and local finetunes."""
    definitions: dict[str, dict[str, Any]] = {}
    for folder, origin in ((wangp_root / "defaults", "default"), (wangp_root / "finetunes", "finetune")):
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError):
                continue
            if isinstance(data, dict) and isinstance(data.get("model"), dict):
                data["_origin"] = origin
                definitions[path.stem] = data
    return definitions


def _entries(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def resolve_weight_groups(definitions: dict[str, dict[str, Any]], model_id: str, depth: int = 0) -> list[list[str]]:
    """Groups of interchangeable weight files for a model. `URLs` may name another model that owns the weights."""
    if depth > 3 or model_id not in definitions:
        return []
    urls = definitions[model_id]["model"].get("URLs")
    if isinstance(urls, str):
        return resolve_weight_groups(definitions, urls, depth + 1)
    files = [str(u) for u in _entries(urls)]
    return [files] if files else []


def module_groups(definition: dict[str, Any]) -> list[list[str]]:
    """Extra weights a variant needs on top of the base model, e.g. a ControlNet union."""
    groups: list[list[str]] = []
    for module in _entries(definition["model"].get("modules")):
        alternatives = [str(u) for u in _entries(module)]
        if alternatives:
            groups.append(alternatives)
    return groups


def lora_files(definition: dict[str, Any]) -> list[str]:
    return [str(u) for u in _entries(definition["model"].get("loras"))]


class Installation:
    """Where WanGP keeps weights, so a definition can be checked against what is on disk."""

    def __init__(self, wangp_root: Path) -> None:
        self.wangp_root = wangp_root
        self.checkpoints = self._index(wangp_root / "ckpts")
        self.loras = self._index(wangp_root / "loras")

    @staticmethod
    def _index(folder: Path) -> dict[str, Path]:
        found: dict[str, Path] = {}
        if folder.is_dir():
            for path in folder.rglob("*"):
                if path.is_file() and path.suffix.lower() in WEIGHT_SUFFIXES:
                    found.setdefault(path.name, path)
        return found

    def present(self, url_or_path: str, index: dict[str, Path]) -> Path | None:
        """A URL contributes its file name; a finetune may instead point at an absolute local path."""
        candidate = Path(url_or_path)
        if candidate.is_absolute():
            return candidate if candidate.is_file() else None
        return index.get(url_or_path.rsplit("/", 1)[-1])

    def any_present(self, alternatives: list[str], index: dict[str, Path]) -> Path | None:
        for item in alternatives:
            found = self.present(item, index)
            if found is not None:
                return found
        return None


def inspect(definitions: dict[str, dict[str, Any]], installation: Installation, model_id: str) -> dict[str, Any]:
    definition = definitions[model_id]
    model = definition["model"]
    weight_groups = resolve_weight_groups(definitions, model_id)
    weights = installation.any_present(weight_groups[0], installation.checkpoints) if weight_groups else None

    missing: list[str] = []
    if weight_groups and weights is None:
        missing.append("weights")
    for group in module_groups(definition):
        if installation.any_present(group, installation.checkpoints) is None:
            missing.append("module:" + group[0].rsplit("/", 1)[-1])
    for lora in lora_files(definition):
        if installation.present(lora, installation.loras) is None:
            missing.append("lora:" + lora.rsplit("/", 1)[-1])

    if not weight_groups:
        status = "undeclared"  # nothing to download listed; cannot be judged from the definition alone
    elif missing:
        status = "unusable"
    else:
        status = "usable"
    return {
        "model_type": model_id,
        "name": model.get("name", ""),
        "origin": definition.get("_origin", "default"),
        "architecture": model.get("architecture"),
        "status": status,
        "missing": missing,
        "weights": str(weights) if weights else None,
        "num_inference_steps": definition.get("num_inference_steps"),
        "guidance_scale": definition.get("guidance_scale"),
        "resolution": definition.get("resolution"),
    }


def survey(wangp_root: Path) -> list[dict[str, Any]]:
    definitions = load_definitions(wangp_root)
    installation = Installation(wangp_root)
    return sorted((inspect(definitions, installation, model_id) for model_id in definitions),
                  key=lambda row: row["model_type"])


def render_table(rows: list[dict[str, Any]]) -> str:
    width = max((len(r["model_type"]) for r in rows), default=10)
    lines = [f"{'model_type'.ljust(width)}  {'steps':>5} {'guid':>5}  name",
             "-" * (width + 60)]
    for row in rows:
        steps = "" if row["num_inference_steps"] is None else str(row["num_inference_steps"])
        guidance = "" if row["guidance_scale"] is None else str(row["guidance_scale"])
        note = "" if row["status"] == "usable" else f"   [{row['status']}: {', '.join(row['missing']) or 'no weights listed'}]"
        lines.append(f"{row['model_type'].ljust(width)}  {steps:>5} {guidance:>5}  {row['name'][:48]}{note}")
    return "\n".join(lines)


def is_variant_of(model_type: str, installed: set[str]) -> bool:
    """True when this id is a longer or shorter spelling of something already installed.

    Ids are built by extending a base name, so `z_image_control` extends the installed `z_image`, and
    `minimax_h3_ref2va` is the installed `minimax_h3_ref2va_pruned` without its suffix. Comparing on underscore
    boundaries keeps unrelated families out.
    """
    for other in installed:
        if model_type == other:
            continue
        if model_type.startswith(other + "_") or other.startswith(model_type + "_"):
            return True
    return False


def render_doc(rows: list[dict[str, Any]], wangp_root: Path) -> str:
    usable = [r for r in rows if r["status"] == "usable"]
    installed = {r["model_type"] for r in usable}
    # Listing all 200-odd unusable definitions would bury the useful ones; show only variants of something
    # already installed, which are the ids someone is realistically about to reach for.
    unusable = [r for r in rows if r["status"] == "unusable" and is_variant_of(r["model_type"], installed)]
    other_unusable = sum(1 for r in rows if r["status"] == "unusable") - len(unusable)
    stamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    def table(entries: list[dict[str, Any]], with_missing: bool = False) -> list[str]:
        header = "| model_type | steps | guidance | model |" + (" missing |" if with_missing else "")
        rule = "|---|---|---|---|" + ("---|" if with_missing else "")
        out = [header, rule]
        for row in entries:
            steps = "" if row["num_inference_steps"] is None else row["num_inference_steps"]
            guidance = "" if row["guidance_scale"] is None else row["guidance_scale"]
            line = f"| `{row['model_type']}` | {steps} | {guidance} | {row['name']} |"
            if with_missing:
                line += f" {', '.join(row['missing'])} |"
            out.append(line)
        return out

    lines = [
        "# WanGP model types on this workstation",
        "",
        "**Generated file — do not edit by hand.** Refresh with `python tools/wangp_models.py --write`.",
        "",
        f"Generated: {stamp}  ·  WanGP: `{wangp_root}`  ·  definitions: {len(rows)}  ·  usable: {len(usable)}",
        "",
        "`model_type` is the file name of a definition in `<wangp>/defaults` or `<wangp>/finetunes`. Passing anything",
        "else fails in WanGP validation before any GPU work starts. Check one id before submitting:",
        "",
        "```bash",
        "python tools/wangp_models.py --check minimax_h3_ref2va_pruned",
        "```",
        "",
        "## Usable now",
        "",
        "Weights, modules and LoRAs are all present. `steps` and `guidance` are the definition's own defaults.",
        "",
        *table(usable),
        "",
        "## Variants of the same models that are not usable",
        "",
        "The definition exists, so the name looks plausible, but something it needs is not on disk.",
        "",
        *table(unusable, with_missing=True),
        "",
        f"A further {other_unusable} definitions for models not installed here are omitted; "
        "`python tools/wangp_models.py --all` lists everything.",
        "",
        "## Notes",
        "",
        "- A definition may borrow another model's weights (`URLs` naming another id), so two ids can share one file.",
        "- Which ids have actually produced output here is visible in the Control Tower job history, not in this file.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wangp-root", type=Path, default=DEFAULT_WANGP_ROOT)
    parser.add_argument("--all", action="store_true", help="include model types whose weights are missing")
    parser.add_argument("--json", action="store_true", help="print the full survey as JSON")
    parser.add_argument("--check", metavar="MODEL_TYPE", help="exit 0 when that model type is usable, 2 otherwise")
    parser.add_argument("--write", nargs="?", const=str(DEFAULT_DOC), metavar="PATH",
                        help=f"regenerate the checked-in reference (default {DEFAULT_DOC.relative_to(REPO_ROOT)})")
    args = parser.parse_args(argv)

    if not args.wangp_root.is_dir():
        print(f"error: WanGP not found at {args.wangp_root}", file=sys.stderr)
        return 2
    rows = survey(args.wangp_root)

    if args.check:
        match = next((r for r in rows if r["model_type"] == args.check), None)
        if match is None:
            usable = [r["model_type"] for r in rows if r["status"] == "usable"]
            near = [m for m in usable if args.check in m or m in args.check]
            print(f"unknown model type: {args.check}", file=sys.stderr)
            if near:
                print("did you mean: " + ", ".join(near), file=sys.stderr)
            return 2
        print(json.dumps(match, ensure_ascii=False, indent=2))
        return 0 if match["status"] == "usable" else 2

    if args.write:
        path = Path(args.write)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_doc(rows, args.wangp_root), encoding="utf-8")
        print(f"wrote {path} ({sum(1 for r in rows if r['status'] == 'usable')} usable of {len(rows)})")
        return 0

    shown = rows if args.all else [r for r in rows if r["status"] == "usable"]
    if args.json:
        print(json.dumps(shown, ensure_ascii=False, indent=2))
    else:
        print(render_table(shown))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
