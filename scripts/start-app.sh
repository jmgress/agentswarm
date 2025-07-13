#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting AgentSwarm Application...${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check required ports using our improved script
echo -e "${BLUE}� Checking required ports...${NC}"

if ! "$SCRIPT_DIR/check-port.sh" 8000 "FastAPI Backend"; then
    echo -e "${RED}❌ Failed to free port 8000${NC}"
    exit 1
fi

if ! "$SCRIPT_DIR/check-port.sh" 5173 "Vite Frontend"; then
    echo -e "${RED}❌ Failed to free port 5173${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎯 All ports are ready!${NC}"
echo -e "${BLUE}Starting services...${NC}"
echo ""

# Change to project root and start the application
cd "$PROJECT_ROOT"

# Start the application
npm run start
