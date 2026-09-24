from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import provision


def sample_config() -> dict:
    return {
        "environment_version": "test-v1",
        "image": "ghcr.io/example/worker:test",
        "workspace_mount": "/workspace",
        "container_disk_gb": 150,
        "max_hourly_price": 1.25,
        "ports": {"web": 7860, "mcp": 8000, "health": 8080, "ssh": 22},
        "worker_env": {"WANGP_PROFILE": "4"},
        "runpod": {
            "name": "worker",
            "gpu_type_ids": ["NVIDIA GeForce RTX 5090"],
            "gpu_count": 1,
            "volume_gb": 200,
        },
        "vast": {
            "label": "worker",
            "gpu_names": ["RTX 5090"],
            "gpu_count": 1,
            "min_gpu_ram_mb": 30000,
        },
    }


class ProvisionTests(unittest.TestCase):
    def test_runpod_payload_has_persistent_mount_and_ports(self) -> None:
        payload = provision.runpod_payload(sample_config())
        self.assertEqual(payload["volumeMountPath"], "/workspace")
        self.assertIn("8000/http", payload["ports"])
        self.assertEqual(payload["env"]["XAI_ENVIRONMENT_VERSION"], "test-v1")

    def test_vast_search_keeps_safety_filters(self) -> None:
        payload = provision.vast_search_payload(sample_config())
        self.assertEqual(payload["verified"], {"eq": True})
        self.assertEqual(payload["rentable"], {"eq": True})
        self.assertEqual(payload["gpu_ram"], {"gte": 30000})

    def test_placeholder_image_is_rejected(self) -> None:
        config = sample_config()
        config["image"] = "ghcr.io/YOUR_ACCOUNT/worker:test"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaises(provision.ConfigError):
                provision.load_config(str(path))

    def test_vast_worker_uses_same_image_and_mount(self) -> None:
        config = sample_config()
        config["vast"]["volume_id"] = 123
        payload = provision.vast_create_payload(config)
        self.assertEqual(payload["image"], config["image"])
        self.assertEqual(payload["volume_info"]["mount_path"], "/workspace")
        self.assertIn("-p 8080:8080", payload["env"])


class ActiveAuditTests(unittest.TestCase):
    def audit(self, responses: dict, days: int = 0) -> dict:
        calls: list[str] = []

        def fake_request(method, url, api_key, payload=None):
            calls.append(url)
            for fragment, value in responses.items():
                if fragment in url:
                    if isinstance(value, Exception):
                        raise value
                    return value
            raise RuntimeError("provider returned HTTP 404: not found")

        original = provision.request_json
        provision.request_json = fake_request
        os.environ["RUNPOD_API_KEY"] = "test-runpod"
        os.environ["VAST_API_KEY"] = "test-vast"
        try:
            report = provision.active_report(["runpod", "vast"], days)
        finally:
            provision.request_json = original
        report["_calls"] = calls
        return report

    def test_storage_only_account_is_flagged(self) -> None:
        report = self.audit(
            {
                "/pods": {"pods": []},
                "/network-volumes": {
                    "networkVolumes": [
                        {"id": "vol1", "name": "wangp", "size": 200, "dataCenterId": "EU-RO-1"}
                    ]
                },
                "/instances/": {"instances": []},
                "/volumes/": {"volumes": []},
            }
        )
        self.assertEqual(report["totals"]["persistent_storage_gb"], 200)
        self.assertEqual(report["totals"]["hourly_burn"], 0)
        self.assertEqual(report["totals"]["running_compute"], 0)
        self.assertTrue(any("billing with no compute" in w for w in report["warnings"]))

    def test_only_running_compute_counts_toward_burn(self) -> None:
        report = self.audit(
            {
                "/pods": {
                    "pods": [
                        {"id": "a", "desiredStatus": "RUNNING", "costPerHr": 0.89},
                        {"id": "b", "desiredStatus": "EXITED", "costPerHr": 0.89},
                    ]
                },
                "/network-volumes": {"networkVolumes": []},
                "/instances/": {"instances": []},
                "/volumes/": {"volumes": []},
            }
        )
        self.assertEqual(report["totals"]["running_compute"], 1)
        self.assertEqual(report["totals"]["stopped_compute"], 1)
        self.assertEqual(report["totals"]["hourly_burn"], 0.89)
        self.assertTrue(any("non-running compute" in w for w in report["warnings"]))

    def test_v2_cost_field_counts_toward_burn(self) -> None:
        report = self.audit(
            {
                "/pods": {"pods": [{"id": "a", "status": "RUNNING", "cost": 0.44}]},
                "/network-volumes": {"networkVolumes": []},
                "/instances/": {"instances": []},
                "/volumes/": {"volumes": []},
            }
        )
        self.assertEqual(report["totals"]["hourly_burn"], 0.44)

    def test_one_failing_endpoint_does_not_hide_the_others(self) -> None:
        report = self.audit(
            {
                "/pods": RuntimeError("provider returned HTTP 500: upstream"),
                "/network-volumes": {
                    "networkVolumes": [{"id": "vol1", "size": 50, "dataCenterId": "EU-RO-1"}]
                },
                "/instances/": {
                    "instances": [
                        {"id": 7, "actual_status": "running", "dph_total": 0.4, "gpu_name": "RTX 5090"}
                    ]
                },
                "/volumes/": {"volumes": []},
            }
        )
        self.assertEqual(report["totals"]["persistent_storage_gb"], 50)
        self.assertEqual(report["totals"]["hourly_burn"], 0.4)
        self.assertTrue(any("runpod pods" in note for note in report["notes"]))

    def test_audit_uses_v2_and_skips_billing_when_days_is_zero(self) -> None:
        report = self.audit(
            {
                "/pods": {"pods": []},
                "/network-volumes": {"networkVolumes": []},
                "/instances/": {"instances": []},
                "/volumes/": {"volumes": []},
            }
        )
        self.assertTrue(all("rest.runpod.io" not in url for url in report["_calls"]))
        self.assertTrue(any("api.runpod.io/v2/pods" in url for url in report["_calls"]))
        self.assertFalse(any("billing" in url for url in report["_calls"]))

    def test_failed_probe_makes_the_report_incomplete(self) -> None:
        report = self.audit(
            {
                "/pods": RuntimeError("provider returned HTTP 403: error code: 1010"),
                "/network-volumes": RuntimeError("provider returned HTTP 403: error code: 1010"),
                "/instances/": {"instances": []},
                "/volumes/": {"volumes": []},
            }
        )
        self.assertFalse(report["complete"])
        self.assertTrue(report["warnings"][0].startswith("INCOMPLETE:"))

    def test_successful_audit_is_marked_complete(self) -> None:
        report = self.audit(
            {
                "/pods": {"pods": []},
                "/network-volumes": {"networkVolumes": []},
                "/instances/": {"instances": []},
                "/volumes/": {"volumes": []},
            }
        )
        self.assertTrue(report["complete"])
        self.assertEqual(report["warnings"], [])

    def test_billing_window_is_requested_when_days_given(self) -> None:
        report = self.audit(
            {
                "/pods": {"pods": []},
                "/network-volumes": {"networkVolumes": []},
                "/billing/network-volumes": {"records": []},
                "/instances/": {"instances": []},
                "/volumes/": {"volumes": []},
            },
            days=30,
        )
        billing_calls = [url for url in report["_calls"] if "billing" in url]
        self.assertEqual(len(billing_calls), 1)
        self.assertIn("bucketSize=day", billing_calls[0])
        self.assertIn("startTime=", billing_calls[0])


class RequestHeaderTests(unittest.TestCase):
    def test_explicit_user_agent_avoids_cloudflare_signature_block(self) -> None:
        captured = {}

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b"{}"

        def fake_urlopen(request, timeout=None):
            captured["headers"] = dict(request.header_items())
            return FakeResponse()

        original = provision.urllib.request.urlopen
        provision.urllib.request.urlopen = fake_urlopen
        try:
            provision.request_json("GET", "https://example.invalid/x", "key")
        finally:
            provision.urllib.request.urlopen = original

        headers = {k.lower(): v for k, v in captured["headers"].items()}
        self.assertEqual(headers["User-agent".lower()], provision.USER_AGENT)
        self.assertNotIn("python-urllib", headers["User-agent".lower()].lower())
        self.assertEqual(headers["Authorization".lower()], "Bearer key")


class LifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.original_file = provision.ACTIVE_FILE
        provision.ACTIVE_FILE = Path(self.tmp.name) / "active-resources.json"
        self.addCleanup(lambda: setattr(provision, "ACTIVE_FILE", self.original_file))
        os.environ["RUNPOD_API_KEY"] = "test-key"

    def patch_request(self, handler) -> None:
        original = provision.request_json
        provision.request_json = handler
        self.addCleanup(lambda: setattr(provision, "request_json", original))

    def test_terminate_is_unverified_while_the_pod_still_reports_running(self) -> None:
        calls = []

        def handler(method, url, api_key, payload=None):
            calls.append((method, url))
            if method == "DELETE":
                return {}
            return {"pod": {"id": "p1", "desiredStatus": "RUNNING", "costPerHr": 0.9}}

        self.patch_request(handler)
        provision.time.sleep = lambda _s: None
        outcome = provision.runpod_terminate("p1", "k")
        self.assertFalse(outcome["verified"])
        self.assertFalse(outcome["terminated"])
        self.assertEqual(calls[0], ("DELETE", f"{provision.RUNPOD_API_V2}/pods/p1"))

    def test_terminate_is_verified_when_the_pod_is_gone(self) -> None:
        def handler(method, url, api_key, payload=None):
            if method == "DELETE":
                return {}
            raise provision.ProviderHTTPError(404, "not found")

        self.patch_request(handler)
        provision.time.sleep = lambda _s: None
        provision.record_active("p1", {"environment_version": "v1"})
        outcome = provision.runpod_terminate("p1", "k")
        self.assertTrue(outcome["verified"])
        self.assertEqual(provision.read_active(), [])

    def test_terminate_is_not_verified_on_provider_failure(self) -> None:
        def handler(method, url, api_key, payload=None):
            if method == "DELETE":
                return {}
            raise provision.ProviderHTTPError(500, "upstream unavailable")

        self.patch_request(handler)
        provision.time.sleep = lambda _s: None
        provision.record_active("p1", {"environment_version": "v1"})
        outcome = provision.runpod_terminate("p1", "k")
        self.assertFalse(outcome["verified"])
        self.assertEqual(provision.read_active()[0]["pod_id"], "p1")

    def test_terminate_is_not_verified_by_an_empty_status_response(self) -> None:
        def handler(method, url, api_key, payload=None):
            return {}

        self.patch_request(handler)
        provision.time.sleep = lambda _s: None
        outcome = provision.runpod_terminate("p1", "k")
        self.assertFalse(outcome["verified"])

    def test_successful_create_records_the_billable_pod(self) -> None:
        config_path = Path(self.tmp.name) / "config.json"
        config_path.write_text(json.dumps(sample_config()), encoding="utf-8")
        self.patch_request(lambda *args, **kwargs: {"id": "new-pod"})
        with redirect_stdout(StringIO()):
            result = provision.main(
                ["runpod-create", "--config", str(config_path), "--execute"]
            )
        self.assertEqual(result, 0)
        self.assertEqual(provision.read_active()[0]["pod_id"], "new-pod")

    def test_wait_ready_distinguishes_never_running_from_never_healthy(self) -> None:
        config = sample_config()
        provision.time.sleep = lambda _s: None
        self.patch_request(lambda *a, **k: {"pod": {"id": "p1", "desiredStatus": "PENDING"}})
        provision.health_ready = lambda _url: False
        outcome = provision.wait_ready("p1", config, "k", timeout=0)
        self.assertFalse(outcome["ready"])
        self.assertIn("never reached RUNNING", outcome["reason"])

        self.patch_request(lambda *a, **k: {"pod": {"id": "p1", "desiredStatus": "RUNNING"}})
        outcome = provision.wait_ready("p1", config, "k", timeout=0)
        self.assertIn("health never reported ready", outcome["reason"])

    def test_wait_ready_succeeds_once_the_worker_answers(self) -> None:
        provision.time.sleep = lambda _s: None
        self.patch_request(lambda *a, **k: {"pod": {"id": "p1", "desiredStatus": "RUNNING"}})
        provision.health_ready = lambda _url: True
        outcome = provision.wait_ready("p1", sample_config(), "k", timeout=0)
        self.assertTrue(outcome["ready"])
        self.assertIn("proxy.runpod.net", outcome["endpoints"]["health"])

    def test_orphan_check_flags_a_pod_nobody_recorded(self) -> None:
        def handler(method, url, api_key, payload=None):
            if "/pods" in url:
                return {"pods": [{"id": "ghost", "desiredStatus": "RUNNING", "costPerHr": 1.2}]}
            return {"networkVolumes": []}

        self.patch_request(handler)
        report = provision.orphan_check("k")
        self.assertEqual(len(report["billing_but_never_recorded"]), 1)
        self.assertEqual(report["still_billing_from_our_records"], [])

    def test_orphan_check_reports_a_recorded_pod_that_is_gone(self) -> None:
        provision.record_active("old", {"environment_version": "v1"})

        def handler(method, url, api_key, payload=None):
            return {"pods": []} if "/pods" in url else {"networkVolumes": []}

        self.patch_request(handler)
        report = provision.orphan_check("k")
        self.assertEqual(len(report["recorded_but_already_gone"]), 1)
        self.assertTrue(report["complete"])


if __name__ == "__main__":
    unittest.main()
