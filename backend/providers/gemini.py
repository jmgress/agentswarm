import os
import google.generativeai as genai
from typing import Any, Dict, List
from .base import BaseProvider

class GeminiProvider(BaseProvider):
    """
    Google Gemini provider.
    """

    def __init__(self, model: str, api_key: str = None):
        self._model = model
        self._api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self._api_key:
            raise ValueError("Google API key not provided. Set it in the GOOGLE_API_KEY environment variable.")
        genai.configure(api_key=self._api_key)
        self._client = genai.GenerativeModel(self._model)

    @property
    def name(self) -> str:
        return "gemini"

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Generate a chat completion using the Gemini API.
        """
        try:
            # Gemini uses a different message format, so we need to adapt it.
            # This is a simplified example. A real implementation would need a more robust conversion.
            history = [messages[0]['content']] if messages else []
            response = await self._client.generate_content_async(
                history,
                **kwargs,
            )
            return {"text": response.text}
        except Exception as e:
            raise Exception(f"Gemini API error: {e}") from e

    async def stream_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Stream a chat completion using the Gemini API.
        """
        try:
            history = [messages[0]['content']] if messages else []
            stream = await self._client.generate_content_async(
                history,
                stream=True,
                **kwargs,
            )
            async for chunk in stream:
                yield {"text": chunk.text}
        except Exception as e:
            raise Exception(f"Gemini API error: {e}") from e

    def get_model_configuration(self) -> Dict[str, Any]:
        """
        Get the provider's model configuration.
        """
        return {"model": self._model}

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the provider's capabilities.
        """
        return {"streaming": True, "safety_settings": True}
