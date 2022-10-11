from django import forms
from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Button
from crispy_forms.bootstrap import InlineCheckboxes

from filip.models.ngsi_v2.base import AttrsFormat
from filip.utils.simple_ql import Operator

from subscriptions.models import Subscription
from entirety.fields import MQTTURLField, HTTPURLField


class AttributesForm(forms.Form):
    def __init__(
        self,
        data=None,
        choices=[],
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=None,
        empty_permitted=False,
        field_order=None,
        use_required_attribute=None,
        renderer=None,
    ):
        super(AttributesForm, self).__init__(
            data,
            files,
            auto_id,
            prefix,
            initial,
            error_class,
            label_suffix,
            empty_permitted,
            field_order,
            use_required_attribute,
            renderer,
        )

        self.fields["attributes"] = forms.MultipleChoiceField(
            choices=choices if choices else [],
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            InlineCheckboxes("attributes"),
        )


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
    entity_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Entity id or id pattern. "
                         "Notification will be triggered "
                         "by changes in the matched entities.",
            },
        ),)

    type_selector = forms.ChoiceField(choices=_type_choices, required=False)
    entity_type = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "data-bs-toggle": "tooltip",
                                          "data-bs-placement": "top",
                                          "title": "Entity type or type pattern.",
                                      },
                                  )
                                  )

    def __init__(self, *args, **kwargs):
        super(EntitiesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # disabled because htmx is configured to always send csrf token
        self.helper.disable_csrf = True
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


class ExpressionForm(forms.Form):
    operators = forms.ChoiceField(
        choices=[(op.value, op.value) for op in Operator],
        initial=Operator.EQUAL.value,
    )


Expressions = forms.formset_factory(ExpressionForm, extra=1)


class SubscriptionForm(forms.ModelForm):
    # Base info
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "A free text used by the client to describe the subscription.",
            }
        )
        # help_text="A free text used by the client to describe the subscription."
    )
    expires = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "datetime-local",
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Subscription expiration date format."
                "Permanent subscriptions must omit this field.",
            },
        ),
        required=False,
        # help_text="Subscription expiration date format. "
        # "Permanent subscriptions must omit this field.",
    )
    throttling = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Minimal period of time in seconds which must elapse "
                "between two consecutive notifications. "
                "It is optional.",
            }
        )
        # help_text="Minimal period of time in seconds which must elapse "
        # "between two consecutive notifications. "
        # "It is optional.",
    )

    # Subject

    # TODO: expression

    # Notification

    # TODO: httpCustom
    http = HTTPURLField(required=False,
                        widget=forms.TextInput(
                            attrs={
                                "data-bs-toggle": "tooltip",
                                "data-bs-placement": "top",
                                "title": "HTTP endpoint to receive the notification.",
                            }
                        )
                        )
    # TODO: mqttCustom
    mqtt = MQTTURLField(required=False,
                        widget=forms.TextInput(
                            attrs={
                                "data-bs-toggle": "tooltip",
                                "data-bs-placement": "top",
                                "title": "MQTT endpoint to receive the notification.",
                            }
                        )
                        )

    metadata = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "List of metadata to be included in notification messages.",
            }
        )
        # help_text="List of metadata to be included in notification messages.",
    )
    # metadata = forms.

    # TODO: attrs or exceptAttrs

    # n_attributes = forms.CharField(
    #     required=False,
    #     label="Attributes",
    #     help_text="Comma separated list of attribute names to include in notification",
    # )
    # n_except_attributes = forms.CharField(
    #     required=False,
    #     label="Except Attributes",
    #     help_text="Comma separated list of attribute names to exclude in notification",
    # )

    attributes_format = forms.ChoiceField(
        choices=[(format.value, format.value) for format in AttrsFormat],
        # help_text="Specifies how the entities are represented in notifications.",
        initial="normalized",
    )
    only_changed_attributes = forms.BooleanField(required=False, initial=False)

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
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "A short name to identify the notification.",
                }
            ),
        }
