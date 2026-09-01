#!/usr/bin/env python3
"""Compile one durable C3 idea request into storyboard candidates with a local LLM."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "meromero26b-a4b-hermes:latest"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def validate(schema_path: Path, document: dict[str, Any]) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path))
    if errors:
        detail = "; ".join(f"{'/'.join(map(str, item.path)) or '<root>'}: {item.message}" for item in errors[:5])
        raise ValueError(f"schema validation failed: {detail}")


def build_prompt(repo_root: Path, request: dict[str, Any], resolved: dict[str, Any]) -> str:
    skill = (repo_root / "skills" / "idea-to-production" / "SKILL.md").read_text(encoding="utf-8")
    output_schema = (repo_root / "schemas" / "storyboard-candidates-v1.schema.json").read_text(encoding="utf-8")
    return f"""Follow the IDEA-TO-PRODUCTION skill below. Return one JSON object only.
Do not claim to render anything. This step ends at storyboard candidates.
Use only the supplied resolved reference summaries. Asset IDs remain opaque.
The output must validate against the supplied closed JSON Schema.

SKILL:
{skill}

OUTPUT JSON SCHEMA:
{output_schema}

VALIDATED REQUEST:
{json.dumps(request, ensure_ascii=False)}

APPROVED ADAPTER RESOLUTION:
{json.dumps(resolved, ensure_ascii=False)}
"""


def generate(prompt: str, model: str) -> dict[str, Any]:
    payload = json.dumps({
        "model": model,
        "stream": False,
        "format": "json",
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": 0.25},
    }).encode("utf-8")
    request = urllib.request.Request(OLLAMA_CHAT, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=600) as response:
        result = json.load(response)
    return json.loads(result["message"]["content"])


def structured_failure(request_id: str, code: str, message: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "request_id": request_id,
        "status": "failed",
        "storyboards": [],
        "errors": [{"code": code, "message": message}],
    }


def process(job_dir: Path, repo_root: Path, model: str) -> None:
    request_path = job_dir / "request.json"
    resolved_path = job_dir / "resolved-references.json"
    status_path = job_dir / "status.json"
    request = json.loads(request_path.read_text(encoding="utf-8"))
    resolved = json.loads(resolved_path.read_text(encoding="utf-8"))
    input_schema = repo_root / "schemas" / "idea-production-request-v1.schema.json"
    output_schema = repo_root / "schemas" / "storyboard-candidates-v1.schema.json"
    validate(input_schema, request)
    atomic_json(status_path, {"status": "running", "updated_at": now(), "model": model})
    try:
        missing = [item for item in resolved.get("assets", []) if item.get("status") != "resolved"]
        missing += [item for item in resolved.get("characters", []) if item.get("status") != "resolved"]
        if missing:
            result = structured_failure(request["request_id"], "reference_not_found", "One or more approved references could not be resolved.")
        else:
            result = generate(build_prompt(repo_root, request, resolved), model)
        validate(output_schema, result)
        if result["request_id"] != request["request_id"]:
            raise ValueError("output request_id does not match the durable request")
        atomic_json(job_dir / "storyboards.json", result)
        atomic_json(status_path, {
            "status": result["status"], "updated_at": now(), "model": model,
            "storyboard_count": len(result["storyboards"]),
            "error": result["errors"][0]["message"] if result["errors"] else None,
        })
    except Exception as exc:
        failure = structured_failure(request.get("request_id", "req_unknown"), "storyboard_generation_failed", f"{type(exc).__name__}: {exc}")
        atomic_json(job_dir / "storyboards.json", failure)
        atomic_json(status_path, {"status": "failed", "updated_at": now(), "model": model, "error": failure["errors"][0]["message"]})
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    process(args.job_dir.resolve(), args.repo_root.resolve(), args.model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
