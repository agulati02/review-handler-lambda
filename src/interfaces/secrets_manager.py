from abc import ABC, abstractmethod


class SecretsManagerInterface(ABC):
    @abstractmethod
    def get_secret(self, secret_name: str) -> str:
        """Retrieve the secret value for the given secret name."""
        pass
