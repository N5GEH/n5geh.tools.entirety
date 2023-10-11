from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from semantics.models import Prefix
from django.forms import modelformset_factory
from entirety.widgets import ListTextWidget

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

# class Prefix(forms.ModelForm):
#     class Meta:
#         model = Prefix
#         fields = ['name', 'value']

PrefixFormSet = modelformset_factory(Prefix, fields=("name", "value", "include"), extra=1)

class PrefixBasicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrefixBasicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    projectid = forms.CharField(
        required=True,
        max_length=256,
        label="Project ID",
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Project ID",
            },
        )
    )

class PrefixForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrefixForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                "name",
                "value",
                "include",
                HTML(
                    "<button class='remove-form btn btn-danger rounded-pill btn-sm'><i class='bi "
                    "bi-trash'></i></button>"
                ),
                css_class="d_attr_form col-6",
            )
        )

    name = forms.CharField(
        required=True,
        max_length=64,
        label="Prefix Name",
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Prefix Name",
            }   
        )
    )
    value = forms.CharField(
        required=True,
        max_length=64,
        label="Prefix Value",
        widget=forms.TextInput(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "title": "Prefix string value",
            }
        )
    )
    include = forms.BooleanField(label="include", required=False)
