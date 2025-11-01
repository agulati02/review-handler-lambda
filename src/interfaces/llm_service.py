import os
import json
from abc import ABC, abstractmethod
from typing import Union
from typing import Any
from commons.models.enums import UserAction  # type: ignore


class LLMServiceInterface(ABC):
    def _load_message_templates(self, trigger: UserAction) -> dict[str, Any]:
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "resources", "llm_config.json"
        )
        with open(config_path, "r") as config_file:
            return json.load(config_file).get(trigger.value, {})
    
    @abstractmethod
    def get_code_review(
        self, user_action: UserAction, diff: str, context: Union[str, None] = None
    ) -> str:
        pass

    @abstractmethod
    def get_comment_response(
        self, user_action: UserAction, diff: str, comment_body: str, previous_comments: list[dict[str, Any]]
    ) -> str:
        pass
