# Connecting Google Drive from an Ephemeral Pod

Updated: 2026-09-18

Status: `PROCEDURE — not yet executed against the real account`

Drive is the durable store for this project's cloud sessions: weights and character inputs come
down, session output goes up. See [PC-less cloud studio plan](pc-less-cloud-studio-plan.md).

## The constraint

A pod has no browser and no human at a console, so it cannot complete an interactive OAuth flow.
Every workable approach is the same shape: **authorise once, somewhere that has a browser, then
inject the resulting credential into every later pod as a secret.** Never bake it into the image
and never commit it.

## Step 0 — create your own Google OAuth client ID first

Do this before anything else. rclone ships a shared default client ID that Google rate-limits
hard, and it is a common cause of "Drive is slow" conclusions that are really throttling.

1. Google Cloud Console → new project.
2. Enable the **Google Drive API**.
3. OAuth consent screen → External → add your own account as a test user.
4. Credentials → Create credentials → **OAuth client ID** → *Desktop app*.
5. Keep the client ID and client secret.

This is also what makes the Drive-vs-hub throughput measurement meaningful; measuring with the
shared ID measures rclone's rate limit, not Drive.

## Step 1 — authorise once

Pick the path that matches what you have.

### Path A — a machine with a browser is available (simplest)

On that machine, with rclone installed:

```bash
rclone config
# n) New remote      name> gdrive      Storage> drive
# client_id / client_secret> the ones from Step 0
# scope> 1 (full access)
# service_account_file> (leave blank)
# Edit advanced config? n
# Use web browser to automatically authenticate? y
```

Approve in the browser. The remote now works. Go to Step 2.

### Path B — phone only

Start the first pod, join it to the tailnet, then run the same `rclone config` on the pod and
choose the automatic browser option. rclone listens on `127.0.0.1:53682` for the callback, so
expose that to the tailnet for the duration of the flow:

```bash
socat TCP-LISTEN:53682,fork,reuseaddr TCP:127.0.0.1:53682 &
```

Open `http://<pod-tailnet-ip>:53682/auth` on the phone, approve, then stop the forwarder. The
pod is only reachable inside your tailnet, so nothing is exposed publicly.

### Path C — Google Workspace with a Shared Drive

Use a **service account**: create it in Cloud Console, download its JSON key, and add the service
account's address as a member of the Shared Drive. rclone then needs no token refresh and no
interaction ever.

Do **not** use a service account with a personal Gmail account's My Drive. A service account has
no storage quota of its own, so files it tries to create there fail. It works only where the
Shared Drive owns the files.

## Step 2 — turn the credential into pod secrets

rclone reads a whole remote from environment variables using
`RCLONE_CONFIG_<REMOTE>_<OPTION>`, so no config file has to be shipped:

```text
RCLONE_CONFIG_GDRIVE_TYPE=drive
RCLONE_CONFIG_GDRIVE_CLIENT_ID=<from step 0>
RCLONE_CONFIG_GDRIVE_CLIENT_SECRET=<from step 0>
RCLONE_CONFIG_GDRIVE_TOKEN=<the token JSON from ~/.config/rclone/rclone.conf>
RCLONE_CONFIG_GDRIVE_ROOT_FOLDER_ID=<optional: scope it to one folder>
```

Copy `token` verbatim from the generated `rclone.conf`; it carries a refresh token, so it keeps
working without further interaction. Store these wherever the launcher keeps secrets and pass
them to the pod as environment variables. They are credentials: never in Git, never in the image,
never in a run record.

`ROOT_FOLDER_ID` is worth setting — it limits a pod to one Drive folder rather than the whole
account.

## Step 3 — use copy/sync, not mount

```bash
# inputs, at boot
rclone copy gdrive:xai/inputs /workspace/inputs \
  --transfers 8 --checkers 16 --fast-list

# weights, only the profile this session needs
rclone copy gdrive:xai/models/<profile> /workspace/models \
  --transfers 8 --drive-chunk-size 256M

# outputs, continuously during the session
rclone copy /workspace/outputs gdrive:xai/outputs/<session-id> \
  --transfers 8 --drive-chunk-size 256M --update
```

Prefer `copy`/`sync` over `rclone mount`. A mount is convenient but a poor host for large
sequential writes and an actively written SQLite file, and a stall becomes a generation failure
rather than a retryable transfer.

Run the output copy on a short timer for the whole session, not only at teardown. Continuous sync
is what makes a short idle timeout safe to set.

### Tuning notes

- `--drive-chunk-size` dominates large-file throughput; 256M is a reasonable start and costs RAM
  per transfer.
- `--fast-list` cuts API calls on directories with many files.
- Drive caps uploads at 750 GB/day. Repeatedly pulling one large file many times in a day can
  trip a per-file download quota.

## Step 4 — verify before trusting it

```bash
rclone about gdrive:                       # credential works, quota visible
rclone lsd gdrive:xai                      # expected folders
rclone check /workspace/outputs gdrive:xai/outputs/<session-id>
```

`rclone check` compares hashes on both sides. Teardown must gate on a clean check, not on a copy
command's exit status alone — the project's export-verified teardown rule applies here.

## Drive throughput is a load-bearing assumption, not a tuning detail

If Drive is slow the architecture does not merely get slower, it stops working as designed:
continuous output sync cannot keep up with generation, so a short idle timeout is no longer safe;
and the verified final export runs while the GPU is still billing. **Measure before building the
worker image, not after.**

Upload is the critical path, not download — output leaves the pod and teardown gates on it — and
Drive upload is typically slower than download.

The dangerous case is **many small files**. Per-file API overhead dominates, so 200 PNGs can be
far slower than one 5 GB video, and image batches are the common output here. Measure all four:

```bash
# upload, one large file  (video session teardown time)
time rclone copy /workspace/big.mp4 gdrive:xai/bench/ --drive-chunk-size 256M

# upload, many small files  (THE risky case)
time rclone copy /workspace/batch-200-png gdrive:xai/bench/batch --transfers 16 --checkers 32

# download, one large file  (weight delivery)
time rclone copy gdrive:xai/bench/big.mp4 /tmp/ --transfers 8 --drive-chunk-size 256M

# download, many small files  (character sheets, references)
time rclone copy gdrive:xai/bench/batch /tmp/batch --transfers 16 --fast-list

# hub comparison for public weights
HF_HUB_ENABLE_HF_TRANSFER=1 time hf download <repo> <comparable-file> --local-dir /tmp/
```

All of it with the own client ID from Step 0; the shared default measures rclone's rate limit.
None of it needs a GPU — run it on the cheap CPU pod that also inspects the old network volume
before it is deleted.

### If Drive is too slow

The design survives; the transport changes.

1. **Archive small files before upload.** One tar per batch removes the per-file API overhead.
   The Gallery reads from the pod's local disk anyway, so Drive only needs the bundle. This alone
   likely fixes the worst case.
2. **Use S3-compatible object storage for the hot path.** Cloudflare R2 has no egress fee and
   costs roughly $1.5/month for 100 GB. `docs/render-broker.md` already anticipates "one
   provider-neutral S3-compatible interface", so this is a route the project reserved, not a new
   dependency.
3. **Split the roles**: object storage for in-session transfer, Drive for the durable archive.

Record the measured MB/s figures in the cloud plan's open-measurements section. They decide what
the worker image is built to talk to.
