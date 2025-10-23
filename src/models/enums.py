from enum import Enum


class SecretName(str, Enum):
    GITHUB_PRIVATE_KEY = "github-app-private-key"
    LLM_API_KEY = "llm-api-key"
