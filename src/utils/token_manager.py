import jwt
import requests
from datetime import datetime, timedelta, timezone
from ..config import GITHUB_PRIVATE_KEY_PATH, CLIENT_ID, JWT_ALGORITHM, ENV
from ..interfaces import SecretsManagerInterface


class TokenManager:
    def __init__(self, secrets_manager: SecretsManagerInterface) -> None:
        self.secrets_manager = secrets_manager

    def get_jwt_token(self) -> str:
        private_key = None
        if ENV.lower() == "local":
            with open(GITHUB_PRIVATE_KEY_PATH, "r") as key_file:
                private_key = key_file.read()
        else:
            private_key = self.secrets_manager.get_secret(GITHUB_PRIVATE_KEY_PATH)

        payload = {
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "exp": int(
                (datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp()
            ),
            "iss": CLIENT_ID,
            "alg": JWT_ALGORITHM,
        }

        jwt_token = jwt.encode(payload, private_key, algorithm=JWT_ALGORITHM)
        return jwt_token

    def get_installation_access_token(self, jwt_token: str, installation_id: int) -> str:
        url = (
            f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        )
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        }

        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json().get("token", None)
