from django.views.generic import ListView
from filip.clients.ngsi_v2 import ContextBrokerClient
from filip.models import FiwareHeader

from projects.mixins import ProjectContextMixin


class EntityList(ProjectContextMixin, ListView):
    template_name = "entities/entity_list.html"

    def get_queryset(self):
        data = []
        with ContextBrokerClient(
            url="http://127.0.0.1:1026",
            fiware_header=FiwareHeader(service="w2f", service_path="/testing"),
        ) as cb_client:
            for entity in cb_client.get_entity_list():
                data.append(entity)
        return data
