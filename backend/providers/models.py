"""
Provider-specific models and configurations
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from .base import ProviderType, ProviderCapability, ProviderStatus


class ProviderInfo(BaseModel):
    """Information about a provider instance"""
    provider_id: str
    provider_type: ProviderType
    name: str
    description: str
    config: Dict[str, Any]
    default_model: Optional[str] = None


class ProviderCreate(BaseModel):
    """Model for creating a new provider instance"""
    provider_id: str
    provider_type: ProviderType
    name: str
    description: str
    config: Dict[str, Any]


class ProviderListResponse(BaseModel):
    """Response model for listing providers"""
    providers: List[ProviderInfo]
    total: int


class ProviderHealthResponse(BaseModel):
    """Response model for provider health check"""
    provider_id: str
    status: ProviderStatus


class ChatRequest(BaseModel):
    """Request model for chat completion"""
    provider_id: str
    messages: List[Dict[str, str]]
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: bool = False