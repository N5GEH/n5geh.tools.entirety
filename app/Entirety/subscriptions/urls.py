from django.urls import path

from subscriptions.views import (
    Create,
    List,
    Update,
    Status,
    Attributes,
    Entities,
    Delete,
)

app_name = "subscriptions"
urlpatterns = [
    path("", List.as_view(), name="list"),
    path("<str:pk>/update/", Update.as_view(), name="update"),
    path("<str:pk>/status/", Status.as_view(), name="status"),
    path("<str:pk>/delete/", Delete.as_view(), name="delete"),
    path("attributes/", Attributes.as_view(), name="attributes"),
    path("entities/", Entities.as_view(), name="entities"),
    path("create/", Create.as_view(), name="create"),
]
