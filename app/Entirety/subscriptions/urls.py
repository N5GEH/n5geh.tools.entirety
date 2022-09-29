from django.urls import path

from subscriptions.views import Create, List, Update, Status, Attributes

app_name = "subscriptions"
urlpatterns = [
    path("", List.as_view(), name="list"),
    path("<str:pk>/update/", Update.as_view(), name="update"),
    path("<str:pk>/status/", Status.as_view(), name="status"),
    path("attributes/", Attributes.as_view(), name="attributes"),
    path("create/", Create.as_view(), name="create"),
]
