#!/bin/bash

echo "🧪 Running AgentSwarm Tests..."
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: No package.json found. Are you in the root directory?"
    exit 1
fi

# Setup backend testing using existing .venv
echo "🐍 Setting up backend tests..."
if [ ! -d ".venv" ]; then
    echo "❌ Error: .venv virtual environment not found. Run setup first."
    echo "To create it: python3 -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt"
    exit 1
fi

# Use the existing .venv instead of creating venv
source .venv/bin/activate

# Check if requirements are installed
echo "Checking backend dependencies..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing backend requirements..."
    pip install -r backend/requirements.txt > /dev/null
fi

echo "Running backend tests..."
python -m pytest backend/tests/ --tb=short
backend_result=$?

# Setup frontend testing if needed  
echo ""
echo "⚛️ Setting up frontend tests..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install > /dev/null
fi

echo "Running frontend tests..."
npm test
frontend_result=$?

cd ..

echo ""
echo "📊 Test Results Summary:"
if [ $backend_result -eq 0 ]; then
    echo "✅ Backend tests: PASSED"
else
    echo "❌ Backend tests: FAILED"
fi

if [ $frontend_result -eq 0 ]; then
    echo "✅ Frontend tests: PASSED"
else
    echo "❌ Frontend tests: FAILED"
fi

# Exit with error if any tests failed
if [ $backend_result -ne 0 ] || [ $frontend_result -ne 0 ]; then
    echo ""
    echo "❌ Some tests failed. Please check the output above."
    exit 1
else
    echo ""
    echo "🎉 All tests passed!"
    exit 0
fi