from django.conf import settings
from django.views.generic import ListView

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader

from projects.mixins import ProjectContextAndViewOnlyMixin
from subscriptions.models import Subscription


class List(ProjectContextAndViewOnlyMixin, ListView):
    """
    View class used to list subscriptions linked to project
    """

    model = Subscription
    template_name = "subscriptions/subscription_list.html"

    def get_queryset(self):
        # Use queryset not in the way it's intended
        data = []
        qs = super().get_queryset().filter(project_id=self.project.uuid)
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            for sub in qs:
                cb_sub = cb_client.get_subscription(sub.uuid)
                sub.description = cb_sub.description
                sub.status = cb_sub.status
                data.append(sub)
        return data

    def get_context_data(self, **kwargs):
        context = super(ProjectContextAndViewOnlyMixin, self).get_context_data(**kwargs)
        context["view_only"] = (
            True
            if self.request.user in self.project.viewers.all()
            and self.request.user not in self.project.maintainers.all()
            and self.request.user not in self.project.users.all()
            and self.request.user is not self.project.owner
            else False
        )
        return context
