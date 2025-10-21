from abc import ABC, abstractmethod


class RepositoryServiceInterface(ABC):
    @abstractmethod
    async def get_diff(self, pull_request_url: str) -> str:
        pass
