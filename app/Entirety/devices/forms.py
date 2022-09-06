from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms
from django.forms import formset_factory
from filip.models.ngsi_v2.iot import DataType


ATTRIBUTES_TYPE = [
    DataType.NUMBER.value,
    DataType.FLOAT.value,
    DataType.INTEGER.value,
    DataType.BOOLEAN.value,
    DataType.TEXT.value,
    DataType.DATETIME.value,
    DataType.ARRAY.value
]

COMMANDS_TYPE = [
    DataType.COMMAND.value
]


class DeviceBasic(forms.Form):
    device_id = forms.CharField(label="Device ID", max_length=100, required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "data-bs-toggle": "tooltip",
                                        "data-bs-placement": "top ",
                                        "title": "Deice id",
                                    }
                                ),
                                )
    entity_name = forms.CharField(label="Entity Name", max_length=100, required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "data-bs-toggle": "tooltip",
                                          "data-bs-placement": "top ",
                                          "title": "Entity id",
                                      }
                                  ),
                                  )
    entity_type = forms.CharField(label="Entity Type", max_length=100,
                                  widget=forms.TextInput(
                                      attrs={
                                          "data-bs-toggle": "tooltip",
                                          "data-bs-placement": "top ",
                                          "title": "Entity type",
                                      }
                                  ),
                                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class DeviceAttributes(forms.Form):
    name = forms.CharField(label="Name", required=True)
    type_choices = tuple([(f"{i}", t) for i, t in enumerate(ATTRIBUTES_TYPE)])
    type = forms.ChoiceField(label="Type", required=True, choices=type_choices)
    object_id = forms.CharField(label="Object ID", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                "name",
                "type",
                "object_id",
                HTML(
                    "<button class='remove-form btn btn-danger rounded-pill btn-sm'><i class='bi bi-trash'></i></button>"
                ),
                css_class="d_attr_form col-6",
            )
        )


class DeviceCommands(forms.Form):
    name = forms.CharField(label="Name", required=True)
    type_choices = tuple([(f"{i}", t) for i, t in enumerate(COMMANDS_TYPE)])
    type = forms.ChoiceField(label="Type", required=True, choices=type_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                "name",
                "type",
                HTML(
                    "<button class='remove-form btn btn-danger rounded-pill btn-sm'><i class='bi bi-trash'></i></button>"
                ),
                css_class="d_attr_form col-6",
            )
        )


Attributes = formset_factory(DeviceAttributes, extra=1)
Commands = formset_factory(DeviceCommands, extra=1)
