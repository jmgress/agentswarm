#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# --- Backend Setup ---
echo "Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# --- Frontend Setup ---
echo "Setting up frontend..."
cd frontend
npm install
cd ..

# --- Start Servers ---
echo "Starting servers..."

# Start backend in the background
echo "Starting backend server..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Start frontend in the background
echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes to complete
wait $BACKEND_PID
wait $FRONTEND_PID
