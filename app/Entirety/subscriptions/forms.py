from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.subscriptions import Notification
from filip.models.ngsi_v2.base import AttrsFormat

from subscriptions.models import Subscription
from entirety.fields import SelectTextMultiField, MQTTURLField


class EntitiesForm(forms.Form):
    _entity_choices = [
        ("id", "id"),
        ("id_pattern", "id pattern"),
    ]
    _type_choices = [
        ("type", "type"),
        ("type_pattern", "type pattern"),
    ]

    entity_selector = forms.ChoiceField(choices=_entity_choices)
    entity = forms.CharField()

    type_selector = forms.ChoiceField(choices=_type_choices, required=False)
    entity_type = forms.CharField(required=False)


Entities = forms.formset_factory(EntitiesForm)


class SubscriptionForm(forms.ModelForm):
    _newly_created: bool

    # Base info
    description = forms.CharField(
        help_text="A free text used by the client to describe the subscription."
    )
    expires = forms.DateField(
        widget=forms.TextInput(
            attrs={"type": "date"},
        ),
        required=False,
        help_text="Subscription expiration date format. "
        "Permanent subscriptions must omit this field.",
    )
    throttling = forms.IntegerField(
        required=False,
        help_text="Minimal period of time in seconds which must elapse "
        "between two consecutive notifications. "
        "It is optional.",
    )

    # Subject
    entities = Entities()
    attributes = forms.MultipleChoiceField(
        choices=[("id", "id")],
        widget=forms.CheckboxSelectMultiple,
    )

    # entities = SelectTextMultiField(
    #     choices=_entity_choices,
    #     initial=["id_pattern", ".*"]
    # )

    # Notification

    # TODO: attrs or exceptAttrs
    # TODO: httpCustom
    http = forms.URLField(required=False)
    # TODO: mqttCustom
    mqtt = MQTTURLField(required=False)

    attributes_format = forms.ChoiceField(
        choices=[(format.value, format.value) for format in AttrsFormat],
        help_text="specifies how the entities are represented in notifications.",
        initial="normalized",
    )

    # TODO: metadata

    # Not implemented in Filip
    # times_sent = forms.IntegerField(disabled=True, required=False)
    # last_notification = forms.DateField(disabled=True, required=False)
    # last_failure = forms.DateField(disabled=True, required=False)

    def __init__(self, *args, **kwargs):
        self._newly_created = (
            kwargs.get("instance") is None
        )  # instance won't be None after super init
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
                # self.initial["id_select"] = "id_pattern" if cb_sub else "id"

    def clean(self):
        cleaned_data = super().clean()
        if not self.entities.is_valid():
            test = self.entities.errors
        if not (bool(cleaned_data.get("http")) != bool(cleaned_data.get("mqtt"))):
            message = "Exactly one of http or mqtt must have a value."
            self.add_error("http", message)
            self.add_error("mqtt", message)

    class Meta:
        model = Subscription
        exclude = ["uuid", "project"]
        # fields = "__all__"
