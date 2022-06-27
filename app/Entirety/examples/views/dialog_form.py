from django.shortcuts import render, HttpResponse
from django.views.generic import View

from examples.forms import ExampleForm


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
            form.save()
            return HttpResponse(status=204)

        return render(
            request,
            "examples/dialog_form.html",
            {
                "form": form,
            },
        )
