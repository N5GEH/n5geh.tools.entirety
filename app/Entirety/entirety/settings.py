import os
import logging.config as LOG

from pathlib import Path
from typing import List, Any, Optional, Sequence, Union, Dict
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
from entirety.settings_pydantic import entirety_settings
from utils.generators import generate_secret_key
from django.contrib.messages import constants as messages


__version__ = "1.1.0"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: DirectoryPath = Path(__file__).resolve().parent.parent

add_type("text/css", ".css", True)

LOCAL_AUTH = entirety_settings.LOCAL_AUTH
LOKI = entirety_settings.LOKI.model_dump()
APP_LOAD = entirety_settings.APP_LOAD.model_dump()

VERSION = __version__

# Application definition
INSTALLED_APPS: List[str] = entirety_settings.INSTALLED_APPS

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE: List[str] = entirety_settings.MIDDLEWARE

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

ROOT_URLCONF = "entirety.urls"
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
TEMPLATES: List[dict] = [
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
    }
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

LOGGING_CONFIG: Union[str, None] = None

LOGGERS = entirety_settings.LOGGERS
HANDLER = entirety_settings.HANDLER

LOGGING = {
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
MEDIA_URL = "/media/"

# Settings provided by environment
SECRET_KEY: str = entirety_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = entirety_settings.DEBUG

ALLOWED_HOSTS: List = entirety_settings.ALLOWED_HOSTS

CB_URL: AnyUrl = entirety_settings.CB_URL
MQTT_BASE_TOPIC: str = entirety_settings.MQTT_BASE_TOPIC

QL_URL: AnyUrl = entirety_settings.QL_URL

IOTA_URL: AnyUrl = entirety_settings.IOTA_URL

# CSRF
CSRF_TRUSTED_ORIGINS: list = entirety_settings.CSRF_TRUSTED_ORIGINS

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = entirety_settings.DATABASES.model_dump()

# TODO double check
if entirety_settings.LOCAL_AUTH:
    LOGIN_REDIRECT_URL: str = entirety_settings.LOGIN_REDIRECT_URL
else:
    # INSTALLED_APPS.append("mozilla_django_oidc")  # remove
    # MIDDLEWARE.append("mozilla_django_oidc.middleware.SessionRefresh")  # remove
    AUTHENTICATION_BACKENDS: Sequence[str] = ("entirety.oidc.CustomOIDCAB",)

    LOGIN_URL: str = entirety_settings.LOGIN_URL

    LOGIN_REDIRECT_URL: str = entirety_settings.LOGIN_REDIRECT_URL

    OIDC_RP_SIGN_ALGO: str = entirety_settings.OIDC_RP_SIGN_ALGO
    OIDC_OP_JWKS_ENDPOINT: str = entirety_settings.OIDC_OP_JWKS_ENDPOINT

    OIDC_RP_CLIENT_ID: str = entirety_settings.OIDC_RP_CLIENT_ID
    OIDC_RP_CLIENT_SECRET: str = entirety_settings.OIDC_RP_CLIENT_SECRET
    OIDC_OP_AUTHORIZATION_ENDPOINT: str = (
        entirety_settings.OIDC_OP_AUTHORIZATION_ENDPOINT
    )
    OIDC_OP_TOKEN_ENDPOINT: str = entirety_settings.OIDC_OP_TOKEN_ENDPOINT
    OIDC_OP_USER_ENDPOINT: str = entirety_settings.OIDC_OP_USER_ENDPOINT

    OIDC_SUPER_ADMIN_ROLE: str = entirety_settings.OIDC_SUPER_ADMIN_ROLE
    OIDC_SERVER_ADMIN_ROLE: str = entirety_settings.OIDC_SERVER_ADMIN_ROLE
    OIDC_PROJECT_ADMIN_ROLE: str = entirety_settings.OIDC_PROJECT_ADMIN_ROLE
    OIDC_USER_ROLE: str = entirety_settings.OIDC_USER_ROLE
    OIDC_TOKEN_ROLE_FIELD: str = entirety_settings.OIDC_TOKEN_ROLE_FIELD

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE: str = entirety_settings.LANGUAGE_CODE

STATIC_ROOT: DirectoryPath = entirety_settings.STATIC_ROOT
MEDIA_ROOT: DirectoryPath = entirety_settings.MEDIA_ROOT

TIME_ZONE: str = entirety_settings.TIME_ZONE

COMPRESS_ENABLED: bool = entirety_settings.COMPRESS_ENABLED

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"
