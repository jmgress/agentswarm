from pydantic import BaseModel, Field
from typing import Optional

class McpConnection(BaseModel):
    """MCP connection information."""
    endpoint: str = Field(..., description="The endpoint URL of the MCP.")
    metadata: Optional[dict] = Field(None, description="Metadata for the MCP connection.")

class Agent(BaseModel):
    """Represents an agent in the system."""
    name: str = Field(..., description="The name of the agent.")
    type: str = Field(..., description="The type of the agent (e.g., utility, task, orchestration).")
    description: str = Field(..., description="A description of the agent's purpose.")
    mcp_connection: McpConnection = Field(..., description="MCP connection information.")
