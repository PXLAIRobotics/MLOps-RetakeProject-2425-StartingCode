#!/bin/bash

# ----------------------------
# Configurable variables
# ----------------------------
IMAGE_NAME="pxl_mlops_devbox"
CONTAINER_NAME="$IMAGE_NAME"

# ----------------------------
# Check if container exists
# ----------------------------
if docker ps -a --format '{{.Names}}' | grep -wq "$CONTAINER_NAME"; then
    echo "Stopping and removing container: $CONTAINER_NAME"
    docker rm -f "$CONTAINER_NAME"
else
    echo "No container named $CONTAINER_NAME found."
fi

# ----------------------------
# Check if image exists
# ----------------------------
if docker images --format '{{.Repository}}' | grep -wq "$IMAGE_NAME"; then
    echo "Removing image: $IMAGE_NAME"
    docker rmi "$IMAGE_NAME"
else
    echo "No image named $IMAGE_NAME found."
fi
