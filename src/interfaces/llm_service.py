from abc import ABC, abstractmethod
from typing import Union

from commons.models.enums import UserAction  # type: ignore


class LLMServiceInterface(ABC):
    @abstractmethod
    def get_code_review(
        self, user_action: UserAction, diff: str, context: Union[str, None] = None
    ) -> str:
        pass
