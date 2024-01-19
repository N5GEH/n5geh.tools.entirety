from abc import ABC

from django.apps import apps
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from projects.models import Project


class ApplicationLoadMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["entities_load"] = apps.is_installed("entities")
        context["devices_load"] = apps.is_installed("devices")
        context["notifications_load"] = apps.is_installed("subscriptions")
        context["semantics_load"] = apps.is_installed("semantics")

        return context


class ProjectBaseMixin(
    LoginRequiredMixin, UserPassesTestMixin, ApplicationLoadMixin, ABC
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["project_permissions"] = (
            self.request.user.is_project_admin or self.request.user.is_server_admin
        )

        return context


class ProjectContextMixin(ProjectBaseMixin):
    project: Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["project"] = self.project

        return context

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs.get("project_id", None))

        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return (
            self.project.is_owner(user=self.request.user)
            or self.project.is_user(user=self.request.user)
            or self.request.user.is_server_admin
            or self.project.is_maintainer(self.request.user)
        )


class ProjectSelfMixin(ProjectBaseMixin):
    def test_func(self):
        obj = self.get_object()
        return (
            (self.request.user.is_project_admin and obj.owner == self.request.user)
            or self.request.user.is_server_admin
            or obj.is_maintainer(self.request.user)
        )


class ProjectContextAndViewOnlyMixin(ProjectContextMixin):
    def test_func(self):
        super_test_func = super().test_func()
        return super_test_func, self.project.is_viewer(self.request.user)


class ProjectCreateMixin(ProjectBaseMixin):
    def test_func(self):
        return self.request.user.is_project_admin or self.request.user.is_server_admin
