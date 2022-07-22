from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, View

from subscriptions.models import Subscription, SubscriptionList
from subscriptions.forms import SubscriptionForm
from projects.mixins import ProjectContextMixin


class List(ProjectContextMixin, ListView):
    model = SubscriptionList
    template_name = "subscriptions/subscription_list.html"


class Update(ProjectContextMixin, UpdateView):
    model = Subscription
    template_name = "subscriptions/detail.html"
    form_class = SubscriptionForm
