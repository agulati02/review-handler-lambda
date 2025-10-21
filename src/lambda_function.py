import orjson
from .utils.dependencies import get_llm_service, get_repo_service
from .models.enums import UserAction
from .handlers import handle_review_request, handle_discussion_comment


class ProcessRouter:
    handlers = {
        UserAction.REVIEW_REQUESTED: handle_review_request,
        UserAction.DISCUSSION_COMMENT: handle_discussion_comment
    }

    def route_event(self, event: dict) -> dict:
        message_payload = orjson.loads(event["Records"][0]["body"])
        user_action = UserAction(message_payload["trigger"])
        handler = self.handlers.get(user_action)
        if not handler:
            raise ValueError(f"No handler found for action: {user_action}")
        llm_service = get_llm_service()
        repo_service = get_repo_service()
        return handler(message_payload, llm_service, repo_service)


def lambda_handler(event, context):
    try:
        router = ProcessRouter()
        return router.route_event(event)
    except Exception as e:
        return {"statusCode": 500, "body": orjson.dumps(f"Error: {str(e)}")}
