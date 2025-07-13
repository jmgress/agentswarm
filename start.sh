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

# Setup backend if needed
if [ ! -d "backend/venv" ]; then
    echo "🐍 Setting up backend virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Setup frontend if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo "✅ Setup complete!"
echo "🚀 Starting both backend and frontend..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both services"

# Start both services
npm start