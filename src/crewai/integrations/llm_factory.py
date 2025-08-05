"""LLM Factory with Token Storage Support"""
from typing import Optional, Any, Dict
from crewai.integrations.token_storage import TokenStorageIntegration
from crewai.llm import LLM

class LLMFactory:
    """Factory for creating LLMs with token storage support"""
    
    def __init__(self, token_manager=None):
        self.token_storage = TokenStorageIntegration(token_manager)
    
    def create_llm(
        self,
        provider: str = "openai",
        model: str = None,
        config: Dict[str, Any] = None,
        **kwargs
    ) -> Any:
        """Create LLM instance with token from storage"""
        
        # Get API key from token storage ONLY - no fallbacks!
        api_key = self.token_storage.get_api_key(provider)
        
        if not api_key:
            raise ValueError(
                f"No API key found for {provider} in token storage. "
                f"Please store your API key using the token management API: "
                f"POST /api/v1/tokens/store with service='llm_provider_{provider}_api_key'"
            )
        
        # Create LLM instance with the API key from token storage
        # CrewAI's LLM class will handle the provider-specific initialization
        
        # Model must be explicitly specified
        if not model:
            raise ValueError(
                f"Model must be specified for provider '{provider}'. "
                f"No default models are assumed. "
                f"Examples: 'gpt-4', 'claude-3-opus-20240229', 'mixtral-8x7b-32768'"
            )
        
        # Build the model string for CrewAI's LLM class
        if provider == "openai":
            model_str = model
        elif provider == "anthropic":
            model_str = f"anthropic/{model}"
        elif provider == "groq":
            model_str = f"groq/{model}"
        elif provider == "openrouter":
            # OpenRouter models are already in the correct format
            model_str = model
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Create and return CrewAI LLM instance
        return LLM(
            model=model_str,
            api_key=api_key,
            **(config or {}),
            **kwargs
        )