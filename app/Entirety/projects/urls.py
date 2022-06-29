from django.urls import path

from projects.views import Index

urlpatterns = [
    path("", Index.as_view(), name="projects"),
]
