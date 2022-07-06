from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("create", views.Create.as_view(), name="create"),
    path("<str:pk>/update", views.Update.as_view(), name="update"),
    path("<str:pk>/delete", views.Delete.as_view(), name="delete")
]
