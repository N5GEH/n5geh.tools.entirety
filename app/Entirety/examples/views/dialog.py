from django.shortcuts import render
from django.views.generic import View


class Dialog(View):
    def get(self, request):
        context = {}
        return render(request, "examples/dialog.html", context)
