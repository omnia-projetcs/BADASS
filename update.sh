#!/usr/bin/env bash
# Update BADASS: pull the latest code, rebuild the Docker images, restart if it was running.
set -euo pipefail
cd "$(dirname "$0")"
source docker/common.sh

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  sed -n '2p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi

if [[ -d .git ]]; then
  if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
    echo "Local modifications detected; commit or stash them first:" >&2
    git status --short --untracked-files=no >&2
    exit 1
  fi
  echo "==> Pulling latest version..."
  git pull --ff-only
else
  echo "Not a git checkout: skipping code update."
fi

require_docker

WAS_RUNNING=""
if "${DOCKER[@]}" ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
  WAS_RUNNING=1
fi

build_images --pull
"${DOCKER[@]}" image prune -f --filter "dangling=true" >/dev/null || true

if [[ -n "$WAS_RUNNING" ]]; then
  echo "==> Restarting the server..."
  exec ./run.sh
fi
echo "Update complete. Start with ./run.sh"
