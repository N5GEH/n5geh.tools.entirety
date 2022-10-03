from django.urls import path

from subscriptions.views import Create, List, Update, Status, Attributes, Entities

app_name = "subscriptions"
urlpatterns = [
    path("", List.as_view(), name="list"),
    path("<str:pk>/update/", Update.as_view(), name="update"),
    path("<str:pk>/status/", Status.as_view(), name="status"),
    path("attributes/", Attributes.as_view(), name="attributes"),
    path("entities/", Entities.as_view(), name="entities"),
    # path("entities/<index>", Entities.as_view(), name="entities_delete"),
    path("create/", Create.as_view(), name="create"),
]
