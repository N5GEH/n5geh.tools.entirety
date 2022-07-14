import requests

from django.shortcuts import render


def home(request):
    context = {}
    return render(request, "home.html", context)


def __generic_error_handler(request, status_code: int):
    context = {"error_code": status_code}
    return render(request, "error.html", context)


def custom_page_not_found_view(request, *args, **kwargs):
    return __generic_error_handler(request, status_code=404)


def custom_error_view(request, *args, **kwargs):
    return __generic_error_handler(request, status_code=500)


def custom_permission_denied_view(request, *args, **kwargs):
    return __generic_error_handler(request, status_code=403)


def custom_bad_request_view(request, *args, **kwargs):
    return __generic_error_handler(request, status_code=400)
