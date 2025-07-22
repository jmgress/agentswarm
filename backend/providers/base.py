"""
Base Provider Abstract Class for AI Model Integration
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, AsyncIterator, Any
from pydantic import BaseModel
from enum import Enum


class ProviderType(str, Enum):
    """Supported AI provider types"""
    OLLAMA = "ollama"
    OPENAI = "openai"
    GEMINI = "gemini"


class ProviderCapability(str, Enum):
    """Provider capability types"""
    CHAT_COMPLETION = "chat_completion"
    STREAMING = "streaming"
    FUNCTION_CALLING = "function_calling"
    TOOL_USE = "tool_use"
    SAFETY_SETTINGS = "safety_settings"


class ChatMessage(BaseModel):
    """Standard chat message format"""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatCompletionRequest(BaseModel):
    """Standard request format for chat completion"""
    messages: List[ChatMessage]
    model: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: bool = False
    metadata: Optional[Dict[str, Any]] = None


class ChatCompletionResponse(BaseModel):
    """Standard response format for chat completion"""
    message: ChatMessage
    model: str
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class ProviderStatus(BaseModel):
    """Provider health status"""
    available: bool
    error: Optional[str] = None
    models: List[str] = []
    capabilities: List[ProviderCapability] = []


class BaseProvider(ABC):
    """
    Abstract base class for AI providers.
    All AI providers must implement this interface.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize provider with configuration"""
        self.config = config
        self._provider_type = self.get_provider_type()
    
    @property
    def provider_type(self) -> ProviderType:
        """Get the provider type"""
        return self._provider_type
    
    @abstractmethod
    def get_provider_type(self) -> ProviderType:
        """Return the provider type"""
        pass
    
    @abstractmethod
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """
        Perform chat completion using the provider's API
        
        Args:
            request: Chat completion request
            
        Returns:
            Chat completion response
        """
        pass
    
    @abstractmethod
    async def stream_completion(self, request: ChatCompletionRequest) -> AsyncIterator[str]:
        """
        Stream chat completion responses
        
        Args:
            request: Chat completion request with stream=True
            
        Yields:
            Streamed response chunks
        """
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """
        Get list of available models for this provider
        
        Returns:
            List of model names
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> ProviderStatus:
        """
        Check provider health and availability
        
        Returns:
            Provider status information
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[ProviderCapability]:
        """
        Get list of capabilities supported by this provider
        
        Returns:
            List of supported capabilities
        """
        pass
    
    def get_default_model(self) -> Optional[str]:
        """
        Get the default model for this provider
        
        Returns:
            Default model name or None
        """
        return self.config.get("default_model")
    
    def validate_config(self) -> bool:
        """
        Validate provider configuration
        
        Returns:
            True if configuration is valid
        """
        return True