import json

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms

from entirety.widgets import ListTextWidget
from entities.requests import AttributeTypes, get_entities_types
from smartdatamodels.models import SmartDataModel


class EntityForm(forms.Form):
    def __init__(self, project, *args, **kwargs):
        super(EntityForm, self).__init__(*args, **kwargs)
        self.fields["type"] = forms.CharField(
            required=True,
            max_length=256,
            label="Entity Type",
            widget=ListTextWidget(
                data_list=get_entities_types(project),
                name="entity-type-list",
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "Type of the context entity. Combination of ID and Type must be unique.",
                },
            ),
        )

    id = forms.CharField(
        label="Entity ID",
        max_length=256,
        required=True,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "ID of the context entity, e. g. urn:ngsi-ld:Room:001. Combination of ID and Type must be "
                "unique.",
            }
        ),
    )


class AttributeForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=256,
        label="Attribute Name",
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Unique name to identify this attribute in the context entity",
            }
        ),
    )
    type = forms.CharField(
        required=True,
        max_length=256,
        label="Attribute Type",
        widget=ListTextWidget(
            data_list=[x.value for x in AttributeTypes],
            name="attr-type-list",
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Type of the context attribute.",
            },
        ),
    )
    value = forms.CharField(
        required=False,
        label="Attribute Value",
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "(optional) Value of the attribute",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(AttributeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                "name",
                "type",
                "value",
                HTML(
                    "<button class='remove-form btn btn-danger rounded-pill btn-sm'><i class='bi "
                    "bi-trash'></i></button>"
                ),
                css_class="d_attr_form col-6",
            )
        )


class SubscriptionForm(forms.Form):
    name = forms.BooleanField(label="name", required=False)
    description = forms.CharField(widget=forms.HiddenInput(), required=False)
    subject = forms.CharField(widget=forms.HiddenInput(), required=False)
    status = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False


class DeviceForm(forms.Form):
    name = forms.BooleanField(label="name", required=False)
    entity_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False


class RelationshipForm(forms.Form):
    name = forms.BooleanField(label="name", required=False)
    type = forms.CharField(widget=forms.HiddenInput(), required=False)
    attribute_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(RelationshipForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False


class SelectionForm(forms.Form):
    subscriptions = forms.BooleanField(initial=False, required=False)
    relationships = forms.BooleanField(initial=False, required=False)
    devices = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(SelectionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False


class JSONForm(forms.Form):
    entity_json = forms.JSONField(
        required=True,
        initial={
            "actionType": "append",
            "entities": [
                {
                    "id": "urn:ngsi-ld:Example:001",
                    "type": "Example",
                    "attribute_example": {"type": "Number", "value": 0},
                }
            ],
        },
    )


class SmartDataModelEntitiesForm(forms.Form):
    smart_data_model = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(SmartDataModelEntitiesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        qs = SmartDataModel.objects.all()
        list_of_schemas = []
        for set in qs:
            list_of_schemas.append(
                {"name": set.name, "value": set.name}
            )
        list_of_schemas.append({"name": "..", "value": ".."})
        self.fields["smart_data_model"] = forms.ChoiceField(
            choices=[(x.get("value"), x.get("name")) for x in list_of_schemas]
        )
