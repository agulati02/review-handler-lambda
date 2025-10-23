from typing import Any

import orjson
from commons.models.enums import UserAction  # type: ignore
from commons.utils.dependencies import get_repository_service  # type: ignore

from .config import AWS_REGION_NAME, GITHUB_PRIVATE_KEY_PATH
from .handlers import handle_discussion_comment, handle_review_request
from .utils.dependencies import get_llm_service


class ProcessRouter:
    handlers: dict[UserAction, Any] = {
        UserAction.REVIEW_REQUESTED: handle_review_request,
        UserAction.DISCUSSION_COMMENT: handle_discussion_comment,
    }

    def route_event(self, event: dict[str, Any]) -> dict[str, Any]:
        message_payload = orjson.loads(event["Records"][0]["body"])
        user_action = UserAction(message_payload["trigger"])
        handler = self.handlers.get(user_action)
        if not handler:
            raise ValueError(f"No handler found for action: {user_action}")
        llm_service = get_llm_service()
        repo_service = get_repository_service(
            aws_region_name=AWS_REGION_NAME,
            repo_private_key_path=GITHUB_PRIVATE_KEY_PATH,
        )
        return handler(message_payload, llm_service, repo_service)


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    try:
        router = ProcessRouter()
        return router.route_event(event)
    except Exception as e:
        return {"statusCode": 500, "body": orjson.dumps(f"Error: {str(e)}")}
