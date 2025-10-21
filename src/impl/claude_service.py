import os
import json
from typing import Union
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from ..interfaces import LLMServiceInterface, SecretsManagerInterface
from ..config import ENV, LLM_API_KEY_PATH, LLM_MODEL_NAME, LLM_MAX_RESPONSE_TOKENS
from ..models.enums import UserAction
from ..models.requests import LLMResponseStructure


class AnthropicLLMService(LLMServiceInterface):
    def __init__(self, secrets_manager: SecretsManagerInterface) -> None:
        self.secrets_manager = secrets_manager
        self.llm = ChatAnthropic(
            model=LLM_MODEL_NAME,
            api_key=self._load_api_key(),
            max_tokens=LLM_MAX_RESPONSE_TOKENS,
        ).with_structured_output(LLMResponseStructure, include_raw=True)

    def _load_api_key(self) -> str:
        if ENV.lower() == 'local':
            with open(os.path.join(os.path.dirname(__file__), '..', 'resources', 'claude-api-key.txt'), 'r') as key_file:
                return key_file.read().strip()
        else:
            return self.secrets_manager.get_secret(LLM_API_KEY_PATH)
    
    def _load_message_templates(self, trigger: UserAction) -> dict:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'llm_config.json')
        with open(config_path, 'r') as config_file:
            return json.load(config_file).get(trigger.value, {})

    def get_code_review(self, user_action: UserAction, diff: str, context: Union[str, None] = None) -> str:
        messages = self._load_message_templates(user_action)
        # Convert messages to ChatPromptTemplate
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", messages["system"]),
            ("human", messages["human"])
        ])
        prompt = prompt_template.invoke({"diff": diff, "context": context or ""})
        response = self.llm.invoke(prompt)
        return response
