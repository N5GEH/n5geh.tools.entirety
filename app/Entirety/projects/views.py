from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView, \
    DeleteView

from .forms import ProjectForm
from .models import Project


class Index(View):
    def get(self, request):
        projects = Project.objects.filter(
            name__icontains=request.GET.get('search', default=""))
        context = {'project_list': projects}
        return render(request, 'projects/index.html', context)


class Update(UpdateView):
    model = Project
    template_name = 'projects/detail.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse("projects:index")


class Create(CreateView):
    model = Project
    template_name = 'projects/detail.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse("projects:index")


class Delete(DeleteView):
    model = Project
    template_name = 'projects/index.html'

    def get_success_url(self):
        return reverse("projects:index")
