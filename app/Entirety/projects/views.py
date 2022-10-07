from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from filip.clients.ngsi_v2 import ContextBrokerClient, QuantumLeapClient, IoTAClient
from filip.models import FiwareHeader

from .forms import ProjectForm
from .mixins import ProjectCreateMixin, ProjectSelfMixin, ApplicationLoadMixin
from .models import Project


class Index(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/index.html"

    def get_queryset(self):
        return Project.objects.order_by("date_modified").filter(
            name__icontains=self.request.GET.get("search", default="")
        )

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context["view_permissions"] = (
            self.request.user.is_project_admin or self.request.user.is_server_admin
        )
        return context


class Detail(LoginRequiredMixin, ApplicationLoadMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"


class Update(LoginRequiredMixin, ProjectSelfMixin, ApplicationLoadMixin, UpdateView):
    model = Project
    template_name = "projects/update.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse("projects:index")


class Create(LoginRequiredMixin, ProjectCreateMixin, CreateView):
    model = Project
    template_name = "projects/update.html"
    form_class = ProjectForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super(Create, self).form_valid(form)

    def get_success_url(self):
        return reverse("projects:index")


class Delete(LoginRequiredMixin, ProjectSelfMixin, DeleteView):
    model = Project
    template_name = "projects/index.html"

    def get_success_url(self):
        return reverse("projects:index")


def broker(request):
    with ContextBrokerClient(
        url=settings.CB_URL,
        fiware_header=FiwareHeader(service="", service_path=""),
    ) as cb_client:
        try:
            version = cb_client.get_version()
            if version:
                return HttpResponse(
                    "<i class='bi bi-lightbulb-fill icon-green'></i>"
                    "<small class='d-none d-md-inline-flex text-sm-end'>Orion Broker</small>"
                )
        except:
            return HttpResponse(
                "<i class='bi bi-lightbulb-fill icon-red'></i>"
                "<small class='d-none d-md-inline-flex text-sm-end'>Orion Broker</small>"
            )


def ql(request):
    with QuantumLeapClient(
        url=settings.QL_URL,
        fiware_header=FiwareHeader(service="", service_path=""),
    ) as ql_client:
        try:
            version = ql_client.get_version()
            if version:
                return HttpResponse(
                    "<i class='bi bi-lightbulb-fill icon-green'></i>"
                    "<small class='d-none d-md-inline-flex'>Quantum Leap</small>"
                )
        except:
            return HttpResponse(
                "<i class='bi bi-lightbulb-fill icon-red'></i>"
                "<small class='d-none d-md-inline-flex'>Quantum Leap</small>"
            )


def iota(request):
    with IoTAClient(
        url=settings.IOTA_URL,
        fiware_header=FiwareHeader(service="", service_path=""),
    ) as iota_client:
        try:
            version = iota_client.get_version()
            if version:
                return HttpResponse(
                    "<i class='bi bi-lightbulb-fill icon-green'></i>"
                    "<small class='d-none d-md-inline-flex text-sm-end'>IOT Agent</small>"
                )
        except:
            return HttpResponse(
                "<i class='bi bi-lightbulb-fill icon-red'></i>"
                "<small class='d-none d-md-inline-flex text-sm-end'>IOT Agent</small>"
            )
