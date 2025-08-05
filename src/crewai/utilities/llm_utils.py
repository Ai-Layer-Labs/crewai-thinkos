from typing import Any, Dict, List, Optional, Union

from crewai.cli.constants import LITELLM_PARAMS
from crewai.llm import LLM, BaseLLM


def create_llm(
    llm_value: Union[str, LLM, Any, None] = None,
) -> Optional[LLM | BaseLLM]:
    """
    Creates or returns an LLM instance based on the given llm_value.

    Args:
        llm_value (str | BaseLLM | Any | None):
            - str: The model name (e.g., "gpt-4").
            - BaseLLM: Already instantiated BaseLLM (including LLM), returned as-is.
            - Any: Attempt to extract known attributes like model_name, temperature, etc.
            - None: Use environment-based or fallback default model.

    Returns:
        A BaseLLM instance if successful, or None if something fails.
    """

    # 1) If llm_value is already a BaseLLM or LLM object, return it directly
    if isinstance(llm_value, LLM) or isinstance(llm_value, BaseLLM):
        return llm_value

    # 2) If llm_value is a string (model name)
    if isinstance(llm_value, str):
        try:
            created_llm = LLM(model=llm_value)
            return created_llm
        except Exception as e:
            print(f"Failed to instantiate LLM with model='{llm_value}': {e}")
            return None

    # 3) If llm_value is None, parse environment variables or use default
    if llm_value is None:
        return _llm_via_environment_or_fallback()

    # 4) Otherwise, attempt to extract relevant attributes from an unknown object
    try:
        # Extract attributes with explicit types
        model = (
            getattr(llm_value, "model", None)
            or getattr(llm_value, "model_name", None)
            or getattr(llm_value, "deployment_name", None)
            or str(llm_value)
        )
        temperature: Optional[float] = getattr(llm_value, "temperature", None)
        max_tokens: Optional[int] = getattr(llm_value, "max_tokens", None)
        logprobs: Optional[int] = getattr(llm_value, "logprobs", None)
        timeout: Optional[float] = getattr(llm_value, "timeout", None)
        api_key: Optional[str] = getattr(llm_value, "api_key", None)
        base_url: Optional[str] = getattr(llm_value, "base_url", None)
        api_base: Optional[str] = getattr(llm_value, "api_base", None)

        created_llm = LLM(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            logprobs=logprobs,
            timeout=timeout,
            api_key=api_key,
            base_url=base_url,
            api_base=api_base,
        )
        return created_llm
    except Exception as e:
        print(f"Error instantiating LLM from unknown object type: {e}")
        return None


def _llm_via_environment_or_fallback() -> Optional[LLM]:
    """
    NO ENVIRONMENT VARIABLES ALLOWED - Token storage required!
    This function exists only for backward compatibility but will raise an error.
    """
    raise ValueError(
        "Environment variables are not supported for LLM configuration. "
        "Please use token_manager with Agent/Crew or provide an initialized LLM instance. "
        "Store your API keys using the token storage API: "
        "POST /api/v1/tokens/store with service='llm_provider_{provider}_api_key'"
    )


def _normalize_key_name(key_name: str) -> str:
    """
    Maps environment variable names to recognized litellm parameter keys,
    using patterns from LITELLM_PARAMS.
    """
    for pattern in LITELLM_PARAMS:
        if pattern in key_name:
            return pattern
    return key_name
