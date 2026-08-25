from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


RUNPOD_API = "https://rest.runpod.io/v1"
VAST_API = "https://console.vast.ai/api/v0"


class ConfigError(ValueError):
    pass


def load_config(path: str) -> dict[str, Any]:
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    required = ["environment_version", "image", "workspace_mount", "ports", "runpod", "vast"]
    missing = [key for key in required if key not in config]
    if missing:
        raise ConfigError(f"missing configuration keys: {', '.join(missing)}")
    if "YOUR_ACCOUNT" in config["image"]:
        raise ConfigError("replace YOUR_ACCOUNT in image before provisioning")
    if float(config.get("max_hourly_price", 0)) <= 0:
        raise ConfigError("max_hourly_price must be greater than zero")
    for port_name in ("web", "mcp", "health", "ssh"):
        if port_name not in config["ports"]:
            raise ConfigError(f"missing ports.{port_name}")
    return config


def worker_env(config: dict[str, Any]) -> dict[str, str]:
    ports = config["ports"]
    values = {str(k): str(v) for k, v in config.get("worker_env", {}).items()}
    values.update(
        {
            "XAI_ENVIRONMENT_VERSION": str(config["environment_version"]),
            "WANGP_WORKSPACE": str(config["workspace_mount"]),
            "WANGP_WEB_PORT": str(ports["web"]),
            "WANGP_MCP_PORT": str(ports["mcp"]),
            "HEALTH_PORT": str(ports["health"]),
        }
    )
    return values


def runpod_payload(config: dict[str, Any]) -> dict[str, Any]:
    rp = config["runpod"]
    ports = config["ports"]
    payload: dict[str, Any] = {
        "name": rp["name"],
        "imageName": config["image"],
        "computeType": "GPU",
        "cloudType": rp.get("cloud_type", "COMMUNITY"),
        "gpuTypeIds": rp["gpu_type_ids"],
        "gpuTypePriority": "availability",
        "gpuCount": int(rp.get("gpu_count", 1)),
        "interruptible": bool(rp.get("interruptible", False)),
        "containerDiskInGb": int(config.get("container_disk_gb", 150)),
        "volumeInGb": int(rp.get("volume_gb", 0)),
        "volumeMountPath": config["workspace_mount"],
        "allowedCudaVersions": rp.get("allowed_cuda_versions", []),
        "minRAMPerGPU": int(rp.get("min_ram_per_gpu_gb", 64)),
        "minVCPUPerGPU": int(rp.get("min_vcpu_per_gpu", 8)),
        "supportPublicIp": True,
        "ports": [
            f"{ports['web']}/http",
            f"{ports['mcp']}/http",
            f"{ports['health']}/http",
            f"{ports['ssh']}/tcp",
        ],
        "env": worker_env(config),
    }
    if rp.get("network_volume_id"):
        payload["networkVolumeId"] = rp["network_volume_id"]
    return payload


def vast_search_payload(config: dict[str, Any]) -> dict[str, Any]:
    vast = config["vast"]
    return {
        "gpu_name": {"in": vast["gpu_names"]},
        "num_gpus": {"gte": int(vast.get("gpu_count", 1))},
        "gpu_ram": {"gte": int(vast.get("min_gpu_ram_mb", 30000))},
        "reliability": {"gte": float(vast.get("min_reliability", 0.99))},
        "verified": {"eq": bool(vast.get("verified_only", True))},
        "rentable": {"eq": True},
        "type": vast.get("offer_type", "ondemand"),
        "limit": int(vast.get("search_limit", 10)),
        "order": [["dph_total", "asc"]],
    }


def vast_create_payload(config: dict[str, Any]) -> dict[str, Any]:
    vast = config["vast"]
    ports = config["ports"]
    env = worker_env(config)
    for port_name in ("web", "mcp", "health"):
        port = ports[port_name]
        env[f"-p {port}:{port}"] = "1"
    payload: dict[str, Any] = {
        "image": config["image"],
        "label": vast["label"],
        "disk": int(config.get("container_disk_gb", 150)),
        "runtype": vast.get("runtype", "ssh_direct"),
        "target_state": "running",
        "env": env,
        "onstart": "mkdir -p /workspace/logs && nohup /usr/local/bin/xai-worker-entrypoint >/workspace/logs/onstart.log 2>&1 &",
        "cancel_unavail": True,
    }
    if vast.get("volume_id") is not None:
        payload["volume_info"] = {
            "volume_id": vast["volume_id"],
            "mount_path": config["workspace_mount"],
        }
    return payload


def request_json(method: str, url: str, api_key: str, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {api_key}")
    request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"provider returned HTTP {exc.code}: {detail}") from exc


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def require_key(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfigError(f"{name} is required with --execute")
    return value


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Dry-run-first RunPod/Vast WanGP provisioner")
    sub = result.add_subparsers(dest="command", required=True)
    for name in ("validate", "runpod-create", "vast-search"):
        command = sub.add_parser(name)
        command.add_argument("--config", required=True)
        if name != "validate":
            command.add_argument("--execute", action="store_true")
    create = sub.add_parser("vast-create")
    create.add_argument("--config", required=True)
    create.add_argument("--offer-id", required=True, type=int)
    create.add_argument("--offer-price", required=True, type=float)
    create.add_argument("--execute", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    config = load_config(args.config)
    if args.command == "validate":
        print_json({"valid": True, "environment_version": config["environment_version"]})
        return 0
    if args.command == "runpod-create":
        payload = runpod_payload(config)
        if not args.execute:
            print_json({"dry_run": True, "method": "POST", "url": f"{RUNPOD_API}/pods", "payload": payload})
            return 0
        print_json(request_json("POST", f"{RUNPOD_API}/pods", require_key("RUNPOD_API_KEY"), payload))
        return 0
    if args.command == "vast-search":
        payload = vast_search_payload(config)
        if not args.execute:
            print_json({"dry_run": True, "method": "POST", "url": f"{VAST_API}/bundles/", "payload": payload})
            return 0
        result = request_json("POST", f"{VAST_API}/bundles/", require_key("VAST_API_KEY"), payload)
        ceiling = float(config["max_hourly_price"])
        offers = [offer for offer in result.get("offers", []) if float(offer.get("dph_total", float("inf"))) <= ceiling]
        print_json({"max_hourly_price": ceiling, "offers": offers})
        return 0
    if args.command == "vast-create":
        ceiling = float(config["max_hourly_price"])
        if args.offer_price > ceiling:
            raise ConfigError(f"offer price ${args.offer_price:.3f}/hr exceeds ${ceiling:.3f}/hr limit")
        payload = vast_create_payload(config)
        url = f"{VAST_API}/asks/{args.offer_id}/"
        if not args.execute:
            print_json({"dry_run": True, "accepted_offer_price": args.offer_price, "method": "PUT", "url": url, "payload": payload})
            return 0
        print_json(request_json("PUT", url, require_key("VAST_API_KEY"), payload))
        return 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ConfigError, OSError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
