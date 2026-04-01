import time
import requests
from django.conf import settings


class ClientCredentialsToken:
    def __init__(self):
        self.access_token = None
        self.expires_at = 0

    def get_token(self):
        if not self.access_token or time.time() > self.expires_at - 30:
            response = requests.post(
                f"{settings.KEYCLOAK_HOST}/realms/{settings.REALM}/protocol/openid-connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": settings.KEYCLOAK_CLIENT_ID,
                    "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
                },
            )

            if response.status_code != 200:
                raise Exception(f"Keycloak error: {response.text}")

            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.expires_at = time.time() + token_data["expires_in"]

        return self.access_token


client_token_service = ClientCredentialsToken()
