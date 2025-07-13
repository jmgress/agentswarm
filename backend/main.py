from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Agent

app = FastAPI(title="AgentSwarm API", version="1.0.0")

# In-memory database
agents_db: List[Agent] = []

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/agents", response_model=Agent, status_code=201)
async def create_agent(agent: Agent):
    """Creates a new agent."""
    agents_db.append(agent)
    return agent

@app.get("/agents", response_model=List[Agent])
async def get_agents():
    """Returns a list of all agents."""
    return agents_db

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)