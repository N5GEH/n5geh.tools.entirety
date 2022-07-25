from django.urls import path

from subscriptions.views import Create, List, Update

app_name = "subscriptions"
urlpatterns = [
    path("", List.as_view(), name="list"),
    path("<str:pk>/update/", Update.as_view(), name="update"),
    path("create/", Create.as_view(), name="create"),
]
