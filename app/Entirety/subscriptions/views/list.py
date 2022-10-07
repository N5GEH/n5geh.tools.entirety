from django.conf import settings
from django.views.generic import ListView

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader

from projects.mixins import ProjectContextMixin
from subscriptions.models import Subscription


class List(ProjectContextMixin, ListView):
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
