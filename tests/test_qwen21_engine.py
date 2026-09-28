"""Qwen Image 2.1 (`qwen21`) as an explicit Character Manager engine, and Krea2/Z-Image staying as they were."""

import argparse
import json
from pathlib import Path

import pytest
import character_manager as cm
import character_scene as scene
import local_wangp
import wangp_recorder
from test_shared_authority import shared, put, sample  # noqa: F401  (pytest fixture)

QWEN_MODEL = "qwen_image_21_uncensored_q4_k_m"
KREA_ONLY_FIELDS = {"model_filename", "NAG_scale", "NAG_tau", "NAG_alpha", "type"}


@pytest.fixture
def creation(shared, monkeypatch):
    runtime, private, catalog = shared
    library = private.parent / "library"; library.mkdir()
    catalog["creation_records"] = {"status": "shared-new-sessions", "version": 1, "layout": "character-generations-v1", "library_root": str(library)}
    catalog["skills"]["definitions"] = ["character-manager"]
    put(private / "control/shared-resources.json", catalog)
    put(private / "records/ch-synthetic/character.json", sample())
    skill = private / "skills/character-manager/SKILL.md"; skill.parent.mkdir(parents=True); skill.write_bytes(b"# skill\n")
    monkeypatch.setattr(scene, "ASSET_LIBRARY", library)
    face = private.parent / "face-master.png"; face.write_bytes(b"selected face master bytes")
    return library, face


def settings_of(session: Path, name: str) -> dict:
    return json.loads((session / name).read_text(encoding="utf-8"))


def batch_of(session: Path) -> dict:
    return json.loads((session / "batch.yaml").read_text(encoding="utf-8"))


def test_qwen21_is_registered_but_never_default():
    assert scene.ENGINES["qwen21"] == ("qwen21.settings.json", QWEN_MODEL)
    assert set(scene.REFERENCE_ENGINES) == {"krea2", "qwen21"}
    source = Path(scene.__file__).read_text(encoding="utf-8")
    assert source.count('add_argument("--engines", default="z-image,krea2")') == 2


def test_qwen21_template_is_minimal_and_conservative():
    template = json.loads((scene.TEMPLATES / "qwen21.settings.json").read_text(encoding="utf-8"))
    assert template["model_type"] == QWEN_MODEL
    assert template["base_model_type"] == "qwen_image_21_7B"
    assert (template["resolution"], template["num_inference_steps"], template["guidance_scale"]) == ("832x608", 40, 4.0)
    assert template["custom_settings"] == {"qwen21_kv_cache": "Disabled", "rgba": "Disabled"}
    assert template["prompt_enhancer"] == "" and template["video_prompt_type"] == ""
    assert "image_refs" not in template
    assert not KREA_ONLY_FIELDS & set(template)


def test_qwen21_text_job_prepares_exact_model_under_outputs_qwen21(creation):
    session = scene.prepare("ch-synthetic", "An adult seated by a window", cm.DEFAULT_MODEL, 3, ["qwen21"], actor="claude")
    settings = settings_of(session, "qwen21.settings.json")
    assert settings["model_type"] == QWEN_MODEL
    assert (settings["batch_size"], settings["repeat_generation"]) == (1, 3)
    assert "image_refs" not in settings and "_xai" not in settings
    job = batch_of(session)["jobs"][0]
    assert (job["engine"], job["model"], job["output_dir"], job["count"]) == ("qwen21", QWEN_MODEL, "outputs/qwen21", 3)
    assert job["reference_inputs"] == []


@pytest.mark.parametrize("actor", ["hermes", "claude"])
def test_qwen21_reference_job_is_hash_bound_and_records_the_real_actor(creation, actor):
    _, face = creation
    session = scene.prepare("ch-synthetic", "profile view, same person", cm.DEFAULT_MODEL, 1, ["qwen21"],
                            actor=actor, identity_reference=str(face), reference_asset_id="ast-face-1")
    settings = settings_of(session, "qwen21.settings.json")
    assert settings["model_type"] == QWEN_MODEL
    assert settings["image_refs"] == [str(face.resolve())]
    assert settings["video_prompt_type"] == "I"
    assert not KREA_ONLY_FIELDS & set(settings)
    assert settings["num_inference_steps"] == 40 and settings["guidance_scale"] == 4.0
    xai = settings["_xai"]
    assert xai["engine"] == "qwen21" and xai["model_type"] == QWEN_MODEL
    assert xai["reference_sha256s"] == [wangp_recorder.sha256_file(face)]
    assert xai["reference_byte_counts"] == [face.stat().st_size]
    assert xai["reference_asset_ids"] == ["ast-face-1"]
    assert xai["allow_text_fallback"] is False
    assert xai["requested_by"] == actor
    batch = batch_of(session)
    assert batch["session"]["created_by"] == actor
    assert batch["session"]["reference_inputs"][0]["asset_id"] == "ast-face-1"
    assert batch["jobs"][0]["model"] == QWEN_MODEL
    trace = json.loads((session / "prompt-trace.json").read_text(encoding="utf-8"))
    assert trace["invoked_by"] == actor
    assert scene.session_requester(session, batch) == actor
    # The prepared file passes the submit-time gate and yields the same hash-bound record.
    records = local_wangp.validate_reference_settings(settings)
    assert records[0]["sha256"] == xai["reference_sha256s"][0]
    assert records[0]["asset_id"] == "ast-face-1"


@pytest.mark.parametrize("engines", [["qwen21", "krea2"], ["z-image"], ["krea2", "qwen21"], ["z-image", "qwen21"]])
def test_reference_requires_exactly_one_reference_capable_engine(creation, engines):
    _, face = creation
    with pytest.raises(cm.CharacterError, match="no text-only fallback"):
        scene.prepare("ch-synthetic", "scene", cm.DEFAULT_MODEL, 1, engines, identity_reference=str(face))


def test_unsupported_engine_cannot_bind_a_reference():
    with pytest.raises(cm.CharacterError, match="cannot bind an identity reference"):
        scene.apply_identity_reference({"model_type": "z_image"}, {"path": "x", "sha256": "a", "byte_count": 1}, "ch", "r", "codex", "z-image")


def test_krea2_and_z_image_preparation_is_unchanged(creation):
    _, face = creation
    session = scene.prepare("ch-synthetic", "scene", cm.DEFAULT_MODEL, 4, ["z-image", "krea2"])
    for name in ("z-image.settings.json", "krea2.settings.json"):
        template = json.loads((scene.TEMPLATES / name).read_text(encoding="utf-8"))
        prepared = settings_of(session, name)
        assert set(prepared) == set(template)
        assert (prepared["batch_size"], prepared["repeat_generation"]) == (4, 1)
        assert {k: v for k, v in prepared.items() if k not in {"batch_size", "repeat_generation", "seed"}} == \
               {k: v for k, v in template.items() if k not in {"batch_size", "repeat_generation", "seed"}}
    bound = scene.prepare("ch-synthetic", "bound scene", cm.DEFAULT_MODEL, 2, ["krea2"], identity_reference=str(face))
    krea = settings_of(bound, "krea2.settings.json")
    assert krea["model_type"] == krea["base_model_type"] == "krea2_turbo_edit"
    assert krea["video_prompt_type"] == "KI" and krea["num_inference_steps"] == 8 and krea["guidance_scale"] == 0
    assert krea["model_filename"] == str(scene.KREA2_IDENTITY_EDIT_CHECKPOINT)
    # Krea2 provenance keeps its historical keys exactly; engine/model fields are Qwen-only additions.
    assert set(krea["_xai"]) == {"kind", "schema_version", "character_id", "reference_role", "reference_asset_ids",
                                 "reference_sha256s", "reference_byte_counts", "operator_request", "requested_by",
                                 "allow_text_fallback"}
    assert batch_of(bound)["jobs"][0]["model"] == "krea2_turbo_edit"


def qwen_settings(image: Path, **overrides) -> dict:
    settings = {
        "model_type": QWEN_MODEL, "base_model_type": "qwen_image_21_7B", "video_prompt_type": "I",
        "image_refs": [str(image)],
        "_xai": {"kind": "reference_transformation", "reference_role": "identity", "engine": "qwen21",
                 "reference_sha256s": [wangp_recorder.sha256_file(image)], "reference_byte_counts": [image.stat().st_size]},
    }
    settings.update(overrides)
    return settings


def test_local_validator_accepts_registered_qwen_and_refuses_everything_else(tmp_path):
    image = tmp_path / "face.png"; image.write_bytes(b"face")
    assert local_wangp.validate_reference_settings(qwen_settings(image))[0]["role"] == "identity"
    assert local_wangp.validate_reference_settings(qwen_settings(image, base_model_type=QWEN_MODEL))
    with pytest.raises(ValueError, match="ignores image_refs"):
        local_wangp.validate_reference_settings(qwen_settings(image, video_prompt_type=""))
    with pytest.raises(ValueError, match="between 1 and 1"):
        local_wangp.validate_reference_settings(qwen_settings(image, image_refs=[str(image), str(image)]))
    with pytest.raises(ValueError, match="fallback is disabled"):
        local_wangp.validate_reference_settings(qwen_settings(image, base_model_type="qwen_image_20B"))
    with pytest.raises(ValueError, match="fallback is disabled"):
        # An unregistered model is refused even though it carries image_refs.
        local_wangp.validate_reference_settings(qwen_settings(image, model_type="qwen_image_21_7B", base_model_type=""))
    with pytest.raises(ValueError, match="prepared for qwen21 cannot run"):
        local_wangp.validate_reference_settings(qwen_settings(image, model_type="krea2_turbo_edit", base_model_type="krea2_turbo_edit"))
    prepared = qwen_settings(image)
    image.write_bytes(b"face, edited later")
    with pytest.raises(ValueError, match="changed after preparation"):
        local_wangp.validate_reference_settings(prepared)


def test_changed_or_missing_reference_fails_before_the_worker_starts(tmp_path, monkeypatch):
    image = tmp_path / "face.png"; image.write_bytes(b"face")
    settings = qwen_settings(image)
    image.write_bytes(b"face swapped after preparation")
    settings_path = tmp_path / "qwen21.settings.json"; settings_path.write_text(json.dumps(settings), encoding="utf-8")
    prompt = tmp_path / "prompt.txt"; prompt.write_text("same person", encoding="utf-8")

    def no_worker(*args, **kwargs):
        raise AssertionError("the GPU worker must not start")

    monkeypatch.setattr(local_wangp.subprocess, "Popen", no_worker)
    args = argparse.Namespace(
        wangp_root=str(tmp_path), wangp_python=str(Path(local_wangp.sys.executable)), prompt_file=str(prompt),
        settings_file=str(settings_path), runs_root=str(tmp_path / "session" / "runs"), requested_by="claude",
        executor=None, project_id="p", prompt_id="p-qwen21", run_id="run-qwen", output_dir=str(tmp_path / "out"),
        profile=4, vram_safety=0.8,
    )
    with pytest.raises(ValueError, match="changed"):
        local_wangp.submit(args)
    image.unlink()
    args.run_id = "run-qwen-2"
    with pytest.raises(ValueError, match="not found"):
        local_wangp.submit(args)
