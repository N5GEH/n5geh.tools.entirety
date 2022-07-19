from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .forms import ProjectForm
from .mixins import ProjectCreateMixin, ProjectSelfMixin
from .models import Project


class Index(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        projects = Project.objects.filter(
            name__icontains=request.GET.get("search", default="")
        )
        context = {
            "project_list": projects,
            "add_project": (user.is_project_admin or user.is_server_admin),
        }
        return render(request, "projects/index.html", context)


class Update(LoginRequiredMixin, ProjectSelfMixin, UpdateView):
    model = Project
    template_name = "projects/detail.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse("projects:index")


class Create(LoginRequiredMixin, ProjectCreateMixin, CreateView):
    model = Project
    template_name = "projects/detail.html"
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
