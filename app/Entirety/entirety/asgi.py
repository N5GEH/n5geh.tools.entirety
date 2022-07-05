"""
ASGI config for entirety project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from pydantic_settings import SetUp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entirety.settings.Settings")
SetUp().configure()
application = get_asgi_application()
