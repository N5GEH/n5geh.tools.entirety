from django.contrib.auth.decorators import login_required
from django.urls import path

from subscriptions.views import List, Update

app_name = "subscriptions"
urlpatterns = [
    path("", List.as_view(), name="list"),
    path("<str:pk>/update/", Update.as_view(), name="update"),
]
