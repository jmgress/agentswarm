#!/bin/bash

echo "🚀 Starting AgentSwarm..."

# Check if dependencies are installed
if [ ! -f "package.json" ]; then
    echo "❌ Error: No package.json found. Are you in the root directory?"
    exit 1
fi

# Install root dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing root dependencies..."
    npm install
fi

# Setup backend if needed (check for .venv instead of venv)
if [ ! -d ".venv" ]; then
    echo "🐍 Setting up Python virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements.txt
fi

# Setup frontend if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo "✅ Setup complete!"

# Check and kill processes on required ports before starting
echo "� Checking for processes using required ports..."

# Use our improved port checking
if [ -f "scripts/check-port.sh" ]; then
    scripts/check-port.sh 8000 "FastAPI Backend"
    scripts/check-port.sh 5173 "Vite Frontend"
else
    echo "⚠️  Port checking script not found, proceeding anyway..."
fi

echo ""
echo "�🚀 Starting both backend and frontend..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both services"

# Start both services using the direct method to avoid recursion
npm run start:direct