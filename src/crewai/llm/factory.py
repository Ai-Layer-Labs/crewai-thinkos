"""LLM Factory with Token Storage Support"""
from typing import Optional, Any, Dict
from crewai.integrations.token_storage import TokenStorageIntegration

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
        
        # Import providers dynamically to avoid dependencies
        if provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=model or "gpt-4",
                api_key=api_key,
                **(config or {}),
                **kwargs
            )
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=model or "claude-3-opus-20240229",
                anthropic_api_key=api_key,
                **(config or {}),
                **kwargs
            )
        elif provider == "groq":
            from langchain_groq import ChatGroq
            return ChatGroq(
                model=model or "mixtral-8x7b-32768",
                groq_api_key=api_key,
                **(config or {}),
                **kwargs
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")