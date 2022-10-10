import json
import logging
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from examples.forms import ExampleForm, Attributes, Commands, BasicInfoForm
from django.contrib import messages


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
        basic_info = BasicInfoForm()
        attributes = Attributes(prefix="attr")
        commands = Commands(prefix="cmd")
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
        }
        # add messages
        messages.debug(request, 'DEBUG: send POST request to orion')  # debug level msg will not be displayed
        messages.info(request, 'INFO: please do something')
        messages.success(request, 'SUCCESS: devices successfully created')
        messages.warning(request, 'WARNING: service group not matched, errors may occur')
        messages.error(request, 'ERROR: entity name is illegal')
        return render(request, "examples/dialog.html", context)

    def post(self, request):
        return render(request, "examples/dialog_form.html")
