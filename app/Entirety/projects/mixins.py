from django.core.exceptions import PermissionDenied
from projects.models import Project
from django.shortcuts import get_object_or_404


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
