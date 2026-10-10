"""Validate versioned screenplay-storyboard lineage without modifying artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "screenplay-storyboard-v1.schema.json"


class StoryboardRevisionError(ValueError):
    pass


def sha256(path: Path) -> str:
    """Hash canonical UTF-8 text, independent of BOM and platform line endings."""
    text = path.read_bytes().decode("utf-8-sig")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def read_frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise StoryboardRevisionError("storyboard must begin with YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise StoryboardRevisionError("storyboard frontmatter has no closing delimiter") from exc
    value = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(value, dict):
        raise StoryboardRevisionError("storyboard frontmatter must be an object")
    return value


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _resolve_bound_path(root: Path, value: str, required_prefix: str) -> Path:
    logical = PurePosixPath(value)
    if logical.is_absolute() or ".." in logical.parts or not logical.parts:
        raise StoryboardRevisionError(f"unsafe repository-relative path: {value}")
    if logical.parts[0] != required_prefix:
        raise StoryboardRevisionError(f"path must stay under {required_prefix}/: {value}")
    target = (root / Path(*logical.parts)).resolve()
    if not _inside(target, root.resolve()):
        raise StoryboardRevisionError(f"path escapes repository: {value}")
    return target


def validate_storyboard(
    storyboard: Path,
    *,
    root: Path = ROOT,
    schema_path: Path = SCHEMA,
) -> dict[str, Any]:
    errors: list[str] = []
    root = root.resolve()
    storyboard = storyboard.resolve()
    try:
        if not _inside(storyboard, (root / "storyboards").resolve()):
            raise StoryboardRevisionError("storyboard file must be under storyboards/")
        if not storyboard.is_file():
            raise StoryboardRevisionError(f"storyboard file is missing: {storyboard}")
        metadata = read_frontmatter(storyboard)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(metadata), key=lambda item: list(item.path))
        if schema_errors:
            errors.extend(
                f"schema:{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
                for error in schema_errors
            )
            return {"ok": False, "storyboard": str(storyboard), "errors": errors}

        source = metadata["source_scenario"]
        source_path = _resolve_bound_path(root, source["path"], "scenarios")
        if not source_path.is_file():
            raise StoryboardRevisionError(f"source scenario is missing: {source['path']}")
        actual_source_hash = sha256(source_path)
        if source["sha256"] != actual_source_hash:
            errors.append(
                f"canonical source hash mismatch: expected {source['sha256']}, actual {actual_source_hash}"
            )

        parent = metadata["parent_storyboard"]
        if parent is not None:
            parent_path = _resolve_bound_path(root, parent["path"], "storyboards")
            if parent_path == storyboard:
                errors.append("parent storyboard cannot be the current storyboard")
            elif not parent_path.is_file():
                errors.append(f"parent storyboard is missing: {parent['path']}")
            else:
                actual_parent_hash = sha256(parent_path)
                if parent["sha256"] != actual_parent_hash:
                    errors.append(
                        f"canonical parent hash mismatch: expected {parent['sha256']}, actual {actual_parent_hash}"
                    )
                parent_metadata = read_frontmatter(parent_path)
                if parent_metadata.get("storyboard_id") != metadata["storyboard_id"]:
                    errors.append("parent storyboard_id does not match")
                if parent_metadata.get("revision") != parent["revision"]:
                    errors.append("parent declared revision does not match parent file")
                if parent["revision"] >= metadata["revision"]:
                    errors.append("parent revision must be lower than current revision")

        return {
            "ok": not errors,
            "storyboard": str(storyboard),
            "storyboard_id": metadata["storyboard_id"],
            "revision": metadata["revision"],
            "source": source,
            "errors": errors,
        }
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        return {"ok": False, "storyboard": str(storyboard), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate a storyboard's source and parent bindings")
    validate.add_argument("--storyboard", required=True, type=Path)
    validate.add_argument("--json", action="store_true", help="emit a JSON report")

    digest = subparsers.add_parser("hash", help="print the SHA-256 of a source or storyboard file")
    digest.add_argument("--path", required=True, type=Path)

    args = parser.parse_args()
    if args.command == "hash":
        print(sha256(args.path.resolve()))
        return 0

    report = validate_storyboard(args.storyboard)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["ok"]:
        print(f"OK {report['storyboard_id']} revision {report['revision']}")
    else:
        for error in report["errors"]:
            print(f"ERROR {error}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
