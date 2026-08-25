from __future__ import annotations

import json
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


if __name__ == "__main__":
    unittest.main()
