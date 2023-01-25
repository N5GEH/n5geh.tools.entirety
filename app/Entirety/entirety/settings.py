import os

from pathlib import Path
from typing import List, Any, Optional, Sequence
from mimetypes import add_type

import django_loki
import dj_database_url
from pydantic import BaseSettings, Field, AnyUrl, validator, DirectoryPath
from pydantic_settings import PydanticSettings
from pydantic_settings.database import DatabaseDsn
from pydantic_settings.settings import (
    DatabaseSettings,
    PydanticSettings,
    TemplateBackendModel,
)
from utils.generators import generate_secret_key
from django.contrib.messages import constants as messages

__version__ = "0.4.0"


class Databases(DatabaseSettings):
    DEFAULT: DatabaseDsn = Field(
        env="DATABASE_URL", default="postgres://username:password@host:port/db"
    )

    @validator("DEFAULT", pre=True)
    def set_url(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            os.environ["DATABASE_URL"] = v
            return v
        else:
            raise Exception

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class LokiSettings(BaseSettings):
    LOKI_ENABLE: str = Field(default=False, env="LOKI_ENABLE")
    LOKI_LEVEL: str = Field(default="INFO", env="LOKI_LEVEL")
    LOKI_PORT: int = Field(default=3100, env="LOKI_PORT")
    LOKI_TIMEOUT: float = Field(default=0.5, env="LOKI_TIMEOUT")
    LOKI_PROTOCOL: str = Field(default="http", env="LOKI_PROTOCOL")
    LOKI_SRC_HOST: str = Field(default="entirety", env="LOKI_SRC_HOST")
    LOKI_TIMEZONE: str = Field(default="Europe/Berlin", env="LOKI_TIMEZONE")
    LOKI_HOST: str = Field(default="localhost", env="LOKI_HOST")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class AuthenticationSettings(BaseSettings):
    LOCAL_AUTH = Field(default=True, env="LOCAL_AUTH")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class AppLoadSettings(BaseSettings):
    ENTITIES_LOAD: bool = Field(default=True, env="ENTITIES_LOAD")
    DEVICES_LOAD: bool = Field(default=True, env="DEVICES_LOAD")
    NOTIFICATIONS_LOAD: bool = Field(default=True, env="NOTIFICATIONS_LOAD")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(PydanticSettings):
    add_type("text/css", ".css", True)
    __auth = AuthenticationSettings()
    LOCAL_AUTH = __auth.LOCAL_AUTH
    LOKI = LokiSettings()
    APP_LOAD = AppLoadSettings()

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR: DirectoryPath = Path(__file__).resolve().parent.parent

    VERSION = __version__

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

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

    CRISPY_TEMPLATE_PACK = "bootstrap5"

    MIDDLEWARE: List[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    MESSAGE_TAGS = {
        messages.DEBUG: "alert-info",
        messages.INFO: "alert-info",
        messages.SUCCESS: "alert-success",
        messages.WARNING: "alert-warning",
        messages.ERROR: "alert-danger",
    }

    ROOT_URLCONF = "entirety.urls"
    FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
    TEMPLATES: List[TemplateBackendModel] = [
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

    WSGI_APPLICATION = "entirety.wsgi.application"

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

    AUTH_USER_MODEL = "users.User"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = "static/"

    STATICFILES_DIRS: List[DirectoryPath] = [
        os.path.join(BASE_DIR, "static"),
    ]

    STATICFILES_FINDERS: List[str] = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "compressor.finders.CompressorFinder",
    ]

    COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    if LOKI.LOKI_ENABLE:
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "loki": {
                    "class": "django_loki.LokiFormatter",
                    "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] "
                    "[%(funcName)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {"class": "logging.StreamHandler", "level": "DEBUG"},
                "loki": {
                    "level": LOKI.LOKI_LEVEL,
                    "class": "django_loki.LokiHttpHandler",
                    "host": LOKI.LOKI_HOST,
                    "formatter": "loki",
                    "port": LOKI.LOKI_PORT,
                    "timeout": LOKI.LOKI_TIMEOUT,
                    "protocol": LOKI.LOKI_PROTOCOL,
                    "source": "Loki",
                    "src_host": LOKI.LOKI_SRC_HOST,
                    "tz": LOKI.LOKI_TIMEZONE,
                },
            },
            "loggers": {
                "": {
                    "handlers": ["loki"],
                    "level": "INFO",
                },
            },
        }

    # Media location
    # https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files
    # -uploaded-by-a-user-during-development
    MEDIA_URL = "/media/"

    # Settings provided by environment
    SECRET_KEY: str = Field(default=generate_secret_key(), env="DJANGO_SECRET_KEY")

    @validator("SECRET_KEY")
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

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    DATABASES: Databases = Field({})

    LOGOUT_REDIRECT_URL: str = Field(default="/", env="LOGOUT_REDIRECT_URL")

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

    DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

    if APP_LOAD.ENTITIES_LOAD is True:
        INSTALLED_APPS.append("entities")
    if APP_LOAD.DEVICES_LOAD is True:
        INSTALLED_APPS.append("devices")
    if APP_LOAD.NOTIFICATIONS_LOAD is True:
        INSTALLED_APPS.append("subscriptions")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
