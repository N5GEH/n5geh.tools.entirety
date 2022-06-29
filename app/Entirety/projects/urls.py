from django.contrib.auth.decorators import login_required
from django.urls import path

from projects.views import Index

urlpatterns = [
    path("", login_required(Index.as_view()), name="projects"),
]
