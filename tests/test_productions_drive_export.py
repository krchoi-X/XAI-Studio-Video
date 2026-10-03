import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import productions_drive_export as pde  # noqa: E402
from test_control_tower_productions import FAKE_MP4, make_library, write  # noqa: E402

FULL = "VIDEO-20261002-112000-full"


def age(root: Path, seconds: int = 3600) -> None:
    old = os.path.getmtime(root) - seconds
    for path in root.rglob("*"):
        if path.is_file():
            os.utime(path, (old, old))


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "videos"
        self.dest = base / "drive" / "Productions"
        self.state = base / "state"
        make_library(self.root)
        age(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *argv):
        args = pde.build_parser().parse_args(["--root", str(self.root), "--destination-root", str(self.dest),
                                              "--state-dir", str(self.state), *argv])
        return pde.run(args)

    def folder(self) -> Path:
        found = [p for p in self.dest.iterdir() if FULL in p.name]
        self.assertEqual(len(found), 1)
        return found[0]

    def test_plan_lists_only_the_backup_set_with_a_readable_layout(self):
        plan = self.cli("plan", "--all")
        planned = [i for i in plan["items"] if FULL in i["key"]]
        self.assertEqual({i["action"] for i in planned}, {"copy"})
        self.assertEqual(len(planned), 8)
        relative = sorted(Path(i["destination"]).relative_to(self.dest).parts[1:] for i in planned)
        self.assertIn(("Videos", "rooftop-final.mp4"), [tuple(r) for r in relative])
        self.assertIn(("Videos", "exp", "shot02", "B.mp4"), [tuple(r) for r in relative])
        self.assertIn(("Images", "minseo.png"), [tuple(r) for r in relative])
        self.assertIn(("Record", "session-provenance.json"), [tuple(r) for r in relative])
        joined = json.dumps(plan, ensure_ascii=False)
        for excluded in ("norm-01", "raw", "candidates", "scratch", "concat.txt", "run.json", "stray.mp4", "no-provenance"):
            self.assertNotIn(excluded, joined)
        self.assertFalse(self.dest.exists(), "plan must not write anything")

    def test_sync_copies_verifies_and_is_idempotent(self):
        first = self.cli("sync", "--session-id", FULL)
        self.assertTrue(first["ok"])
        self.assertEqual(first["results"], {"copied": 8})
        copied = self.folder() / "Videos" / "rooftop-final.mp4"
        self.assertEqual(copied.read_bytes(), FAKE_MP4)
        second = self.cli("sync", "--session-id", FULL)
        self.assertEqual(second["results"], {})
        again = self.cli("plan", "--session-id", FULL)["summary"]
        self.assertEqual((again.get("skip"), again.get("copy")), (8, None))
        status = pde.status(pde.build_parser().parse_args(["--state-dir", str(self.state), "status"]))
        self.assertEqual((status["recorded_files"], status["destinations_missing"]), (8, 0))

    def test_files_still_being_written_wait(self):
        write(self.root / FULL / "outputs" / "fresh.mp4", FAKE_MP4)  # just written: not aged
        plan = self.cli("plan", "--session-id", FULL)
        fresh = [i for i in plan["items"] if i["key"].endswith("fresh.mp4")]
        self.assertEqual([i["action"] for i in fresh], ["wait"])
        self.cli("sync", "--session-id", FULL)
        self.assertFalse(any(p.name == "fresh.mp4" for p in self.dest.rglob("*")))

    def test_a_changed_video_is_a_conflict_and_never_overwrites(self):
        self.cli("sync", "--session-id", FULL)
        source = self.root / FULL / "outputs" / "rooftop-final.mp4"
        source.write_bytes(FAKE_MP4 + b"changed")
        age(self.root)
        result = self.cli("sync", "--session-id", FULL)
        self.assertFalse(result["ok"])
        self.assertEqual(result["results"], {"conflict": 1})
        self.assertEqual((self.folder() / "Videos" / "rooftop-final.mp4").read_bytes(), FAKE_MP4)

    def test_a_changed_record_becomes_a_new_revision(self):
        self.cli("sync", "--session-id", FULL)
        prov = self.root / FULL / "session-provenance.json"
        original = prov.read_text(encoding="utf-8")
        prov.write_text(original.replace("needs_review", "completed"), encoding="utf-8")
        age(self.root)
        result = self.cli("sync", "--session-id", FULL)
        self.assertEqual(result["results"], {"copied": 1})
        folder = self.folder()
        self.assertEqual((folder / "Record" / "session-provenance.json").read_text(encoding="utf-8"), original)
        revisions = list((folder / "Record" / "_revisions").glob("session-provenance.*.json"))
        self.assertEqual(len(revisions), 1)
        self.assertIn("completed", revisions[0].read_text(encoding="utf-8"))
        self.assertEqual(self.cli("sync", "--session-id", FULL)["results"], {})

    def test_title_change_keeps_the_original_session_folder(self):
        self.cli("sync", "--session-id", FULL)
        original_folder = self.folder()
        prov = self.root / FULL / "session-provenance.json"
        data = json.loads(prov.read_text(encoding="utf-8"))
        data["title"] = "Renamed production"
        data["status"] = "completed"
        prov.write_text(json.dumps(data), encoding="utf-8")
        age(self.root)

        result = self.cli("sync", "--session-id", FULL)
        self.assertEqual(result["results"], {"copied": 1})
        self.assertEqual(self.folder(), original_folder)
        self.assertFalse(any("Renamed production" in p.name for p in self.dest.iterdir()))
        ledger = pde.read_ledger(self.state)
        self.assertEqual(Path(ledger["sessions"][FULL]["destination_folder"]), original_folder)

    def test_v1_ledger_infers_and_freezes_the_existing_folder(self):
        self.cli("sync", "--session-id", FULL)
        original_folder = self.folder()
        ledger_path = self.state / pde.LEDGER
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger.pop("sessions")
        ledger["schema_version"] = 1
        ledger_path.write_text(json.dumps(ledger), encoding="utf-8")

        prov = self.root / FULL / "session-provenance.json"
        data = json.loads(prov.read_text(encoding="utf-8"))
        data["title"] = "Renamed legacy production"
        prov.write_text(json.dumps(data), encoding="utf-8")
        age(self.root)

        result = self.cli("sync", "--session-id", FULL)
        self.assertEqual(result["results"], {"copied": 1})
        self.assertEqual(self.folder(), original_folder)
        migrated = pde.read_ledger(self.state)
        self.assertEqual(migrated["schema_version"], 2)
        self.assertEqual(Path(migrated["sessions"][FULL]["destination_folder"]), original_folder)

    def test_nothing_on_drive_is_ever_deleted(self):
        self.cli("sync", "--session-id", FULL)
        (self.root / FULL / "outputs" / "shot-01.mp4").unlink()
        self.cli("sync", "--session-id", FULL)
        self.assertTrue((self.folder() / "Videos" / "shot-01.mp4").is_file())

    def test_matching_destination_is_adopted(self):
        plan = self.cli("plan", "--session-id", FULL)
        target = Path(next(i for i in plan["items"] if i["key"].endswith("shot-01.mp4"))["destination"])
        target.parent.mkdir(parents=True)
        target.write_bytes(FAKE_MP4)
        result = self.cli("sync", "--session-id", FULL)
        self.assertEqual(result["results"], {"copied": 7, "adopted": 1})

    def test_a_deleted_copy_is_restored_when_the_source_is_unchanged(self):
        self.cli("sync", "--session-id", FULL)
        (self.folder() / "Videos" / "shot-01.mp4").unlink()
        result = self.cli("sync", "--session-id", FULL)
        self.assertEqual(result["results"], {"copied": 1})

    def test_a_file_that_changes_while_copying_is_not_promoted(self):
        real = shutil.copy2

        def corrupting(src, dst, *a, **k):
            real(src, dst, *a, **k)
            with open(dst, "ab") as handle:
                handle.write(b"torn")
            return dst

        with mock.patch.object(pde.shutil, "copy2", corrupting):
            result = self.cli("sync", "--session-id", FULL)
        self.assertFalse(result["ok"])
        self.assertEqual(result["results"], {"unstable": 8})
        self.assertFalse(self.dest.exists() and any(p.is_file() for p in self.dest.rglob("*")))
        self.assertEqual(pde.read_ledger(self.state)["files"], {})

    def test_guards(self):
        with self.assertRaises(pde.ExportError):
            self.cli("sync")
        inside = pde.build_parser().parse_args(["--root", str(self.root), "--destination-root", str(self.root / "out"),
                                                "--state-dir", str(self.state), "plan", "--all"])
        with self.assertRaises(pde.ExportError):
            pde.run(inside)

    def test_long_filenames_are_shortened_with_a_hash_tag(self):
        name = "x" * 200 + ".mp4"
        write(self.root / FULL / "outputs" / name, FAKE_MP4 + b"long")
        age(self.root)
        plan = self.cli("plan", "--session-id", FULL)
        item = next(i for i in plan["items"] if i["key"].startswith(FULL) and i["key"].endswith(".mp4") and "xxxx" in i["key"])
        destination = Path(item["destination"])
        self.assertLessEqual(len(destination.name.encode("utf-8")), pde.FILENAME_BYTES)
        self.assertTrue(destination.name.endswith(".mp4"))
        self.assertIn(item["content_hash"][:8], destination.name)


if __name__ == "__main__":
    unittest.main()
