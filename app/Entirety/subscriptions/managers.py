from django.db import models
from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.base import Status

# class SubscriptionsManager(models.Manager):
#     def get_queryset(self):
#         cleaned_obj = [subscriptions.schemas.SubscriptionSchema(
#             uuid=sub.uuid,
#             name=sub.name,
#             # description=""
#         ) for sub in super().get_queryset()]
#         return cleaned_obj


class SubscriptionsManager(models.Manager):
    def get_queryset(self):
        data = []
        with ContextBrokerClient(
            url="http://127.0.0.1:1026",
            fiware_header=FiwareHeader(service="test", service_path="/"),
        ) as cb_client:

            for sub in super().get_queryset():
                cb_sub = cb_client.get_subscription(sub.uuid)
                sub.description = cb_sub.description
                sub.active = cb_sub.status == Status.ACTIVE
                data.append(sub)
        return data
