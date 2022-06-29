from django import forms

from examples.models import ExampleModel


class ExampleForm(forms.ModelForm):
    class Meta:
        model = ExampleModel
        fields = ["title", "year", "rating"]
