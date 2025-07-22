"""
Provider Registry for managing AI providers
"""
from typing import Dict, List, Optional, Type, Any
from .base import BaseProvider, ProviderType, ProviderStatus
import asyncio


class ProviderRegistry:
    """Registry for managing AI providers"""
    
    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {}
        self._provider_classes: Dict[ProviderType, Type[BaseProvider]] = {}
    
    def register_provider_class(self, provider_type: ProviderType, provider_class: Type[BaseProvider]):
        """
        Register a provider class
        
        Args:
            provider_type: Provider type enum
            provider_class: Provider class to register
        """
        self._provider_classes[provider_type] = provider_class
    
    def create_provider(self, provider_id: str, provider_type: ProviderType, config: Dict[str, Any]) -> BaseProvider:
        """
        Create and register a provider instance
        
        Args:
            provider_id: Unique identifier for this provider instance
            provider_type: Type of provider to create
            config: Provider configuration
            
        Returns:
            Created provider instance
            
        Raises:
            ValueError: If provider type is not registered
        """
        if provider_type not in self._provider_classes:
            raise ValueError(f"Provider type {provider_type} is not registered")
        
        provider_class = self._provider_classes[provider_type]
        provider = provider_class(config)
        
        if not provider.validate_config():
            raise ValueError(f"Invalid configuration for provider {provider_id}")
        
        self._providers[provider_id] = provider
        return provider
    
    def get_provider(self, provider_id: str) -> Optional[BaseProvider]:
        """
        Get a provider by ID
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            Provider instance or None if not found
        """
        return self._providers.get(provider_id)
    
    def remove_provider(self, provider_id: str) -> bool:
        """
        Remove a provider from the registry
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            True if provider was removed, False if not found
        """
        if provider_id in self._providers:
            del self._providers[provider_id]
            return True
        return False
    
    def list_providers(self) -> List[str]:
        """
        Get list of all registered provider IDs
        
        Returns:
            List of provider IDs
        """
        return list(self._providers.keys())
    
    def list_provider_types(self) -> List[ProviderType]:
        """
        Get list of all registered provider types
        
        Returns:
            List of provider types
        """
        return list(self._provider_classes.keys())
    
    async def health_check_all(self) -> Dict[str, ProviderStatus]:
        """
        Run health checks on all registered providers
        
        Returns:
            Dictionary mapping provider IDs to their status
        """
        results = {}
        
        # Run health checks concurrently
        tasks = []
        provider_ids = []
        
        for provider_id, provider in self._providers.items():
            tasks.append(provider.health_check())
            provider_ids.append(provider_id)
        
        if tasks:
            statuses = await asyncio.gather(*tasks, return_exceptions=True)
            
            for provider_id, status in zip(provider_ids, statuses):
                if isinstance(status, Exception):
                    results[provider_id] = ProviderStatus(
                        available=False,
                        error=str(status)
                    )
                else:
                    results[provider_id] = status
        
        return results
    
    def get_providers_by_type(self, provider_type: ProviderType) -> List[BaseProvider]:
        """
        Get all providers of a specific type
        
        Args:
            provider_type: Provider type to filter by
            
        Returns:
            List of providers of the specified type
        """
        return [
            provider for provider in self._providers.values()
            if provider.provider_type == provider_type
        ]


# Global provider registry instance
provider_registry = ProviderRegistry()