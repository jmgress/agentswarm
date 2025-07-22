"""
Tests for provider functionality
"""
import pytest
from fastapi.testclient import TestClient
from main import app, provider_registry
from providers.base import ProviderType, ProviderCapability
from providers.ollama import OllamaProvider
from providers.openai import OpenAIProvider
from providers.gemini import GeminiProvider
import httpx
from unittest.mock import AsyncMock, patch


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_providers():
    """Clear provider registry before each test"""
    # Get list of provider IDs to avoid modifying during iteration
    provider_ids = list(provider_registry.list_providers())
    for provider_id in provider_ids:
        provider_registry.remove_provider(provider_id)


class TestProviderRegistry:
    """Test provider registry functionality"""
    
    def test_register_provider_class(self):
        """Test registering provider classes"""
        provider_registry.register_provider_class(ProviderType.OLLAMA, OllamaProvider)
        assert ProviderType.OLLAMA in provider_registry.list_provider_types()
    
    def test_create_provider(self):
        """Test creating provider instances"""
        provider_registry.register_provider_class(ProviderType.OLLAMA, OllamaProvider)
        
        config = {"base_url": "http://localhost:11434"}
        provider = provider_registry.create_provider("test_ollama", ProviderType.OLLAMA, config)
        
        assert provider.provider_type == ProviderType.OLLAMA
        assert provider.config == config
    
    def test_get_provider(self):
        """Test retrieving providers"""
        provider_registry.register_provider_class(ProviderType.OLLAMA, OllamaProvider)
        
        config = {"base_url": "http://localhost:11434"}
        provider_registry.create_provider("test_ollama", ProviderType.OLLAMA, config)
        
        retrieved = provider_registry.get_provider("test_ollama")
        assert retrieved is not None
        assert retrieved.provider_type == ProviderType.OLLAMA
    
    def test_remove_provider(self):
        """Test removing providers"""
        provider_registry.register_provider_class(ProviderType.OLLAMA, OllamaProvider)
        
        config = {"base_url": "http://localhost:11434"}
        provider_registry.create_provider("test_ollama", ProviderType.OLLAMA, config)
        
        assert provider_registry.remove_provider("test_ollama") is True
        assert provider_registry.get_provider("test_ollama") is None
        assert provider_registry.remove_provider("test_ollama") is False


class TestProviderEndpoints:
    """Test provider API endpoints"""
    
    def test_list_providers_empty(self):
        """Test listing providers when none exist"""
        response = client.get("/providers")
        assert response.status_code == 200
        data = response.json()
        assert data["providers"] == []
        assert data["total"] == 0
    
    def test_create_provider(self):
        """Test creating a provider via API"""
        provider_data = {
            "provider_id": "test_ollama",
            "provider_type": "ollama",
            "name": "Test Ollama",
            "description": "Test Ollama provider",
            "config": {"base_url": "http://localhost:11434"}
        }
        
        response = client.post("/providers", json=provider_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["provider_id"] == "test_ollama"
        assert data["provider_type"] == "ollama"
        assert data["name"] == "Test Ollama"
    
    def test_create_duplicate_provider(self):
        """Test creating provider with duplicate ID fails"""
        provider_data = {
            "provider_id": "duplicate_test",
            "provider_type": "ollama",
            "name": "Test Provider",
            "description": "Test",
            "config": {"base_url": "http://localhost:11434"}
        }
        
        # Create first provider
        response1 = client.post("/providers", json=provider_data)
        assert response1.status_code == 200
        
        # Try to create duplicate
        response2 = client.post("/providers", json=provider_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]
    
    def test_delete_provider(self):
        """Test deleting a provider"""
        provider_data = {
            "provider_id": "delete_test",
            "provider_type": "ollama",
            "name": "Delete Test",
            "description": "Test",
            "config": {"base_url": "http://localhost:11434"}
        }
        
        # Create provider
        client.post("/providers", json=provider_data)
        
        # Delete provider
        response = client.delete("/providers/delete_test")
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get("/providers")
        data = response.json()
        assert len(data["providers"]) == 0
    
    def test_delete_nonexistent_provider(self):
        """Test deleting non-existent provider returns 404"""
        response = client.delete("/providers/nonexistent")
        assert response.status_code == 404


class TestProviderImplementations:
    """Test specific provider implementations"""
    
    def test_ollama_provider_creation(self):
        """Test creating Ollama provider"""
        config = {"base_url": "http://localhost:11434", "timeout": 30.0}
        provider = OllamaProvider(config)
        
        assert provider.provider_type == ProviderType.OLLAMA
        assert provider.base_url == "http://localhost:11434"
        assert provider.timeout == 30.0
        assert ProviderCapability.CHAT_COMPLETION in provider.get_capabilities()
        assert ProviderCapability.STREAMING in provider.get_capabilities()
    
    def test_openai_provider_creation(self):
        """Test creating OpenAI provider"""
        config = {"api_key": "test-key", "base_url": "https://api.openai.com/v1"}
        provider = OpenAIProvider(config)
        
        assert provider.provider_type == ProviderType.OPENAI
        assert provider.api_key == "test-key"
        assert provider.base_url == "https://api.openai.com/v1"
        assert ProviderCapability.FUNCTION_CALLING in provider.get_capabilities()
    
    def test_gemini_provider_creation(self):
        """Test creating Gemini provider"""
        config = {"api_key": "test-key", "safety_settings": {}}
        provider = GeminiProvider(config)
        
        assert provider.provider_type == ProviderType.GEMINI
        assert provider.api_key == "test-key"
        assert ProviderCapability.SAFETY_SETTINGS in provider.get_capabilities()
    
    def test_provider_validation(self):
        """Test provider configuration validation"""
        # Valid Ollama config
        ollama_provider = OllamaProvider({"base_url": "http://localhost:11434"})
        assert ollama_provider.validate_config() is True
        
        # Invalid OpenAI config (no API key)
        openai_provider = OpenAIProvider({})
        assert openai_provider.validate_config() is False
        
        # Valid OpenAI config
        openai_provider_valid = OpenAIProvider({"api_key": "test-key"})
        assert openai_provider_valid.validate_config() is True


@pytest.mark.asyncio
class TestProviderHealthChecks:
    """Test provider health check functionality"""
    
    async def test_openai_health_check_no_api_key(self):
        """Test OpenAI health check without API key"""
        provider = OpenAIProvider({})
        status = await provider.health_check()
        
        assert status.available is False
        assert "No API key" in status.error
    
    async def test_gemini_health_check_no_api_key(self):
        """Test Gemini health check without API key"""
        provider = GeminiProvider({})
        status = await provider.health_check()
        
        assert status.available is False
        assert "No API key" in status.error


class TestAgentProviderIntegration:
    """Test agent creation with provider configuration"""
    
    def test_create_agent_with_provider_config(self):
        """Test creating agent with provider configuration"""
        agent_data = {
            "name": "Provider Test Agent",
            "agent_type": "utility",
            "description": "Agent with provider config",
            "mcp_connection": {
                "endpoint_url": "http://localhost:8080/mcp"
            },
            "provider_config": {
                "provider_id": "test_provider",
                "provider_type": "ollama",
                "model": "llama2",
                "config": {"temperature": 0.7},
                "fallback_providers": ["backup_provider"]
            }
        }
        
        response = client.post("/agents", json=agent_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Provider Test Agent"
        assert data["provider_config"]["provider_id"] == "test_provider"
        assert data["provider_config"]["provider_type"] == "ollama"
        assert data["provider_config"]["model"] == "llama2"
    
    def test_create_agent_without_provider_config(self):
        """Test creating agent without provider configuration"""
        agent_data = {
            "name": "No Provider Agent",
            "agent_type": "task",
            "description": "Agent without provider config",
            "mcp_connection": {
                "endpoint_url": "http://localhost:8080/mcp"
            }
        }
        
        response = client.post("/agents", json=agent_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["provider_config"] is None