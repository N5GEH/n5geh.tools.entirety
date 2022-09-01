from django.urls import path, include

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("create", views.Create.as_view(), name="create"),
    path("<str:pk>/update", views.Update.as_view(), name="update"),
    path("<str:pk>/delete", views.Delete.as_view(), name="delete"),
    path("<str:project_id>/alarming/", include("alarming.urls")),
    path("<str:project_id>/devices/", include("devices.urls"))
]
