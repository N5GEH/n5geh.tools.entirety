import time

import jwt
import requests
from django.conf import settings
from filip.models.base import FiwareHeaderSecure

from users.services import client_token_service


def get_fiware_header(request, project):
    token = get_valid_token(request)

    return FiwareHeaderSecure(
        service=project.fiware_service,
        service_path=project.fiware_service_path,
        authorization=f"Bearer {token}",
    )


def refresh_access_token(request):
    refresh_token = request.session.get("refresh_token")

    if not refresh_token:
        return None

    response = requests.post(
        f"{settings.KEYCLOAK_HOST}/realms/{settings.REALM}/protocol/openid-connect/token",
        data={
            "grant_type": "refresh_token",
            "client_id": settings.KEYCLOAK_CLIENT_ID,
            "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
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
    if settings.LOCAL_AUTH:
        return client_token_service.get_token()

    token = request.session.get("access_token")

    if not token:
        return None

    try:
        # TODO: verify signature
        decoded = jwt.decode(token, options={"verify_signature": False})
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

    if settings.LOCAL_AUTH:
        token = client_token_service.get_token()
    else:
        token = request.session.get("access_token")
        if not token:
            return []

    try:
        # TODO: verify signature
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("fiware-service", [])
    except Exception:
        return []
