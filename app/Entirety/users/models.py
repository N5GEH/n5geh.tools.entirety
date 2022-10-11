from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    is_server_admin = models.BooleanField(
        default=False,
        help_text="User can create and update projects for any project admin.",
        verbose_name="server admin status",
    )
    is_project_admin = models.BooleanField(
        default=False,
        help_text="User can create projects and update self created.",
        verbose_name="project admin status",
    )
    if settings.LOCAL_AUTH:
        objects = UserManager()
