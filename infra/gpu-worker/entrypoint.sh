#!/usr/bin/env bash
set -euo pipefail

workspace="${WANGP_WORKSPACE:-/workspace}"
wangp_root="${WANGP_ROOT:-/opt/WanGP}"
python_bin="${wangp_root}/.venv/bin/python"

mkdir -p "${workspace}/models" "${workspace}/outputs" "${workspace}/logs" "${workspace}/config"
ln -sfnT "${workspace}/models" "${wangp_root}/ckpts"
ln -sfnT "${workspace}/outputs" "${wangp_root}/outputs"

export XAI_WORKER_STATE_FILE="${workspace}/worker-state.json"
"${python_bin}" /opt/xai-worker/health_server.py >>"${workspace}/logs/health.log" 2>&1 &

web_args=(
  --listen
  --server-name 0.0.0.0
  --server-port "${WANGP_WEB_PORT:-7860}"
  --output-dir "${workspace}/outputs"
  --config "${workspace}/config"
  --settings "${workspace}/config/settings"
  --profile "${WANGP_PROFILE:-4}"
  --vram-safety-coefficient "${WANGP_VRAM_SAFETY:-0.90}"
)

if [[ -n "${WANGP_ATTENTION:-}" ]]; then
  web_args+=(--attention "${WANGP_ATTENTION}")
fi

cd "${wangp_root}"
service_mode="${WANGP_SERVICE_MODE:-mcp}"
if [[ "$service_mode" == "web" ]]; then
  "${python_bin}" wgp.py "${web_args[@]}" >>"${workspace}/logs/wangp-web.log" 2>&1 &
  service_pid=$!
elif [[ "$service_mode" == "mcp" ]]; then
  "${python_bin}" wgp.py \
    --mcp \
    --mcp-transport streamable-http \
    --mcp-host 0.0.0.0 \
    --mcp-port "${WANGP_MCP_PORT:-8000}" \
    --output-dir "${workspace}/outputs" \
    --config "${workspace}/config" \
    --settings "${workspace}/config/settings" \
    --profile "${WANGP_PROFILE:-4}" \
    --vram-safety-coefficient "${WANGP_VRAM_SAFETY:-0.90}" \
    >>"${workspace}/logs/wangp-mcp.log" 2>&1 &
  service_pid=$!
else
  echo "Unsupported WANGP_SERVICE_MODE: ${service_mode}" >&2
  exit 2
fi

printf '{"status":"started","mode":"%s","pids":[%s]}\n' "$service_mode" "$service_pid" >"${XAI_WORKER_STATE_FILE}"

trap 'kill "$service_pid" 2>/dev/null || true; wait || true' TERM INT
wait "$service_pid"
exit_code=$?
printf '{"status":"failed","exit_code":%s}\n' "$exit_code" >"${XAI_WORKER_STATE_FILE}"
exit "$exit_code"
