from abc import ABC, abstractmethod
from typing import Union


class LLMServiceInterface(ABC):
    @abstractmethod
    def get_code_review(self, diff: str, context: Union[str, None] = None) -> str:
        pass
