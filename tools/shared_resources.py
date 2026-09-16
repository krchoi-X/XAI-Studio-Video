"""Read shared-resource paths and current hashes without generation or writes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import character_manager as cm


def describe() -> dict:
    resource = cm.shared_resource_catalog()
    if resource is None:
        return {"active": False, "character_root": str(cm.CHARACTERS)}
    private, catalog = resource
    root = cm.shared_authority_root()
    records = []
    for file in sorted(root.glob("ch-*/character.json")):
        file = cm.character_record_path(file.parent.name)
        record = cm.load(file)
        records.append({"id": record["id"], "version": record["version"], "path": str(file),
                        "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
    skills = {}
    for name in catalog["skills"]["definitions"]:
        file = cm.shared_skill_path(name)
        skills[name] = {"path": str(file), "sha256": hashlib.sha256(file.read_bytes()).hexdigest()}
    import yaml
    locator = Path(os.environ.get("XAI_WORKSPACE_FILE", "D:/AI_Studio/workspace.yaml")).resolve()
    workspace = yaml.safe_load(locator.read_text(encoding="utf-8"))
    repositories = yaml.safe_load((private / "control/repositories.yaml").read_text(encoding="utf-8"))
    repository = catalog["knowledge"]["repository"]
    workspace_root = (locator.parent / workspace["workspace_root"]).resolve()
    knowledge = workspace_root / repositories["repositories"][repository]["path"]
    if not knowledge.is_dir():
        raise cm.CharacterError("configured knowledge repository is missing")
    return {"active": True, "characters": records, "skills": skills, "knowledge": str(knowledge.resolve()),
            "creation_records": catalog["creation_records"], "runtime_sessions": str(cm.CHARACTERS)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", help="return one current shared skill source path")
    parser.add_argument("--sets", metavar="CHARACTER_ID", help="list complete shared identity and LoRA sets")
    parser.add_argument("--record-archives", metavar="CHARACTER_ID", help="list historical record archives")
    parser.add_argument("--record-bundles", action="store_true", help="list historical standalone/report bundles")
    args = parser.parse_args()
    if args.skill:
        print(cm.shared_skill_path(args.skill))
    elif args.sets:
        from character_sets import describe_sets
        print(json.dumps(describe_sets(args.sets), ensure_ascii=False, indent=2))
    elif args.record_archives:
        from record_archives import describe_archives
        print(json.dumps(describe_archives(args.record_archives), ensure_ascii=False, indent=2))
    elif args.record_bundles:
        from artifact_bundles import describe_bundles
        print(json.dumps(describe_bundles(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(describe(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
