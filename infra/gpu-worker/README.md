# Ephemeral WanGP GPU Worker Skeleton

This skeleton creates the same MiniMax H3 / WanGP worker shape on RunPod or
Vast.ai. It deliberately separates reusable environment configuration from
billable provisioning.

## What is included

- one provider-neutral worker image (`Dockerfile`)
- a persistent `/workspace` layout for models, outputs, logs, and the Python environment
- selectable WanGP web UI on port `7860` or streamable-HTTP MCP on port `8000`
- a standard health endpoint on port `8080`
- a dependency-free provisioning CLI for RunPod and Vast.ai
- dry-run by default; billable creation requires `--execute`
- maximum hourly price enforcement for Vast offers

The image pins WanGP commit `01a67f0a1ca268a8276a6c46e97d70baa7440ab9`,
the commit inspected on the local workstation. Change the build argument only
after testing a newer commit.

## 1. Build and publish the image

Replace the image name in `config.example.json` with an image in a registry
that both providers can pull, then build it:

```powershell
docker build -t ghcr.io/YOUR_ACCOUNT/xai-wangp-h3:0.1.0 infra/gpu-worker
docker push ghcr.io/YOUR_ACCOUNT/xai-wangp-h3:0.1.0
```

The image contains WanGP and Python dependencies, but not the large model
checkpoints. RunPod may keep checkpoints under `/workspace/models` on its
persistent network volume. Vast defaults to an empty-start, one-session worker:
the bootstrap downloads only the required model profile, results are exported
and verified, and the instance is destroyed rather than stopped.

The full Vast operator procedure is in `docs/vast-ephemeral-runbook.md`.

## 2. Create a local configuration

Copy `config.example.json` to a file outside Git or to
`infra/gpu-worker/config.local.json` (ignored by Git), then set:

- the published image name
- provider GPU identifiers
- optional persistent volume IDs
- price and disk limits

Do not put API keys in the JSON file.

```powershell
$env:RUNPOD_API_KEY = '...'
$env:VAST_API_KEY = '...'
```

## 3. Validate without spending money

```powershell
python infra/gpu-worker/provision.py validate --config infra/gpu-worker/config.local.json
python infra/gpu-worker/provision.py runpod-create --config infra/gpu-worker/config.local.json
python infra/gpu-worker/provision.py vast-search --config infra/gpu-worker/config.local.json
```

Without `--execute`, commands print the redacted request and make no network
request. This is the expected mode for prompt planning and CI.

## 4. Provision intentionally

RunPod selects capacity from the configured GPU type list:

```powershell
python infra/gpu-worker/provision.py runpod-create --config infra/gpu-worker/config.local.json --execute
```

Vast is a two-step marketplace flow. Search first, inspect price/reliability,
then create from an explicit offer ID:

```powershell
python infra/gpu-worker/provision.py vast-search --config infra/gpu-worker/config.local.json --execute
python infra/gpu-worker/provision.py vast-create --config infra/gpu-worker/config.local.json --offer-id 12345678 --offer-price 0.85 --execute
```

`vast-create` refuses an offer price above `max_hourly_price`. The price is
passed explicitly so that a stale marketplace selection cannot silently exceed
the approved budget.

Treat each Vast create as a fresh machine. The selected image, bootstrap
version, model manifest, prompt/settings, and artifact destination must all be
known before `--execute` is used. Do not depend on files from an earlier Vast
instance.

## 5. Readiness contract

After the provider reports the instance running, require all of these before
submitting an expensive render:

```text
GET :8080/healthz     -> process-level worker health
WanGP :7860           -> human UI when WANGP_SERVICE_MODE=web
WanGP :8000/mcp       -> broker service when WANGP_SERVICE_MODE=mcp (default)
```

The health endpoint reports `starting` until the WanGP processes have been
launched. It does not claim that every H3 checkpoint has already been
downloaded; model capability must still be checked through WanGP before queueing.

Do not run Web UI and MCP as separate WanGP processes on one GPU. Select one
service mode so model weights are not loaded twice. The default is `mcp` because
Hermes and the Render Broker own submission and durable records.

## Important limits

- This skeleton does not create billable resources during tests.
- It does not delete persistent volumes.
- Provider creation success is not renderer readiness; poll health and inspect
  the WanGP model schema.
- Final media must be copied and checksum-verified before an ephemeral instance
  is stopped or destroyed.
- Vast instances must be destroyed after verified export. `Stop` is only a
  temporary recovery action because instance storage remains billable.
- Vast hosts vary. Keep `verified`, reliability, VRAM, disk, and price filters
  enabled instead of choosing only the cheapest offer.

Official provider contracts used by the CLI:

- RunPod: `POST https://rest.runpod.io/v1/pods`
- Vast search: `POST https://console.vast.ai/api/v0/bundles/`
- Vast create: `PUT https://console.vast.ai/api/v0/asks/{offer_id}/`
