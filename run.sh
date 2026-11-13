#!/usr/bin/env bash
# BADASS micro-server in Docker: every vulnerable/fixed fixture behind one HTTP port.
#
#   ./run.sh              start in background (HTTP :8808 + HTTPS/FTP/Telnet/SMTP/LDAP/DNS/RESP/TCP)
#   ./run.sh --blind      opaque ids; answer key copied to .netlab/mapping.json
#   ./run.sh logs         follow the server logs
#   ./run.sh stop         stop the server
#   ./run.sh status       show container state
#   PORT=9000 ./run.sh    change the HTTP port
#   BIND=0.0.0.0 ./run.sh expose on the local LAN (isolated lab networks only!)
#
# Extra options are passed to tools/netserve.py (e.g. --language python --cwe CWE-89 --proto-variant fixed).
# By default all ports bind to 127.0.0.1; only set BIND=0.0.0.0 on an isolated lab LAN.
set -euo pipefail
cd "$(dirname "$0")"
source docker/common.sh

case "${1:-start}" in
  -h|--help|help)
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
  logs)   require_docker; exec "${DOCKER[@]}" logs -f "$CONTAINER" ;;
  stop)   require_docker; "${DOCKER[@]}" rm -f "$CONTAINER" >/dev/null 2>&1 && echo "Stopped." || echo "Not running."; exit 0 ;;
  status) require_docker; "${DOCKER[@]}" ps -a --filter "name=^${CONTAINER}$" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'; exit 0 ;;
  start)  [[ $# -gt 0 ]] && shift ;;
  *)      ;;  # options only: implicit start
esac

require_docker

ARGS=(--named --services)
EXTRA=()
BLIND=""
for arg in "$@"; do
  if [[ "$arg" == "--blind" ]]; then BLIND=1; ARGS=(--mapping /tmp/mapping.json --services); else EXTRA+=("$arg"); fi
done

if ! "${DOCKER[@]}" image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "First run: building images (needs network access, takes several minutes)."
  build_images
fi

"${DOCKER[@]}" rm -f "$CONTAINER" >/dev/null 2>&1 || true
"${DOCKER[@]}" run -d --name "$CONTAINER" \
  --read-only --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 512 --memory 2g --cpus 2 \
  -p "$BIND:$PORT:8808" \
  -p "$BIND:8443:8443" \
  -p "$BIND:2121:2121" \
  -p "$BIND:2122:2122" \
  -p "$BIND:2323:2323" \
  -p "$BIND:2525:2525" \
  -p "$BIND:3389:3389" \
  -p "$BIND:5353:5353/tcp" \
  -p "$BIND:5353:5353/udp" \
  -p "$BIND:6379:6379" \
  -p "$BIND:9001:9001" \
  --tmpfs /tmp:rw,nosuid,size=256m \
  --tmpfs /lab/.build:rw,exec,nosuid,mode=1777,size=2g \
  --env PYTHONUNBUFFERED=1 \
  "$IMAGE" "${ARGS[@]}" "${EXTRA[@]}" >/dev/null

echo "Starting server..."
for _ in $(seq 1 150); do
  if ! "${DOCKER[@]}" ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "The server stopped unexpectedly:" >&2
    "${DOCKER[@]}" logs --tail 40 "$CONTAINER" >&2 || true
    exit 1
  fi
  if "${DOCKER[@]}" logs "$CONTAINER" 2>&1 | grep -q '^Serving'; then
    "${DOCKER[@]}" logs "$CONTAINER" 2>&1 | grep -E '^(Service |Serving|SKIP|BUILD FAIL)' \
      | sed -e "s#0.0.0.0:8808#$BIND:$PORT#" -e "s#0.0.0.0:#$BIND:#g"
    if [[ -n "$BLIND" ]]; then
      mkdir -p .netlab
      "${DOCKER[@]}" exec "$CONTAINER" cat /tmp/mapping.json > .netlab/mapping.json
      echo "Answer key: .netlab/mapping.json (do not give it to the scanner)"
    fi
    echo "Ready on $BIND (HTTP :$PORT)   (./run.sh logs | ./run.sh stop)"
    exit 0
  fi
  sleep 1
done
echo "Still starting; follow progress with ./run.sh logs"
