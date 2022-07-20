from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView


from subscriptions.models import Subscription
from projects.mixins import ProjectContextMixin


class SubscriptionList(ProjectContextMixin, ListView):
    model = Subscription

    template_name = "subscriptions/subscription_list.html"

    # def get_queryset(self):
    #     return Subscription.objects.filter(project=self.project)
