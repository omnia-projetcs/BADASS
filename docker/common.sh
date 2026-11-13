#!/usr/bin/env bash
# Shared settings for run.sh / update.sh / uninstall.sh.
BASE_IMAGE="${BASE_IMAGE:-badass-lab:local}"
IMAGE="${IMAGE:-badass-server:local}"
CONTAINER="${CONTAINER:-badass-server}"
PORT="${PORT:-8808}"
BIND="${BIND:-127.0.0.1}"

require_docker() {
  if [[ -n "${DOCKER[*]:-}" ]]; then
    return 0
  fi
  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed (https://docs.docker.com/engine/install/)." >&2
    exit 1
  fi
  if docker info >/dev/null 2>&1; then
    DOCKER=(docker)
    DOCKER_BUILD=(env DOCKER_BUILDKIT=1 docker)
  else
    echo "Docker requires elevated rights for $(id -un); using sudo." >&2
    echo "(Tip: 'sudo usermod -aG docker $(id -un)' then log out/in to avoid sudo.)" >&2
    DOCKER=(sudo docker)
    DOCKER_BUILD=(sudo env DOCKER_BUILDKIT=1 docker)
    "${DOCKER[@]}" info >/dev/null || { echo "Cannot reach the Docker daemon." >&2; exit 1; }
  fi
}

build_images() {
  require_docker
  echo "==> Building runtime image $BASE_IMAGE (all 14 technologies)..."
  "${DOCKER_BUILD[@]}" build "$@" -t "$BASE_IMAGE" .
  echo "==> Building server image $IMAGE..."
  "${DOCKER_BUILD[@]}" build --build-arg BASE="$BASE_IMAGE" \
    -f docker/server.Dockerfile -t "$IMAGE" .
}
