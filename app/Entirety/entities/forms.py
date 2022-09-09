from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms


class EntityForm(forms.Form):
    id = forms.CharField(
        label="Entity ID",
        max_length=80,
        required=True,
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Entity id",
            }
        ),
    )
    type = forms.ChoiceField(choices=[("weather_station", "weather_station")])


class AttributeForm(forms.Form):
    name = forms.CharField()
    type = forms.CharField()
    value = forms.CharField()

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
    name = forms.CharField(required=False)


class RelationshipForm(forms.Form):
    name = forms.BooleanField(label="name", required=False)
    type = forms.CharField(widget=forms.HiddenInput(), required=False)
    attribute_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(RelationshipForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
