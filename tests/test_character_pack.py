import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import character_pack as packs


ROOT = Path(__file__).resolve().parents[1]


def binding_for(path: Path) -> dict:
    content = path.read_bytes()
    return {
        "asset_id": "ast-master",
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(content).hexdigest(),
        "byte_count": len(content),
        "approval_id": "mfa-test",
    }


def dna_binding() -> dict:
    return {"version": 4, "stable_dna_sha256": "d" * 64}


class FrozenClock:
    def __init__(self):
        self.tick = 0

    def __call__(self) -> str:
        self.tick += 1
        return f"2026-10-07T00:00:{self.tick:02d}+00:00"


class FakeRenderer:
    def __init__(self, output_root: Path, fail_slot: str | None = None):
        self.output_root = output_root
        self.fail_slot = fail_slot
        self.requests: list[dict] = []

    def render(self, request: dict) -> dict:
        self.requests.append(request)
        if request["slot_id"] == self.fail_slot:
            raise RuntimeError("synthetic renderer failure")
        path = self.output_root / f"{request['request_id']}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        from PIL import Image
        color = (40 + len(self.requests) * 15, 90, 130) if request["stage"] == "face" else (90, 110, 50 + len(self.requests) * 10)
        Image.new("RGB", (96, 128), color).save(path)
        return {
            "output_path": str(path),
            "model_type": request["model_type"],
            "seed": 1000 + request["attempt"],
            "executor": "fake-renderer",
            "run_id": f"run-{request['request_id']}",
            "session_id": f"session-{request['request_id']}",
            "automatic_qa": {"identity_score_is_advisory": True},
        }


class FakeImporter:
    def __init__(self):
        self.imports: list[tuple[dict, dict]] = []

    def import_output(self, request: dict, result: dict) -> str:
        self.imports.append((request, result))
        return f"ast-{request['slot_id']}-{request['attempt']}"


@pytest.fixture
def master(tmp_path: Path) -> Path:
    path = tmp_path / "master.png"
    path.write_bytes(b"frozen-master-face")
    return path


def make_job(tmp_path: Path, master: Path, *, include_body: bool = False) -> packs.CharacterPackJob:
    return packs.create_job(
        tmp_path / "job",
        character_id="ch-synthetic",
        requested_by="user",
        dna=dna_binding(),
        master_face=binding_for(master),
        include_body=include_body,
        job_id="cpj-test-001",
        clock=FrozenClock(),
    )


def validate_persisted(job: packs.CharacterPackJob) -> None:
    contract_job = json.loads((ROOT / "schemas" / "character-pack-job-v1.schema.json").read_text(encoding="utf-8"))
    contract_manifest = json.loads((ROOT / "schemas" / "character-pack-candidate-manifest-v1.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(contract_job).validate(json.loads(job.job_path.read_text(encoding="utf-8")))
    Draft202012Validator(contract_manifest).validate(json.loads(job.manifest_path.read_text(encoding="utf-8")))


def test_create_job_freezes_bindings_and_uses_stage_defaults(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master, include_body=True)

    assert [slot["slot_id"] for slot in job.job["slots"]] == list(packs.FACE_SLOTS + packs.BODY_SLOTS)
    assert job.default_engine_map() == {
        **{slot_id: "qwen21" for slot_id in packs.FACE_SLOTS},
        **{slot_id: "krea2" for slot_id in packs.BODY_SLOTS},
    }
    assert job.job["master_face"] == binding_for(master)
    assert job.manifest["dna"] == dna_binding()
    validate_persisted(job)


def test_run_pending_requires_explicit_per_slot_engines_and_records_provenance(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master, include_body=True)
    renderer = FakeRenderer(tmp_path / "outputs")
    importer = FakeImporter()

    with pytest.raises(packs.CharacterPackError, match="explicit engine selection missing"):
        job.run_pending(engine_by_slot={}, renderer=renderer, importer=importer)
    candidates = job.run_pending(
        engine_by_slot=job.default_engine_map(), renderer=renderer, importer=importer
    )

    assert len(candidates) == 9
    assert len(renderer.requests) == len(importer.imports) == 9
    assert {request["engine"] for request in renderer.requests[:5]} == {"qwen21"}
    assert {request["engine"] for request in renderer.requests[5:]} == {"krea2"}
    assert all(request["settings"]["fallback"] == "none" for request in renderer.requests)
    assert all(request["master_face"]["sha256"] == binding_for(master)["sha256"] for request in renderer.requests)
    assert job.job["status"] == "needs_review"
    assert all(slot["status"] == "needs_review" and slot["attempts"] == 1 for slot in job.job["slots"])
    validate_persisted(job)


def test_resume_skips_completed_candidates_even_if_job_state_was_stale(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs")
    importer = FakeImporter()
    job.run_pending(engine_by_slot=job.default_engine_map(), renderer=renderer, importer=importer)
    assert len(renderer.requests) == 5

    stale = json.loads(job.job_path.read_text(encoding="utf-8"))
    stale["status"] = "generating"
    stale["slots"][0].update({"status": "running", "attempts": 0})
    job.job_path.write_text(json.dumps(stale), encoding="utf-8")
    resumed = packs.CharacterPackJob(job.directory, clock=FrozenClock())
    result = resumed.run_pending(engine_by_slot={}, renderer=renderer, importer=importer)

    assert result == []
    assert len(renderer.requests) == 5
    assert resumed.job["slots"][0]["status"] == "needs_review"
    assert resumed.job["slots"][0]["attempts"] == 1
    assert resumed.job["status"] == "needs_review"


def test_regeneration_appends_with_a_new_explicit_engine(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs")
    importer = FakeImporter()
    first = job.generate("face_front", engine="qwen21", renderer=renderer, importer=importer)
    second = job.regenerate("face_front", engine="krea2", renderer=renderer, importer=importer)

    candidates = job.manifest["slots"][0]["candidates"]
    assert candidates == [first, second]
    assert [candidate["engine"] for candidate in candidates] == ["qwen21", "krea2"]
    assert [candidate["candidate_id"] for candidate in candidates] == [
        "cpj-test-001.face_front.a001",
        "cpj-test-001.face_front.a002",
    ]
    assert len({candidate["output"]["sha256"] for candidate in candidates}) == 2
    assert job.job["slots"][0]["attempts"] == 2
    validate_persisted(job)


def test_failure_does_not_fallback_or_append_a_candidate(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs", fail_slot="face_front")
    importer = FakeImporter()

    with pytest.raises(packs.CharacterPackError, match="synthetic renderer failure"):
        job.generate("face_front", engine="krea2", renderer=renderer, importer=importer)

    assert [request["engine"] for request in renderer.requests] == ["krea2"]
    assert importer.imports == []
    assert job.manifest["slots"][0]["candidates"] == []
    assert job.job["slots"][0]["status"] == "failed"
    assert job.job["slots"][0]["attempts"] == 1
    assert job.job["status"] == "failed"


def test_master_binding_is_rechecked_before_every_attempt(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs")
    importer = FakeImporter()
    master.write_bytes(b"changed-after-job-creation")

    with pytest.raises(packs.CharacterPackError, match="Master Face byte count changed"):
        job.generate("face_front", engine="qwen21", renderer=renderer, importer=importer)

    assert renderer.requests == []
    assert importer.imports == []


def test_completed_slot_engine_cannot_be_silently_resubmitted_by_resume(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs")
    importer = FakeImporter()
    job.generate("face_front", engine="qwen21", renderer=renderer, importer=importer)

    pending = [slot_id for slot_id in packs.FACE_SLOTS if slot_id != "face_front"]
    with pytest.raises(packs.CharacterPackError, match="completed or unknown"):
        job.run_pending(
            engine_by_slot={**{slot_id: "qwen21" for slot_id in pending}, "face_front": "krea2"},
            renderer=renderer,
            importer=importer,
        )

    assert len(renderer.requests) == 1


def test_queued_regeneration_records_engine_and_completes_append_only(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs")
    importer = FakeImporter()
    first = job.generate("face_front", engine="qwen21", renderer=renderer, importer=importer)

    queued = job.queue_regeneration("face_front", engine="krea2", request_id="cpr-test-001")
    assert queued["engine"] == "krea2"
    assert job.job["slots"][0]["status"] == "queued"
    assert job.job["status"] == "generating"

    second = job.run_regeneration_request("cpr-test-001", renderer=renderer, importer=importer)
    request = json.loads((job.directory / "regeneration-requests" / "cpr-test-001.json").read_text(encoding="utf-8"))
    assert request["status"] == "completed"
    assert request["candidate_id"] == second["candidate_id"]
    assert [item["candidate_id"] for item in job.manifest["slots"][0]["candidates"]] == [
        first["candidate_id"], second["candidate_id"],
    ]
    assert [item["engine"] for item in job.manifest["slots"][0]["candidates"]] == ["qwen21", "krea2"]


def test_queued_regeneration_failure_is_durable_and_never_falls_back(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs", fail_slot="face_left30")
    importer = FakeImporter()
    job.queue_regeneration("face_left30", engine="krea2", request_id="cpr-fail-001")

    with pytest.raises(packs.CharacterPackError, match="synthetic renderer failure"):
        job.run_regeneration_request("cpr-fail-001", renderer=renderer, importer=importer)

    request = json.loads((job.directory / "regeneration-requests" / "cpr-fail-001.json").read_text(encoding="utf-8"))
    assert request["status"] == "failed"
    assert [item["engine"] for item in renderer.requests] == ["krea2"]
    assert job.job["slots"][1]["status"] == "failed"
    assert job.manifest["slots"][1]["candidates"] == []


def test_regeneration_request_is_single_use(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs")
    importer = FakeImporter()
    job.queue_regeneration("face_right30", engine="qwen21", request_id="cpr-once-001")
    job.run_regeneration_request("cpr-once-001", renderer=renderer, importer=importer)

    with pytest.raises(packs.CharacterPackError, match="is not queued"):
        job.run_regeneration_request("cpr-once-001", renderer=renderer, importer=importer)
    assert len(renderer.requests) == 1


def test_gallery_asset_can_be_attached_only_to_unchanged_candidate(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master)
    renderer = FakeRenderer(tmp_path / "outputs")
    candidate = job.generate(
        "face_front", engine="qwen21", renderer=renderer,
        importer=lambda _request, _result: None,
    )
    assert candidate["output"]["asset_id"] is None

    attached = job.attach_gallery_asset("face_front", candidate["candidate_id"], "ast-imported")
    assert attached["output"]["asset_id"] == "ast-imported"
    assert job.attach_gallery_asset("face_front", candidate["candidate_id"], "ast-imported")["output"]["asset_id"] == "ast-imported"
    with pytest.raises(packs.CharacterPackError, match="different Gallery asset"):
        job.attach_gallery_asset("face_front", candidate["candidate_id"], "ast-other")


def generated_face_job(tmp_path: Path, master: Path) -> packs.CharacterPackJob:
    job = make_job(tmp_path, master)
    job.run_pending(
        engine_by_slot=job.default_engine_map(),
        renderer=FakeRenderer(tmp_path / "outputs"),
        importer=FakeImporter(),
    )
    return job


def select_all(job: packs.CharacterPackJob) -> None:
    for slot in job.manifest["slots"]:
        job.select(slot["slot_id"], slot["candidates"][0]["candidate_id"])


def test_select_and_reject_are_recoverable_without_removing_candidates(tmp_path: Path, master: Path) -> None:
    job = generated_face_job(tmp_path, master)
    first_id = job.manifest["slots"][0]["candidates"][0]["candidate_id"]
    second = job.regenerate(
        "face_front",
        engine="krea2",
        renderer=FakeRenderer(tmp_path / "regenerated"),
        importer=FakeImporter(),
    )

    job.select_candidate("face_front", first_id)
    assert job.job["slots"][0]["status"] == "selected"
    assert job.job["status"] == "partially_reviewed"
    job.reject_candidate("face_front", second["candidate_id"])
    assert job.manifest["slots"][0]["selected_candidate_id"] == first_id
    assert job.job["slots"][0]["status"] == "selected"
    job.select("face_front", second["candidate_id"])
    states = [candidate["review_state"] for candidate in job.manifest["slots"][0]["candidates"]]
    assert states == ["needs_review", "selected"]
    rejected = job.reject("face_front", second["candidate_id"])

    assert rejected["review_state"] == "rejected"
    assert job.manifest["slots"][0]["selected_candidate_id"] is None
    assert [candidate["candidate_id"] for candidate in job.manifest["slots"][0]["candidates"]] == [
        first_id,
        second["candidate_id"],
    ]
    assert job.job["slots"][0]["status"] == "needs_review"


def test_identity_set_requires_one_selected_candidate_for_every_required_slot(tmp_path: Path, master: Path) -> None:
    job = generated_face_job(tmp_path, master)
    first = job.manifest["slots"][0]["candidates"][0]
    job.select("face_front", first["candidate_id"])

    with pytest.raises(packs.CharacterPackError, match="exactly one selected candidate: face_left30"):
        job.prepare_identity_set(approved_by="user", approved_at="2026-10-07T01:00:00+00:00")
    with pytest.raises(packs.CharacterPackError, match="explicit user decision"):
        job.prepare_identity_set(approved_by="codex", approved_at="2026-10-07T01:00:00+00:00")


def test_identity_set_rejects_missing_gallery_id_and_changed_output(tmp_path: Path, master: Path) -> None:
    job = generated_face_job(tmp_path, master)
    select_all(job)
    first = job.manifest["slots"][0]["candidates"][0]
    first["output"]["asset_id"] = None
    job._persist_manifest()
    with pytest.raises(packs.CharacterPackError, match="durable Gallery asset id"):
        job.prepare_identity_set(approved_by="user")

    first["output"]["asset_id"] = "ast-restored"
    job._persist_manifest()
    Path(first["output"]["path"]).write_bytes(b"mutated")
    with pytest.raises(packs.CharacterPackError, match="byte count changed|SHA-256 changed"):
        job.prepare_identity_set(approved_by="user")


def test_publish_identity_set_snapshots_provenance_and_refuses_overwrite(tmp_path: Path, master: Path) -> None:
    job = generated_face_job(tmp_path, master)
    select_all(job)
    destination = tmp_path / "identity-set-v1"
    manifest_path = job.publish_identity_set(
        destination,
        approved_by="user",
        approved_at="2026-10-07T01:00:00+00:00",
    )
    published = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_snapshot = destination / published["source"]["snapshot"]

    assert job.job["status"] == "approved"
    assert published["review_state"] == "approved"
    assert published["approved_by"] == "user"
    assert [member["slot_id"] for member in published["members"]] == list(packs.FACE_SLOTS)
    assert all(member["asset_id"].startswith("ast-") for member in published["members"])
    assert hashlib.sha256(source_snapshot.read_bytes()).hexdigest() == published["source"]["manifest_sha256"]
    for member in published["members"]:
        content = (destination / member["file"]).read_bytes()
        assert len(content) == member["byte_count"]
        assert hashlib.sha256(content).hexdigest() == member["sha256"]
    assert {sheet["file"] for sheet in published["sheets"]} == {
        "sheets/face-sheet.png", "sheets/master-sheet.png",
    }
    assert all(sheet["review_aid_only"] is True for sheet in published["sheets"])
    for sheet in published["sheets"]:
        content = (destination / sheet["file"]).read_bytes()
        assert len(content) == sheet["byte_count"]
        assert hashlib.sha256(content).hexdigest() == sheet["sha256"]
    with pytest.raises(FileExistsError, match="already exists"):
        job.publish_identity_set(destination, approved_by="user")


def test_published_body_pack_has_separate_body_and_master_review_sheets(tmp_path: Path, master: Path) -> None:
    job = make_job(tmp_path, master, include_body=True)
    job.run_pending(
        engine_by_slot=job.default_engine_map(),
        renderer=FakeRenderer(tmp_path / "outputs"),
        importer=FakeImporter(),
    )
    select_all(job)

    manifest = json.loads(job.publish_identity_set(
        tmp_path / "identity-set-with-body", approved_by="user",
    ).read_text(encoding="utf-8"))

    assert {sheet["file"] for sheet in manifest["sheets"]} == {
        "sheets/face-sheet.png", "sheets/body-sheet.png", "sheets/master-sheet.png",
    }
    body = next(sheet for sheet in manifest["sheets"] if sheet["file"] == "sheets/body-sheet.png")
    assert body["source_slots"] == list(packs.BODY_SLOTS)


def test_all_selected_slots_make_job_ready_for_pack_approval(tmp_path: Path, master: Path) -> None:
    job = generated_face_job(tmp_path, master)
    select_all(job)

    assert job.job["status"] == "ready_for_pack_approval"
    assert all(slot["status"] == "selected" for slot in job.job["slots"])
    validate_persisted(job)

