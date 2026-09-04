"""Execute one durable, reference-bound Krea2 variation request."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from reference_transformation_contract import normalize_request


TERMINAL_RUN_STATES = {"succeeded", "needs_review", "failed", "cancelled", "interrupted", "timed_out"}


def compile_edit_instruction(request: dict[str, Any], plan: dict[str, Any]) -> str:
    """Build WanGP-safe prose; its prompt templater treats JSON braces as variables."""
    lines = [
        "Edit the provided reference image.",
        f"Requested change: {request['operator_request'].strip()}",
        "Explicit operations:",
    ]
    for operation in plan["operations"]:
        lines.append(
            f"- {operation['kind']} [{operation['strength']}]: {operation['instruction'].strip()}"
        )
    lines.extend([
        "Preserve exactly: " + ", ".join(plan["effective_preserve"]) + ".",
        "Do not invent, add, remove, or alter any unrequested visual detail.",
    ])
    return "\n".join(lines)


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def update_status(job_dir: Path, status: str, **details: Any) -> None:
    current = json.loads((job_dir / "status.json").read_text(encoding="utf-8")) if (job_dir / "status.json").is_file() else {}
    write_json(job_dir / "status.json", {**current, "status": status, "updated_at": now(), **details})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wait_for_run(run_dir: Path, timeout_seconds: int = 1800) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        record = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        if record.get("status") in TERMINAL_RUN_STATES:
            return record
        time.sleep(1)
    raise TimeoutError(f"Krea2 run timed out: {run_dir.name}")


def settings_for(request: dict[str, Any], seed: int, wangp_root: Path) -> dict[str, Any]:
    plan = request.get("_normalized_plan") or normalize_request(request)
    return {
        "settings_version": 2.73,
        "model_type": "krea2_turbo_edit",
        "base_model_type": "krea2_turbo_edit",
        "model_filename": str(wangp_root / "ckpts" / "Krea2Turbo_quanto_bf16_int8.safetensors"),
        "image_mode": 1,
        "resolution": request.get("source_resolution") or "768x1024",
        "video_prompt_type": "KI",
        "image_refs": [request["reference_path"]],
        "remove_background_images_ref": 0,
        "num_inference_steps": 8,
        "guidance_scale": 0,
        "batch_size": 1,
        "repeat_generation": 1,
        "seed": seed,
        # krea2_turbo_edit owns Identity Edit v1.2 activation. Adding it here loads it twice.
        "activated_loras": [],
        "loras_multipliers": "",
        "image_quality": "jpeg_95",
        "_xai": {
            "kind": "reference_transformation",
            "schema_version": 2,
            "source_schema_version": plan["source_schema_version"],
            "variation_id": request["variation_id"],
            "character_id": request["character_id"],
            "reference_asset_ids": [request["reference_asset_id"]],
            "operator_request": request["operator_request"],
            "operations": plan["operations"],
            "effective_preserve": plan["effective_preserve"],
            "resolved_strategy": plan["resolved_strategy"],
            "effective_strength": plan["effective_strength"],
        },
    }


def run(args: argparse.Namespace) -> int:
    job_dir = Path(args.job_dir).resolve()
    repo_root = Path(args.repo_root).resolve()
    request = json.loads((job_dir / "request.json").read_text(encoding="utf-8"))
    plan = normalize_request(request)
    request["_normalized_plan"] = plan
    compiled_prompt = compile_edit_instruction(request, plan)
    if plan["resolved_strategy"] != "identity_edit":
        update_status(
            job_dir, "blocked_capability", progress="검증된 레퍼런스 재구성 경로가 필요함",
            error=f"Strategy {plan['resolved_strategy']} is not locally verified; no text-to-image fallback was used",
            resolved_strategy=plan["resolved_strategy"], strategy_reason=plan["strategy_reason"],
        )
        return 3
    source = Path(request["reference_path"]).resolve()
    if not source.is_file() or sha256_file(source) != request["reference_sha256"]:
        raise ValueError("reference image is missing or no longer matches its queued SHA-256")

    wangp_root = Path(args.wangp_root).resolve()
    required = [
        wangp_root / "ckpts" / "Krea2Turbo_quanto_bf16_int8.safetensors",
        wangp_root / "loras" / "krea2" / "krea2_identity_edit_v1_2.safetensors",
        wangp_root / "ckpts" / "Qwen3-VL-4B-Instruct" / "Qwen3-VL-4B-Instruct_vision_bf16.safetensors",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        update_status(job_dir, "blocked_dependency", progress="Krea2 편집 모델 구성요소가 필요함", error="Missing: " + ", ".join(missing))
        return 2

    session_dir = repo_root / "characters" / request["character_id"] / "02_generations" / request["session_slug"]
    output_dir = Path(args.library_root).resolve() / "characters" / request["character_id"] / "generations" / request["session_slug"] / "outputs" / "krea2"
    runs_root = session_dir / "runs"
    session_dir.mkdir(parents=True, exist_ok=False)
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = session_dir / "prompt.txt"
    settings_path = session_dir / "krea2.settings.json"
    prompt_path.write_text(compiled_prompt + "\n", encoding="utf-8")
    write_json(session_dir / "prompt-trace.json", {
        "schema_version": 2,
        "kind": "reference_transformation",
        "raw_user_prompt": request["operator_request"],
        "source_schema_version": plan["source_schema_version"],
        "normalized_operations": plan["operations"],
        "requested_preserve": plan["requested_preserve"],
        "resolved_conflicts": plan["resolved_conflicts"],
        "effective_preserve": plan["effective_preserve"],
        "strategy": {"requested": plan["requested_strategy"], "resolved": plan["resolved_strategy"], "reason": plan["strategy_reason"]},
        "stages": [{"id": "stage-1", "strategy": "identity_edit", "reference_asset_id": request["reference_asset_id"]}],
        "effective_strength": plan["effective_strength"],
        "compiled_edit_instruction": compiled_prompt,
        "reference": {"asset_id": request["reference_asset_id"], "path": str(source), "sha256": request["reference_sha256"], "byte_count": request["reference_byte_count"]},
        "source_prompt": request.get("source_prompt"),
        "renderer": {"engine": "krea2_identity_edit", "model_type": "krea2_turbo_edit", "identity_edit_lora_activation": "preset-owned", "reference_binding": "image_refs"},
        "created_at": request["created_at"],
    })
    batch = {
        "schema_version": 1,
        "session": {
            "id": request["session_slug"], "title": f"Reference variation · {request['operator_request']}",
            "character_id": request["character_id"], "asset_root": str(output_dir.parent),
            "visibility": "restricted", "phase": "reference-variation", "prompt_trace_file": "prompt-trace.json",
        },
        "engines": {"krea2": {"backend": "local-wangp", "model": "krea2_turbo_edit", "count": request["count"], "reference_asset_id": request["reference_asset_id"]}},
        "jobs": [],
    }
    (session_dir / "batch.yaml").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    update_status(job_dir, "running", progress="Krea2 레퍼런스 변형 실행 중", session_dir=str(session_dir))

    local_adapter = repo_root / "tools" / "local_wangp.py"
    run_records = []
    for index in range(request["count"]):
        settings = settings_for(request, int(datetime.now().timestamp()) + index, wangp_root)
        write_json(settings_path, settings)
        command = [
            sys.executable, str(local_adapter), "submit", "--runs-root", str(runs_root),
            "--prompt-file", str(prompt_path), "--settings-file", str(settings_path),
            "--project-id", request["variation_id"], "--prompt-id", f"candidate-{index + 1}",
            "--wangp-root", str(wangp_root), "--wangp-python", str(Path(args.wangp_python).resolve()),
            "--output-dir", str(output_dir),
        ]
        submitted = subprocess.run(command, cwd=str(repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if submitted.returncode != 0:
            raise RuntimeError((submitted.stderr or submitted.stdout).strip() or "Krea2 submission failed")
        submission = json.loads(submitted.stdout)
        update_status(job_dir, "running", progress=f"Krea2 후보 {index + 1}/{request['count']} 생성 중")
        record = wait_for_run(Path(submission["run_dir"]))
        run_records.append({"run_id": record["run_id"], "run_dir": submission["run_dir"], "status": record["status"], "artifacts": record.get("artifacts", [])})
        if record["status"] not in {"succeeded", "needs_review"}:
            raise RuntimeError(((record.get("error") or {}).get("message")) or f"Krea2 run ended as {record['status']}")

    batch["jobs"] = [{"engine": "krea2", "backend": "local-wangp", **record} for record in run_records]
    (session_dir / "batch.yaml").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    synced = False
    sync_error = None
    try:
        urllib.request.urlopen(urllib.request.Request(args.sync_url, method="POST"), timeout=120).read()
        synced = True
    except Exception as exc:
        sync_error = str(exc)
    result_session_id = "ses-" + request["session_slug"].lower()
    update_status(job_dir, "completed", progress="변형 완료", result_session_id=result_session_id, session_dir=str(session_dir), runs=run_records, synced=synced, sync_error=sync_error)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Durable Krea2 reference variation worker")
    parser.add_argument("--job-dir", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--wangp-root", required=True)
    parser.add_argument("--wangp-python", required=True)
    parser.add_argument("--library-root", required=True)
    parser.add_argument("--sync-url", default="http://127.0.0.1:8787/api/sync")
    args = parser.parse_args(argv)
    try:
        return run(args)
    except Exception as exc:
        update_status(Path(args.job_dir), "failed", progress="변형 실패", error=f"{type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
