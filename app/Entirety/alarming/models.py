from django.db import models

from utils.generators import generate_uuid

from projects.models import Project


class Subscription(models.Model):
    uuid = models.CharField(
        unique=True, max_length=64, default=generate_uuid, primary_key=True
    )  # later uuid from cb
    name = models.CharField(max_length=64)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
