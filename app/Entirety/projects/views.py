import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from filip.clients.ngsi_v2 import ContextBrokerClient, QuantumLeapClient, IoTAClient
from filip.models.base import FiwareHeaderSecure

from users.services import client_token_service
from utils.auth import get_fiware_services
from .forms import ProjectForm
from .mixins import ProjectCreateMixin, ProjectSelfMixin, ProjectBaseMixin
from .models import Project

logger = logging.getLogger(__name__)


class Index(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/index.html"

    def get_queryset(self):
        logger.info(
            "Fetching projects for "
            + str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
        )
        search_query = self.request.GET.get("search", default="")
        qs = Project.objects.filter(name__icontains=search_query)

        if not settings.LOCAL_AUTH:
            fiware_services = get_fiware_services(self.request)
            qs = qs.filter(fiware_service__in=fiware_services)

        # Apply user role filters
        user = self.request.user
        if user.is_server_admin:
            return qs.order_by("-date_modified")

        elif user.is_project_admin:
            # Projects where user is owner, users, maintainers, or viewers
            return (
                qs.filter(owner=user).distinct()
                | qs.filter(users=user).distinct()
                | qs.filter(maintainers=user).distinct()
                | qs.filter(viewers=user).distinct()
            ).order_by("-date_modified")

        else:
            # Regular user: users, maintainers, viewers
            return (
                qs.filter(users=user).distinct()
                | qs.filter(maintainers=user).distinct()
                | qs.filter(viewers=user).distinct()
            ).order_by("-date_modified")


class Detail(ProjectBaseMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get(self, request, *args, **kwargs):
        _render = super(Detail, self).get(request, *args, **kwargs)
        logger.info(
            str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + f" view project {self.object.name}"
        )
        return _render

    def test_func(self):
        accessed_project = Project.objects.get(pk=self.kwargs["pk"])
        return (
            accessed_project.is_owner(user=self.request.user)
            or accessed_project.is_user(user=self.request.user)
            or accessed_project.is_maintainer(user=self.request.user)
            or accessed_project.is_viewer(user=self.request.user)
            or self.request.user.is_server_admin
        )


class Update(ProjectSelfMixin, UpdateView):
    model = Project
    template_name = "projects/update.html"
    form_class = ProjectForm

    def get_success_url(self):
        logger.info(
            str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + " has updated the project "
            + self.object.name
        )
        return reverse("projects:detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(Update, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["request"] = self.request
        return kwargs


class Create(ProjectCreateMixin, CreateView):
    model = Project
    template_name = "projects/update.html"
    form_class = ProjectForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super(Create, self).form_valid(form)

    def get_success_url(self):
        logger.info(
            str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + " has created the project "
            + self.object.name
        )
        return reverse("projects:detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(Create, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["request"] = self.request
        return kwargs


class Delete(ProjectSelfMixin, DeleteView):
    model = Project
    template_name = "projects/index.html"

    def get_success_url(self):
        logger.info(
            str(
                self.request.user.first_name
                if self.request.user.first_name
                else self.request.user.username
            )
            + " has deleted the project "
            + self.object.name
        )
        return reverse("projects:index")


class BrokerHealth(View):
    def get(self, request, *args, **kwargs):
        return _get_status(ContextBrokerClient, settings.CB_URL, request)


class QLHealth(View):
    def get(self, request, *args, **kwargs):
        return _get_status(QuantumLeapClient, settings.QL_URL, request)


class IOTAHealth(View):
    def get(self, request, *args, **kwargs):
        return _get_status(IoTAClient, settings.IOTA_URL, request)


from filip.clients.exceptions import BaseHttpClientException


def _get_status(client_cls, url, request):
    try:
        token = None
        if not settings.LOCAL_AUTH:
            token = client_token_service.get_token()

        fiware_header_kwargs = {
            "service": "entirety",
            "service_path": "/",
        }
        if token:
            fiware_header_kwargs["authorization"] = f"Bearer {token}"

        fiware_header = FiwareHeaderSecure(**fiware_header_kwargs)
        with client_cls(url=url, fiware_header=fiware_header) as fiware_client:
            version = fiware_client.get_version()

            if version:
                return render(request, "good_health.html")
            else:
                return render(request, "bad_health.html")

    except BaseHttpClientException as e:
        return render(request, "bad_health.html")

    except Exception as e:
        return render(request, "bad_health.html")
