from typing import Dict, Type
from .base import BaseProvider
from .ollama import OllamaProvider
from .openai import OpenAIProvider
from .gemini import GeminiProvider

class ProviderRegistry:
    """
    Registry for AI providers.
    """

    def __init__(self):
        self._providers: Dict[str, Type[BaseProvider]] = {}
        self._register_defaults()

    def _register_defaults(self):
        """
        Register the default providers.
        """
        self.register("ollama", OllamaProvider)
        self.register("openai", OpenAIProvider)
        self.register("gemini", GeminiProvider)

    def register(self, name: str, provider_class: Type[BaseProvider]):
        """
        Register a new provider.
        """
        if name in self._providers:
            raise ValueError(f"Provider with name '{name}' is already registered.")
        self._providers[name] = provider_class

    def get_provider(self, name: str, **kwargs) -> BaseProvider:
        """
        Get an instance of a provider by name.
        """
        provider_class = self._providers.get(name)
        if not provider_class:
            raise ValueError(f"Provider with name '{name}' not found.")
        return provider_class(**kwargs)

    def list_providers(self) -> list[str]:
        """
        List the names of all registered providers.
        """
        return list(self._providers.keys())

# Global instance of the registry
provider_registry = ProviderRegistry()
