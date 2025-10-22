from abc import ABC, abstractmethod
from ..models.requests import LLMResponseStructure


class RepositoryServiceInterface(ABC):
    @abstractmethod
    async def get_diff(self, pull_request_url: str) -> str:
        pass

    @abstractmethod
    def post_review_comments(self, pull_request_url: str, installation_id: str, reviews: LLMResponseStructure) -> None:
        pass
