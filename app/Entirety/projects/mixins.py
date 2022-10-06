from django.apps import apps
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from projects.models import Project


class ProjectContextMixin:
    project = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["project"] = self.project

        return context

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs.get("project_id", None))

        if not (
            self.project.is_owner(user=request.user)
            or self.project.is_user(user=request.user)
        ):
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)


class ApplicationLoadMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["entities_load"] = apps.is_installed("entities")
        context["devices_load"] = apps.is_installed("devices")
        context["notifications_load"] = apps.is_installed("alarming")

        return context


class ProjectSelfMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (
            self.request.user.is_project_admin and obj.owner == self.request.user
        ) or self.request.user.is_server_admin


class ProjectCreateMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_project_admin or self.request.user.is_server_admin
