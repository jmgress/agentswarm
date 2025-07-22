"""
Gemini Provider Implementation
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


class GeminiProvider(BaseProvider):
    """Gemini provider for Google's AI models"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://generativelanguage.googleapis.com/v1")
        self.timeout = config.get("timeout", 30.0)
        self.safety_settings = config.get("safety_settings", {})
        self.default_models = [
            "gemini-pro", "gemini-pro-vision"
        ]
    
    def get_provider_type(self) -> ProviderType:
        return ProviderType.GEMINI
    
    def get_capabilities(self) -> List[ProviderCapability]:
        return [
            ProviderCapability.CHAT_COMPLETION,
            ProviderCapability.STREAMING,
            ProviderCapability.SAFETY_SETTINGS
        ]
    
    def validate_config(self) -> bool:
        """Validate Gemini configuration"""
        return self.api_key is not None
    
    def _convert_role(self, role: str) -> str:
        """Convert standard role to Gemini role format"""
        role_mapping = {
            "user": "user",
            "assistant": "model",
            "system": "user"  # Gemini doesn't have system role, use user
        }
        return role_mapping.get(role, "user")
    
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """
        Perform chat completion using Gemini API
        """
        # Convert messages to Gemini format
        contents = []
        for msg in request.messages:
            contents.append({
                "role": self._convert_role(msg.role),
                "parts": [{"text": msg.content}]
            })
        
        # If first message is system, combine with first user message
        if contents and request.messages[0].role == "system":
            system_msg = contents.pop(0)
            if contents and contents[0]["role"] == "user":
                contents[0]["parts"].insert(0, system_msg["parts"][0])
        
        payload = {
            "contents": contents
        }
        
        # Add generation config
        generation_config = {}
        if request.temperature is not None:
            generation_config["temperature"] = request.temperature
        if request.max_tokens is not None:
            generation_config["maxOutputTokens"] = request.max_tokens
            
        if generation_config:
            payload["generationConfig"] = generation_config
        
        # Add safety settings
        if self.safety_settings:
            payload["safetySettings"] = self.safety_settings
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/models/{request.model}:generateContent",
                    params={"key": self.api_key},
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                if "candidates" not in result or not result["candidates"]:
                    error_msg = "No response from Gemini"
                    if "promptFeedback" in result:
                        feedback = result["promptFeedback"]
                        if "blockReason" in feedback:
                            error_msg = f"Content blocked: {feedback['blockReason']}"
                    raise Exception(error_msg)
                
                candidate = result["candidates"][0]
                content = candidate["content"]["parts"][0]["text"]
                
                return ChatCompletionResponse(
                    message=ChatMessage(
                        role="assistant",
                        content=content
                    ),
                    model=request.model,
                    usage=result.get("usageMetadata", {}),
                    metadata={
                        "provider": "gemini",
                        "finish_reason": candidate.get("finishReason"),
                        "safety_ratings": candidate.get("safetyRatings", [])
                    }
                )
                
        except httpx.RequestError as e:
            raise Exception(f"Gemini connection error: {e}")
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_data = e.response.json()
                error_detail = error_data.get("error", {}).get("message", "")
            except:
                error_detail = e.response.text
            raise Exception(f"Gemini API error: {e.response.status_code} - {error_detail}")
    
    async def stream_completion(self, request: ChatCompletionRequest) -> AsyncIterator[str]:
        """
        Stream chat completion responses from Gemini
        """
        contents = []
        for msg in request.messages:
            contents.append({
                "role": self._convert_role(msg.role),
                "parts": [{"text": msg.content}]
            })
        
        # Handle system messages
        if contents and request.messages[0].role == "system":
            system_msg = contents.pop(0)
            if contents and contents[0]["role"] == "user":
                contents[0]["parts"].insert(0, system_msg["parts"][0])
        
        payload = {
            "contents": contents
        }
        
        # Add generation config
        generation_config = {}
        if request.temperature is not None:
            generation_config["temperature"] = request.temperature
        if request.max_tokens is not None:
            generation_config["maxOutputTokens"] = request.max_tokens
            
        if generation_config:
            payload["generationConfig"] = generation_config
        
        if self.safety_settings:
            payload["safetySettings"] = self.safety_settings
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/models/{request.model}:streamGenerateContent",
                    params={"key": self.api_key},
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                
                                if "candidates" in data and data["candidates"]:
                                    candidate = data["candidates"][0]
                                    if "content" in candidate and "parts" in candidate["content"]:
                                        for part in candidate["content"]["parts"]:
                                            if "text" in part:
                                                yield part["text"]
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.RequestError as e:
            raise Exception(f"Gemini connection error: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Gemini API error: {e.response.status_code}")
    
    async def get_available_models(self) -> List[str]:
        """
        Get list of available models from Gemini
        """
        if not self.validate_config():
            return self.default_models  # Return default models if no API key
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    params={"key": self.api_key}
                )
                response.raise_for_status()
                
                result = response.json()
                models = []
                
                if "models" in result:
                    for model in result["models"]:
                        # Extract model name from full name (e.g., "models/gemini-pro" -> "gemini-pro")
                        model_name = model["name"].split("/")[-1]
                        # Filter for text generation models
                        if "gemini" in model_name.lower():
                            models.append(model_name)
                
                return models if models else self.default_models
                
        except (httpx.RequestError, httpx.HTTPStatusError):
            return self.default_models  # Return default models on error
    
    async def health_check(self) -> ProviderStatus:
        """
        Check Gemini API health and availability
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
                    params={"key": self.api_key}
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