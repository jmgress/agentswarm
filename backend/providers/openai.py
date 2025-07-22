"""
OpenAI Provider Implementation
"""
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
import json


class OpenAIProvider(BaseProvider):
    """OpenAI provider for GPT models"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")
        self.timeout = config.get("timeout", 30.0)
        self.default_models = [
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"
        ]
    
    def get_provider_type(self) -> ProviderType:
        return ProviderType.OPENAI
    
    def get_capabilities(self) -> List[ProviderCapability]:
        return [
            ProviderCapability.CHAT_COMPLETION,
            ProviderCapability.STREAMING,
            ProviderCapability.FUNCTION_CALLING,
            ProviderCapability.TOOL_USE
        ]
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration"""
        return self.api_key is not None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """
        Perform chat completion using OpenAI API
        """
        # Convert messages to OpenAI format
        openai_messages = []
        for msg in request.messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        payload = {
            "model": request.model,
            "messages": openai_messages
        }
        
        # Add optional parameters
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                if "choices" not in result or not result["choices"]:
                    raise Exception("No response from OpenAI")
                
                choice = result["choices"][0]
                
                return ChatCompletionResponse(
                    message=ChatMessage(
                        role="assistant",
                        content=choice["message"]["content"]
                    ),
                    model=result["model"],
                    usage=result.get("usage", {}),
                    metadata={"provider": "openai", "finish_reason": choice.get("finish_reason")}
                )
                
        except httpx.RequestError as e:
            raise Exception(f"OpenAI connection error: {e}")
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_data = e.response.json()
                error_detail = error_data.get("error", {}).get("message", "")
            except:
                error_detail = e.response.text
            raise Exception(f"OpenAI API error: {e.response.status_code} - {error_detail}")
    
    async def stream_completion(self, request: ChatCompletionRequest) -> AsyncIterator[str]:
        """
        Stream chat completion responses from OpenAI
        """
        openai_messages = []
        for msg in request.messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        payload = {
            "model": request.model,
            "messages": openai_messages,
            "stream": True
        }
        
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]  # Remove "data: " prefix
                            
                            if data_str == "[DONE]":
                                break
                            
                            try:
                                data = json.loads(data_str)
                                
                                if "choices" in data and data["choices"]:
                                    choice = data["choices"][0]
                                    if "delta" in choice and "content" in choice["delta"]:
                                        yield choice["delta"]["content"]
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.RequestError as e:
            raise Exception(f"OpenAI connection error: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"OpenAI API error: {e.response.status_code}")
    
    async def get_available_models(self) -> List[str]:
        """
        Get list of available models from OpenAI
        """
        if not self.validate_config():
            return self.default_models  # Return default models if no API key
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                
                result = response.json()
                models = []
                
                if "data" in result:
                    for model in result["data"]:
                        # Filter for chat completion models
                        if "gpt" in model["id"].lower():
                            models.append(model["id"])
                
                return sorted(models) if models else self.default_models
                
        except (httpx.RequestError, httpx.HTTPStatusError):
            return self.default_models  # Return default models on error
    
    async def health_check(self) -> ProviderStatus:
        """
        Check OpenAI API health and availability
        """
        if not self.validate_config():
            return ProviderStatus(
                available=False,
                error="No API key configured"
            )
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self._get_headers()
                )
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
            error_detail = ""
            try:
                error_data = e.response.json()
                error_detail = error_data.get("error", {}).get("message", "")
            except:
                error_detail = str(e.response.status_code)
            
            return ProviderStatus(
                available=False,
                error=f"API error: {error_detail}"
            )