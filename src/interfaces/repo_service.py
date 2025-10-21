from abc import ABC, abstractmethod


class RespositoryServiceInterface(ABC):
    @abstractmethod
    async def get_diff(self, pull_request_url: str) -> str:
        pass
