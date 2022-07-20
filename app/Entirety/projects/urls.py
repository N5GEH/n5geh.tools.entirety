from django.contrib.auth.decorators import login_required
from django.urls import path, include

from projects.views import Index

urlpatterns = [
    path("", login_required(Index.as_view()), name="projects"),
    path("<str:project_id>/subscriptions/", include("subscriptions.urls")),
]
