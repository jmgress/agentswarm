from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Agent, AgentCreate
from providers.registry import provider_registry
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AgentSwarm API", version="1.0.0")

# In-memory storage for agents (in production, this would be a database)
agents_storage: List[Agent] = []

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/agents", response_model=Agent)
async def create_agent(agent_data: AgentCreate):
    """Create a new agent"""
    # Check if agent with same name already exists
    existing_agent = next((agent for agent in agents_storage if agent.name == agent_data.name), None)
    if existing_agent:
        raise HTTPException(status_code=400, detail="Agent with this name already exists")
    
    # Create new agent
    try:
        new_agent = Agent.from_create(agent_data)
        agents_storage.append(new_agent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return new_agent


@app.get("/agents", response_model=List[Agent])
async def get_agents():
    """Get all agents"""
    return agents_storage


@app.get("/providers", response_model=List[str])
async def get_providers():
    """Get all available providers"""
    return provider_registry.list_providers()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)