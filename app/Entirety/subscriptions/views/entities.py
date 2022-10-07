from django.shortcuts import render
from django.views.generic import View

from projects.mixins import ProjectContextMixin
from subscriptions import forms


class Entities(ProjectContextMixin, View):
    http_method_names = "post"

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()

        total = int(post["entity-TOTAL_FORMS"])
        post["entity-TOTAL_FORMS"] = total + 1
        request.POST = post

        entities = forms.Entities(request.POST, prefix="entity")

        return render(request, "subscriptions/entities.html", {"entities": entities})
