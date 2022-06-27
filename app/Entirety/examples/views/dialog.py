from django.shortcuts import render, HttpResponse
from django.views.generic import View

from examples.forms import ExampleForm


class Dialog(View):
    def get(self, request):
        context = {}
        return render(request, "examples/dialog.html", context)

    def add(self, request):
        if request.method == "POST":
            form = MovieForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(status=204)
        else:
            form = MovieForm()
        return render(
            request,
            "dialog_form.html",
            {
                "form": form,
            },
        )
