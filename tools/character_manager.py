#!/usr/bin/env python3
"""Repository control plane for Hermes/local-LLM character management."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / "characters"
def _confined_resource(root: Path, value: str) -> Path:
    candidate = (root / value).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise CharacterError("shared resource escapes its authority")
    return candidate


def shared_resource_catalog() -> tuple[Path, dict] | None:
    """Resolve the existing workspace contract without caching mutable pointers."""
    locator = Path(os.environ.get("XAI_WORKSPACE_FILE", "D:/AI_Studio/workspace.yaml"))
    if not locator.is_file():
        if "XAI_WORKSPACE_FILE" in os.environ:
            raise CharacterError("explicit workspace locator is missing")
        return None
    import yaml
    try:
        workspace = yaml.safe_load(locator.read_text(encoding="utf-8")) or {}
        private = (locator.parent / workspace["private_repo"]).resolve()
        catalog_path = private / "control" / "shared-resources.json"
        if not catalog_path.is_file():
            policy_path = private / "control" / "characters.yaml"
            policy = yaml.safe_load(policy_path.read_text(encoding="utf-8")) if policy_path.is_file() else {}
            if policy.get("mode") == "shared":
                raise CharacterError("active shared resource catalog is missing")
            return None
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        if catalog.get("version") != 1:
            raise CharacterError("unsupported shared resource catalog version")
        if catalog.get("status") in {"pending-root-activation", "inactive"}:
            return None
        if catalog.get("status") != "active":
            raise CharacterError("invalid shared resource activation status")
        return private, catalog
    except (OSError, KeyError, TypeError, ValueError, AttributeError, yaml.YAMLError) as exc:
        raise CharacterError(f"invalid shared character authority: {exc}") from exc


def shared_authority_root() -> Path | None:
    resource = shared_resource_catalog()
    if resource is None:
        return None
    private, catalog = resource
    try:
        root = _confined_resource(private, catalog["characters"]["authority_root"])
    except (KeyError, TypeError) as exc:
        raise CharacterError("invalid shared character authority root") from exc
    if not root.is_dir():
        raise CharacterError("active shared character authority is missing")
    return root


def shared_skill_path(name: str) -> Path:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise CharacterError("invalid skill name")
    resource = shared_resource_catalog()
    if resource is None:
        path = ROOT / "skills" / name / "SKILL.md"
        if path.is_file() and "shared-resource-adapter: 1" in path.read_text(encoding="utf-8"):
            raise CharacterError("shared skill adapter requires an active authority")
    else:
        private, catalog = resource
        try:
            if name not in catalog["skills"]["definitions"]:
                raise CharacterError("skill is absent from shared catalog")
            base = _confined_resource(private, catalog["skills"]["source_root"])
            path = _confined_resource(base, name + "/SKILL.md")
        except (KeyError, TypeError) as exc:
            raise CharacterError("invalid shared skill catalog") from exc
    if not path.is_file():
        raise CharacterError("skill source is missing")
    return path


def character_record_path(character_id: str) -> Path:
    if not ID_RE.fullmatch(character_id):
        raise CharacterError("invalid character identifier")
    authority = shared_authority_root()
    root = authority if authority is not None else CHARACTERS
    path = _confined_resource(root, character_id + "/character.json")
    if authority is not None and not path.is_file():
        raise CharacterError(f"active shared character record is missing: {character_id}")
    return path


def character_session_root(character_id: str) -> Path:
    if not ID_RE.fullmatch(character_id):
        raise CharacterError("invalid character identifier")
    return _confined_resource(CHARACTERS, character_id)


def shared_creation_library() -> Path | None:
    resource = shared_resource_catalog()
    if resource is None:
        return None
    _, catalog = resource
    config = catalog.get("creation_records", {})
    if not isinstance(config, dict):
        raise CharacterError("invalid shared creation-record configuration")
    if config.get("status") in {None, "project-owned-pending-transition"}:
        return None
    if config.get("status") != "shared-new-sessions" or config.get("version") != 1 or config.get("layout") != "character-generations-v1":
        raise CharacterError("invalid shared creation-record configuration")
    value = config.get("library_root")
    if not isinstance(value, str) or not Path(value).is_absolute():
        raise CharacterError("shared creation Library must be an absolute root")
    root = Path(value).resolve()
    if not root.is_dir() or root.is_relative_to(ROOT.resolve()):
        raise CharacterError("shared creation Library is missing or inside the runtime project")
    return root


def generation_session_path(character_id: str, session_id: str, library_root: Path | None = None, runtime_characters: Path | None = None) -> Path:
    if not ID_RE.fullmatch(character_id) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", session_id):
        raise CharacterError("invalid character or session identifier")
    library = shared_creation_library()
    if library is not None:
        if library_root is not None and library_root.resolve() != library:
            raise CharacterError("explicit Library conflicts with shared creation authority")
        return _confined_resource(library, f"characters/{character_id}/generations/{session_id}")
    return _confined_resource(runtime_characters if runtime_characters is not None else CHARACTERS, f"{character_id}/02_generations/{session_id}")


def reserve_generation_session(character_id: str, session_id: str, library_root: Path | None = None, runtime_characters: Path | None = None) -> Path:
    path = generation_session_path(character_id, session_id, library_root, runtime_characters)
    if shared_creation_library() is not None:
        legacy = (runtime_characters if runtime_characters is not None else CHARACTERS) / character_id / "02_generations" / session_id
        if legacy.exists():
            raise CharacterError("session identifier already exists in legacy records")
        try:
            path.mkdir(parents=True, exist_ok=False)
        except FileExistsError as exc:
            raise CharacterError("shared session already exists; resume its recorded path") from exc
    return path


def validate_generation_session(path: Path) -> Path:
    import yaml
    root = path.resolve()
    legacy = root.is_relative_to(CHARACTERS.resolve()) and root.parent.name == "02_generations" and root.parent.parent.parent == CHARACTERS.resolve()
    library = shared_creation_library()
    shared = library is not None and root.is_relative_to(library) and root.parent.name == "generations" and root.parent.parent.parent == library / "characters"
    if not (legacy or shared):
        raise CharacterError("session-dir is outside configured character session roots")
    if shared:
        for relative in ("batch.yaml", "prompt.txt", "outputs"):
            _confined_resource(root, relative)
    if not (root / "batch.yaml").is_file() or not (root / "prompt.txt").is_file():
        raise CharacterError("session-dir is missing batch.yaml or prompt.txt")
    batch = yaml.safe_load((root / "batch.yaml").read_text(encoding="utf-8")) or {}
    session = batch.get("session") or {}
    identifier = session.get("character_id") or batch.get("character_id")
    if shared and identifier != root.parent.parent.name:
        raise CharacterError("session character does not match its directory")
    if shared and session.get("id") != root.name:
        raise CharacterError("session identifier does not match its directory")
    if shared and Path(str(session.get("asset_root") or root / "outputs")).resolve() != root / "outputs":
        raise CharacterError("shared session output root conflicts with its directory")
    return root


DRAFTS = CHARACTERS / ".drafts"
INDEX = CHARACTERS / "index.json"
DEFAULT_MODEL = "meromero26b-a4b-hermes:latest"
OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"

# Hermes already routes local models: its gateway fronts the llama.cpp server on an
# ephemeral port and keeps Ollama registered as one more provider behind the same address.
# Every tool here has been going straight to Ollama instead, which is why a second model
# ends up resident beside the one Hermes is already serving on an 8 GB card. These are read
# from the environment so no key is ever committed; with neither set, nothing changes and
# the call goes to Ollama exactly as before.
HERMES_BASE_URL_ENV = "XAI_HERMES_BASE_URL"
HERMES_API_KEY_ENV = "XAI_HERMES_API_KEY"
HERMES_MODEL_ENV = "XAI_HERMES_MODEL"


_DISCOVERED_KEY: dict[str, str] = {}


HERMES_SERVER_DESCRIPTOR = Path.home() / "AppData/Local/hermes/runtimes/llamacpp/server.json"


def _key_from_descriptor(base_url: str) -> str | None:
    """Hermes records the router it started, address and key together, when it starts it."""
    try:
        record = json.loads(HERMES_SERVER_DESCRIPTOR.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if str(record.get("base_url", "")).rstrip("/") != base_url.rstrip("/"):
        return None
    return str(record.get("api_key") or "") or None


def discover_gateway_key(base_url: str) -> str | None:
    """Find the gateway's key without anyone having to copy it.

    Hermes issues its llama.cpp router a new `--api-key` on every launch, so a key pinned
    in a file goes stale the next time it restarts. It does write the pair down, in
    `runtimes/llamacpp/server.json`, which is read first because it is cheap and exact.
    Failing that the key is read off the running process's own command line, which still
    works if that file is missing, stale or belongs to a server that has since died.
    Best effort throughout: on any failure the caller simply has no gateway.
    """
    from_file = _key_from_descriptor(base_url)
    if from_file:
        return from_file
    port = base_url.rsplit(":", 1)[-1].split("/")[0]
    if not port.isdigit():
        return None
    query = (
        "Get-CimInstance Win32_Process -Filter \"Name='llama-server.exe'\" | "
        "Select-Object -ExpandProperty CommandLine"
    )
    try:
        completed = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", query],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=20, check=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError):
        return None
    for line in (completed.stdout or "").splitlines():
        if f"--port {port}" not in line or "--api-key" not in line:
            continue
        parts = line.split()
        index = parts.index("--api-key")
        if index + 1 < len(parts):
            return parts[index + 1]
    return None


def hermes_chat_config(*, rediscover: bool = False) -> tuple[str, str, str | None] | None:
    """The Hermes gateway to use, or None to stay on Ollama.

    An address is required; the key is optional here because it can be discovered. What is
    never done is guessing the address: without one there is no gateway, and a call that
    quietly went somewhere else would make the answering model depend on which variable
    somebody remembered to set.
    """
    base_url = (os.environ.get(HERMES_BASE_URL_ENV) or "").strip().rstrip("/")
    if not base_url:
        return None
    api_key = (os.environ.get(HERMES_API_KEY_ENV) or "").strip()
    if rediscover or not api_key:
        found = _DISCOVERED_KEY.get(base_url) if not rediscover else None
        if found is None:
            found = discover_gateway_key(base_url)
            if found:
                _DISCOVERED_KEY[base_url] = found
        api_key = found or api_key
    if not api_key:
        return None
    return base_url, api_key, (os.environ.get(HERMES_MODEL_ENV) or "").strip() or None


def active_chat_route() -> str:
    """Which router a `chat_json` call would reach right now. For traces and diagnostics."""
    return "hermes" if hermes_chat_config() else "ollama"


def _gateway_chat(config: tuple[str, str, str | None], prompt: str, model: str,
                  temperature: float, timeout: float) -> Any:
    base_url, api_key, override = config
    payload = json.dumps({
        "model": override or model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "stream": False,
    }).encode("utf-8")
    request = urllib.request.Request(
        base_url + "/chat/completions", data=payload,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    return json.loads(result["choices"][0]["message"]["content"])


def chat_json(prompt: str, model: str, *, temperature: float = 0.25, timeout: float = 600.0) -> Any:
    """One local-model call that must answer with JSON, through whichever router is configured.

    Both routers are asked for JSON explicitly rather than by instruction: Ollama through
    `format`, an OpenAI-compatible gateway through `response_format`. The caller gets the
    parsed document and never sees which one answered.
    """
    hermes = hermes_chat_config()
    if hermes is not None:
        try:
            return _gateway_chat(hermes, prompt, model, temperature, timeout)
        except urllib.error.HTTPError as error:
            if error.code != 401:
                raise
            # The router was restarted and issued itself a new key. Find it and try once more.
            refreshed = hermes_chat_config(rediscover=True)
            if refreshed is None or refreshed[1] == hermes[1]:
                raise
            return _gateway_chat(refreshed, prompt, model, temperature, timeout)
    payload = json.dumps({
        "model": model, "stream": False, "format": "json",
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": temperature},
    }).encode("utf-8")
    request = urllib.request.Request(OLLAMA_CHAT, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    return json.loads(result["message"]["content"])

ID_RE = re.compile(r"^ch-[a-z0-9]+(?:-[a-z0-9]+)*$")

FACE_FIELDS = ("shape", "eyes", "eyebrows", "nose", "lips", "jaw")
BODY_FIELDS = (
    "height_impression", "limb_proportions", "shoulders", "torso", "bust",
    "waist", "pelvis_hips", "lower_body", "body_hair",
)


class CharacterError(ValueError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_hash(record: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(record["stable_dna"]).encode("utf-8")).hexdigest()


def validate(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "id", "name", "status", "version", "stable_dna", "scene_defaults", "provenance"):
        if key not in record:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors
    if record["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not ID_RE.fullmatch(str(record["id"])):
        errors.append("id must match ch-lowercase-slug")
    if record["status"] not in {"draft", "candidate", "approved", "deprecated"}:
        errors.append("invalid status")
    if not isinstance(record["version"], int) or record["version"] < 1:
        errors.append("version must be a positive integer")
    dna = record.get("stable_dna", {})
    for key in ("adult_age_range", "visual_background", "face", "body", "hair", "skin", "distinctive_marks"):
        if key not in dna:
            errors.append(f"stable_dna missing: {key}")
    for key in FACE_FIELDS:
        if not str(dna.get("face", {}).get(key, "")).strip():
            errors.append(f"stable_dna.face missing: {key}")
    for key in BODY_FIELDS:
        if not str(dna.get("body", {}).get(key, "")).strip():
            errors.append(f"stable_dna.body missing: {key}")
    return errors


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        handle.write(text)
        temp = Path(handle.name)
    os.replace(temp, path)


def render_core(record: dict[str, Any]) -> str:
    dna = record["stable_dna"]
    face = dna["face"]
    body = dna["body"]
    anchors = "\n".join(f"- {x}" for x in dna.get("recognition_anchors", [])) or "- 미정"
    marks = "\n".join(f"- {x}" for x in dna.get("distinctive_marks", [])) or "- 없음/미정"
    return f"""# {record['name']} — Character Core

- ID: `{record['id']}`
- version: `{record['version']}`
- status: `{record['status']}`
- Stable DNA SHA-256: `{stable_hash(record)}`

## Stable identity

- adult age range: {dna['adult_age_range']}
- visual background: {dna['visual_background']}
- face shape: {face['shape']}
- eyes: {face['eyes']}
- eyebrows: {face['eyebrows']}
- nose: {face['nose']}
- lips: {face['lips']}
- jaw: {face['jaw']}
- hair: {dna['hair']}
- skin: {dna['skin']}
- height impression: {body['height_impression']}
- limb proportions: {body['limb_proportions']}
- shoulders: {body['shoulders']}
- torso: {body['torso']}
- bust: {body['bust']}
- waist: {body['waist']}
- pelvis / hips: {body['pelvis_hips']}
- lower body: {body['lower_body']}
- body hair: {body['body_hair']}

## Recognition anchors

{anchors}

## Distinctive marks

{marks}

## Scene defaults (mutable)

{chr(10).join(f'- {k}: {v}' for k, v in record.get('scene_defaults', {}).items())}

Scene-specific pose, expression, outfit, camera, lens, lighting, location, and action belong in a Scene Delta. They must not be added to Stable DNA.
"""


def render_base_prompt(record: dict[str, Any], exclude_fields: set[str] | None = None) -> str:
    """Render Stable DNA while omitting fields explicitly replaced by a Scene Spec."""
    exclude_fields = exclude_fields or set()
    dna = record["stable_dna"]
    f = dna["face"]
    b = dna["body"]
    hair = "" if "hair" in exclude_fields else f"Hair: {dna['hair']}. "
    return (
        f"An adult {dna['visual_background']} character named {record.get('romanized_name') or record['name']}. "
        # Every face attribute the record carries, in the order it is stored. Naming six of them here meant a
        # new one could be promoted into the DNA, validate, and then never reach a single prompt - which is
        # what happened to ch-lia's nose_profile and chin_profile on 2026-09-11.
        f"Face: {'; '.join(str(value) for key, value in f.items() if key not in exclude_fields)}. "
        f"{hair}Skin: {dna['skin']}. "
        # distinctive_marks is the field that exists to pin identity, and it reached no prompt at all: five
        # characters carried one and none of them appeared in a single generated line.
        + (f"Distinctive: {'; '.join(dna['distinctive_marks'])}. "
           if dna.get("distinctive_marks") and "distinctive_marks" not in exclude_fields else "") +
        f"Body: {b['height_impression']}; {b['limb_proportions']}; shoulders {b['shoulders']}; "
        f"torso {b['torso']}; bust {b['bust']}; waist {b['waist']}; pelvis and hips {b['pelvis_hips']}; "
        f"lower body {b['lower_body']}; body hair {b['body_hair']}. "
        "Preserve one coherent adult identity and anatomically consistent body. Keep pose, expression, outfit, camera, lens, lighting, location, and action as scene variables."
    )


def rebuild_index() -> list[dict[str, Any]]:
    items = []
    authority = shared_authority_root()
    root = authority if authority is not None else CHARACTERS
    if root.exists():
        for path in sorted(root.glob("ch-*/character.json")):
            record = load(path)
            items.append({
                "id": record["id"], "name": record["name"], "romanized_name": record.get("romanized_name", ""),
                "status": record["status"], "version": record["version"],
                "stable_dna_sha256": stable_hash(record),
                "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "path": path.relative_to(root if authority else ROOT).as_posix(),
                "reference_defaults": record.get("reference_defaults", {}),
                "approved_references": record.get("approved_references", []),
            })
    index_path = root / "index.json" if authority is not None else INDEX
    atomic_write(index_path, json.dumps({"schema_version": 1, "updated_at": now(), "characters": items}, ensure_ascii=False, indent=2) + "\n")
    return items


def preserve_prior(target: Path) -> None:
    """Retain exact record and derived text before shared authoring replaces them."""
    if not target.is_file():
        return
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    history = target.parent / "history" / digest
    for relative in ("character.json", "00_character-core/character_core.md", "01_prompts/base_appearance.txt"):
        source = target.parent / relative
        if not source.is_file():
            continue
        saved = history / relative
        data = source.read_bytes()
        if saved.exists():
            if saved.read_bytes() != data:
                # A refresh can change derived text while preserving record bytes.
                saved = history / "derived-variants" / hashlib.sha256(data).hexdigest() / relative
        saved.parent.mkdir(parents=True, exist_ok=True)
        try:
            with saved.open("xb") as handle:
                handle.write(data)
        except FileExistsError:
            if saved.read_bytes() != data:
                raise CharacterError("prior history conflicts with saved bytes")


def ollama_draft(request: str, model: str) -> dict[str, Any]:
    prompt = f"""Create one character record from the user's Korean or English request.
Return JSON only. Do not invent biography. All people must be adults.
Stable DNA contains identity only; scene_defaults may contain mutable default expression/makeup/gaze.
Required structure:
{{"schema_version":1,"id":"ch-slug","name":"...","romanized_name":"...","status":"draft","version":1,
"stable_dna":{{"adult_age_range":"...","visual_background":"...","face":{{"shape":"...","eyes":"...","eyebrows":"...","nose":"...","lips":"...","jaw":"..."}},"body":{{"height_impression":"...","limb_proportions":"...","shoulders":"...","torso":"...","bust":"...","waist":"...","pelvis_hips":"...","lower_body":"...","body_hair":"..."}},"hair":"...","skin":"...","distinctive_marks":[],"recognition_anchors":[]}},
"scene_defaults":{{"expression":"...","makeup":"...","gaze":"..."}},"approved_references":[],"prompt_sources":[],"lora_associations":[],"video_test_associations":[],"provenance":{{"created_at":"","updated_at":"","created_by":"hermes-local-llm","sources":[]}}}}
User request: {request}"""
    record = chat_json(prompt, model, temperature=0.2, timeout=600)
    stamp = now()
    record.setdefault("provenance", {})
    record["provenance"].update({"created_at": stamp, "updated_at": stamp, "created_by": "hermes-local-llm"})
    if not record["provenance"].get("sources"):
        record["provenance"]["sources"] = ["natural-language-request"]
    record["status"] = "draft"
    record["schema_version"] = 1
    record["version"] = 1
    record["provenance"]["stable_dna_sha256"] = stable_hash(record)
    return record


def save_draft(record: dict[str, Any], request: str = "") -> Path:
    errors = validate(record)
    if errors:
        raise CharacterError("invalid draft:\n- " + "\n- ".join(errors))
    target = DRAFTS / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{record['id']}" / "character.json"
    atomic_write(target, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    atomic_write(target.with_name("request-summary.md"), render_core(record))
    if request:
        atomic_write(target.with_name("request.txt"), request.rstrip() + "\n")
    return target


def promote(path: Path, allow_stable_change: bool, reason: str) -> Path:
    path = path.resolve()
    if not path.is_relative_to(DRAFTS.resolve()):
        raise CharacterError(f"promotion source must be under {DRAFTS}")
    record = load(path)
    errors = validate(record)
    if errors:
        raise CharacterError("validation failed:\n- " + "\n- ".join(errors))
    authority = shared_authority_root()
    target_dir = _confined_resource(authority if authority is not None else CHARACTERS, record["id"])
    target = target_dir / "character.json"
    if target.exists():
        current = load(target)
        if stable_hash(current) != stable_hash(record) and not (allow_stable_change and reason.strip()):
            raise CharacterError("Stable DNA drift blocked. Re-run with --allow-stable-change and --reason.")
        record["version"] = current["version"] + 1
        record["provenance"]["created_at"] = current["provenance"]["created_at"]
        if authority is not None:
            preserve_prior(target)
    record["status"] = "candidate" if record["status"] == "draft" else record["status"]
    record["provenance"]["updated_at"] = now()
    record["provenance"]["stable_dna_sha256"] = stable_hash(record)
    if reason:
        record["provenance"]["change_reason"] = reason
    atomic_write(target, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    atomic_write(target_dir / "00_character-core" / "character_core.md", render_core(record))
    atomic_write(target_dir / "01_prompts" / "base_appearance.txt", render_base_prompt(record) + "\n")
    rebuild_index()
    return target


def cmd_validate(character: str | None) -> int:
    root = shared_authority_root() or CHARACTERS
    paths = [character_record_path(character)] if character else sorted(root.glob("ch-*/character.json"))
    failures = 0
    for path in paths:
        if not path.exists():
            print(f"MISSING {path}")
            failures += 1
            continue
        record = load(path)
        errors = validate(record)
        stored = record.get("provenance", {}).get("stable_dna_sha256")
        if stored and stored != stable_hash(record):
            errors.append("stored stable_dna_sha256 does not match content")
        if errors:
            failures += 1
            print(f"FAIL {record.get('id', path.parent.name)}: {'; '.join(errors)}")
        else:
            print(f"OK   {record['id']} v{record['version']} {stable_hash(record)[:12]}")
    return 1 if failures else 0


def refresh(character: str) -> Path:
    target = character_record_path(character)
    if not target.is_file():
        raise CharacterError(f"unknown character: {character}")
    record = load(target)
    errors = validate(record)
    if errors:
        raise CharacterError("validation failed:\n- " + "\n- ".join(errors))
    if shared_authority_root() is not None:
        preserve_prior(target)
    record["provenance"]["stable_dna_sha256"] = stable_hash(record)
    atomic_write(target, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    atomic_write(target.parent / "00_character-core" / "character_core.md", render_core(record))
    atomic_write(target.parent / "01_prompts" / "base_appearance.txt", render_base_prompt(record) + "\n")
    rebuild_index()
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("list")
    check = sub.add_parser("validate")
    check.add_argument("--character")
    draft = sub.add_parser("draft")
    draft.add_argument("--request", required=True)
    draft.add_argument("--model", default=DEFAULT_MODEL)
    promote_parser = sub.add_parser("promote")
    promote_parser.add_argument("draft", type=Path)
    promote_parser.add_argument("--allow-stable-change", action="store_true")
    promote_parser.add_argument("--reason", default="")
    refresh_parser = sub.add_parser("refresh")
    refresh_parser.add_argument("--character", required=True)
    args = parser.parse_args()

    try:
        if args.command == "doctor":
            print(f"root={ROOT}")
            print(f"characters={CHARACTERS}")
            print(f"ollama={OLLAMA_CHAT}")
            return cmd_validate(None)
        if args.command == "list":
            for item in rebuild_index():
                print(f"{item['id']}\t{item['status']}\tv{item['version']}\t{item['name']}")
            return 0
        if args.command == "validate":
            return cmd_validate(args.character)
        if args.command == "draft":
            path = save_draft(ollama_draft(args.request, args.model), args.request)
            print(path)
            return 0
        if args.command == "promote":
            print(promote(args.draft.resolve(), args.allow_stable_change, args.reason))
            return 0
        if args.command == "refresh":
            print(refresh(args.character))
            return 0
    except (CharacterError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
