from django.shortcuts import render
from django.views.generic import ListView

from alarming.models import Subscription
from projects.mixins import ProjectContextMixin


class SubscriptionList(ProjectContextMixin, ListView):
    model = Subscription

    def get_queryset(self):
        return Subscription.objects.filter(project=self.project)
