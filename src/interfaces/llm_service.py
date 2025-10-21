from abc import ABC, abstractmethod
from typing import Union
from ..models.enums import UserAction


class LLMServiceInterface(ABC):
    @abstractmethod
    def get_code_review(self, user_action: UserAction, diff: str, context: Union[str, None] = None) -> str:
        pass
