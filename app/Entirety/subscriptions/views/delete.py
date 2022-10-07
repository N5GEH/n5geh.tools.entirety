import json

from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.urls import reverse
from django.views.generic import DeleteView

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader

from projects.mixins import ProjectContextMixin
from subscriptions.models import Subscription


class Delete(ProjectContextMixin, DeleteView):
    model = Subscription
    template_name = "subscriptions/confirm_delete.html"

    def form_valid(self, form):
        success_url = self.get_success_url()

        uuid = self.object.uuid

        self.object.delete()

        with ContextBrokerClient(
            url=settings.CB_URL,
            fiware_header=FiwareHeader(
                service=self.project.fiware_service,
                service_path=self.project.fiware_service_path,
            ),
        ) as cb_client:
            cb_client.delete_subscription(uuid)

        return HttpResponse(status=204, headers={"HX-Redirect": success_url})

    def get_success_url(self):
        return reverse(
            "projects:subscriptions:list", kwargs={"project_id": self.project.uuid}
        )
