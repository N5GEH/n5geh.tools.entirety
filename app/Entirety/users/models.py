from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_server_admin = models.BooleanField(default=False)
    is_project_admin = models.BooleanField(default=False)
