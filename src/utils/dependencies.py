from functools import lru_cache

from commons.utils.dependencies import get_secrets_manager  # type: ignore

from ..config import AWS_REGION_NAME
from ..impl import AnthropicLLMService
from ..interfaces import LLMServiceInterface


@lru_cache(maxsize=1)
def get_llm_service() -> LLMServiceInterface:
    return AnthropicLLMService(secrets_manager=get_secrets_manager(AWS_REGION_NAME))
