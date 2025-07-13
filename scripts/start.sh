#!/bin/bash
set -e

# Start the FastAPI backend
(
  cd "$(dirname "$0")/../backend" && uvicorn main:app --reload
) &
BACKEND_PID=$!

# Start the React frontend
(
  cd "$(dirname "$0")/../frontend" && npm run dev
) &
FRONTEND_PID=$!

trap 'kill $BACKEND_PID $FRONTEND_PID' EXIT

wait $BACKEND_PID $FRONTEND_PID
