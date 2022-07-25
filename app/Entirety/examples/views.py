import json
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from examples.forms import ExampleForm, Attributes, Commands, BasicInfoForm


class DialogForm(View):
    def get(self, request):
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
        attributes = Attributes()
        commands = Commands()
        context = {
            "basic_info": basic_info,
            "attributes": attributes,
            "commands": commands,
        }
        return render(request, "examples/dialog.html", context)
