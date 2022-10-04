from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms

from examples.models import ExampleModel
from django.forms import formset_factory


class ExampleForm(forms.ModelForm):
    class Meta:
        model = ExampleModel
        fields = ["title", "year", "rating"]


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
                    "<button class='remove-form btn btn-danger rounded-pill btn-sm'><i class='bi bi-trash'></i></button>"
                ),
                css_class="d_attr_form col-6",
            )
        )


class CommandForm(forms.Form):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CommandForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                "name",
                "type",
                "value",
                HTML(
                    "<button class='remove-form btn btn-danger rounded-pill btn-sm'><i class='bi bi-trash'></i></button>"
                ),
                css_class="d_attr_form col-6",
            )
        )


class BasicInfoForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    type = forms.CharField()


Attributes = formset_factory(AttributeForm, extra=1)
Commands = formset_factory(CommandForm, extra=1)
