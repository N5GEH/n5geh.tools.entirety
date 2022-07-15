from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.forms import UserForm


@login_required()
def user_info(request, *args, **kwargs):
    form = UserForm(instance=request.user)
    context = {"form": form}
    return render(request, "profile.html", context=context)
