import os

from pathlib import Path
from typing import List, Sequence

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl, DirectoryPath, field_validator
from utils.generators import generate_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: DirectoryPath = Path(__file__).resolve().parent.parent


class PostgresDB(BaseSettings):
    ENGINE: str = "django.db.backends.postgresql"
    HOST: str = Field(default="localhost", env="DATABASE_HOST")
    # TODO may need to add a new variable "DATABASE_NAME"
    NAME: str = Field(default="postgres", env="DATABASE_NAME")
    PASSWORD: str = Field(default="postgrespw", env="DATABASE_PASSWORD")
    PORT: int = Field(default=5432, env="DATABASE_PORT")
    USER: str = Field(default="postgres", env="DATABASE_USER")
    OPTIONS: dict = Field(default={}, env="DATABASE_OPTIONS")


class Databases(BaseSettings):
    default: PostgresDB = PostgresDB()


class LokiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )
    LOKI_ENABLE: bool = Field(default=False, env="LOKI_ENABLE")
    LOKI_LEVEL: str = Field(default="INFO", env="LOKI_LEVEL")
    LOKI_PORT: int = Field(default=3100, env="LOKI_PORT")
    LOKI_TIMEOUT: float = Field(default=0.5, env="LOKI_TIMEOUT")
    LOKI_PROTOCOL: str = Field(default="http", env="LOKI_PROTOCOL")
    LOKI_SRC_HOST: str = Field(default="entirety", env="LOKI_SRC_HOST")
    LOKI_TIMEZONE: str = Field(default="Europe/Berlin", env="LOKI_TIMEZONE")
    LOKI_HOST: str = Field(default="localhost", env="LOKI_HOST")


loki_settings = LokiSettings()


class AuthenticationSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )
    LOCAL_AUTH: bool = Field(default=True, env="LOCAL_AUTH")


class AppLoadSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )

    ENTITIES_LOAD: bool = Field(default=True, env="ENTITIES_LOAD")
    DEVICES_LOAD: bool = Field(default=True, env="DEVICES_LOAD")
    NOTIFICATIONS_LOAD: bool = Field(default=True, env="NOTIFICATIONS_LOAD")
    SEMANTICS_LOAD: bool = Field(default=True, env="SEMANTICS_LOAD")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )
    __auth = AuthenticationSettings()
    LOCAL_AUTH: bool = __auth.LOCAL_AUTH
    LOKI: LokiSettings = loki_settings
    APP_LOAD: AppLoadSettings = AppLoadSettings()

    # TODO @sba check again
    LOGGERS: dict = {
        "projects.views": {
            "propagate": False,
            "level": "INFO",
        },
        "filip": {
            "propagate": False,
            "level": "INFO",
        },
        "entirety.oidc": {
            "propagate": False,
            "level": "INFO",
        },
        "entities.views": {
            "propagate": False,
            "level": "INFO",
        },
        "django.server": {
            "propagate": False,
            "level": "INFO",
        },
        "devices.views": {
            "propagate": False,
            "level": "INFO",
        },
        "subscriptions.views": {
            "propagate": False,
            "level": "INFO",
        },
    }

    @field_validator("LOGGERS")
    @classmethod
    def validate_logger(cls, v) -> dict:
        if loki_settings.LOKI_ENABLE is True:
            for LOGGER in v:
                v[LOGGER]["handlers"] = ["loki"]
        else:
            for LOGGER in v:
                v[LOGGER]["handlers"] = ["console"]
        return v

    HANDLER: dict = {}

    @field_validator("HANDLER")
    @classmethod
    def validate_handler(cls, v) -> dict:
        if loki_settings.LOKI_ENABLE is True:
            return {
                "loki": {
                    "level": "DEBUG",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(BASE_DIR, "logs/entirety_logs.log"),
                    "maxBytes": 1 * 1024 * 1024,
                    "backupCount": 2,
                    "formatter": "default",
                }
            }
        else:
            return {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "default",
                }
            }

    # Settings provided by environment
    SECRET_KEY: str = Field(default=generate_secret_key(), env="DJANGO_SECRET_KEY")

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_not_empty(cls, v) -> str:
        v_cleaned = v.strip()
        if not v_cleaned:
            v_cleaned = generate_secret_key()
        elif len(v_cleaned) < 32:
            raise ValueError("Django secret should be at least 32 characters long")
        return v_cleaned

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG: bool = Field(default=False, env="DJANGO_DEBUG")

    ALLOWED_HOSTS: List = Field(default=["*"], env="ALLOWED_HOSTS")

    CB_URL: AnyUrl = Field(default="http://localhost:1026", env="CB_URL")
    MQTT_BASE_TOPIC: str = Field(default="/Entirety", env="MQTT_BASE_TOPIC")

    QL_URL: AnyUrl = Field(default="http://localhost:8668", env="QL_URL")

    IOTA_URL: AnyUrl = Field(default="http://localhost:4041", env="IOTA_URL")

    # CSRF
    CSRF_TRUSTED_ORIGINS: list = Field(default=[], env="CSRF_TRUSTED_ORIGINS ")

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    DATABASES: Databases = Databases()

    LOGOUT_REDIRECT_URL: str = Field(default="/", env="LOGOUT_REDIRECT_URL")

    # Application definition
    INSTALLED_APPS: List[str] = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.forms",
        "django_tables2",
        "compressor",
        "crispy_forms",
        "crispy_bootstrap5",
        "projects",
        "examples",
        "users",
    ]

    MIDDLEWARE: List[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    if __auth.LOCAL_AUTH:
        LOGIN_REDIRECT_URL: str = Field(default="/", env="LOGIN_REDIRECT_URL")
    else:
        INSTALLED_APPS.append("mozilla_django_oidc")
        MIDDLEWARE.append("mozilla_django_oidc.middleware.SessionRefresh")
        AUTHENTICATION_BACKENDS: Sequence[str] = ("entirety.oidc.CustomOIDCAB",)

        LOGIN_URL: str = Field(default="/oidc/authenticate", env="LOGIN_URL")

        LOGIN_REDIRECT_URL: str = Field(
            default="/oidc/callback/", env="LOGIN_REDIRECT_URL"
        )

        OIDC_RP_SIGN_ALGO: str = Field(default="RS256", env="OIDC_RP_SIGN_ALGO")
        OIDC_OP_JWKS_ENDPOINT: str = Field(env="OIDC_OP_JWKS_ENDPOINT")

        OIDC_RP_CLIENT_ID: str = Field(env="OIDC_RP_CLIENT_ID")
        OIDC_RP_CLIENT_SECRET: str = Field(env="OIDC_RP_CLIENT_SECRET")
        OIDC_OP_AUTHORIZATION_ENDPOINT: str = Field(
            env="OIDC_OP_AUTHORIZATION_ENDPOINT"
        )
        OIDC_OP_TOKEN_ENDPOINT: str = Field(env="OIDC_OP_TOKEN_ENDPOINT")
        OIDC_OP_USER_ENDPOINT: str = Field(env="OIDC_OP_USER_ENDPOINT")

        OIDC_SUPER_ADMIN_ROLE: str = Field(
            default="super_admin", env="OIDC_SUPER_ADMIN_ROLE"
        )
        OIDC_SERVER_ADMIN_ROLE: str = Field(
            default="server_admin", env="OIDC_SERVER_ADMIN_ROLE"
        )
        OIDC_PROJECT_ADMIN_ROLE: str = Field(
            default="project_admin", env="OIDC_PROJECT_ADMIN_ROLE"
        )
        OIDC_USER_ROLE: str = Field(default="user", env="OIDC_USER_ROLE")
        OIDC_TOKEN_ROLE_FIELD: str = Field(default="roles", env="OIDC_TOKEN_ROLE_FIELD")

    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE: str = Field(default="en-us", env="LANGUAGE_CODE")

    STATIC_ROOT: DirectoryPath = Field(
        default=os.path.join(BASE_DIR, "cache/"), env="STATIC_ROOT"
    )
    MEDIA_ROOT: DirectoryPath = Field(
        default=os.path.join(BASE_DIR, "media/"), env="MEDIA_ROOT"
    )

    TIME_ZONE: str = Field(default="Europe/Berlin", env="TIME_ZONE")

    COMPRESS_ENABLED: bool = Field(default=not DEBUG, env="COMPRESS_ENABLED")

    if APP_LOAD.ENTITIES_LOAD is True:
        INSTALLED_APPS.append("entities")
    if APP_LOAD.DEVICES_LOAD is True:
        INSTALLED_APPS.append("devices")
    if APP_LOAD.NOTIFICATIONS_LOAD is True:
        INSTALLED_APPS.append("subscriptions")
    if APP_LOAD.SEMANTICS_LOAD is True:
        INSTALLED_APPS.append("semantics")


entirety_settings = Settings()
