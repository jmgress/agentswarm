from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
import uuid


from providers.base import BaseProvider
from providers.registry import provider_registry


class ProviderConfig(BaseModel):
    """Model for provider configuration"""
    name: str
    settings: Optional[Dict[str, Any]] = {}


class AgentCreate(BaseModel):
    """Model for creating a new agent"""
    name: str
    agent_type: Literal["utility", "task", "orchestration"]
    description: str
    provider_config: ProviderConfig


class Agent(BaseModel):
    """Model representing an agent in the system"""
    id: str
    name: str
    agent_type: Literal["utility", "task", "orchestration"]
    description: str
    provider_config: ProviderConfig
    created_at: datetime
    provider: Optional[BaseProvider] = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_create(cls, agent_data: AgentCreate) -> "Agent":
        """Create an Agent instance from AgentCreate data"""
        agent = cls(
            id=str(uuid.uuid4()),
            name=agent_data.name,
            agent_type=agent_data.agent_type,
            description=agent_data.description,
            provider_config=agent_data.provider_config,
            created_at=datetime.utcnow()
        )
        agent.provider = provider_registry.get_provider(
            name=agent.provider_config.name,
            **agent.provider_config.settings
        )
        return agent