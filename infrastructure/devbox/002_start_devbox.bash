#!/bin/bash

# ----------------------------
# Configuration Variables
# ----------------------------
IMAGE_NAME="pxl_mlops_devbox"
CONTAINER_NAME="$IMAGE_NAME"
HOSTNAME="$CONTAINER_NAME"

# Define volumes as an array of HOST:CONTAINER mappings
VOLUMES=(
    "$(realpath ../../data):/data"
    "$(realpath ../../scripts):/scripts"
    "$(realpath ../../commands):/commands"
    "$(realpath ../../config):/config"
)

# ----------------------------
# Build docker run command
# ----------------------------
DOCKER_RUN_CMD=(docker run --rm -it \
  --name "$CONTAINER_NAME" \
  --hostname "$HOSTNAME"
)

# Add all volumes to the command
for VOLUME in "${VOLUMES[@]}"; do
  DOCKER_RUN_CMD+=(-v "$VOLUME")
done

# Add image name at the end
DOCKER_RUN_CMD+=("$IMAGE_NAME")

# ----------------------------
# Execute
# ----------------------------
"${DOCKER_RUN_CMD[@]}"
