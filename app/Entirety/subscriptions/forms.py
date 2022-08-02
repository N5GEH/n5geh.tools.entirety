from django import forms
from django.conf import settings
from crispy_bootstrap5.bootstrap5 import Field, FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import PrependedText

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader

from subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):
    _newly_created: bool

    description = forms.CharField()
    entities = forms.CharField()
    entity_select = forms.ChoiceField(
        choices=[
            ("id", "ID"),
            ("id_pattern", "ID Pattern"),
            ("type", "Type"),
            ("type_pattern", "Type Pattern"),
        ]
    )

    # helper = FormHelper()
    # helper.layout = Layout(
    #     Field('name'),
    #     Field('description'),
    #     # FloatingField('entities')
    #     # CustomPrependedText('entities', entity_select),
    # )

    # entities: List[EntityPattern]
    # attrs: Optional[List[str]]
    # expression: Optional[List[str]]
    # notification: Notification

    def __init__(self, *args, **kwargs):
        self._newly_created = kwargs.get("instance") is None
        super().__init__(*args, **kwargs)
        self.__populate()

    # def save(self, commit=True, *args, **kwargs):
    #     instance = super(SubscriptionForm, self).save(commit=False, *args, **kwargs)
    #
    #     with ContextBrokerClient(
    #             url=settings.CB_URL,
    #             fiware_header=FiwareHeader(
    #                 service=instance.project.fiware_service,
    #                 service_path=instance.project.fiware_service_path,
    #             ),
    #     ) as cb_client:
    #         if instance.pk:
    #             cb_sub = cb_client.get_subscription(instance.pk)
    #             cb_sub.description = self.cleaned_data["description"]
    #             cb_client.update_subscription(cb_sub)
    #         else:
    #             cb_sub = Subscription()
    #             cb_sub.description = self.cleaned_data["description"]
    #             cb_client.update_subscription(cb_sub)
    #     if commit:
    #         instance.save()
    #     return instance

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

    class Meta:
        model = Subscription
        fields = ["name", "description", "entity_select", "entities"]
