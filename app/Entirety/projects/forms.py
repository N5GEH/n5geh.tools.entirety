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
        fields = ["name", "description", "fiware_service", "webpage_url", "logo"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "Project name",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "Project description",
                }
            ),
            "fiware_service": forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "Fiware service",
                }
            ),
            "webpage_url": forms.URLInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "Project webpage url",
                }
            ),
            "logo": forms.ClearableFileInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": "Project logo",
                }
            ),
        }
