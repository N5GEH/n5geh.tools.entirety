from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from smartdatamodels.models import SmartDataModel


class SmartDataModelForm(forms.ModelForm):
    schema_link = forms.URLField(required=False)
    jsonschema = forms.JSONField(required=False)

    def __init__(self, view_only: bool = True, *args, **kwargs):
        super(SmartDataModelForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if not view_only:
            self.helper.layout.append(Submit(name="save", value="Save"))
        self.helper.form_tag = False

    class Meta:
        model = SmartDataModel
        fields = ["name", "schema_link", "jsonschema"]


class SmartDataModelQueryForm(forms.Form):
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
            label="Load data model",
            choices=[(x.get("value"), x.get("name")) for x in list_of_schemas],
            widget=forms.Select(
                attrs={
                    "style": "width: 400px;",
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "Select data model to prefill entity form",
                }
            ),
        )
