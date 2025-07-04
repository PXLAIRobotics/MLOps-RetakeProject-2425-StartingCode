#!/bin/bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Build the MLOps Devbox Docker Image
# -----------------------------------------------------------------------------

# === Configurable Parameters ===
IMAGE_NAME="pxl_mlops_devbox"
DOCKERFILE_PATH="."                 # Can be changed to a relative path
LABEL="source=pxl_mlops_devbox"

USERNAME="user"
USER_UID="1000"
USER_GID="1000"
USER_PASSWORD="pxl"

# === Optional: override via environment ===
: "${USERNAME:=user}"
: "${USER_UID:=1000}"
: "${USER_GID:=1000}"
: "${USER_PASSWORD:=pxl}"

# === Build ===
echo "🔧 Building Docker image: $IMAGE_NAME"
echo "👤 User: $USERNAME (UID: $USER_UID, GID: $USER_GID)"

docker build \
  --label "$LABEL" \
  --build-arg USERNAME="$USERNAME" \
  --build-arg USER_UID="$USER_UID" \
  --build-arg USER_GID="$USER_GID" \
  --build-arg USER_PASSWORD="$USER_PASSWORD" \
  -t "$IMAGE_NAME" \
  "$DOCKERFILE_PATH"

echo "✅ Image '$IMAGE_NAME' built successfully."
