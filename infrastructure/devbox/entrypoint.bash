#!/bin/bash
set -e

source /env_vars

# Default to bash login shell
if [ $# -eq 0 ]; then
  set -- bash -l
fi

# Set HOME explicitly and cd to it
export HOME="/home/$USERNAME"
cd "$HOME"

# Exec user shell with correct env and working directory
exec gosu "$USERNAME" env HOME="$HOME" "$@"
