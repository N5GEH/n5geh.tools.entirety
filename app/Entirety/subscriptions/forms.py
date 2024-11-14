from django import forms
from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Button, Field
from crispy_forms.bootstrap import InlineCheckboxes

from filip.models.ngsi_v2.base import AttrsFormat
from filip.models.ngsi_v2.subscriptions import HttpMethods
from filip.utils.simple_ql import Operator

from subscriptions.models import Subscription
from entirety.fields import MQTTURLField, HTTPURLField, DropdownOrTextField
from entities.requests import get_entities_list, get_entities_types


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


class EntityIdList:
    def __init__(self, project):
        self.list = get_entities_list(self, None, None, project)
        pass

    def id_list(self):
        id_only_list = []
        for item in self.list:
            id_only_list.append((item.id, item.id))
        return id_only_list


class EntityTypeList:
    def __init__(self, project):
        self.list = get_entities_types(project)
        pass

    def type_list(self):
        id_only_list = []
        for item in self.list:
            id_only_list.append((item, item))
        return id_only_list


class EntityListForm(forms.ChoiceField):
    choices = []


class EntitiesForm(forms.Form):
    _entity_choices = [
        ("id", "id"),
        ("id_pattern", "id pattern"),
    ]
    _type_choices = [
        ("type", "type"),
        ("type_pattern", "type pattern"),
    ]

    entity_selector = forms.ChoiceField(
        choices=_entity_choices,
        widget=forms.Select(
            attrs={"onChange": "updateEntityList(this.value, this.id)"}
        ),
    )
    type_selector = forms.ChoiceField(
        choices=_type_choices,
        required=False,
        widget=forms.Select(
            attrs={"onChange": "updateEntityList(this.value, this.id)"}
        ),
    )

    entity_id_list = []
    entity_type_list = []

    entity_id = DropdownOrTextField(
        choices=entity_id_list, tooltip="Entity type or type pattern."
    )

    entity_type = forms.ChoiceField(choices=entity_type_list)

    def __init__(self, *args, **kwargs):
        project = None
        if "project" in kwargs:
            project = kwargs.pop("project")
        super(EntitiesForm, self).__init__(*args, **kwargs)

        if project != None:
            entity_id_list = EntityIdList(project).id_list()
            entity_type_list = EntityTypeList(project).type_list()
        else:
            entity_id_list = []
            entity_type_list = []

        entity_selector = type_selector = None
        entity_pattern = type_pattern = None
        entity_id = entity_type = None

        if "initial" in kwargs:
            initial = kwargs["initial"]
            if "entity_selector" in initial:
                if initial["entity_selector"] == "id":
                    entity_selector = "id"
                    if "entity_id" in initial:
                        entity_id = initial["entity_id"]
                        initial["entity_id"] = (
                            initial["entity_id"],
                            "---",
                        )
                if initial["entity_selector"] == "id_pattern":
                    entity_selector = "pattern"
                    if "entity_id" in initial:
                        entity_pattern = initial["entity_id"]
                        initial["entity_id"] = (
                            "",
                            initial["entity_id"],
                        )
            if "type_selector" in initial:
                if initial["type_selector"] == "id":
                    type_selector = "type"
                    if "entity_type" in initial:
                        entity_type = initial["entity_type"]
                        initial["entity_type"] = (
                            initial["entity_type"],
                            "---",
                        )
                if initial["type_selector"] == "type_pattern":
                    type_selector = "pattern"
                    if "entity_type" in initial:
                        type_pattern = initial["entity_type"]
                        initial["entity_type"] = (
                            "",
                            initial["entity_type"],
                        )

        entity_kwargs = {
            "selector": entity_selector,
            "pattern": entity_pattern,
            "id": entity_id,
        }

        type_kwargs = {
            "selector": type_selector,
            "pattern": type_pattern,
            "id": entity_type,
        }

        self.fields["entity_id"] = DropdownOrTextField(
            choices=entity_id_list, **entity_kwargs, tooltip="Entity id"
        )
        self.fields["entity_type"] = DropdownOrTextField(
            choices=entity_type_list, **type_kwargs, tooltip="Entity type"
        )

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
        ),
        # help_text="Minimal period of time in seconds which must elapse "
        # "between two consecutive notifications. "
        # "It is optional.",
    )

    # Subject

    # TODO: expression

    # Notification

    _notification_choices = [("http", "HTTP"), ("mqtt", "MQTT")]
    endpoint_type = forms.ChoiceField(
        required=True,
        choices=_notification_choices,
    )

    metadata = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "List of metadata to be included in notification messages.",
            }
        ),
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


class HTTPForm(forms.Form):
    http_url = HTTPURLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "HTTP endpoint to receive the notification.",
            }
        ),
    )
    http_method = forms.ChoiceField(
        required=False,
        choices=[(method.value, method.value) for method in HttpMethods],
        widget=forms.Select(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "HTTP method to send the notification with.",
            }
        ),
    )
    http_qs = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "HTTP query parameters to include in the notification.",
            }
        ),
    )
    http_headers = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "HTTP headers to include in the notification.",
            }
        ),
    )
    http_payload = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "HTTP payload to include in the notification.",
            }
        ),
    )
    http_json = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "HTTP json to include in the notification.",
            }
        ),
    )
    http_ngsi = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "HTTP ngsi to include in the notification.",
            }
        ),
    )
    http_timeout = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "maximum time (in milliseconds) the subscription waits for the response.",
            }
        ),
    )


class MQTTForm(forms.Form):
    mqtt_url = MQTTURLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "MQTT endpoint to receive the notification.",
            }
        ),
    )
    mqtt_topic = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "MQTT topic to use for the notification.",
            }
        ),
    )
    mqtt_payload = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "MQTT payload to include in the notification.",
            }
        ),
    )
    mqtt_json = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "MQTT json to include in the notification.",
            }
        ),
    )
    mqtt_ngsi = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "MQTT ngsi to include in the notification.",
            }
        ),
    )
