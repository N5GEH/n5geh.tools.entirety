from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit(name="save", value="Save"))

    class Meta:
        model = Project
        fields = {'name', 'description', 'fiware_service', 'webpage_url','logo'}


