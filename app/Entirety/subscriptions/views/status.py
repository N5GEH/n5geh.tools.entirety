from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.base import Status as CBStatus

from projects.mixins import ProjectContextMixin
from subscriptions.models import Subscription


class Status(ProjectContextMixin, View):
    """
    View class used to dynamically update subscription status
    """

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get("pk", None)
        sub = Subscription.objects.get(pk=uuid)
        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            cb_sub = cb_client.get_subscription(uuid)
            cb_sub.status = (
                CBStatus.INACTIVE
                if cb_sub.status is CBStatus.ACTIVE
                else CBStatus.ACTIVE
            )
            cb_client.update_subscription(cb_sub)

            sub.description = cb_sub.description
            sub.status = cb_sub.status

        return render(
            request,
            "subscriptions/panel.html",
            {"project": self.project, "subscription": sub},
        )
