from typing import Any
from datetime import datetime, timezone
from commons.interfaces import RepositoryServiceInterface, DatabaseServiceInterface  # type: ignore
from commons.models.enums import UserAction # type: ignore
from ..interfaces import LLMServiceInterface
from ..config import EVENTS_COLLECTION, CLIENT_ID
from ..models.enums import EventStatus


def handle_discussion_comment(
    message_payload: dict[str, Any],
    llm_service: LLMServiceInterface,
    repo_service: RepositoryServiceInterface,
    database_service: DatabaseServiceInterface
) -> dict[str, Any]:
    if not EVENTS_COLLECTION:
        raise ValueError("EVENTS_COLLECTION not set")
    database_service.update(
        collection=EVENTS_COLLECTION,
        filter={
            "trigger_id": message_payload['trigger_id'],
        },
        diff={
            "status": EventStatus.IN_REVIEW,
            "timestamp": datetime.now(tz=timezone.utc)
        }
    )
    diff = repo_service.get_diff(
        pull_request_url=message_payload["issue"]["pull_request"]["url"],
        installation_id=message_payload["installation"]["id"],
        app_client_id=CLIENT_ID,
    )
    comments = repo_service.get_issue_comments(
        comments_url=message_payload["issue"]["comments_url"],
        installation_id=message_payload["installation"]["id"],
        app_client_id=CLIENT_ID
    )
    response = llm_service.get_comment_response(
        diff=diff, 
        user_action=UserAction.DISCUSSION_COMMENT, 
        comment_body=message_payload["comment"]["body"], 
        previous_comments=comments
    )
    repo_service.post_issue_comment(
        comments_url=message_payload["issue"]["comments_url"],
        installation_id=message_payload["installation"]["id"],
        content=f"@{message_payload["issue"]["user"]["login"]} - {response}",
        app_client_id=CLIENT_ID,
    )
    database_service.update(
        collection=EVENTS_COLLECTION,
        filter={
            "trigger_id": message_payload['trigger_id'],
        },
        diff={
            "status": EventStatus.COMPLETED,
            "timestamp": datetime.now(tz=timezone.utc)
        }
    )
    return {"statusCode": 200, "body": "Response posted to discusion"}
