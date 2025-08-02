"""Token Storage Integration for ThinkOS"""
from typing import Optional, Any
import asyncio

class TokenStorageIntegration:
    """Integration layer for ThinkOS token storage"""
    
    def __init__(self, token_manager=None):
        self.token_manager = token_manager
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key from token storage"""
        if not self.token_manager:
            return None
            
        token_key = f"llm_provider_{provider}_api_key"
        
        # Handle async token manager in sync context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're already in an async context
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.token_manager.get_token(token_key))
                    token_info = future.result()
            else:
                token_info = loop.run_until_complete(self.token_manager.get_token(token_key))
        except RuntimeError:
            # No event loop, create one
            token_info = asyncio.run(self.token_manager.get_token(token_key))
        
        return token_info.token if token_info else None
    
    @staticmethod
    def inject_token_manager(obj, token_manager):
        """Inject token manager into an object"""
        if hasattr(obj, '__dict__'):
            obj.token_manager = token_manager
            obj._token_storage = TokenStorageIntegration(token_manager)
        return obj