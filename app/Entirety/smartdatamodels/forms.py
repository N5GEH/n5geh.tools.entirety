from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from smartdatamodels.models import SmartDataModel


class SmartDataModelForm(forms.ModelForm):
    schema_link = forms.URLField(required=False)
    jsonschema = forms.JSONField(required=False)

    def __init__(self, *args, **kwargs):
        super(SmartDataModelForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit(name="save", value="Save"))
        self.helper.form_tag = False

    class Meta:
        model = SmartDataModel
        fields = ["name", "schema_link", "jsonschema"]


class SmartDataModelQueryForm(forms.Form):
    data_model = forms.ChoiceField(
        label="Data model",
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Select data model to prefill entity form",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(SmartDataModelQueryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        qs = SmartDataModel.objects.all()
        list_of_schemas = []
        for set in qs:
            list_of_schemas.append({"name": set.name, "value": set.name})
        list_of_schemas.append({"name": "..", "value": ".."})
        self.fields["data_model"] = forms.ChoiceField(
            choices=[(x.get("value"), x.get("name")) for x in list_of_schemas]
        )