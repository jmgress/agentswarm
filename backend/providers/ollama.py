"""
Ollama Provider Implementation
"""
import asyncio
from typing import List, AsyncIterator, Dict, Any
from .base import (
    BaseProvider, 
    ProviderType, 
    ProviderCapability,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    ProviderStatus
)
import httpx


class OllamaProvider(BaseProvider):
    """Ollama provider for local AI model inference"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.timeout = config.get("timeout", 30.0)
    
    def get_provider_type(self) -> ProviderType:
        return ProviderType.OLLAMA
    
    def get_capabilities(self) -> List[ProviderCapability]:
        return [
            ProviderCapability.CHAT_COMPLETION,
            ProviderCapability.STREAMING
        ]
    
    def validate_config(self) -> bool:
        """Validate Ollama configuration"""
        required_fields = []  # Ollama has minimal config requirements
        return all(field in self.config for field in required_fields)
    
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """
        Perform chat completion using Ollama API
        """
        # Convert messages to Ollama format
        ollama_messages = []
        for msg in request.messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        payload = {
            "model": request.model,
            "messages": ollama_messages,
            "stream": False
        }
        
        # Add optional parameters
        if request.temperature is not None:
            payload["options"] = {"temperature": request.temperature}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                return ChatCompletionResponse(
                    message=ChatMessage(
                        role="assistant",
                        content=result["message"]["content"]
                    ),
                    model=request.model,
                    usage=result.get("usage", {}),
                    metadata={"provider": "ollama"}
                )
                
        except httpx.RequestError as e:
            raise Exception(f"Ollama connection error: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Ollama API error: {e.response.status_code} - {e.response.text}")
    
    async def stream_completion(self, request: ChatCompletionRequest) -> AsyncIterator[str]:
        """
        Stream chat completion responses from Ollama
        """
        ollama_messages = []
        for msg in request.messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        payload = {
            "model": request.model,
            "messages": ollama_messages,
            "stream": True
        }
        
        if request.temperature is not None:
            payload["options"] = {"temperature": request.temperature}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                import json
                                data = json.loads(line)
                                if "message" in data and "content" in data["message"]:
                                    yield data["message"]["content"]
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.RequestError as e:
            raise Exception(f"Ollama connection error: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Ollama API error: {e.response.status_code}")
    
    async def get_available_models(self) -> List[str]:
        """
        Get list of available models from Ollama
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                
                result = response.json()
                models = []
                
                if "models" in result:
                    for model in result["models"]:
                        models.append(model["name"])
                
                return models
                
        except httpx.RequestError:
            return []  # Return empty list if Ollama is not available
        except httpx.HTTPStatusError:
            return []
    
    async def health_check(self) -> ProviderStatus:
        """
        Check Ollama server health and availability
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                
                models = await self.get_available_models()
                
                return ProviderStatus(
                    available=True,
                    models=models,
                    capabilities=self.get_capabilities()
                )
                
        except httpx.RequestError as e:
            return ProviderStatus(
                available=False,
                error=f"Connection error: {e}"
            )
        except httpx.HTTPStatusError as e:
            return ProviderStatus(
                available=False,
                error=f"HTTP error: {e.response.status_code}"
            )