from enum import Enum


class UserAction(str, Enum):
    REVIEW_REQUESTED = "review_requested"
    DISCUSSION_COMMENT = "discussion_comment"
    UNKNOWN = "unknown"


class SecretName(str, Enum):
    GITHUB_PRIVATE_KEY = "github-app-private-key"
    LLM_API_KEY = "llm-api-key"
