from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from filip.clients.ngsi_v2 import ContextBrokerClient, QuantumLeapClient, IoTAClient
from filip.models import FiwareHeader

from .forms import ProjectForm
from .mixins import ProjectCreateMixin, ProjectSelfMixin, ProjectBaseMixin
from .models import Project


class Index(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/index.html"

    def get_queryset(self):
        if self.request.user.is_server_admin:
            return Project.objects.order_by("date_modified").filter(
                name__icontains=self.request.GET.get("search", default="")
            )
        elif self.request.user.is_project_admin:
            return Project.objects.order_by("date_modified").filter(
                name__icontains=self.request.GET.get("search", default=""),
                owner=self.request.user,
            ) | Project.objects.order_by("date_modified").filter(
                name__icontains=self.request.GET.get("search", default=""),
                users=self.request.user,
            )
        else:
            return Project.objects.order_by("date_modified").filter(
                name__icontains=self.request.GET.get("search", default=""),
                users=self.request.user,
            )


class Detail(ProjectBaseMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"

    def test_func(self):
        accessed_project = Project.objects.get(pk=self.kwargs["pk"])
        return (
            accessed_project.is_owner(user=self.request.user)
            or accessed_project.is_user(user=self.request.user)
            or self.request.user.is_server_admin
        )


class Update(ProjectSelfMixin, UpdateView):
    model = Project
    template_name = "projects/update.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse("projects:index")

    def get_form_kwargs(self):
        kwargs = super(Update, self).get_form_kwargs()
        kwargs["user"] = self.request.user
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
        return reverse("projects:index")

    def get_form_kwargs(self):
        kwargs = super(Create, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class Delete(ProjectSelfMixin, DeleteView):
    model = Project
    template_name = "projects/index.html"

    def get_success_url(self):
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


def _get_status(client, url, request):
    with client(
        url=url,
        fiware_header=FiwareHeader(service="", service_path=""),
    ) as fiware_client:
        try:
            version = fiware_client.get_version()
            if version:
                return render(request, "good_health.html")
        except:
            return render(request, "bad_health.html")
