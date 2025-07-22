# AgentSwarm

Generative AI system to build an agent swarm for task and problem solving.

This is a full-stack application with a FastAPI backend and React frontend.

## Quick Start

### Easy Start (Recommended)
```bash
# Clone the repository
git clone https://github.com/jmgress/agentswarm.git
cd agentswarm

# Start both backend and frontend (with automatic port management)
npm start
# or
./start.sh
```

**✨ New Feature**: The start script now automatically checks for and shuts down any existing processes on ports 8000 (backend) and 5173 (frontend) before starting new services.

### Run Tests
```bash
# Run all tests
npm test
# or
./test.sh

# Run tests individually  
npm run test:backend
npm run test:frontend
```

## Available Scripts

### Root Level Commands
- `npm start` - Start both services with automatic port management and cleanup
- `npm run start:direct` - Start both services without port checking (legacy mode)
- `npm test` - Run all tests (backend + frontend)
- `npm run setup` - Install all dependencies for both services
- `npm run start:backend` - Start only the backend server (with port 8000 check)
- `npm run start:frontend` - Start only the frontend server (with port 5173 check)
- `npm run test:backend` - Run only backend tests
- `npm run test:frontend` - Run only frontend tests

### Port Management
The application uses intelligent port management:
- **Backend**: Port 8000 (FastAPI server)
- **Frontend**: Port 5173 (Vite dev server)
- **Auto-cleanup**: Existing processes are gracefully terminated before starting
- **Manual port check**: Use `./scripts/check-port.sh <port> <service_name>`

### Shell Scripts
- `./start.sh` - Interactive startup with dependency checking and installation
- `./test.sh` - Run tests with detailed output and summary

## Project Structure

```
agentswarm/
├── backend/          # FastAPI backend application
│   ├── main.py       # Main FastAPI application with health endpoint
│   ├── models.py     # Pydantic models for agents and providers
│   ├── providers/    # AI provider implementations
│   │   ├── base.py   # Base provider class
│   │   ├── ollama.py # Ollama provider
│   │   ├── openai.py # OpenAI provider
│   │   ├── gemini.py # Gemini provider
│   │   └── registry.py # Provider registry
│   ├── requirements.txt # Python dependencies
│   └── tests/        # Backend tests (pytest)
├── frontend/         # React frontend application
│   ├── src/          # React source code
│   │   └── test/     # Frontend tests (vitest)
│   ├── public/       # Static assets
│   └── package.json  # Node.js dependencies
├── .env.example      # Example environment variables file
├── package.json      # Root package.json with coordinated scripts
├── start.sh          # Enhanced startup script
├── test.sh           # Enhanced testing script
└── README.md         # This file
```

## Providers

This application uses a provider-based architecture to connect to different AI models. The following providers are currently supported:

- **Ollama**: For local model inference.
- **OpenAI**: For GPT models.
- **Gemini**: For Google's Gemini models.

### Configuration

To use a provider, you need to create a `.env` file from the `.env.example` file and fill in the required API keys.

### Adding a New Provider

To add a new provider, you need to:

1. Create a new provider class in the `backend/providers` directory that inherits from `BaseProvider`.
2. Implement the required methods in the new provider class.
3. Register the new provider in the `ProviderRegistry` in `backend/providers/registry.py`.

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Manual Setup (if needed)

### Backend (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   **On macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **On Windows (Command Prompt):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   **On Windows (PowerShell):**
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

   You should see `(venv)` at the beginning of your command prompt when the virtual environment is active.

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   python main.py
   ```

The backend will start on `http://localhost:8000`

- Health endpoint: `http://localhost:8000/health`
- API documentation: `http://localhost:8000/docs`

### Frontend (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm run dev
   ```

The frontend will start on `http://localhost:5173`

## Testing

### Backend Tests
- **Framework**: pytest
- **Coverage**: FastAPI application setup and health endpoint
- **Command**: `npm run test:backend` or `cd backend && python -m pytest tests/ -v`

### Frontend Tests  
- **Framework**: vitest with @testing-library/react
- **Coverage**: React component rendering and functionality
- **Command**: `npm run test:frontend` or `cd frontend && npm test`

### Test Examples
```bash
# Quick test run
npm test

# Detailed test output with setup
./test.sh

# Individual service tests
npm run test:backend
npm run test:frontend
```

## Features

### Backend
- ✅ FastAPI application with basic structure
- ✅ `/health` endpoint that returns `{"status": "ok"}`
- ✅ CORS enabled for frontend communication
- ✅ Auto-generated API documentation
- ✅ pytest test suite with health endpoint testing

### Frontend
- ✅ React application built with Vite and TypeScript
- ✅ Health check integration with backend
- ✅ Real-time status display
- ✅ Error handling for backend connectivity issues
- ✅ vitest test suite with component testing

## Development

Both the backend and frontend can be run independently:

1. **Backend only**: Start the FastAPI server and test endpoints using the auto-generated docs at `/docs`
2. **Frontend only**: The React app will show connection errors if the backend is not running
3. **Full stack**: Start both servers to test the complete application

## API Endpoints

### Health Check
- **GET** `/health`
  - Returns: `{"status": "ok"}`
  - Purpose: Verify backend is running and accessible

## Technology Stack

### Backend
- FastAPI - Modern, fast web framework for building APIs
- Uvicorn - ASGI server for running FastAPI
- CORS middleware for cross-origin requests
- pytest - Testing framework
- httpx - HTTP client for testing

### Frontend
- React 18 - UI library
- TypeScript - Type-safe JavaScript
- Vite - Fast build tool and development server
- vitest - Testing framework
- @testing-library/react - React testing utilities
