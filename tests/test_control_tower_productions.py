import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient  # noqa: E402

from control_tower import productions  # noqa: E402
from control_tower.app import create_app  # noqa: E402
from control_tower.config import Config  # noqa: E402
from control_tower.db import Database  # noqa: E402
from control_tower.monitor import MonitorService  # noqa: E402
from test_control_tower_api import FakeAdapter, FakeGpu, FakeProcesses, wangp_worker_row  # noqa: E402

FAKE_MP4 = b"\x00\x00\x00\x18ftypmp42" + b"0123456789abcdef" * 8


def write(path: Path, data=b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


def make_library(root: Path) -> None:
    full = root / "VIDEO-20261002-112000-full"
    write(full / "session-provenance.json", json.dumps({
        "session_id": full.name, "title": "Full production", "requested_by": "claude", "status": "needs_review",
        "created_at": "2026-10-02T11:18:04+09:00", "source_idea": "docs/x.md"}))
    write(full / "outputs" / "rooftop-final.mp4", FAKE_MP4)
    write(full / "outputs" / "shot-01.mp4", FAKE_MP4)
    write(full / "outputs" / "norm-01.mp4", FAKE_MP4)          # intermediate: never listed or backed up
    write(full / "outputs" / "concat.txt", "list")             # not a media or record file
    write(full / "outputs" / "raw" / "run-1.mp4", FAKE_MP4)    # duplicate of a clip
    write(full / "outputs" / "exp" / "shot02" / "B.mp4", FAKE_MP4)
    write(full / "refs" / "minseo.png", b"\x89PNGfake")
    write(full / "refs" / "candidates" / "c0.jpg", b"jpg")     # candidate stills are not backed up
    write(full / "shot-01.txt", "prompt")
    write(full / "shot-01.settings.json", "{}")
    write(full / "experiments" / "shot02" / "B.txt", "prompt B")
    write(full / "runs" / "run-1" / "run.json", "{}")          # machine logs are excluded
    write(full / "scratch" / "contact.png", b"png")
    minimal = root / "VIDEO-20260901-000000-minimal"
    write(minimal / "session-provenance.json", json.dumps({"session_id": minimal.name}))
    broken = root / "VIDEO-20260801-000000-broken"
    write(broken / "session-provenance.json", "{not json")
    write(root / "no-provenance" / "outputs" / "a.mp4", FAKE_MP4)
    write(root / "stray.mp4", FAKE_MP4)


class ProductionsModelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "videos"
        make_library(self.root)
        self.full = "VIDEO-20261002-112000-full"

    def tearDown(self):
        self.tmp.cleanup()

    def test_discovery_requires_provenance_and_orders_newest_first(self):
        rows = productions.list_productions(self.root)
        self.assertEqual([r["id"] for r in rows],
                         [self.full, "VIDEO-20260901-000000-minimal", "VIDEO-20260801-000000-broken"])
        by_id = {r["id"]: r for r in rows}
        self.assertEqual(by_id[self.full]["title"], "Full production")
        self.assertEqual(by_id[self.full]["final_video"], "outputs/rooftop-final.mp4")
        self.assertEqual(by_id[self.full]["clip_count"], 1)
        self.assertEqual(by_id[self.full]["experiment_count"], 1)
        self.assertIsNone(by_id["VIDEO-20260901-000000-minimal"]["final_video"])
        self.assertEqual(by_id["VIDEO-20260901-000000-minimal"]["status"], "unknown")
        self.assertEqual(by_id["VIDEO-20260801-000000-broken"]["status"], "unreadable")
        self.assertIn("unreadable", by_id["VIDEO-20260801-000000-broken"]["problem"])

    def test_missing_root_lists_nothing(self):
        self.assertEqual(productions.list_productions(self.root / "nope"), [])

    def test_classification_leaves_out_intermediates_raw_candidates_and_logs(self):
        files = productions.classify(self.root / self.full)
        names = {k: sorted(x["path"] for x in v) for k, v in files.items()}
        self.assertEqual(names["final"], ["outputs/rooftop-final.mp4"])
        self.assertEqual(names["clips"], ["outputs/shot-01.mp4"])
        self.assertEqual(names["experiments"], ["outputs/exp/shot02/B.mp4"])
        self.assertEqual(names["images"], ["refs/minseo.png"])
        self.assertEqual(names["records"], ["experiments/shot02/B.txt", "session-provenance.json", "shot-01.settings.json", "shot-01.txt"])

    def test_backup_manifest_categories(self):
        manifest = productions.backup_manifest(self.root / self.full)
        self.assertEqual(sorted(manifest), sorted([
            ("Videos", "outputs/rooftop-final.mp4"), ("Videos", "outputs/shot-01.mp4"), ("Videos", "outputs/exp/shot02/B.mp4"),
            ("Images", "refs/minseo.png"),
            ("Record", "experiments/shot02/B.txt"), ("Record", "session-provenance.json"),
            ("Record", "shot-01.settings.json"), ("Record", "shot-01.txt")]))

    def test_resolve_media_accepts_only_files_inside_a_production(self):
        ok = productions.resolve_media(self.root, self.full, "outputs/shot-01.mp4")
        self.assertEqual(ok, (self.root / self.full / "outputs" / "shot-01.mp4").resolve())
        self.assertIsNotNone(productions.resolve_media(self.root, self.full, "outputs\\shot-01.mp4"))
        bad = [
            "../VIDEO-20260901-000000-minimal/session-provenance.json", "..", "outputs/../../stray.mp4",
            "/etc/passwd", "C:/Windows/win.ini", "", "outputs/raw/run-1.mp4", "runs/run-1/run.json",
            "outputs/concat.txt.exe", "outputs/missing.mp4", "outputs", "outputs/\x00.mp4",
        ]
        for rel in bad:
            self.assertIsNone(productions.resolve_media(self.root, self.full, rel), rel)
        for sid in ("..", "", "no-provenance", "a/b", "a\\b", "VIDEO-20260901-000000-minimal/../" + self.full):
            self.assertIsNone(productions.resolve_media(self.root, sid, "session-provenance.json"), sid)

    def test_resolve_media_rejects_a_symlink_that_leaves_the_session(self):
        outside = Path(self.tmp.name) / "secret.mp4"
        outside.write_bytes(FAKE_MP4)
        link = self.root / self.full / "outputs" / "link.mp4"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks not permitted on this host")
        self.assertIsNone(productions.resolve_media(self.root, self.full, "outputs/link.mp4"))
        classified = productions.classify(self.root / self.full)
        self.assertNotIn("outputs/link.mp4", [item["path"] for item in classified["clips"]])
        self.assertNotIn(("Videos", "outputs/link.mp4"), productions.backup_manifest(self.root / self.full))


class ProductionsConfigTests(unittest.TestCase):
    def test_default_root_is_the_library_videos_folder(self):
        # A "" typo once turned this into a vertical tab; only a live check noticed.
        self.assertEqual(str(Config().productions_root), "D:\\AI_Studio\\library\\videos")
        self.assertEqual(Config().productions_root.parts[-2:], ("library", "videos"))
        self.assertEqual(Config().productions_backup_status.name, "last-run.json")

    def test_backup_status_reader_is_bounded_and_reports_invalid_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "last-run.json"
            self.assertIsNone(productions.read_backup_status(path))
            path.write_text(json.dumps({"ok": True, "checked_at": "now", "secret": "not exposed"}), encoding="utf-8")
            self.assertEqual(productions.read_backup_status(path), {"ok": True, "checked_at": "now"})
            path.write_text("[]", encoding="utf-8")
            self.assertFalse(productions.read_backup_status(path)["ok"])


class ProductionsApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "videos"
        make_library(self.root)
        self.backup_status = base / "last-run.json"
        self.backup_status.write_text(json.dumps({"ok": True, "checked_at": "2026-10-03T10:00:00+09:00"}), encoding="utf-8")
        cfg = Config(db_path=base / "ct.sqlite3", scan_roots=[base / "none"], night_batch_root=base / "none",
                     web_job_roots=[], productions_root=self.root, productions_backup_status=self.backup_status)
        service = MonitorService(cfg, db=Database(cfg.db_path), gpu_collector=FakeGpu(),
                                 process_observer=FakeProcesses([wangp_worker_row(28141)]), adapters=[FakeAdapter([])])
        self.client = TestClient(create_app(cfg, monitor=service))
        self.full = "VIDEO-20261002-112000-full"

    def tearDown(self):
        self.tmp.cleanup()

    def test_page_list_detail_and_file(self):
        with self.client as client:
            page = client.get("/productions")
            self.assertEqual(page.status_code, 200)
            self.assertIn("작품", page.text)
            listing = client.get("/api/productions").json()
            self.assertEqual(listing["productions"][0]["id"], self.full)
            self.assertTrue(listing["backup"]["ok"])
            detail = client.get(f"/api/productions/{self.full}").json()
            self.assertEqual(detail["files"]["final"][0]["path"], "outputs/rooftop-final.mp4")
            self.assertEqual(detail["provenance"]["requested_by"], "claude")
            media = client.get(f"/api/productions/{self.full}/file", params={"path": "outputs/rooftop-final.mp4"})
            self.assertEqual(media.status_code, 200)
            self.assertEqual(media.headers["content-type"], "video/mp4")
            self.assertEqual(media.content, FAKE_MP4)
            ranged = client.get(f"/api/productions/{self.full}/file", params={"path": "outputs/rooftop-final.mp4"},
                                headers={"Range": "bytes=0-3"})
            self.assertEqual(ranged.status_code, 206, "tablets need byte ranges to seek")
            text = client.get(f"/api/productions/{self.full}/file", params={"path": "shot-01.txt"})
            self.assertTrue(text.headers["content-type"].startswith("text/plain"))

    def test_unknown_and_escaping_requests_are_404(self):
        with self.client as client:
            self.assertEqual(client.get("/api/productions/nope").status_code, 404)
            for path in ("../VIDEO-20260901-000000-minimal/session-provenance.json", "outputs/raw/run-1.mp4", "runs/run-1/run.json"):
                response = client.get(f"/api/productions/{self.full}/file", params={"path": path})
                self.assertEqual(response.status_code, 404, path)
            self.assertEqual(client.get("/api/productions/no-provenance").status_code, 404)

    def test_existing_endpoints_are_unaffected(self):
        with self.client as client:
            self.assertTrue(client.get("/api/health").json()["ok"])
            self.assertEqual(client.get("/").status_code, 200)


if __name__ == "__main__":
    unittest.main()
