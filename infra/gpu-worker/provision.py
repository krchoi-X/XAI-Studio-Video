from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


RUNPOD_API = "https://rest.runpod.io/v1"
# REST v1 is deprecated and retires 2026-11-15. Read-only account auditing already
# uses v2; the create path still targets v1 and must be migrated before that date.
RUNPOD_API_V2 = "https://api.runpod.io/v2"
VAST_API = "https://console.vast.ai/api/v0"
# Both providers sit behind Cloudflare, which rejects the default urllib
# client signature with HTTP 403 "error code: 1010". Send an explicit
# User-Agent so an audit cannot be mistaken for an empty account.
USER_AGENT = os.environ.get("XAI_HTTP_USER_AGENT", "").strip() or "xai-studio-gpu-worker/0.1"


class ConfigError(ValueError):
    pass


class ProviderHTTPError(RuntimeError):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        super().__init__(f"provider returned HTTP {status_code}: {detail}")


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
    request.add_header("Accept", "application/json")
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = response.read().decode("utf-8").strip()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ProviderHTTPError(exc.code, detail) from exc


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def require_key(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfigError(f"{name} is required with --execute")
    return value


def pick(record: Any, *names: str, default: Any = None) -> Any:
    """Read the first present field, tolerating provider field-name drift."""
    if not isinstance(record, dict):
        return default
    for name in names:
        if record.get(name) is not None:
            return record[name]
    return default


def rows(payload: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        value = payload.get(key)
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
        return []
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    return []


def probe(label: str, url: str, api_key: str, notes: list[str]) -> Any:
    """GET one endpoint. A failure is recorded, never raised, so one broken
    endpoint cannot hide a billable resource reported by another."""
    try:
        return request_json("GET", url, api_key, None)
    except (RuntimeError, OSError, json.JSONDecodeError) as exc:
        notes.append(f"{label}: {exc}")
        return None


def runpod_active(api_key: str, days: int, notes: list[str]) -> dict[str, Any]:
    pods = [
        {
            "id": pick(pod, "id", "podId"),
            "name": pick(pod, "name"),
            "state": pick(pod, "desiredStatus", "status", "state"),
            "hourly_cost": float(pick(pod, "cost", "costPerHr", "costPerHour", default=0.0) or 0.0),
            "gpu": pick(pod, "machineType", "gpuTypeId", "gpu"),
            "network_volume_id": pick(pod, "networkVolumeId"),
        }
        for pod in rows(probe("runpod pods", f"{RUNPOD_API_V2}/pods", api_key, notes), "pods")
    ]
    volumes = [
        {
            "id": pick(volume, "id", "networkVolumeId"),
            "name": pick(volume, "name"),
            "size_gb": int(pick(volume, "size", "sizeInGb", default=0) or 0),
            "data_center": pick(volume, "dataCenterId", "dataCenter"),
        }
        for volume in rows(
            probe("runpod network volumes", f"{RUNPOD_API_V2}/network-volumes", api_key, notes),
            "networkVolumes",
        )
    ]
    billing = None
    if days > 0:
        end = datetime.now(timezone.utc)
        query = urllib.parse.urlencode(
            {
                "startTime": (end - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "endTime": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "bucketSize": "day",
            }
        )
        billing = probe(
            "runpod volume billing",
            f"{RUNPOD_API_V2}/billing/network-volumes?{query}",
            api_key,
            notes,
        )
    return {"pods": pods, "network_volumes": volumes, "volume_billing": billing}


def vast_active(api_key: str, notes: list[str]) -> dict[str, Any]:
    instances = [
        {
            "id": pick(instance, "id"),
            "label": pick(instance, "label"),
            "state": pick(instance, "actual_status", "cur_state", "intended_status"),
            "hourly_cost": float(pick(instance, "dph_total", default=0.0) or 0.0),
            "gpu": pick(instance, "gpu_name"),
        }
        for instance in rows(probe("vast instances", f"{VAST_API}/instances/", api_key, notes), "instances")
    ]
    volumes = [
        {
            "id": pick(volume, "id"),
            "label": pick(volume, "label", "name"),
            "size_gb": int(pick(volume, "disk_space", "size", default=0) or 0),
        }
        for volume in rows(probe("vast volumes", f"{VAST_API}/volumes/", api_key, notes), "volumes")
    ]
    return {"instances": instances, "volumes": volumes}


RUNNING_STATES = {"RUNNING", "RUN", "RUNNING_POD", "ACTIVE"}


def is_running(state: Any) -> bool:
    return str(state or "").strip().upper() in RUNNING_STATES


def active_report(providers: list[str], days: int) -> dict[str, Any]:
    notes: list[str] = []
    report: dict[str, Any] = {"checked_at": datetime.now(timezone.utc).isoformat()}
    compute: list[dict[str, Any]] = []
    storage: list[dict[str, Any]] = []

    if "runpod" in providers:
        section = runpod_active(require_key("RUNPOD_API_KEY"), days, notes)
        report["runpod"] = section
        compute.extend(section["pods"])
        storage.extend(section["network_volumes"])
    if "vast" in providers:
        section = vast_active(require_key("VAST_API_KEY"), notes)
        report["vast"] = section
        compute.extend(section["instances"])
        storage.extend(section["volumes"])

    running = [item for item in compute if is_running(item["state"])]
    stopped = [item for item in compute if not is_running(item["state"])]
    storage_gb = sum(int(item.get("size_gb") or 0) for item in storage)
    warnings: list[str] = []
    if storage_gb and not compute:
        warnings.append(
            f"{storage_gb} GB of persistent storage is billing with no compute attached. "
            "Storage bills continuously; pods bill only while running."
        )
    if stopped:
        warnings.append(
            f"{len(stopped)} non-running compute resource(s) still exist. "
            "A stopped resource can still bill for its disk; destroy rather than stop."
        )

    if notes:
        warnings.insert(
            0,
            f"INCOMPLETE: {len(notes)} provider query(ies) failed. The totals below are "
            "NOT a clean bill of health -- billable resources may exist but be unreported. "
            "See notes.",
        )
    report["complete"] = not notes
    report["totals"] = {
        "running_compute": len(running),
        "stopped_compute": len(stopped),
        "hourly_burn": round(sum(item["hourly_cost"] for item in running), 4),
        "persistent_storage_gb": storage_gb,
    }
    report["warnings"] = warnings
    report["notes"] = notes
    return report


ACTIVE_FILE = Path(__file__).resolve().parent / "active-resources.json"


def read_active() -> list[dict[str, Any]]:
    try:
        rows_ = json.loads(ACTIVE_FILE.read_text(encoding="utf-8"))
        return rows_ if isinstance(rows_, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def write_active(records: list[dict[str, Any]]) -> None:
    ACTIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = ACTIVE_FILE.with_name(f"{ACTIVE_FILE.name}.tmp")
    temporary.write_text(json.dumps(records, indent=2), encoding="utf-8")
    os.replace(temporary, ACTIVE_FILE)


def record_active(pod_id: str, config: dict[str, Any]) -> None:
    """Crash-safety net: a rented pod is recorded locally the moment it exists,
    so an orchestrator that dies still leaves a trail to the billable resource."""
    existing = read_active()
    existing.append(
        {
            "provider": "runpod",
            "pod_id": pod_id,
            "environment_version": config.get("environment_version"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    write_active(existing)


def clear_active(pod_id: str) -> None:
    if not ACTIVE_FILE.exists():
        return
    write_active([r for r in read_active() if r.get("pod_id") != pod_id])


def pod_endpoints(pod_id: str, ports: dict[str, Any]) -> dict[str, str]:
    """RunPod publishes each declared HTTP port on its own proxy hostname."""
    base = f"https://{pod_id}-%s.proxy.runpod.net"
    return {
        "health": (base % ports["health"]) + "/healthz",
        "web": base % ports["web"],
        "mcp": (base % ports["mcp"]) + "/mcp",
    }


def runpod_pod(pod_id: str, api_key: str) -> dict[str, Any]:
    payload = request_json("GET", f"{RUNPOD_API_V2}/pods/{pod_id}", api_key, None)
    pod = payload.get("pod", payload) if isinstance(payload, dict) else {}
    return {
        "id": pick(pod, "id", "podId", default=pod_id),
        "name": pick(pod, "name"),
        "state": pick(pod, "desiredStatus", "status", "state"),
        "hourly_cost": float(pick(pod, "cost", "costPerHr", "costPerHour", default=0.0) or 0.0),
        "gpu": pick(pod, "machineType", "gpuTypeId", "gpu"),
    }


def health_ready(url: str) -> bool:
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=10
        ) as response:
            if response.status != 200:
                return False
            body = response.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError, ValueError):
        return False
    try:
        return str(json.loads(body).get("status", "")).lower() in {"ready", "running", "ok", "started"}
    except json.JSONDecodeError:
        return False


def wait_ready(pod_id: str, config: dict[str, Any], api_key: str, timeout: int, poll: int = 10) -> dict[str, Any]:
    """Provider RUNNING is not renderer readiness. Both are polled, and the
    distinction is reported so a timeout says which stage never completed."""
    endpoints = pod_endpoints(pod_id, config["ports"])
    deadline = time.monotonic() + timeout
    last: dict[str, Any] = {}
    running_seen = False
    while True:
        try:
            last = runpod_pod(pod_id, api_key)
        except RuntimeError as exc:
            last = {"id": pod_id, "state": f"query failed: {exc}"}
        if is_running(last.get("state")):
            running_seen = True
            if health_ready(endpoints["health"]):
                return {"ready": True, "pod": last, "endpoints": endpoints}
        if time.monotonic() >= deadline:
            return {
                "ready": False,
                "pod": last,
                "endpoints": endpoints,
                "reason": "worker health never reported ready" if running_seen else "pod never reached RUNNING",
            }
        time.sleep(poll)


def runpod_terminate(pod_id: str, api_key: str) -> dict[str, Any]:
    """Delete, then re-read. An unverified teardown is not a teardown."""
    request_json("DELETE", f"{RUNPOD_API_V2}/pods/{pod_id}", api_key, None)
    time.sleep(3)
    try:
        remaining = runpod_pod(pod_id, api_key)
    except ProviderHTTPError as exc:
        if exc.status_code == 404:
            clear_active(pod_id)
            return {"pod_id": pod_id, "terminated": True, "verified": True}
        return {
            "pod_id": pod_id,
            "terminated": False,
            "verified": False,
            "verification_error": str(exc),
        }
    state = str(remaining.get("state") or "").upper()
    gone = state in {"TERMINATED", "DELETED", "EXITED"}
    if gone:
        clear_active(pod_id)
    return {"pod_id": pod_id, "terminated": gone, "verified": gone, "remaining": remaining}


def orphan_check(api_key: str) -> dict[str, Any]:
    """Reconcile the local record against the provider. Anything the provider
    still bills for, or that we never recorded, is reported."""
    recorded = read_active()
    notes: list[str] = []
    live = runpod_active(api_key, 0, notes)
    live_ids = {str(p["id"]) for p in live["pods"] if p.get("id")}
    recorded_ids = {str(r.get("pod_id")) for r in recorded if r.get("pod_id")}
    still_billing = [p for p in live["pods"] if str(p.get("id")) in recorded_ids]
    unrecorded = [p for p in live["pods"] if str(p.get("id")) not in recorded_ids]
    stale = [r for r in recorded if str(r.get("pod_id")) not in live_ids]
    return {
        "complete": not notes,
        "still_billing_from_our_records": still_billing,
        "billing_but_never_recorded": unrecorded,
        "recorded_but_already_gone": stale,
        "notes": notes,
    }


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
    active = sub.add_parser("list-active", help="audit billable pods, instances and volumes; no config needed")
    active.add_argument("--provider", choices=["runpod", "vast", "all"], default="all")
    active.add_argument("--billing-days", type=int, default=30)
    active.add_argument("--execute", action="store_true")
    status = sub.add_parser("runpod-status", help="one pod, normalized, with its proxy endpoints")
    status.add_argument("--config", required=True)
    status.add_argument("--pod-id", required=True)
    status.add_argument("--execute", action="store_true")
    ready = sub.add_parser("wait-ready", help="poll until the worker answers, not merely until the pod runs")
    ready.add_argument("--config", required=True)
    ready.add_argument("--pod-id", required=True)
    ready.add_argument("--timeout-seconds", type=int, default=900)
    ready.add_argument("--teardown-on-timeout", action="store_true")
    ready.add_argument("--execute", action="store_true")
    kill = sub.add_parser("runpod-terminate", help="terminate and verify the resource is gone")
    kill.add_argument("--pod-id", required=True)
    kill.add_argument("--execute", action="store_true")
    orphan = sub.add_parser("orphan-check", help="reconcile local records against what the provider still bills")
    orphan.add_argument("--execute", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "list-active":
        providers = ["runpod", "vast"] if args.provider == "all" else [args.provider]
        if not args.execute:
            print_json({"dry_run": True, "method": "GET", "providers": providers,
                        "urls": [f"{RUNPOD_API_V2}/pods", f"{RUNPOD_API_V2}/network-volumes",
                                 f"{RUNPOD_API_V2}/billing/network-volumes", f"{VAST_API}/instances/",
                                 f"{VAST_API}/volumes/"]})
            return 0
        report = active_report(providers, args.billing_days)
        print_json(report)
        return 0 if report["complete"] else 1
    if args.command == "runpod-terminate":
        if not args.execute:
            print_json({"dry_run": True, "method": "DELETE",
                        "url": f"{RUNPOD_API_V2}/pods/{args.pod_id}",
                        "then": "re-read the pod and assert it is gone"})
            return 0
        outcome = runpod_terminate(args.pod_id, require_key("RUNPOD_API_KEY"))
        print_json(outcome)
        return 0 if outcome["verified"] else 1
    if args.command == "orphan-check":
        if not args.execute:
            print_json({"dry_run": True, "reads": [str(ACTIVE_FILE), f"{RUNPOD_API_V2}/pods"]})
            return 0
        report = orphan_check(require_key("RUNPOD_API_KEY"))
        print_json(report)
        leaking = report["still_billing_from_our_records"] or report["billing_but_never_recorded"]
        return 0 if (report["complete"] and not leaking) else 1
    config = load_config(args.config)
    if args.command == "runpod-status":
        if not args.execute:
            print_json({"dry_run": True, "method": "GET",
                        "url": f"{RUNPOD_API_V2}/pods/{args.pod_id}",
                        "endpoints": pod_endpoints(args.pod_id, config["ports"])})
            return 0
        key = require_key("RUNPOD_API_KEY")
        print_json({"pod": runpod_pod(args.pod_id, key),
                    "endpoints": pod_endpoints(args.pod_id, config["ports"])})
        return 0
    if args.command == "wait-ready":
        if not args.execute:
            print_json({"dry_run": True, "polls": pod_endpoints(args.pod_id, config["ports"])["health"],
                        "timeout_seconds": args.timeout_seconds,
                        "teardown_on_timeout": bool(args.teardown_on_timeout)})
            return 0
        key = require_key("RUNPOD_API_KEY")
        outcome = wait_ready(args.pod_id, config, key, args.timeout_seconds)
        if not outcome["ready"] and args.teardown_on_timeout:
            outcome["teardown"] = runpod_terminate(args.pod_id, key)
        print_json(outcome)
        return 0 if outcome["ready"] else 1
    if args.command == "validate":
        print_json({"valid": True, "environment_version": config["environment_version"]})
        return 0
    if args.command == "runpod-create":
        payload = runpod_payload(config)
        if not args.execute:
            print_json({"dry_run": True, "method": "POST", "url": f"{RUNPOD_API}/pods", "payload": payload})
            return 0
        created = request_json("POST", f"{RUNPOD_API}/pods", require_key("RUNPOD_API_KEY"), payload)
        created_pod = created.get("pod", created) if isinstance(created, dict) else {}
        pod_id = pick(created_pod, "id", "podId")
        if not pod_id:
            raise RuntimeError(
                "RunPod accepted the create request but returned no pod id; "
                "run list-active --provider runpod --execute immediately"
            )
        record_active(str(pod_id), config)
        print_json(created)
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
