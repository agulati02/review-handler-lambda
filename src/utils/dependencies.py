import boto3
from functools import lru_cache
from ..config import AWS_REGION_NAME
from ..interfaces import SecretsManagerInterface, RespositoryServiceInterface, LLMServiceInterface
from ..impl import SSMSecretsManager, GithubService, AnthropicLLMService


@lru_cache(maxsize=1)
def get_secrets_manager() -> SecretsManagerInterface:
    return SSMSecretsManager()

@lru_cache(maxsize=1)
def get_repo_service() -> RespositoryServiceInterface:
    return GithubService(secrets_manager=get_secrets_manager())

@lru_cache(maxsize=1)
def get_llm_service() -> LLMServiceInterface:
    return AnthropicLLMService(secrets_manager=get_secrets_manager())
