import logging

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.conf import settings

logger = logging.getLogger(__name__)


class CustomOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(CustomOIDCAB, self).create_user(claims)

        return self.__set_user_values(user, claims)

    def update_user(self, user, claims):
        return self.__set_user_values(user, claims)

    def __set_user_values(self, user, claims):
        logger.info(
            user.first_name
            + " is accessing with roles "
            + claims.get("roles").__str__()
        )
        roles = claims.get("roles", [])

        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.username = claims.get("preferred_username", "")

        user.is_superuser = user.is_staff = settings.OIDC_SUPER_ADMIN_ROLE in roles
        user.is_server_admin = settings.OIDC_SERVER_ADMIN_ROLE in roles
        user.is_project_admin = settings.OIDC_PROJECT_ADMIN_ROLE in roles

        # Overwriting password field in model also possible (allow None),
        # but then additional testing for local authentication is needed (None not allowed for local users)
        user.password = "This is not a real password!"

        user.save()

        return user

    def verify_claims(self, claims):
        logger.info(claims.get("given_name") + " is verifying claim")
        verified = super(CustomOIDCAB, self).verify_claims(claims)
        is_user = settings.OIDC_USER_ROLE in claims.get(
            settings.OIDC_TOKEN_ROLE_FIELD, []
        )
        return verified and is_user
