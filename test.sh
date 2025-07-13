#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# --- Backend Setup ---
echo "Setting up backend for testing..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# No backend tests to run yet, but this is where they would go
echo "No backend tests found."
cd ..

# --- Frontend Setup ---
echo "Setting up frontend for testing..."
cd frontend
npm install
npm run lint
echo "Frontend linting complete."
cd ..

echo "All tests passed!"
