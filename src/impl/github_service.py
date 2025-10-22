from httpx import Client
from ..interfaces import RepositoryServiceInterface, SecretsManagerInterface
from ..utils.token_manager import TokenManager
from ..models.requests import LLMResponseStructure


class GithubService(RepositoryServiceInterface):
    def __init__(
            self, 
            secrets_manager: SecretsManagerInterface,
            token_manager: TokenManager,
            connection_timeout: float = 10.0, 
            ca_certs: str = None
        ) -> None:
        self.secrets_manager = secrets_manager
        self.client = Client(
            timeout=connection_timeout,
            verify=ca_certs if ca_certs else True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Connection": "keep-alive",
            }
        )
        self.token_manager = token_manager

    def get_diff(self, pull_request_url: str, installation_id: str) -> str:
        """Fetches the diff for a given pull request payload from GitHub."""
        jwt_token = self.token_manager.get_jwt_token()
        access_token = self.token_manager.get_installation_access_token(
            jwt_token, installation_id
        )
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3.diff",
        }
        response = self.client.get(pull_request_url, headers=headers)
        response.raise_for_status()
        return response.text

    def post_review_comments(self, pull_request_url: str, installation_id: str, reviews: str) -> None:
        """Posts review comments to a given pull request on GitHub."""
        jwt_token = self.token_manager.get_jwt_token()
        access_token = self.token_manager.get_installation_access_token(
            jwt_token, installation_id
        )
        comments_url = f"{pull_request_url}/comments"
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github+json",
        }
        # comments = ""
        # for review in reviews.items:
        #     comments += f"Suggested Change (Lines {review.line_number_start} to {review.line_number_end}):\n"
        #     comments += f"```diff\n{review.suggestion_diff}\n```\n\n"
        
        payload = {
            "body": reviews,
            "event": "COMMENT"
        }
        response = self.client.post(comments_url, headers=headers, json=payload)
        response.raise_for_status()
