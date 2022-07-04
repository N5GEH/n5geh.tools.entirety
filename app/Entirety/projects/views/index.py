from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user

        context = {"add_project": user.is_project_admin}
        return render(request, "index.html", context)
