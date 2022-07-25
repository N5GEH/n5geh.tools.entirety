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


class CommandForm(forms.Form):
    name = forms.CharField()


class BasicInfoForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    type = forms.CharField()


Attributes = formset_factory(AttributeForm, extra=1, can_delete=True)
Commands = formset_factory(CommandForm, extra=1, can_delete=True)
