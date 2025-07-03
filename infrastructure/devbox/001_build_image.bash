#!/bin/bash

docker build \
  --label source=pxl_mlops_devbox \
  --build-arg USERNAME=user \
  --build-arg USER_UID=1000 \
  --build-arg USER_GID=1000 \
  --build-arg USER_PASSWORD=pxl \
  -t pxl_mlops_devbox .
