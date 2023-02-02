from django.db import models

from users.models import User
from utils.generators import generate_uuid


class SmartDataModel(models.Model):
    uuid = models.CharField(
        unique=True, max_length=64, default=generate_uuid, primary_key=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, unique=True)
    jsonschema = models.JSONField(verbose_name="json schema")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="last_modified_by"
    )

    def __str__(self):
        return self.name
