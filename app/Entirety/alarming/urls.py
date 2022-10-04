from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import RedirectView

from alarming.views import SubscriptionList

app_name = "alarming"
urlpatterns = [
    path("subscriptions/", SubscriptionList.as_view(), name="subscriptions"),
    path("", RedirectView.as_view(pattern_name="subscriptions")),
]
