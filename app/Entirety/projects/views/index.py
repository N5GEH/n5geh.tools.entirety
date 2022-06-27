from django.shortcuts import render
from django.views.generic import View


class Index(View):
    def get(self, request):
        context = {}
        return render(request, "projects/index.html", context)
