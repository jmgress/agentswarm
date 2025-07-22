from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional, Union

class BaseProvider(ABC):
    """
    Abstract base class for AI providers.
    Defines the common interface for all providers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass

    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Generate a chat completion.
        """
        pass

    @abstractmethod
    async def stream_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Stream a chat completion.
        """
        pass

    @abstractmethod
    def get_model_configuration(self) -> Dict[str, Any]:
        """
        Get the provider's model configuration.
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the provider's capabilities.
        """
        pass
