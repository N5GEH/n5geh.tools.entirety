from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(CustomOIDCAB, self).create_user(claims)

        return self.__set_user_values(user, claims)

    def update_user(self, user, claims):
        return self.__set_user_values(user, claims)

    def __set_user_values(self, user, claims):
        roles = claims.get("roles", [])

        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.username = claims.get("preferred_username", "")

        user.is_superuser = user.is_staff = "super_admin" in roles
        user.is_server_admin = "server_admin" in roles
        user.is_project_admin = "project_admin" in roles

        user.save()

        return user

    def verify_claims(self, claims):
        verified = super(CustomOIDCAB, self).verify_claims(claims)
        is_user = "user" in claims.get("roles", [])
        return verified and is_user
