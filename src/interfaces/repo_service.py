from abc import ABC, abstractmethod


class RespositoryServiceInterface(ABC):
    @abstractmethod
    async def get_diff(self, payload: dict) -> str:
        pass
    