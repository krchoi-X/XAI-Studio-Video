from __future__ import annotations

import json
import os
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
