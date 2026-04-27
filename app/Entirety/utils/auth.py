import time

import jwt
import requests
from django.conf import settings
from filip.models.base import FiwareHeaderSecure
from jwt import PyJWKClient


def get_fiware_header(request, project):
    token = get_valid_token(request)
    header_kwargs = {
        "service": project.fiware_service,
        "service_path": project.fiware_service_path,
    }

    if token:
        header_kwargs["authorization"] = f"Bearer {token}"

    return FiwareHeaderSecure(**header_kwargs)


def refresh_access_token(request):
    refresh_token = request.session.get("refresh_token")

    if not refresh_token:
        return None

    response = requests.post(
        settings.OIDC_OP_TOKEN_ENDPOINT,
        data={
            "grant_type": "refresh_token",
            "client_id": settings.OIDC_RP_CLIENT_ID,
            "client_secret": settings.OIDC_RP_CLIENT_SECRET,
            "refresh_token": refresh_token,
        },
    )

    if response.status_code != 200:
        request.session.flush()
        return None

    tokens = response.json()

    request.session["access_token"] = tokens["access_token"]
    request.session["refresh_token"] = tokens.get("refresh_token", refresh_token)

    return tokens["access_token"]


def get_valid_token(request):
    token = request.session.get("access_token")

    if not token:
        return None

    try:
        jwks_client = PyJWKClient(settings.OIDC_OP_JWKS_ENDPOINT)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=[settings.OIDC_RP_SIGN_ALGO],
            audience=settings.OIDC_RP_CLIENT_ID,
        )
        exp = decoded.get("exp", 0)

        # refresh 60s before expiry
        if time.time() > exp - 60:
            new_token = refresh_access_token(request)
            if new_token:
                return new_token
            return None

        return token

    except Exception:
        # if token invalid then try refresh
        new_token = refresh_access_token(request)
        return new_token


def get_fiware_services(request):
    token = request.session.get("access_token")
    if not token:
        return []

    try:
        jwks_client = PyJWKClient(settings.OIDC_OP_JWKS_ENDPOINT)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=[settings.OIDC_RP_SIGN_ALGO],
            audience=settings.OIDC_RP_CLIENT_ID,
        )
        return decoded.get("fiware-service", [])
    except Exception:
        return []
