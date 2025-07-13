#!/bin/bash

# Script to activate the correct virtual environment for AgentSwarm

# Change to the project root directory
cd "$(dirname "$0")"

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: .venv virtual environment not found."
    echo "Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt"
    exit 1
fi

# Activate the virtual environment
echo "🐍 Activating .venv virtual environment..."
source .venv/bin/activate

# Verify activation
if [ "$VIRTUAL_ENV" = "$(pwd)/.venv" ]; then
    echo "✅ Successfully activated .venv environment"
    echo "Python path: $(which python)"
else
    echo "❌ Failed to activate .venv environment"
    exit 1
fi

# Keep the shell open with the activated environment
exec "$SHELL"
