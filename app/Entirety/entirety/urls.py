"""entirety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

handler404 = "entirety.views.custom_page_not_found_view"
handler500 = "entirety.views.custom_error_view"
handler403 = "entirety.views.custom_permission_denied_view"
handler400 = "entirety.views.custom_bad_request_view"


urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", include("projects.urls")),
    path("accounts/", include("users.urls")),
    path("examples/", include("examples.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.LOCAL_AUTH:
    urlpatterns += [path("admin/", admin.site.urls)]
else:
    urlpatterns += [
        path("admin/login/", views.CustomLogin.as_view()),
        path("admin/", admin.site.urls),
        path("oidc/", include("mozilla_django_oidc.urls")),
    ]
