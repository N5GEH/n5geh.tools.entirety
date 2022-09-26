from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Button, HTML

from filip.clients.ngsi_v2.cb import ContextBrokerClient
from filip.models import FiwareHeader
from filip.models.ngsi_v2.subscriptions import Notification, Subscription
from filip.models.ngsi_v2.base import AttrsFormat

from subscriptions.models import Subscription
from entirety.fields import SelectTextMultiField, MQTTURLField, HTTPURLField
from entirety.validators import CustomURLValidator


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
    entity_id = forms.CharField()

    type_selector = forms.ChoiceField(choices=_type_choices, required=False)
    entity_type = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(EntitiesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    "Select entities",
                    "entity_selector",
                    "entity_id",
                    "type_selector",
                    "entity_type",
                ),
                HTML(
                    "<button class='remove-entity btn btn-danger rounded-pill btn-sm'><i class='bi "
                    "bi-trash'></i></button>"
                ),
                css_class="d-flex flex-column col-6 col-xl-3 pe-2 entity-form",
            )
        )


Entities = forms.formset_factory(EntitiesForm, extra=0, min_num=1)


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

    attributes = forms.MultipleChoiceField(
        choices=[("id", "id")],
        widget=forms.CheckboxSelectMultiple,
    )

    # entities = Entities(prefix="entity")

    # Notification

    # TODO: attrs or exceptAttrs
    # TODO: httpCustom
    http = HTTPURLField(required=False)
    # TODO: mqttCustom
    mqtt = MQTTURLField(required=False)

    attributes_format = forms.ChoiceField(
        choices=[(format.value, format.value) for format in AttrsFormat],
        help_text="specifies how the entities are represented in notifications.",
        initial="normalized",
    )
    only_changed_attributes = forms.BooleanField(required=False, initial=False)

    # TODO: metadata

    # Not implemented in Filip
    # times_sent = forms.IntegerField(disabled=True, required=False)
    # last_notification = forms.DateField(disabled=True, required=False)
    # last_failure = forms.DateField(disabled=True, required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not (bool(cleaned_data.get("http")) != bool(cleaned_data.get("mqtt"))):
            message = "Exactly one of http or mqtt must have a value."
            self.add_error("http", message)
            self.add_error("mqtt", message)

    class Meta:
        model = Subscription
        exclude = ["uuid", "project"]
        # fields = "__all__"
