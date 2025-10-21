from ..interfaces import RespositoryServiceInterface, SecretsManagerInterface


class GithubService(RespositoryServiceInterface):
    def __init__(self, secrets_manager: SecretsManagerInterface) -> None:
        self.secrets_manager = secrets_manager

    async def get_diff(self, payload: dict) -> str:
        pass
