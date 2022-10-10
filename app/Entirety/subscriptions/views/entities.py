from django.shortcuts import render
from django.views.generic import View

from projects.mixins import ProjectContextMixin
from subscriptions import forms


class Entities(ProjectContextMixin, View):
    """
    View class used to dynamically add entity filters.
    Delete is done via JavaScript
    """

    http_method_names = "post"

    def post(self, request, *args, **kwargs):
        # Make post mutuable
        post = request.POST.copy()

        total = int(post["entity-TOTAL_FORMS"])
        post["entity-TOTAL_FORMS"] = total + 1
        request.POST = post

        entities = forms.Entities(request.POST, prefix="entity")

        return render(request, "subscriptions/entities.html", {"entities": entities})
