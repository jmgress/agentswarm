from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any
from datetime import datetime
import uuid


class MCPConnectionInfo(BaseModel):
    """Model for MCP connection information"""
    endpoint_url: str
    metadata: Optional[dict] = None


class ProviderConfig(BaseModel):
    """Model for AI provider configuration"""
    provider_id: str
    provider_type: Literal["ollama", "openai", "gemini"]
    model: str
    config: Optional[Dict[str, Any]] = None
    fallback_providers: Optional[list[str]] = []


class AgentCreate(BaseModel):
    """Model for creating a new agent"""
    name: str
    agent_type: Literal["utility", "task", "orchestration"]
    description: str
    mcp_connection: MCPConnectionInfo
    provider_config: Optional[ProviderConfig] = None


class Agent(BaseModel):
    """Model representing an agent in the system"""
    id: str
    name: str
    agent_type: Literal["utility", "task", "orchestration"]
    description: str
    mcp_connection: MCPConnectionInfo
    provider_config: Optional[ProviderConfig] = None
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
            provider_config=agent_data.provider_config,
            created_at=datetime.utcnow()
        )