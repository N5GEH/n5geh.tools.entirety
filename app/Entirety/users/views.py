from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from users.forms import UserForm, SignupForm


@login_required()
def user_info(request, *args, **kwargs):
    form = UserForm(instance=request.user)
    context = {"form": form}
    return render(request, "profile.html", context=context)


def provider_logout(request):
    logout_url = settings.OIDC_OP_LOGOUT_ENDPOINT

    oidc_id_token = request.session.get("oidc_id_token", None)
    if oidc_id_token:
        logout_url = (
            settings.OIDC_OP_LOGOUT_ENDPOINT
            + "?"
            + urlencode(
                {
                    "id_token_hint": oidc_id_token,
                    "post_logout_redirect_uri": request.build_absolute_uri(
                        location=settings.LOGOUT_REDIRECT_URL
                    ),
                }
            )
        )
    return logout_url


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in after signup
            return redirect("home")  # Redirect to homepage or dashboard
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


class CustomLocalLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["local_auth_signup"] = settings.LOCAL_AUTH_SIGNUP
        return context_data
