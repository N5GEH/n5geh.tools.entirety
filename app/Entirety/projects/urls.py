from django.apps import apps
from django.urls import path, include

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("create", views.Create.as_view(), name="create"),
    path("<str:pk>/detail", views.Detail.as_view(), name="detail"),
    path("<str:pk>/update", views.Update.as_view(), name="update"),
    path("<str:pk>/delete", views.Delete.as_view(), name="delete"),
    path("broker", views.broker, name="broker"),
    path("ql", views.ql, name="ql"),
    path("iota", views.iota, name="iota"),
]

if apps.is_installed("entities"):
    urlpatterns.append(path("<str:project_id>/entities/", include("entities.urls")))
if apps.is_installed("alarming"):
    urlpatterns.append(path("<str:project_id>/alarming/", include("alarming.urls")))
if apps.is_installed("devices"):
    urlpatterns.append(path("<str:project_id>/devices/", include("devices.urls")))
