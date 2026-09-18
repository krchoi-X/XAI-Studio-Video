#!/usr/bin/env bash
# Measure Google Drive throughput FROM A POD, where the transfer will actually happen.
#
# Measuring this from a home workstation is meaningless: the path that matters is
# RunPod datacenter <-> Google, not a domestic uplink.
#
# Needs no GPU. Run it on the cheap CPU pod that also inspects the old network
# volume before deleting it.
#
#   export RCLONE_CONFIG_GDRIVE_TYPE=drive
#   export RCLONE_CONFIG_GDRIVE_CLIENT_ID=...
#   export RCLONE_CONFIG_GDRIVE_CLIENT_SECRET=...
#   export RCLONE_CONFIG_GDRIVE_TOKEN='{"access_token":...}'
#   ./bench-drive.sh [remote:path]
#
# Upload is the critical path, and many small files is the dangerous shape:
# per-file API overhead can make an image batch far slower than one large video.
set -euo pipefail

REMOTE="${1:-gdrive:xai/bench}"
WORK="${WORK_DIR:-/workspace/bench}"
BIG_MB="${BIG_MB:-4096}"
SMALL_COUNT="${SMALL_COUNT:-200}"
SMALL_MB="${SMALL_MB:-5}"

command -v rclone >/dev/null || { echo "rclone not installed" >&2; exit 2; }

echo "== credential check =="
rclone about "${REMOTE%%:*}:" || { echo "Drive credential is not working" >&2; exit 2; }

echo "== building fixtures (${BIG_MB}MB single, ${SMALL_COUNT} x ${SMALL_MB}MB) =="
mkdir -p "$WORK/batch"
[ -f "$WORK/big.bin" ] || dd if=/dev/urandom of="$WORK/big.bin" bs=1M count="$BIG_MB" status=none
for i in $(seq 1 "$SMALL_COUNT"); do
  [ -f "$WORK/batch/$i.bin" ] || dd if=/dev/urandom of="$WORK/batch/$i.bin" bs=1M count="$SMALL_MB" status=none
done

run() {
  echo
  echo "== $1 =="
  shift
  /usr/bin/time -f 'elapsed %e s' "$@" 2>&1 | tail -20
}

run "UPLOAD  one large file  (video teardown time)" \
  rclone copy "$WORK/big.bin" "$REMOTE/" --drive-chunk-size 256M --stats-one-line --stats 10s -P

run "UPLOAD  many small files  (THE risky case)" \
  rclone copy "$WORK/batch" "$REMOTE/batch" --transfers 16 --checkers 32 --stats-one-line --stats 10s -P

run "UPLOAD  many small files, tarred first  (the mitigation)" \
  bash -c "tar -cf '$WORK/batch.tar' -C '$WORK' batch && rclone copy '$WORK/batch.tar' '$REMOTE/' --drive-chunk-size 256M -P"

run "DOWNLOAD  one large file  (weight delivery)" \
  rclone copy "$REMOTE/big.bin" /tmp/dl-big --transfers 8 --drive-chunk-size 256M --stats-one-line --stats 10s -P

run "DOWNLOAD  many small files  (character sheets, references)" \
  rclone copy "$REMOTE/batch" /tmp/dl-batch --transfers 16 --fast-list --stats-one-line --stats 10s -P

echo
echo "== verifying one transfer =="
rclone check "$WORK/batch" "$REMOTE/batch" --one-way || echo "CHECK FAILED"

echo
echo "== cleaning up remote fixtures =="
rclone purge "$REMOTE" || true
rm -rf "$WORK" /tmp/dl-big /tmp/dl-batch

cat <<'NOTE'

Record the MB/s of each run in docs/cloud-gpu-automation-plan.md section 8.

Reading the result:
  - small-file upload close to large-file upload -> plain Drive sync is fine
  - small-file upload far slower, tarred run fast -> archive batches before upload
  - both uploads slow                            -> move the in-session hot path to
                                                    S3-compatible storage (R2), keep
                                                    Drive as the durable archive
NOTE
