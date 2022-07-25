import json
import logging
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from examples.forms import ExampleForm

logger = logging.getLogger(__name__)


class DialogForm(View):
    def get(self, request):
        logger.info("Dialog form data rendering")
        form = ExampleForm()
        return render(
            request,
            "examples/dialog_form.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = ExampleForm(request.POST)
        if form.is_valid():
            example = form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps({"showMessage": f"{example.title} added."})
                },
            )

        return render(
            request,
            "examples/dialog_form.html",
            {
                "form": form,
            },
        )


class Dialog(View):
    def get(self, request):
        context = {}
        return render(request, "examples/dialog.html", context)
