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
        model: str | None = None,
        config: Dict[str, Any] | None = None,
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
        
        # Normalize hierarchy api_provider > model_provider > model_name
        # - If model already contains '/', pass through untouched (e.g., "openai/gpt-5-chat" or "google/gemini-2.5-flash")
        # - Else prefix with provider when needed
        if model is None:
            raise ValueError("Model must be specified")

        if "/" in model:
            model_str = model
        else:
            # Bare model name; prefix for non-openai
            if provider in {"openai"}:
                model_str = model
            elif provider in {"anthropic", "groq", "mistral", "google", "gemini"}:
                # Allow both google and gemini aliases
                pfx = "gemini" if provider == "google" else provider
                model_str = f"{pfx}/{model}"
            elif provider == "openrouter":
                # openrouter with bare model is ambiguous; pass through
                model_str = model
            else:
                model_str = f"{provider}/{model}"
        
        # Create and return CrewAI LLM instance
        # Pass explicit API provider for litellm
        additional = {"custom_llm_provider": provider}
        if config:
            additional.update(config)
        additional.update(kwargs)
        return LLM(model=model_str, api_key=api_key, **additional)