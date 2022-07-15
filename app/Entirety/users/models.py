from django.contrib.auth.models import AbstractUser
from django.db import models


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
