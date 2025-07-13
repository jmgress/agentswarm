# Agent Swarm

This repository contains a FastAPI backend and a React frontend. The React app calls the backend `/health` endpoint to verify connectivity.

## Backend

Install dependencies and start the server:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

This starts FastAPI on `http://localhost:8000` with `/health` returning `{\"status\": \"ok\"}`.

## Frontend

Install dependencies and start the React development server:

```bash
cd frontend
npm install
npm start
```

The app runs on `http://localhost:3000` and displays the backend status.

## Folder Structure

- `backend/` – FastAPI application
- `frontend/` – React application
