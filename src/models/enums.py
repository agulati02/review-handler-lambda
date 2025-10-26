from enum import Enum


class SecretName(str, Enum):
    GITHUB_PRIVATE_KEY = "github-app-private-key"
    LLM_API_KEY = "llm-api-key"


class EventStatus(str, Enum):
    IN_QUEUE = "in_queue"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    EXCEPTION = "exception" 
