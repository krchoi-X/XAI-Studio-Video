import argparse
import hashlib
import json
import sqlite3
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import drive_media_export as exporter


SCHEMA = """
CREATE TABLE characters(id TEXT PRIMARY KEY,name TEXT,romanized_name TEXT);
CREATE TABLE asset_roots(id TEXT PRIMARY KEY,absolute_path TEXT);
CREATE TABLE generation_sessions(id TEXT PRIMARY KEY,title TEXT,character_id TEXT,engine TEXT,created_at TEXT,settings_json TEXT NOT NULL DEFAULT '{}');
CREATE TABLE assets(id TEXT PRIMARY KEY,root_id TEXT,relative_path TEXT,content_hash TEXT,media_type TEXT,byte_size INTEGER,created_at TEXT);
CREATE TABLE session_assets(session_id TEXT,asset_id TEXT,position INTEGER);
"""


class DriveMediaExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.media = self.root / "media"; self.media.mkdir()
        data = self.root / "data"; data.mkdir()
        self.db = data / "studio.db"
        self.destination = self.root / "drive"
        self.state = self.root / "state"
        connection = sqlite3.connect(self.db)
        try:
            connection.executescript(SCHEMA)
            connection.execute("INSERT INTO characters VALUES (?,?,?)", ("ch-test", "테스트", "Test Person"))
            connection.execute("INSERT INTO characters VALUES (?,?,?)", ("ch-second", "두번째", "Second Person"))
            connection.execute("INSERT INTO asset_roots VALUES (?,?)", ("root-1", str(self.media)))
            connection.commit()
        finally:
            connection.close()

    def tearDown(self):
        self.temp.cleanup()

    def add_asset(self, asset_id="ast_image001", *, relative="krea2/result.jpg", media_type="image/jpeg",
                  content=b"image", character_id="ch-test", character_ids=None,
                  session_id="ses-scene-20260916-204838-test"):
        source = self.media / relative; source.parent.mkdir(parents=True, exist_ok=True); source.write_bytes(content)
        digest = hashlib.sha256(content).hexdigest()
        connection = sqlite3.connect(self.db)
        try:
            settings = {"session": {"character_ids": character_ids}} if character_ids is not None else {}
            connection.execute("INSERT OR IGNORE INTO generation_sessions VALUES (?,?,?,?,?,?)",
                               (session_id, "Evening dress in a bright studio", character_id, "krea2",
                                "2026-09-16T11:48:38+00:00", json.dumps(settings)))
            connection.execute("INSERT INTO assets VALUES (?,?,?,?,?,?,?)",
                               (asset_id, "root-1", relative, digest, media_type, len(content), "2026-09-16T11:49:00+00:00"))
            connection.execute("INSERT INTO session_assets VALUES (?,?,?)", (session_id, asset_id, 0))
            connection.commit()
        finally:
            connection.close()
        return source, digest

    def args(self, command="plan", **overrides):
        values = dict(command=command, database=str(self.db), destination_root=str(self.destination),
                      state_dir=str(self.state), asset_id=None, character_id=None, session_id=None,
                      since=None, limit=100, all=False)
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_plan_builds_character_kind_and_month_tree(self):
        self.add_asset()
        result = exporter.execute(self.args())
        item = result["items"][0]
        self.assertEqual("copy", item["action"])
        self.assertIn(str(Path("Characters") / "Test Person [ch-test]" / "Images" / "2026-09"), item["destination"])
        self.assertTrue(item["destination"].endswith("__krea2__stimage001.jpg"))

    def test_sync_is_incremental_and_hash_verified(self):
        _, digest = self.add_asset()
        first = exporter.execute(self.args("sync", asset_id=["ast_image001"]))
        self.assertEqual({"copied": 1}, first["results"])
        second = exporter.execute(self.args("sync", asset_id=["ast_image001"]))
        self.assertEqual({"skip": 1}, second["results"])
        state = json.loads((self.state / exporter.STATE_FILE).read_text(encoding="utf-8"))
        destination = Path(state["assets"]["ast_image001"]["destination"])
        self.assertEqual(digest, exporter.sha256_file(destination))
        self.assertTrue((self.state / exporter.EVENT_FILE).is_file())

    def test_existing_matching_file_is_adopted_without_overwrite(self):
        source, digest = self.add_asset()
        asset = exporter.load_assets(self.db)[0]
        destination = exporter.destination_for(asset, self.destination)
        destination.parent.mkdir(parents=True); destination.write_bytes(source.read_bytes())
        result = exporter.execute(self.args("sync", asset_id=[asset.asset_id]))
        self.assertEqual({"adopted": 1}, result["results"])
        self.assertEqual(digest, exporter.sha256_file(destination))

    def test_existing_different_file_is_a_conflict(self):
        self.add_asset()
        asset = exporter.load_assets(self.db)[0]
        destination = exporter.destination_for(asset, self.destination)
        destination.parent.mkdir(parents=True); destination.write_bytes(b"different")
        result = exporter.execute(self.args("sync", asset_id=[asset.asset_id]))
        self.assertFalse(result["ok"])
        self.assertEqual({"conflict": 1}, result["results"])
        self.assertEqual(b"different", destination.read_bytes())

    def test_unassigned_video_uses_video_bucket(self):
        self.add_asset(asset_id="ast_video001", relative="h3/clip.mp4", media_type="video/mp4",
                       content=b"video", character_id=None, session_id="ses-video-20260916-101010")
        item = exporter.execute(self.args(asset_id=["ast_video001"]))["items"][0]
        self.assertIn(str(Path("Unassigned") / "Videos" / "2026-09"), item["destination"])

    def test_missing_original_is_reported_not_copied(self):
        source, _ = self.add_asset()
        source.unlink()
        result = exporter.execute(self.args("sync", asset_id=["ast_image001"]))
        self.assertFalse(result["ok"])
        self.assertEqual({"missing": 1}, result["results"])

    def test_sync_requires_scope_or_explicit_all(self):
        self.add_asset()
        with self.assertRaisesRegex(exporter.ExportError, "requires a selector"):
            exporter.execute(self.args("sync"))

    def test_requested_asset_id_must_exist(self):
        self.add_asset()
        with self.assertRaisesRegex(exporter.ExportError, "asset id not found"):
            exporter.execute(self.args(asset_id=["ast_missing"]))

    def test_all_batch_limit_does_not_get_stuck_on_exported_asset(self):
        self.add_asset(asset_id="ast_image001", relative="one.jpg", content=b"one",
                       session_id="ses-scene-20260916-101010-one")
        self.add_asset(asset_id="ast_image002", relative="two.jpg", content=b"two",
                       session_id="ses-scene-20260916-101011-two")
        exporter.execute(self.args("sync", asset_id=["ast_image001"], limit=1))
        batch = exporter.execute(self.args("sync", all=True, limit=1))
        self.assertEqual({"copied": 1}, batch["results"])
        complete = exporter.execute(self.args("sync", all=True, limit=1))
        self.assertEqual({}, complete["results"])
        self.assertEqual({"total": 0}, complete["summary"])

    def test_atomic_state_replace_retries_transient_windows_lock(self):
        target = self.state / "retry.json"
        real_replace = exporter.os.replace
        attempts = 0

        def flaky_replace(source, destination):
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise PermissionError("temporarily locked")
            return real_replace(source, destination)

        with mock.patch.object(exporter.os, "replace", side_effect=flaky_replace), \
             mock.patch.object(exporter.time, "sleep"):
            exporter.atomic_json(target, {"ok": True})
        self.assertEqual(3, attempts)
        self.assertEqual({"ok": True}, json.loads(target.read_text(encoding="utf-8")))

    def test_explicit_multi_character_cast_uses_stable_separate_bucket(self):
        self.add_asset(character_ids=["ch-second", "ch-test"])
        item = exporter.execute(self.args())["items"][0]
        destination = item["destination"]
        self.assertIn(str(Path("Multi-Character")), destination)
        self.assertIn("Second Person [ch-second]", destination)
        self.assertIn("Test Person [ch-test]", destination)

    def test_new_catalog_character_needs_no_exporter_configuration(self):
        connection = sqlite3.connect(self.db)
        try:
            connection.execute("INSERT INTO characters VALUES (?,?,?)", ("ch-future", "미래", "Future Person"))
            connection.commit()
        finally:
            connection.close()
        self.add_asset(character_id="ch-future")
        destination = exporter.execute(self.args())["items"][0]["destination"]
        self.assertIn(str(Path("Characters") / "Future Person [ch-future]"), destination)


if __name__ == "__main__":
    unittest.main()
