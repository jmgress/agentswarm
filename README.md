# AgentSwarm

Generative AI system to build an agent swarm for task and problem solving.

This is a full-stack application with a FastAPI backend and React frontend.

## Project Structure

```
agentswarm/
├── backend/          # FastAPI backend application
│   ├── main.py       # Main FastAPI application with health endpoint
│   └── requirements.txt # Python dependencies
├── frontend/         # React frontend application
│   ├── src/          # React source code
│   ├── public/       # Static assets
│   └── package.json  # Node.js dependencies
└── README.md         # This file
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Getting Started

### Backend (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
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

## Features

### Backend
- ✅ FastAPI application with basic structure
- ✅ `/health` endpoint that returns `{"status": "ok"}`
- ✅ CORS enabled for frontend communication
- ✅ Auto-generated API documentation

### Frontend
- ✅ React application built with Vite and TypeScript
- ✅ Health check integration with backend
- ✅ Real-time status display
- ✅ Error handling for backend connectivity issues

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

### Frontend
- React 18 - UI library
- TypeScript - Type-safe JavaScript
- Vite - Fast build tool and development server
