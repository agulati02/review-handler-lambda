import boto3
from functools import lru_cache
from ..config import AWS_REGION_NAME
from ..interfaces import (
    SecretsManagerInterface,
    RepositoryServiceInterface,
    LLMServiceInterface,
)
from ..impl import SSMSecretsManager, GithubService, AnthropicLLMService
from .token_manager import TokenManager


@lru_cache(maxsize=1)
def get_secrets_manager() -> SecretsManagerInterface:
    return SSMSecretsManager()

@lru_cache(maxsize=1)
def get_token_manager() -> TokenManager:
    return TokenManager(secrets_manager=get_secrets_manager())

@lru_cache(maxsize=1)
def get_repo_service() -> RepositoryServiceInterface:
    return GithubService(secrets_manager=get_secrets_manager(), token_manager=get_token_manager())

@lru_cache(maxsize=1)
def get_llm_service() -> LLMServiceInterface:
    return AnthropicLLMService(secrets_manager=get_secrets_manager())
