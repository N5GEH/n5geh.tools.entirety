from django.shortcuts import render
from django.views.generic import View
from projects.models import Project


class Index(View):
    def get(self, request):
        projects = Project.objects.all()
        context = {'project_list': projects}
        return render(request, 'projects/index.html', context)
