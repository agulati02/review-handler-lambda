from typing import Any
from datetime import datetime, timezone

from commons.interfaces import RepositoryServiceInterface, DatabaseServiceInterface  # type: ignore
from commons.models.enums import UserAction   # type: ignore

from ..config import CLIENT_ID, EVENTS_COLLECTION
from ..interfaces import LLMServiceInterface
from ..models.enums import EventStatus


def handle_review_request(
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
        pull_request_url=message_payload["pull_request"]["url"],
        installation_id=message_payload["installation"]["id"],
        app_client_id=CLIENT_ID,
    )
    review_comments = llm_service.get_code_review(
        diff=diff, user_action=UserAction.REVIEW_REQUESTED
    )
    repo_service.post_issue_comment(
        comments_url=message_payload["pull_request"]["comments_url"],
        installation_id=message_payload["installation"]["id"],
        content=review_comments,
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

    return {"statusCode": 200, "body": {"review_comments": review_comments}}
