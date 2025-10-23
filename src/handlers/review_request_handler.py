from typing import Any

from commons.interfaces import RepositoryServiceInterface  # type: ignore
from commons.models.enums import UserAction  # type: ignore

from ..config import CLIENT_ID
from ..interfaces import LLMServiceInterface


def handle_review_request(
    message_payload: dict[str, Any],
    llm_service: LLMServiceInterface,
    repo_service: RepositoryServiceInterface,
) -> dict[str, Any]:
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

    return {"statusCode": 200, "body": {"review_comments": review_comments}}
