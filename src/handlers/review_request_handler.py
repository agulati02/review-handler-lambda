from ..interfaces import LLMServiceInterface, RepositoryServiceInterface
from ..models.enums import UserAction


def handle_review_request(message_payload: dict, llm_service: LLMServiceInterface, repo_service: RepositoryServiceInterface) -> dict:
    diff = repo_service.get_diff(
        pull_request_url=message_payload["pull_request"]["url"],
        installation_id=message_payload["installation"]["id"]
    )
    review_comments = llm_service.get_code_review(diff=diff, user_action=UserAction.REVIEW_REQUESTED)
    print(review_comments)
    return {
        "statusCode": 200,
        "body": {
            "review_comments": review_comments
        }
    }
