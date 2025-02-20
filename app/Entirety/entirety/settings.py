import os
import logging.config as LOG

from pathlib import Path
from typing import List, Any, Optional, Sequence, Union, Dict, ClassVar
from mimetypes import add_type

import django_loki
import dj_database_url
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    Field,
    AnyUrl,
    validator,
    DirectoryPath,
    field_validator,
    PostgresDsn,
)
from pydjantic import BaseDBConfig, to_django
from utils.generators import generate_secret_key
from django.contrib.messages import constants as messages

__version__ = "1.1.0"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: DirectoryPath = Path(__file__).resolve().parent.parent

# MIME type issue
add_type("text/css", ".css", False)


class PostgresDB(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DATABASE_",
    )
    ENGINE: str = "django.db.backends.postgresql"
    HOST: str = Field(default="localhost", alias="DATABASE_HOST")
    # TODO may need to add a new variable
    NAME: str = Field(default="postgres", alias="DATABASE_NAME")
    PASSWORD: str = Field(default="postgrespw", alias="DATABASE_PASSWORD")
    PORT: int = Field(default=5432, alias="DATABASE_PORT")
    USER: str = Field(default="postgres", alias="DATABASE_USER")
    OPTIONS: dict = Field(default={}, alias="DATABASE_OPTIONS")
    # TODO need to check
    CONN_MAX_AGE: int = Field(default=0, alias="DATABASE_CONN_MAX_AGE")


class Databases(BaseDBConfig):
    default: PostgresDB = PostgresDB()


class LokiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )
    LOKI_ENABLE: bool = Field(default=False, alias="LOKI_ENABLE")
    LOKI_LEVEL: str = Field(default="INFO", alias="LOKI_LEVEL")
    LOKI_PORT: int = Field(default=3100, alias="LOKI_PORT")
    LOKI_TIMEOUT: float = Field(default=0.5, alias="LOKI_TIMEOUT")
    LOKI_PROTOCOL: str = Field(default="http", alias="LOKI_PROTOCOL")
    LOKI_SRC_HOST: str = Field(default="entirety", alias="LOKI_SRC_HOST")
    LOKI_TIMEZONE: str = Field(default="Europe/Berlin", alias="LOKI_TIMEZONE")
    LOKI_HOST: str = Field(default="localhost", alias="LOKI_HOST")


class AuthenticationSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )
    LOCAL_AUTH: bool = Field(default=True, alias="LOCAL_AUTH")


class AppLoadSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )

    ENTITIES_LOAD: bool = Field(default=True, alias="ENTITIES_LOAD")
    DEVICES_LOAD: bool = Field(default=True, alias="DEVICES_LOAD")
    NOTIFICATIONS_LOAD: bool = Field(default=True, alias="NOTIFICATIONS_LOAD")
    SEMANTICS_LOAD: bool = Field(default=True, alias="SEMANTICS_LOAD")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        # ignored_types=["ClassVar"]
    )
    __auth = AuthenticationSettings()
    LOCAL_AUTH: bool = __auth.LOCAL_AUTH
    LOKI: LokiSettings = LokiSettings()
    APP_LOAD: AppLoadSettings = AppLoadSettings()

    VERSION: str = __version__

    # Application definition
    INSTALLED_APPS: List[str] = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.forms",
        "django_jsonforms",
        "django_tables2",
        "compressor",
        "corsheaders",
        "crispy_forms",
        "crispy_bootstrap5",
        "projects",
        "examples",
        "users",
        "smartdatamodels",
    ]
    # TODO how to define constant variable
    CRISPY_ALLOWED_TEMPLATE_PACKS: str = "bootstrap5"

    CRISPY_TEMPLATE_PACK: str = "bootstrap5"

    MIDDLEWARE: List[str] = [
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    MESSAGE_TAGS: dict = {
        messages.DEBUG: "alert-info",
        messages.INFO: "alert-info",
        messages.SUCCESS: "alert-success",
        messages.WARNING: "alert-warning",
        messages.ERROR: "alert-danger",
    }

    ROOT_URLCONF: str = "entirety.urls"
    FORM_RENDERER: str = "django.forms.renderers.TemplatesSetting"
    TEMPLATES: List[Dict] = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION: str = "entirety.wsgi.application"

    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS: List[dict] = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    AUTH_USER_MODEL: str = "users.User"

    USE_I18N: bool = True

    USE_TZ: bool = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL: str = "static/"

    STATICFILES_DIRS: List[DirectoryPath] = [
        os.path.join(BASE_DIR, "static"),
    ]

    STATICFILES_FINDERS: List[str] = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "compressor.finders.CompressorFinder",
    ]

    COMPRESS_PRECOMPILERS: tuple = (("text/x-scss", "django_libsass.SassCompiler"),)

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

    LOGGING_CONFIG: Union[str, None] = None

    # TODO more structured annotation
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

    LOGGER: ClassVar
    HANDLER: ClassVar

    if LOKI.LOKI_ENABLE is True:
        for LOGGER in LOGGERS:
            LOGGERS[LOGGER]["handlers"] = ["loki"]
        HANDLER = {
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
        for LOGGER in LOGGERS:
            LOGGERS[LOGGER]["handlers"] = ["console"]
        HANDLER = {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "default",
            }
        }

    LOGGING: dict = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] "
                "[%(funcName)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": HANDLER,
        "loggers": LOGGERS,
    }

    LOG.dictConfig(LOGGING)

    # Media location
    # https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files
    # -uploaded-by-a-user-during-development
    MEDIA_URL: str = "/media/"

    # Settings provided by environment
    SECRET_KEY: str = Field(default=generate_secret_key(), alias="DJANGO_SECRET_KEY")

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
    DEBUG: bool = Field(default=False, alias="DJANGO_DEBUG")

    ALLOWED_HOSTS: List = Field(default=["*"], alias="ALLOWED_HOSTS")

    CB_URL: AnyUrl = Field(default="http://localhost:1026", alias="CB_URL")
    MQTT_BASE_TOPIC: str = Field(default="/Entirety", alias="MQTT_BASE_TOPIC")

    QL_URL: AnyUrl = Field(default="http://localhost:8668", alias="QL_URL")

    IOTA_URL: AnyUrl = Field(default="http://localhost:4041", alias="IOTA_URL")

    # CSRF
    CSRF_TRUSTED_ORIGINS: list = Field(default=[], alias="CSRF_TRUSTED_ORIGINS ")

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    DATABASES: Databases = Databases()

    LOGIN_REDIRECT_URL: str = Field(default="/", alias="LOGIN_REDIRECT_URL")
    LOGIN_URL: str = Field(default="/accounts/login", alias="LOGIN_URL")
    LOGOUT_REDIRECT_URL: str = Field(default="/", alias="LOGOUT_REDIRECT_URL")

    if not __auth.LOCAL_AUTH:
        INSTALLED_APPS.append("mozilla_django_oidc")
        MIDDLEWARE.append("mozilla_django_oidc.middleware.SessionRefresh")
        AUTHENTICATION_BACKENDS: Sequence[str] = ("entirety.oidc.CustomOIDCAB",)

        OIDC_LOGIN_URL: str = Field(
            default="/oidc/authenticate", alias="OIDC_LOGIN_URL"
        )
        LOGIN_URL = OIDC_LOGIN_URL

        OIDC_LOGIN_REDIRECT_URL: str = Field(
            default="/oidc/callback/", alias="OIDC_LOGIN_REDIRECT_URL"
        )
        LOGIN_REDIRECT_URL = OIDC_LOGIN_REDIRECT_URL

        OIDC_LOGOUT_REDIRECT_URL: str = Field(
            default="/", alias="OIDC_LOGOUT_REDIRECT_URL"
        )
        LOGOUT_REDIRECT_URL = OIDC_LOGOUT_REDIRECT_URL

        OIDC_RP_SIGN_ALGO: str = Field(default="RS256", alias="OIDC_RP_SIGN_ALGO")
        OIDC_OP_JWKS_ENDPOINT: str = Field(alias="OIDC_OP_JWKS_ENDPOINT")

        OIDC_RP_CLIENT_ID: str = Field(alias="OIDC_RP_CLIENT_ID")
        OIDC_RP_CLIENT_SECRET: str = Field(alias="OIDC_RP_CLIENT_SECRET")
        OIDC_OP_AUTHORIZATION_ENDPOINT: str = Field(
            alias="OIDC_OP_AUTHORIZATION_ENDPOINT"
        )
        OIDC_OP_TOKEN_ENDPOINT: str = Field(alias="OIDC_OP_TOKEN_ENDPOINT")
        OIDC_OP_USER_ENDPOINT: str = Field(alias="OIDC_OP_USER_ENDPOINT")
        OIDC_OP_LOGOUT_ENDPOINT: str = Field(alias="OIDC_OP_LOGOUT_ENDPOINT")
        OIDC_OP_LOGOUT_URL_METHOD: str = Field(
            default="users.views.provider_logout", alias="OIDC_OP_LOGOUT_URL_METHOD"
        )
        OIDC_STORE_ID_TOKEN: bool = Field(default=True, alias="OIDC_STORE_ID_TOKEN")

        OIDC_SUPER_ADMIN_ROLE: str = Field(
            default="super_admin", alias="OIDC_SUPER_ADMIN_ROLE"
        )
        OIDC_SERVER_ADMIN_ROLE: str = Field(
            default="server_admin", alias="OIDC_SERVER_ADMIN_ROLE"
        )
        OIDC_PROJECT_ADMIN_ROLE: str = Field(
            default="project_admin", alias="OIDC_PROJECT_ADMIN_ROLE"
        )
        OIDC_USER_ROLE: str = Field(default="user", alias="OIDC_USER_ROLE")
        OIDC_TOKEN_ROLE_PATH: str = Field(
            default="$.entirety.roles", alias="OIDC_TOKEN_ROLE_PATH"
        )

    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE: str = Field(default="en-us", alias="LANGUAGE_CODE")

    STATIC_ROOT: DirectoryPath = Field(
        default=os.path.join(BASE_DIR, "static/"), alias="STATIC_ROOT"
    )
    MEDIA_ROOT: DirectoryPath = Field(
        default=os.path.join(BASE_DIR, "media/"), alias="MEDIA_ROOT"
    )

    TIME_ZONE: str = Field(default="Europe/Berlin", alias="TIME_ZONE")

    COMPRESS_ENABLED: bool = Field(default=not DEBUG, alias="COMPRESS_ENABLED")

    DJANGO_TABLES2_TEMPLATE: str = "django_tables2/bootstrap4.html"

    if APP_LOAD.ENTITIES_LOAD is True:
        INSTALLED_APPS.append("entities")
    if APP_LOAD.DEVICES_LOAD is True:
        INSTALLED_APPS.append("devices")
    if APP_LOAD.NOTIFICATIONS_LOAD is True:
        INSTALLED_APPS.append("subscriptions")
    if APP_LOAD.SEMANTICS_LOAD is True:

        INSTALLED_APPS.append("semantics")


to_django(settings=Settings())
