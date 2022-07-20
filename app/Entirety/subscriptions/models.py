from django.db import models
from filip.models.ngsi_v2.subscriptions import Subscription as CBSubscription
from utils.generators import generate_uuid
from projects.models import Project
from subscriptions.managers import SubscriptionsManager


class Subscription(models.Model):
    default_manager = SubscriptionsManager()
    uuid = models.CharField(
        unique=True, max_length=64, primary_key=True
    )  # later uuid from cb
    name = models.CharField(max_length=64)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    description: str
    active: bool

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
