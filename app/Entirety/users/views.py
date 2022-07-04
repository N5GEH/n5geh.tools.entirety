from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def user_info(request, *args, **kwargs):
    context = {}
    return render(request, "profile.html", context=context)
