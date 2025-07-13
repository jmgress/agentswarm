from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sqlite3

DB_PATH = os.environ.get("AGENTSWARM_DB", os.path.join(os.path.dirname(__file__), "agents.db"))

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        agent_type TEXT NOT NULL,
        description TEXT,
        mcp_url TEXT,
        metadata TEXT
    )
    """
)
conn.commit()

class AgentCreate(BaseModel):
    name: str
    agent_type: str
    description: str | None = None
    mcp_url: str | None = None
    metadata: str | None = None

class Agent(AgentCreate):
    id: int

app = FastAPI(title="AgentSwarm API", version="1.0.0")

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
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    cur = conn.execute(
        "INSERT INTO agents (name, agent_type, description, mcp_url, metadata) VALUES (?, ?, ?, ?, ?)",
        (agent.name, agent.agent_type, agent.description, agent.mcp_url, agent.metadata),
    )
    conn.commit()
    agent_id = cur.lastrowid
    return {"id": agent_id, **agent.model_dump()}


@app.get("/agents", response_model=list[Agent])
async def list_agents():
    """List all agents"""
    cur = conn.execute(
        "SELECT id, name, agent_type, description, mcp_url, metadata FROM agents"
    )
    rows = cur.fetchall()
    return [Agent(**dict(row)) for row in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)