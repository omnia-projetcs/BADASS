#!/usr/bin/env bash
# Uninstall the BADASS micro-server: stop the container, remove images and generated files.
#   ./uninstall.sh          asks for confirmation
#   ./uninstall.sh -y       no prompt
#   ./uninstall.sh --purge  also delete this repository directory
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
source docker/common.sh

YES=""; PURGE=""
for arg in "$@"; do
  case "$arg" in
    -h|--help) sed -n '2,5p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -y|--yes) YES=1 ;;
    --purge) PURGE=1 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

echo "This will remove:"
echo "  - container $CONTAINER"
echo "  - images $IMAGE and $BASE_IMAGE"
echo "  - generated files: .netlab/ .build/"
[[ -n "$PURGE" ]] && echo "  - THE WHOLE DIRECTORY $ROOT"
if [[ -z "$YES" ]]; then
  read -r -p "Continue? [y/N] " answer
  [[ "$answer" =~ ^[yYoO]$ ]] || { echo "Cancelled."; exit 0; }
fi

require_docker

"${DOCKER[@]}" rm -f "$CONTAINER" >/dev/null 2>&1 && echo "Container removed." || true
for image in "$IMAGE" "$BASE_IMAGE"; do
  "${DOCKER[@]}" image rm "$image" >/dev/null 2>&1 && echo "Image $image removed." || true
done
"${DOCKER[@]}" image prune -f --filter "dangling=true" >/dev/null || true
rm -rf .netlab .build
echo "Generated files removed."

if [[ -n "$PURGE" ]]; then
  cd ..
  rm -rf -- "$ROOT"
  echo "Directory $ROOT deleted."
fi
echo "Uninstall complete."
