from django import forms
from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.base import Status

from subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):
    _newly_created: bool
    description = forms.CharField(required=False)
    active = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        self._newly_created = kwargs.get("instance") is None
        super().__init__(*args, **kwargs)
        self.__populate()

    def __populate(self):
        if not self._newly_created:
            with ContextBrokerClient(
                url="http://127.0.0.1:1026",
                fiware_header=FiwareHeader(service="w2f", service_path="/"),
            ) as cb_client:
                cb_sub = cb_client.get_subscription(self.instance.uuid)
                self.initial["description"] = cb_sub.description
                self.initial["active"] = cb_sub.status == Status.ACTIVE

    class Meta:
        model = Subscription
        fields = ["name"]
