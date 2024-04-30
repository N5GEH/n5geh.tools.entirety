from crispy_forms.helper import FormHelper
from django import forms
from smartdatamodels.models import SmartDataModel
import json


class ServiceGroupBasic(forms.Form):
    resource = forms.CharField(
        label="Resource",
        required=True,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "title": "A string representing the southbound resource "
                "that will be used to provision a device, e.g. /iot/json",
            }
        ),
    )
    apikey = forms.CharField(
        label="API Key",
        required=True,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "title": "API key that authenticates the devices of a service group",
            }
        ),
    )
    entity_type = forms.CharField(
        label="Entity Type",
        max_length=256,
        required=False,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "title": "Type of the entity in the Context Broker",
            }
        ),
    )
    explicit_attrs = forms.BooleanField(
        label="Explicit Attributes", required=False, initial=False
    )
    autoprovision = forms.BooleanField(
        label="Auto Provision", required=False, initial=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class SmartDataModelServicesForm(forms.Form):
    select_data_model = forms.ChoiceField(label="Select a Data Model", required=True)
    only_required_attrs = forms.BooleanField(
        label="Only use required attributes", required=False, initial=False
    )

    def __init__(self, *args, **kwargs):
        super(SmartDataModelServicesForm, self).__init__(*args, **kwargs)
        qs = SmartDataModel.objects.all()
        list_of_schemas = []
        for set in qs:
            list_of_schemas.append(
                {"name": set.name, "value": json.dumps(set.jsonschema)}
            )
        list_of_schemas.append({"name": "..", "value": ".."})
        self.fields["select_data_model"] = forms.ChoiceField(
            choices=[(x.get("value"), x.get("name")) for x in list_of_schemas]
        )
        self.helper = FormHelper(self)
        self.helper.form_tag = False
