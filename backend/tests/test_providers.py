import pytest
from unittest.mock import MagicMock, AsyncMock

from backend.providers.base import BaseProvider
from backend.providers.ollama import OllamaProvider
from backend.providers.openai import OpenAIProvider
from backend.providers.gemini import GeminiProvider
from backend.providers.registry import ProviderRegistry, provider_registry


@pytest.fixture
def registry() -> ProviderRegistry:
    return provider_registry


def test_provider_registry_list(registry: ProviderRegistry):
    """Test that the registry lists default providers."""
    assert "ollama" in registry.list_providers()
    assert "openai" in registry.list_providers()
    assert "gemini" in registry.list_providers()


def test_provider_registry_get(registry: ProviderRegistry):
    """Test that the registry can retrieve a provider."""
    provider = registry.get_provider("ollama", model="test")
    assert isinstance(provider, OllamaProvider)


def test_provider_registry_register(registry: ProviderRegistry):
    """Test that a new provider can be registered."""

    class TestProvider(BaseProvider):
        name = "test_provider"

        async def chat_completion(self, messages, **kwargs):
            return {}

        async def stream_completion(self, messages, **kwargs):
            pass

        def get_model_configuration(self):
            return {}

        def get_capabilities(self):
            return {}

    registry.register("test_provider", TestProvider)
    assert "test_provider" in registry.list_providers()
    provider = registry.get_provider("test_provider")
    assert isinstance(provider, TestProvider)


@pytest.mark.asyncio
async def test_ollama_provider():
    """Test the Ollama provider's chat completion."""
    provider = OllamaProvider(model="test")
    provider._client = AsyncMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "test"}
    provider._client.post.return_value = mock_response

    response = await provider.chat_completion([{"role": "user", "content": "hello"}])
    assert response == {"response": "test"}
    provider._client.post.assert_called_once()


@pytest.mark.asyncio
async def test_openai_provider(monkeypatch):
    """Test the OpenAI provider's chat completion."""
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    provider = OpenAIProvider(model="test")
    provider._client = AsyncMock()
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {"choices": [{"message": {"content": "test"}}]}
    provider._client.chat.completions.create.return_value = mock_response

    response = await provider.chat_completion([{"role": "user", "content": "hello"}])
    assert response == {"choices": [{"message": {"content": "test"}}]}
    provider._client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_gemini_provider(monkeypatch):
    """Test the Gemini provider's chat completion."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key")
    provider = GeminiProvider(model="test")
    provider._client = AsyncMock()
    mock_response = MagicMock()
    mock_response.text = "test"
    provider._client.generate_content_async.return_value = mock_response

    response = await provider.chat_completion([{"role": "user", "content": "hello"}])
    assert response == {"text": "test"}
    provider._client.generate_content_async.assert_called_once()
