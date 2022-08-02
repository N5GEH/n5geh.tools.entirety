from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView
import json
from django.shortcuts import HttpResponse

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.subscriptions import Subscription as CBSubscription

from subscriptions.models import Subscription
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

    def form_valid(self, form, *args, **kwargs):
        instance = form.save(commit=False)

        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            cb_sub = cb_client.get_subscription(instance.pk)
            cb_sub.description = form.cleaned_data["description"]
            cb_client.update_subscription(cb_sub)

        return super(Update, self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            "projects:subscriptions:list", kwargs={"project_id": self.project.uuid}
        )


class Create(ProjectContextMixin, CreateView):
    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = SubscriptionForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.project = self.project
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            cb_sub = CBSubscription()
            cb_sub.description = form.cleaned_data["description"]
            cb_sub = cb_client.post_subscription(cb_sub)
            instance.pk = cb_sub.uuid

        return super(Create, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "projects:subscriptions:list", kwargs={"project_id": self.project.uuid}
        )
