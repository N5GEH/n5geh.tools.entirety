from django import forms
from django.conf import settings

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.base import Status

from subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):
    _newly_created: bool
    description = forms.CharField(required=False)
    active = forms.BooleanField(initial=True)

    def __init__(self, *args, **kwargs):
        self._newly_created = kwargs.get("instance") is None
        super().__init__(*args, **kwargs)
        self.__populate()

    def __populate(self):
        if not self._newly_created:
            with ContextBrokerClient(
                url=settings.CB_URL,
                fiware_header=FiwareHeader(
                    service=self.instance.project.fiware_service,
                    service_path=self.instance.project.fiware_service_path,
                ),
            ) as cb_client:
                cb_sub = cb_client.get_subscription(self.instance.uuid)
                self.initial["description"] = cb_sub.description
                self.initial["active"] = cb_sub.status == Status.ACTIVE

    class Meta:
        model = Subscription
        fields = ["name"]
