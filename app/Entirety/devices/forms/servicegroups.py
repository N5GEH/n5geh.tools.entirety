from crispy_forms.helper import FormHelper
from django import forms


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
    explicit_attrs = forms.BooleanField(label="Explicit Attributes", required=False, initial=False)
    # forms.RadioSelect(label="Explicit Attributes", required=False, initial=False)
    # explicit_attrs = forms.ChoiceField(label="Explicit Attributes", required=True, choices=("True", "False"))
    autoprovision = forms.BooleanField(label="Auto Provision", required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
