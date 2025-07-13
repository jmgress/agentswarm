#!/bin/bash

echo "🧪 Running AgentSwarm Tests..."
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: No package.json found. Are you in the root directory?"
    exit 1
fi

# Setup backend testing if needed
echo "🐍 Setting up backend tests..."
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r backend/requirements.txt > /dev/null

echo "Running backend tests..."
python -m pytest backend/tests/ -v
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