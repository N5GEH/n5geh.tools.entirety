from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

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
