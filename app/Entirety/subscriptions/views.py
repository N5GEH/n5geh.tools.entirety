from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.base import Status

from subscriptions.models import Subscription, SubscriptionList
from subscriptions.forms import SubscriptionForm
from projects.mixins import ProjectContextMixin


class List(ProjectContextMixin, ListView):
    model = Subscription
    template_name = "subscriptions/subscription_list.html"

    def get_queryset(self):
        data = []
        qs = super().get_queryset().filter(project_id=self.project.uuid)
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            for sub in qs:
                cb_sub = cb_client.get_subscription(sub.uuid)
                sub.description = cb_sub.description
                sub.status = cb_sub.status
                data.append(sub)
        return data


class Update(ProjectContextMixin, UpdateView):
    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = SubscriptionForm


class Create(ProjectContextMixin, CreateView):
    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = SubscriptionForm

    def get_success_url(self):
        return reverse("projects:subscriptions:list")
