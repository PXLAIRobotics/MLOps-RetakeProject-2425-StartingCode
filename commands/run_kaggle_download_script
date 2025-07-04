#!/bin/bash

# Check if a Python script filename was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <python_script.py>"
  exit 1
fi

SCRIPT_NAME="$1"

# Ensure the specified script exists
if [ ! -f "$SCRIPT_NAME" ]; then
  echo "Error: Python script '$SCRIPT_NAME' not found."
  exit 1
fi

# Ensure Kaggle token exists
if [ ! -f /config/kaggle/kaggle.json ]; then
  echo "Error: /config/kaggle/kaggle.json not found."
  exit 1
fi

# Fix permissions on the Kaggle API key
chmod 600 /config/kaggle/kaggle.json

# Set up Kaggle environment
export KAGGLE_CONFIG_DIR=/config/kaggle

# Run the specified Python script
python "$SCRIPT_NAME"
