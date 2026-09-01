#!/usr/bin/env python
"""Validate the idea-to-production fixtures against the Codex-owned v1 schemas.

Owned by Claude package C3. This script reads only; it never writes a fixture,
never touches Character DNA, and never imports repository tooling. Run it from
anywhere:

    python tests/fixtures/idea-to-production/validate_fixtures.py

Exit code 0 when every fixture is schema-valid and every semantic invariant in
`manifest.json` holds, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - environment problem, not a fixture problem
    sys.exit("jsonschema is required: python -m pip install jsonschema")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

PATHY = ("/", "\\", ".png", ".jpg", ".jpeg", ".webp", ".safetensors", "C:", "D:")

PRECEDENCE = [
    "explicit_user_constraints",
    "stable_character_dna",
    "scene_requirements",
    "style_enrichment",
    "optional_creative_detail",
]

PROBE_TRACE = {
    "raw_user_prompt": "probe",
    "after_character_dna_merge": "probe",
    "after_constraint_validation": {"ok": True},
    "final_prompt_sent_to_image_engine": "probe",
}


class Report:
    def __init__(self) -> None:
        self.passed = 0
        self.failures: list[str] = []
        self._scope = ""

    def scope(self, label: str) -> None:
        self._scope = label

    def check(self, ok: bool, label: str) -> bool:
        if ok:
            self.passed += 1
        else:
            self.failures.append(f"{self._scope}: {label}")
        return ok


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def looks_like_path(value: str) -> bool:
    return any(token in value for token in PATHY)


def validate(rep: Report, validator: Draft202012Validator, doc: Any, label: str) -> bool:
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if not errors:
        return rep.check(True, label)
    for err in errors[:5]:
        pointer = "/".join(str(part) for part in err.path) or "<root>"
        rep.check(False, f"{label} -> {pointer}: {err.message}")
    return False


# --------------------------------------------------------------------------
# per-kind structural checks
# --------------------------------------------------------------------------


def check_opaque_ids(rep: Report, doc: dict[str, Any]) -> None:
    for key in ("character_ids", "reference_asset_ids", "asset_ids"):
        for value in doc.get(key) or []:
            rep.check(
                not looks_like_path(value),
                f"{key} entry {value!r} must stay an opaque ID, not a filesystem path",
            )


def check_storyboard_candidates(
    rep: Report, doc: dict[str, Any], validators: dict[str, Draft202012Validator]
) -> None:
    status = doc["status"]
    if status == "failed":
        rep.check(doc["storyboards"] == [], "failed candidates must carry no storyboards")
        rep.check(bool(doc["errors"]), "failed candidates must carry at least one error")
    else:
        rep.check(bool(doc["storyboards"]), "needs_user_choice must carry at least one storyboard")
        rep.check(doc["errors"] == [], "needs_user_choice must carry no errors")

    ids = [sb["id"] for sb in doc["storyboards"]]
    rep.check(len(ids) == len(set(ids)), "storyboard IDs must be unique")

    job_props = set(validators["renderer_job_request"].schema["properties"])

    for sb in doc["storyboards"]:
        shot_ids = [shot["id"] for shot in sb["shots"]]
        rep.check(
            len(shot_ids) == len(set(shot_ids)),
            f"{sb['id']}: shot IDs must be unique within a storyboard",
        )
        for shot in sb["shots"]:
            where = f"{sb['id']}/{shot['id']}"
            req = shot["sample_request"]
            rep.check("job_id" not in req, f"{where}: sample_request must not carry job_id")
            rep.check(
                "prompt_trace" not in req, f"{where}: sample_request must not carry prompt_trace"
            )
            unknown = set(req) - job_props
            rep.check(
                not unknown,
                f"{where}: sample_request has keys outside renderer-job-request-v1: {sorted(unknown)}",
            )
            rep.check(req.get("stage") == "sample", f"{where}: sample_request stage must be sample")
            rep.check(
                req.get("request_id") == doc["request_id"],
                f"{where}: sample_request request_id must match the document",
            )
            rep.check(
                req.get("storyboard_id") == sb["id"],
                f"{where}: sample_request storyboard_id must match its storyboard",
            )
            rep.check(
                req.get("shot_id") == shot["id"],
                f"{where}: sample_request shot_id must match its shot",
            )
            check_opaque_ids(rep, req)

            probe = dict(req)
            probe["job_id"] = "job_fixture_probe"
            probe["prompt_trace"] = PROBE_TRACE
            validate(
                rep,
                validators["renderer_job_request"],
                probe,
                f"{where}: sample_request + minted job_id/prompt_trace is a valid renderer job",
            )
            if req.get("scene_spec"):
                validate(
                    rep,
                    validators["scene_spec"],
                    req["scene_spec"],
                    f"{where}: sample_request scene_spec conforms to scene-spec-v1",
                )


def check_renderer_job(
    rep: Report, doc: dict[str, Any], validators: dict[str, Draft202012Validator]
) -> None:
    trace = doc["prompt_trace"]
    strategy = doc["prompt_strategy"]
    raw = trace["raw_user_prompt"]
    merged = trace["after_character_dna_merge"]
    final = trace["final_prompt_sent_to_image_engine"]
    expansion = trace.get("after_scene_style_expansion")

    if "raw_user_prompt" in doc:
        rep.check(
            doc["raw_user_prompt"] == raw,
            "job raw_user_prompt must equal prompt_trace.raw_user_prompt",
        )

    if strategy == "exact":
        rep.check(merged == raw, "exact: after_character_dna_merge must equal raw_user_prompt")
        rep.check(
            final == raw, "exact: final_prompt_sent_to_image_engine must equal raw_user_prompt"
        )
        rep.check(expansion is None, "exact: after_scene_style_expansion must be null")
    elif strategy == "strict_translation":
        rep.check(expansion is None, "strict_translation: after_scene_style_expansion must be null")
        rep.check(merged != raw, "strict_translation: DNA merge must change the prompt")
    else:
        rep.check(
            isinstance(expansion, str) and expansion.strip() != "",
            "creative_expansion: after_scene_style_expansion must be a non-empty string",
        )

    validation = trace["after_constraint_validation"]
    rep.check(
        validation.get("precedence") == PRECEDENCE,
        "after_constraint_validation.precedence must be the C3 ladder in order",
    )
    conflicts = validation.get("conflicts", [])
    suppressed = trace.get("suppressed_stable_dna_fields", [])
    rep.check(
        list(suppressed) == sorted(set(suppressed)),
        "suppressed_stable_dna_fields must be sorted and unique",
    )
    rep.check(
        bool(conflicts) == bool(suppressed),
        "a recorded conflict implies a suppressed DNA field and vice versa",
    )
    outranked = {c["outranked"].split(".", 1)[-1] for c in conflicts}
    rep.check(
        outranked == set(suppressed),
        f"conflicts outrank {sorted(outranked)} but suppressed fields are {sorted(suppressed)}",
    )
    rep.check(
        validation.get("errors") == [] or validation.get("ok") is False,
        "after_constraint_validation errors imply ok is false",
    )

    if doc.get("scene_spec"):
        validate(
            rep, validators["scene_spec"], doc["scene_spec"], "scene_spec conforms to scene-spec-v1"
        )
        rep.check(
            doc["scene_spec"].get("mode") == strategy,
            "scene_spec.mode must equal prompt_strategy",
        )
    check_opaque_ids(rep, doc)


def check_production_result(rep: Report, doc: dict[str, Any]) -> None:
    progress = doc["progress"]
    status = doc["status"]
    completed, failed, total = progress["completed"], progress["failed"], progress["total"]

    rep.check(completed + failed <= total, "completed + failed must not exceed total")
    rep.check(
        len(doc["asset_ids"]) == len(set(doc["asset_ids"])), "asset_ids must be unique"
    )
    if status == "completed":
        rep.check(failed == 0, "completed must not report failed images")
        rep.check(doc["errors"] == [], "completed must carry no errors")
        rep.check(
            doc["result_session_id"] is not None,
            "completed must carry a result_session_id for the Gallery handoff",
        )
    if status in {"failed", "interrupted"}:
        rep.check(bool(doc["errors"]), f"{status} must carry at least one structured error")
    if doc["result_session_id"] is not None:
        rep.check(
            not looks_like_path(doc["result_session_id"]),
            "result_session_id is a Gallery key, not a directory path",
        )
    check_opaque_ids(rep, doc)


# --------------------------------------------------------------------------
# expectations declared in manifest.json
# --------------------------------------------------------------------------


def check_expectations(rep: Report, doc: dict[str, Any], expect: dict[str, Any]) -> None:
    for key, want in expect.items():
        if key == "storyboard_count":
            rep.check(len(doc["storyboards"]) == want, f"expected {want} storyboards")
        elif key == "error_codes":
            got = [e["code"] for e in doc["errors"]]
            rep.check(got == want, f"expected error codes {want}, got {got}")
        elif key == "asset_count":
            rep.check(len(doc["asset_ids"]) == want, f"expected {want} asset_ids")
        elif key == "result_session_id_null":
            rep.check(
                (doc["result_session_id"] is None) == want,
                f"expected result_session_id null={want}",
            )
        elif key == "progress":
            got = {k: doc["progress"][k] for k in want}
            rep.check(got == want, f"expected progress {want}, got {got}")
        elif key == "suppressed_stable_dna_fields":
            got = doc["prompt_trace"].get("suppressed_stable_dna_fields", [])
            rep.check(got == want, f"expected suppressed DNA fields {want}, got {got}")
        else:
            rep.check(doc.get(key) == want, f"expected {key}={want!r}, got {doc.get(key)!r}")


# --------------------------------------------------------------------------
# cross-file case checks
# --------------------------------------------------------------------------


def run_case_checks(rep: Report, name: str, docs: dict[str, dict[str, Any]], kinds: dict[str, str]) -> None:
    requests = [d for p, d in docs.items() if kinds[p] == "idea_production_request"]
    candidates = [d for p, d in docs.items() if kinds[p] == "storyboard_candidates"]
    jobs = [d for p, d in docs.items() if kinds[p] == "renderer_job_request"]
    results = [d for p, d in docs.items() if kinds[p] == "production_job_result"]
    by_job = {j["job_id"]: j for j in jobs}

    if name == "distinct_job_ids":
        ids = [j["job_id"] for j in jobs]
        rep.check(len(ids) == len(set(ids)), "every renderer job needs its own durable job_id")
        for res in results:
            rep.check(
                res["job_id"] in by_job,
                f"result {res['job_id']} has no renderer job in this case",
            )

    elif name == "job_total_matches_count_times_engines":
        for res in results:
            job = by_job.get(res["job_id"])
            if job is None:
                continue
            want = job["count"] * len(job["engines"])
            rep.check(
                res["progress"]["total"] == want,
                f"{res['job_id']}: progress.total should be count*engines={want}, got {res['progress']['total']}",
            )

    elif name == "sample_before_final":
        finals = [j for j in jobs if j["stage"] == "final"]
        for fin in finals:
            samples = [
                j
                for j in jobs
                if j["stage"] == "sample" and j.get("shot_id") == fin.get("shot_id")
            ]
            rep.check(bool(samples), f"{fin['job_id']}: final stage requires a prior sample job")
            done = [
                r
                for r in results
                if r["job_id"] in {s["job_id"] for s in samples} and r["status"] == "completed"
            ]
            rep.check(bool(done), f"{fin['job_id']}: the sample must have completed before final")

    elif name == "exact_clamped_to_one_storyboard":
        for req in requests:
            if req.get("mode") != "exact":
                continue
            rep.check(req["candidate_count"] > 1, "fixture should exercise clamping")
            for cand in candidates:
                rep.check(
                    len(cand["storyboards"]) == 1,
                    "exact mode must clamp to exactly one storyboard",
                )
                rep.check(
                    len(cand["storyboards"][0]["shots"]) == 1,
                    "exact mode must produce exactly one shot",
                )

    elif name == "exact_shot_description_is_idea_verbatim":
        idea = requests[0]["idea"]
        shot = candidates[0]["storyboards"][0]["shots"][0]
        rep.check(
            shot["description"] == idea,
            "exact mode shot description must be the idea string character for character",
        )
        for job in jobs:
            rep.check(
                job["prompt_trace"]["final_prompt_sent_to_image_engine"] == idea,
                f"{job['job_id']}: exact mode must send the idea unmodified to the engine",
            )

    elif name == "conflict_recorded_in_trace":
        traced = [
            j
            for j in jobs
            if j["prompt_trace"]["after_constraint_validation"].get("conflicts")
        ]
        rep.check(bool(traced), "a resolved constraint conflict must be recorded in a Prompt Trace")

    elif name == "suppression_matches_conflicts":
        for job in jobs:
            conflicts = job["prompt_trace"]["after_constraint_validation"].get("conflicts", [])
            for conflict in conflicts:
                rep.check(
                    conflict.get("resolution") == "constraint_wins",
                    f"{job['job_id']}: a level-1 constraint must win over Stable DNA",
                )
                rep.check(
                    conflict["outranked"].startswith("stable_dna."),
                    f"{job['job_id']}: outranked field must name a Stable DNA field",
                )

    elif name == "one_error_per_unresolved_reference":
        want = len(requests[0]["reference_asset_ids"])
        got = [e for e in candidates[0]["errors"] if e["code"] == "reference_not_found"]
        rep.check(
            len(got) == want,
            f"expected one reference_not_found per unresolved ID ({want}), got {len(got)}",
        )
        rep.check(
            candidates[0]["storyboards"] == [],
            "a missing reference must not produce a partial candidate set",
        )

    elif name == "retry_preserves_prompt":
        groups: dict[tuple, set[str]] = {}
        for job in jobs:
            key = (job.get("storyboard_id"), job.get("shot_id"), job["stage"])
            groups.setdefault(key, set()).add(
                job["prompt_trace"]["final_prompt_sent_to_image_engine"]
            )
        for key, prompts in groups.items():
            rep.check(
                len(prompts) == 1,
                f"{key}: a retry must not silently change the prompt",
            )

    elif name == "failed_result_keeps_partial_assets":
        for res in results:
            if res["status"] != "failed":
                continue
            rep.check(
                len(res["asset_ids"]) == res["progress"]["completed"],
                f"{res['job_id']}: a failed job must retain every durably stored asset",
            )
            if res["progress"]["completed"] > 0:
                rep.check(
                    res["result_session_id"] is not None,
                    f"{res['job_id']}: partial results still need a Gallery handoff key",
                )
    else:
        rep.check(False, f"unknown case check {name!r}")


# --------------------------------------------------------------------------


def main() -> int:
    manifest = load(HERE / "manifest.json")
    validators = {
        name: Draft202012Validator(load(ROOT / rel))
        for name, rel in manifest["schemas"].items()
    }

    rep = Report()
    listed: set[Path] = set()

    for case in manifest["cases"]:
        print(f"\n[{case['name']}] {case['summary']}")
        docs: dict[str, dict[str, Any]] = {}
        kinds: dict[str, str] = {}

        for entry in case["files"]:
            rel = entry["path"]
            path = HERE / rel
            listed.add(path.resolve())
            rep.scope(rel)

            if not path.is_file():
                rep.check(False, "fixture file is missing")
                continue
            try:
                doc = load(path)
            except json.JSONDecodeError as exc:
                rep.check(False, f"invalid JSON: {exc}")
                continue

            kind = entry["schema"]
            docs[rel] = doc
            kinds[rel] = kind

            ok = validate(rep, validators[kind], doc, f"valid against {manifest['schemas'][kind]}")
            rep.check(
                doc.get("request_id") == entry.get("request_id", case["request_id"]),
                "request_id must match the case",
            )
            if ok:
                if kind == "storyboard_candidates":
                    check_storyboard_candidates(rep, doc, validators)
                elif kind == "renderer_job_request":
                    check_renderer_job(rep, doc, validators)
                elif kind == "production_job_result":
                    check_production_result(rep, doc)
                elif kind == "idea_production_request":
                    check_opaque_ids(rep, doc)
                check_expectations(rep, doc, entry.get("expect", {}))
            print(f"  - {rel}: {kind}")

        for check in case.get("case_checks", []):
            rep.scope(f"{case['name']}/{check}")
            run_case_checks(rep, check, docs, kinds)
            print(f"  - case check: {check}")

    rep.scope("manifest")
    on_disk = {p.resolve() for p in HERE.rglob("*.json") if p.name != "manifest.json"}
    unlisted = sorted(str(p.relative_to(HERE)) for p in on_disk - listed)
    rep.check(not unlisted, f"fixtures not listed in manifest.json: {unlisted}")

    print(f"\n{rep.passed} checks passed, {len(rep.failures)} failed")
    for failure in rep.failures:
        print(f"  FAIL {failure}")
    return 1 if rep.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
