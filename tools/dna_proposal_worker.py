#!/usr/bin/env python3
"""Turn a frozen tablet-review snapshot into a non-mutating Character DNA proposal."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


def stable_hash(character: dict[str, Any]) -> str:
    text = json.dumps(character["stable_dna"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate(snapshot: dict[str, Any], character: dict[str, Any], model: str) -> dict[str, Any]:
    prompt = f"""You are reviewing accumulated human feedback for one adult fictional character.
Return JSON only. You are proposing changes; never claim that you edited the canonical character.

Separate evidence into:
1. stable_dna_changes: only persistent identity traits supported by repeated or explicit user feedback.
2. scene_preferences: outfit, pose, expression, location, camera, lighting, or action preferences.
3. model_findings: renderer-specific successes or failures.
4. rejected_as_dna: feedback that must not alter stable identity.
5. conflicts: contradictory or ambiguous evidence.
6. questions: decisions requiring the user.
7. validation_plan: a small image batch for validating approved changes.

Each stable_dna_changes item must contain path, current, proposed, rationale, evidence_ids, confidence (low/medium/high).
Do not invent traits absent from the current DNA or feedback. Do not infer personality or biography from appearance.
Preserve sensitive physical traits exactly unless the user's feedback explicitly requests a change.

Required top-level JSON fields:
summary, stable_dna_changes, scene_preferences, model_findings, rejected_as_dna, conflicts, questions, validation_plan.

CURRENT CHARACTER:
{json.dumps(character, ensure_ascii=False)}

FROZEN TABLET REVIEW SNAPSHOT:
{json.dumps(snapshot, ensure_ascii=False)}"""
    payload = json.dumps({"model": model, "stream": False, "format": "json", "messages": [{"role": "user", "content": prompt}], "options": {"temperature": 0.15}}).encode("utf-8")
    request = urllib.request.Request(OLLAMA_CHAT, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=600) as response:
        result = json.load(response)
    proposal = json.loads(result["message"]["content"])
    required = {"summary", "stable_dna_changes", "scene_preferences", "model_findings", "rejected_as_dna", "conflicts", "questions", "validation_plan"}
    missing = sorted(required - proposal.keys())
    if missing:
        raise ValueError("proposal missing fields: " + ", ".join(missing))
    return proposal


def markdown(record: dict[str, Any]) -> str:
    proposal = record["proposal"]
    lines = [
        f"# {record['character_name']} DNA 수정 제안서",
        "",
        f"- 제안 ID: `{record['proposal_id']}`",
        f"- 기준 버전: `v{record['base_version']}`",
        f"- 기준 Stable DNA: `{record['base_stable_dna_sha256']}`",
        f"- 작성 모델: `{record['model']}`",
        "",
        "## 요약",
        "",
        str(proposal["summary"]),
        "",
        "## Stable DNA 변경 후보",
        "",
    ]
    changes = proposal.get("stable_dna_changes") or []
    if not changes:
        lines.append("- 변경 근거가 충분한 항목 없음")
    for item in changes:
        lines.extend([
            f"### `{item.get('path', 'unknown')}` · {item.get('confidence', 'unknown')}",
            "",
            f"- 현재: {item.get('current', '')}",
            f"- 제안: {item.get('proposed', '')}",
            f"- 근거: {item.get('rationale', '')}",
            f"- 증거: {', '.join(str(value) for value in item.get('evidence_ids', []))}",
            "",
        ])
    for key, title in (
        ("scene_preferences", "Scene/의상/포즈 선호"),
        ("model_findings", "모델별 발견"),
        ("rejected_as_dna", "DNA로 반영하지 않을 의견"),
        ("conflicts", "충돌·불확실성"),
        ("questions", "사용자 확인 질문"),
        ("validation_plan", "승인 후 검증 계획"),
    ):
        lines.extend([f"## {title}", "", "```json", json.dumps(proposal.get(key), ensure_ascii=False, indent=2), "```", ""])
    lines.extend(["> 이 문서는 제안서이며 canonical Character DNA를 변경하지 않았습니다.", ""])
    return "\n".join(lines)


def process(job_dir: Path, repo_root: Path, model: str) -> None:
    status_path = job_dir / "status.json"
    snapshot = json.loads((job_dir / "snapshot.json").read_text(encoding="utf-8"))
    character_path = repo_root / "characters" / snapshot["character_id"] / "character.json"
    character = json.loads(character_path.read_text(encoding="utf-8"))
    atomic_json(status_path, {"status": "running", "updated_at": now(), "model": model})
    try:
        proposal = generate(snapshot, character, model)
        record = {
            "schema_version": 1,
            "proposal_id": snapshot["proposal_id"],
            "character_id": character["id"],
            "character_name": character["name"],
            "base_version": character["version"],
            "base_stable_dna_sha256": stable_hash(character),
            "snapshot_created_at": snapshot["created_at"],
            "created_at": now(),
            "model": model,
            "status": "needs_review",
            "proposal": proposal,
        }
        atomic_json(job_dir / "proposal.json", record)
        (job_dir / "proposal.md").write_text(markdown(record), encoding="utf-8")
        atomic_json(status_path, {"status": "needs_review", "updated_at": now(), "model": model, "proposal_path": str(job_dir / "proposal.json")})
    except Exception as exc:
        atomic_json(status_path, {"status": "failed", "updated_at": now(), "model": model, "error": f"{type(exc).__name__}: {exc}"})
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
