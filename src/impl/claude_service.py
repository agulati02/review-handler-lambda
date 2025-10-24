import json
import os
from typing import Any, Union

from commons.interfaces import SecretsManagerInterface  # type: ignore
from commons.models.enums import UserAction  # type: ignore
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..config import ENV, LLM_API_KEY_PATH, LLM_MAX_RESPONSE_TOKENS, LLM_MODEL_NAME
from ..interfaces import LLMServiceInterface


class AnthropicLLMService(LLMServiceInterface):
    def __init__(self, secrets_manager: SecretsManagerInterface) -> None:
        self.secrets_manager = secrets_manager
        self.llm = ChatAnthropic(  # type: ignore
            model=LLM_MODEL_NAME,  # type: ignore
            api_key=self._load_api_key(),
            max_tokens=LLM_MAX_RESPONSE_TOKENS,  # type: ignore
        )

    def _load_api_key(self) -> Union[str, None]:
        if ENV.lower() == "local":
            with open(LLM_API_KEY_PATH, "r") as key_file:
                return key_file.read().strip()
        else:
            return self.secrets_manager.get_secret(LLM_API_KEY_PATH)

    def _load_message_templates(self, trigger: UserAction) -> dict[str, Any]:
        config_path = os.path.join(
            os.path.dirname(__file__), "..", "resources", "llm_config.json"
        )
        with open(config_path, "r") as config_file:
            return json.load(config_file).get(trigger.value, {})

    def get_code_review(
        self,
        user_action: UserAction,
        diff: str,
        context: Union[str, None] = None,
    ) -> str:
        messages = self._load_message_templates(user_action)
        # Convert messages to ChatPromptTemplate
        prompt_template = ChatPromptTemplate.from_messages(  # type: ignore
            [("system", messages["system"]), ("human", messages["human"])]
        )
        prompt = prompt_template.invoke({"diff": diff, "context": context or ""})  # type: ignore
        response = self.llm.invoke(prompt)
        return response.content  # type: ignore
