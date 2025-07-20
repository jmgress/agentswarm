from pydantic import BaseModel
from typing import Optional, Literal, List
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


class MessageCreate(BaseModel):
    """Model for creating a new message"""
    content: str
    enabled_agents: List[str] = []  # List of agent IDs that should process this message


class Message(BaseModel):
    """Model representing a message in a chat"""
    id: str
    content: str
    sender: Literal["user", "assistant"]
    created_at: datetime
    enabled_agents: List[str] = []  # Agent IDs that were enabled for this message


class ChatCreate(BaseModel):
    """Model for creating a new chat"""
    title: Optional[str] = None


class Chat(BaseModel):
    """Model representing a chat conversation"""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
    
    @classmethod
    def from_create(cls, chat_data: ChatCreate) -> "Chat":
        """Create a Chat instance from ChatCreate data"""
        now = datetime.utcnow()
        return cls(
            id=str(uuid.uuid4()),
            title=chat_data.title or "New Chat",
            created_at=now,
            updated_at=now,
            messages=[]
        )