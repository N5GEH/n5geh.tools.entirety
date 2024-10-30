from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.forms import UserForm


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
