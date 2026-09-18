#!/usr/bin/env bash
# Measure Google Drive throughput FROM A POD, where the transfer will actually happen.
#
# Measuring this from a home workstation is meaningless: the path that matters is
# RunPod datacenter <-> Google, not a domestic uplink.
#
# Needs no GPU. Run it on the cheap CPU pod that also inspects the old network
# volume before deleting it.
#
# Credential, either way:
#
#   a) by hand -- paste the whole remote. Run `rclone config show gdrive` on the
#      machine where you authorised, then in the pod:
#
#        mkdir -p ~/.config/rclone
#        cat > ~/.config/rclone/rclone.conf <<'EOF'
#        [gdrive]
#        type = drive
#        client_id = ...
#        client_secret = ...
#        scope = drive
#        token = {"access_token":...}
#        EOF
#
#      Easier than exports: the token is JSON and quoting it is error-prone.
#
#   b) automated -- the launcher injects RCLONE_CONFIG_GDRIVE_TYPE,
#      _CLIENT_ID, _CLIENT_SECRET and _TOKEN as pod environment variables.
#
#   WORK_DIR=/root/bench ./bench-drive.sh [remote:path]
#
# Point WORK_DIR away from a network volume you are about to delete.
#
# Upload is the critical path, and many small files is the dangerous shape:
# per-file API overhead can make an image batch far slower than one large video.
set -euo pipefail

REMOTE="${1:-gdrive:xai/bench}"
WORK="${WORK_DIR:-/workspace/bench}"
BIG_MB="${BIG_MB:-4096}"
SMALL_COUNT="${SMALL_COUNT:-200}"
SMALL_MB="${SMALL_MB:-5}"
BATCH_MB=$(( SMALL_COUNT * SMALL_MB ))

command -v rclone >/dev/null || { echo "rclone not installed" >&2; exit 2; }

echo "== credential check =="
rclone about "${REMOTE%%:*}:" || { echo "Drive credential is not working" >&2; exit 2; }

echo
echo "== building fixtures (${BIG_MB}MB single, ${SMALL_COUNT} x ${SMALL_MB}MB) =="
mkdir -p "$WORK/batch"
[ -f "$WORK/big.bin" ] || dd if=/dev/urandom of="$WORK/big.bin" bs=1M count="$BIG_MB" status=none
for i in $(seq 1 "$SMALL_COUNT"); do
  [ -f "$WORK/batch/$i.bin" ] || dd if=/dev/urandom of="$WORK/batch/$i.bin" bs=1M count="$SMALL_MB" status=none
done

RESULTS=()

# No /usr/bin/time: minimal container images do not ship the time package.
run() {
  local label="$1" mb="$2"; shift 2
  echo
  echo "== $label =="
  local start end ms rate
  start=$(date +%s%3N)
  if ! "$@"; then
    echo "-> FAILED"
    RESULTS+=("$(printf '%-46s %10s %12s' "$label" "FAILED" "-")")
    return 0
  fi
  end=$(date +%s%3N)
  ms=$(( end - start )); [ "$ms" -gt 0 ] || ms=1
  rate=$(( mb * 1000 / ms ))
  printf -- '-> %d.%03ds, %d MB/s\n' $(( ms / 1000 )) $(( ms % 1000 )) "$rate"
  RESULTS+=("$(printf '%-46s %8d.%03ds %8d MB/s' "$label" $(( ms / 1000 )) $(( ms % 1000 )) "$rate")")
}

run "UPLOAD   one large file" "$BIG_MB" \
  rclone copy "$WORK/big.bin" "$REMOTE/" --drive-chunk-size 256M --stats-one-line --stats 10s

run "UPLOAD   many small files  (risky case)" "$BATCH_MB" \
  rclone copy "$WORK/batch" "$REMOTE/batch" --transfers 16 --checkers 32 --stats-one-line --stats 10s

tar -cf "$WORK/batch.tar" -C "$WORK" batch
run "UPLOAD   same batch, tarred  (mitigation)" "$BATCH_MB" \
  rclone copy "$WORK/batch.tar" "$REMOTE/" --drive-chunk-size 256M --stats-one-line --stats 10s

run "DOWNLOAD one large file" "$BIG_MB" \
  rclone copy "$REMOTE/big.bin" "$WORK/dl-big" --transfers 8 --drive-chunk-size 256M --stats-one-line --stats 10s

run "DOWNLOAD many small files" "$BATCH_MB" \
  rclone copy "$REMOTE/batch" "$WORK/dl-batch" --transfers 16 --fast-list --stats-one-line --stats 10s

echo
echo "== verifying one transfer =="
rclone check "$WORK/batch" "$REMOTE/batch" --one-way || echo "CHECK FAILED"

echo
echo "=================== RESULTS ==================="
printf '%s\n' "${RESULTS[@]}"
echo "==============================================="

echo
echo "== cleaning up =="
rclone purge "$REMOTE" || true
rm -rf "$WORK"

cat <<'NOTE'

Record these MB/s figures in docs/cloud-gpu-automation-plan.md section 8.

Reading the result:
  - small-file upload close to large-file upload -> plain Drive sync is fine
  - small-file upload far slower, tarred run fast -> archive batches before upload
  - both uploads slow                            -> move the in-session hot path to
                                                    S3-compatible storage (R2), keep
                                                    Drive as the durable archive
NOTE
