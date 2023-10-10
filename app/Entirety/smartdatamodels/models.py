from django.core.exceptions import ValidationError
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
    jsonschema = models.JSONField(verbose_name="json schema", null=True)
    schema_link = models.URLField(verbose_name="schema URL", null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="last_modified_by"
    )

    def clean(self):
        if not self.jsonschema and not self.schema_link:
            raise ValidationError(
                f"One of schema URL and json schema must be specified."
            )

    def __str__(self):
        return self.name
