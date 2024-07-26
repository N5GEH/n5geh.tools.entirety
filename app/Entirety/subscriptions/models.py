from django.db import models
from filip.models.ngsi_v2.subscriptions import Subscription as CBSubscription
from pydantic import Field
from typing import Optional
from utils.generators import generate_uuid
from projects.models import Project


class Subscription(models.Model):
    uuid = models.CharField(unique=True, max_length=64, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid

    class Meta:
        ordering = ["uuid"]
