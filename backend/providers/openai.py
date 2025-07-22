import os
from openai import AsyncOpenAI
from typing import Any, Dict, List
from .base import BaseProvider

class OpenAIProvider(BaseProvider):
    """
    OpenAI provider for GPT models.
    """

    def __init__(self, model: str, api_key: str = None):
        self._model = model
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError("OpenAI API key not provided. Set it in the OPENAI_API_KEY environment variable.")
        self._client = AsyncOpenAI(api_key=self._api_key)

    @property
    def name(self) -> str:
        return "openai"

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Generate a chat completion using the OpenAI API.
        """
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                **kwargs,
            )
            return response.model_dump()
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}") from e

    async def stream_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Stream a chat completion using the OpenAI API.
        """
        try:
            stream = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                stream=True,
                **kwargs,
            )
            async for chunk in stream:
                yield chunk.model_dump_json()
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}") from e

    def get_model_configuration(self) -> Dict[str, Any]:
        """
        Get the provider's model configuration.
        """
        return {"model": self._model}

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the provider's capabilities.
        """
        return {"streaming": True, "function_calling": True, "tool_use": True}
