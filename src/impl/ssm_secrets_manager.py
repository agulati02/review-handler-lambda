import boto3
from ..interfaces.secrets_manager import SecretsManagerInterface
from ..config import AWS_REGION_NAME


class SSMSecretsManager(SecretsManagerInterface):
    def __init__(self) -> None:
        self.ssm_client = boto3.client("ssm", region_name=AWS_REGION_NAME)

    def get_secret(self, secret_name: str) -> str:
        response = self.ssm_client.get_parameter(Name=secret_name, WithDecryption=True)
        return response["Parameter"]["Value"]
