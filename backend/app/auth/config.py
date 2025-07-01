import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class AzureADConfig:
    """
    Config class for Azure AD/Entra Auth. 

    Keeps all Azure AD settings in one place and validates that nothing is missing
    """
    def __init__(self) -> None:
        self.tenant_id = self._get_required_env("AZURE_AD_TENANT_ID")
        self.client_id = self._get_required_env("AZURE_AD_CLIENT_ID")
        self.audience = self._get_required_env("AZURE_AD_AUDIENCE")

        # Entra standard endpoints
        self.jwks_url = f"https://login.microsoftonline.com/{self.tenant_id}/discovery/v2.0/keys"
        self.issuer = f"https://login.microsoftonline.com/{self.tenant_id}/v2.0"


    def _get_required_env(self, key: str) -> str:
        """
        Helper to get env variables.

        If a var is missing, raises an error for debugging deployments.
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(
                f"Missing required env variable: {key}\n"
            )
        return value

azure_ad_config = AzureADConfig()