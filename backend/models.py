from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
import uuid


class MCPConnectionInfo(BaseModel):
    """Model for MCP connection information"""
    endpoint_url: str
    metadata: Optional[dict] = None


class AgentCreate(BaseModel):
    """Model for creating a new agent"""
    name: str
    agent_type: Literal["utility", "task", "orchestration"]
    description: str
    mcp_connection: MCPConnectionInfo


class Agent(BaseModel):
    """Model representing an agent in the system"""
    id: str
    name: str
    agent_type: Literal["utility", "task", "orchestration"]
    description: str
    mcp_connection: MCPConnectionInfo
    created_at: datetime
    
    @classmethod
    def from_create(cls, agent_data: AgentCreate) -> "Agent":
        """Create an Agent instance from AgentCreate data"""
        return cls(
            id=str(uuid.uuid4()),
            name=agent_data.name,
            agent_type=agent_data.agent_type,
            description=agent_data.description,
            mcp_connection=agent_data.mcp_connection,
            created_at=datetime.utcnow()
        )