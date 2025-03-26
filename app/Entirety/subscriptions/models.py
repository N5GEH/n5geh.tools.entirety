from django.db import models
from projects.models import Project


class Subscription(models.Model):
    uuid = models.CharField(unique=True, max_length=64, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid

    class Meta:
        ordering = ["uuid"]
