import httpx
from typing import Any, Dict, List, Optional
from .base import BaseProvider

class OllamaProvider(BaseProvider):
    """
    Ollama provider for local model inference.
    """

    def __init__(self, model: str, endpoint_url: str = "http://localhost:11434"):
        self._model = model
        self._endpoint_url = endpoint_url
        self._client = httpx.AsyncClient(base_url=self._endpoint_url)

    @property
    def name(self) -> str:
        return "ollama"

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Generate a chat completion using the Ollama API.
        """
        try:
            response = await self._client.post(
                "/api/chat",
                json={"model": self._model, "messages": messages, **kwargs},
                timeout=60.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Ollama API error: {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Ollama connection error: {e}") from e

    async def stream_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Stream a chat completion using the Ollama API.
        """
        try:
            async with self._client.stream(
                "POST",
                "/api/chat",
                json={"model": self._model, "messages": messages, "stream": True, **kwargs},
                timeout=60.0,
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    yield chunk
        except httpx.HTTPStatusError as e:
            raise Exception(f"Ollama API error: {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Ollama connection error: {e}") from e

    def get_model_configuration(self) -> Dict[str, Any]:
        """
        Get the provider's model configuration.
        """
        return {"model": self._model, "endpoint_url": self._endpoint_url}

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the provider's capabilities.
        """
        return {"streaming": True}
