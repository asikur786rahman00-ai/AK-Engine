#!/usr/bin/env bash
set -e
# Activate virtual environment if present
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
# Ensure DISCORD_TOKEN is set
if [ -z "$DISCORD_TOKEN" ]; then
  echo "Error: DISCORD_TOKEN environment variable not set."
  exit 1
fi
python "$(dirname "$0")/main.py"
