from django.contrib.auth.decorators import login_required
from django.urls import path

from subscriptions.views import SubscriptionList

app_name = "subscriptions"
urlpatterns = [
    path("", SubscriptionList.as_view(), name="list"),
]
