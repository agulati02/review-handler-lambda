from typing import Any
import logging
import orjson
from commons.models.enums import UserAction  # type: ignore
from commons.utils.dependencies import get_repository_service, get_database_service, get_secrets_manager  # type: ignore

from .config import AWS_REGION_NAME, SECRET_GITHUB_PRIVATE_KEY_PATH, SECRET_DATABASE_USERNAME_PATH, SECRET_DATABASE_PASSWORD_PATH, DATABASE_CONNECTION_STRING, DATABASE_NAME
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
            repo_private_key_path=SECRET_GITHUB_PRIVATE_KEY_PATH,
        )
        db_username, db_password = tuple(get_secrets_manager(AWS_REGION_NAME).get_secrets(
            secrets=[SECRET_DATABASE_USERNAME_PATH, SECRET_DATABASE_PASSWORD_PATH]  # type: ignore
        ))  # type: ignore
        database_service = get_database_service(
            conn_string=DATABASE_CONNECTION_STRING,
            database_name=DATABASE_NAME,
            username=db_username,
            password=db_password
        )
        return handler(message_payload, llm_service, repo_service, database_service)


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    try:
        router = ProcessRouter()
        return router.route_event(event)
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        return {"statusCode": 500, "body": orjson.dumps(f"Error: {str(e)}")}
