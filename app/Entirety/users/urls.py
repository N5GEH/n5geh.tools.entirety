from django.conf import settings
from django.urls import path, include

from mozilla_django_oidc.urls import OIDCAuthenticateClass
from mozilla_django_oidc.views import OIDCLogoutView

from users import views

urlpatterns = [path("", views.user_info, name="user")]

if settings.LOCAL_AUTH:
    urlpatterns += [path("", include("django.contrib.auth.urls"))]
else:
    urlpatterns += [
        path("login/", OIDCAuthenticateClass.as_view(), name="login"),
        path("logout/", OIDCLogoutView.as_view(), name="logout"),
    ]
