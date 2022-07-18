import os

from pathlib import Path
from typing import List
from mimetypes import add_type
from pydantic import BaseSettings, Field, AnyUrl, validator

from utils.generators import generate_secret_key

__version__ = "0.2.0"


class Settings(BaseSettings):
    add_type("text/css", ".css", True)
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    VERSION = __version__

    # Application definition
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "mozilla_django_oidc",
        "compressor",
        "crispy_forms",
        "crispy_bootstrap5",
        "projects.apps.ProjectsConfig",
        "examples.apps.ExamplesConfig",
        "users.apps.UsersConfig",
        "alarming.apps.AlarmingConfig",
    ]

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

    CRISPY_TEMPLATE_PACK = "bootstrap5"

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "mozilla_django_oidc.middleware.SessionRefresh",
    ]

    ROOT_URLCONF = "entirety.urls"

    TEMPLATES = [
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

    AUTH_PASSWORD_VALIDATORS = [
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

    AUTHENTICATION_BACKENDS = ("entirety.oidc.CustomOIDCAB",)
    AUTH_USER_MODEL = "users.User"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = "static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "compressor.finders.CompressorFinder",
    ]

    COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

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
                "level": "DEBUG",
                "class": "django_loki.LokiHttpHandler",
                "host": "localhost",
                "formatter": "loki",
                "port": 3100,
                "timeout": 0.5,
                "protocol": "http",
                "source": "Loki",
                "src_host": "entirety",
                "tz": "UTC",
            },
        },
        "loggers": {
            "mozilla_django_oidc": {"handlers": ["console"], "level": "DEBUG"},
            "django": {
                "handlers": ["loki"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

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

    ALLOWED_HOSTS: List = Field(default=[], env="ALLOWED_HOSTS")

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    # TODO
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    LOGIN_URL: str = Field(default="/oidc/authenticate", env="LOGIN_URL")

    LOGIN_REDIRECT_URL: str = Field(default="/oidc/callback/", env="LOGIN_REDIRECT_URL")
    LOGOUT_REDIRECT_URL: str = Field(default="/", env="LOGOUT_REDIRECT_URL")

    OIDC_RP_SIGN_ALGO: str = Field(default="RS256", env="OIDC_RP_SIGN_ALGO")
    OIDC_OP_JWKS_ENDPOINT: str = Field(env="OIDC_OP_JWKS_ENDPOINT")

    OIDC_RP_CLIENT_ID: str = Field(env="OIDC_RP_CLIENT_ID")
    OIDC_RP_CLIENT_SECRET: str = Field(env="OIDC_RP_CLIENT_SECRET")
    OIDC_OP_AUTHORIZATION_ENDPOINT: str = Field(env="OIDC_OP_AUTHORIZATION_ENDPOINT")
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

    TIME_ZONE: str = Field(default="Europe/Berlin", env="TIME_ZONE")

    COMPRESS_ENABLED: bool = Field(default=not DEBUG, env="COMPRESS_ENABLED")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
