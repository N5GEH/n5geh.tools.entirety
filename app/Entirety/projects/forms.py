from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from users.models import User
from .models import Project


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields["owner"].widget.attrs = {
            "data-bs-toggle": "tooltip",
            "data-bs-placement": "left",
            "title": "Owner can not be edited. It is assigned automatically on project creation.",
            "disabled": True,
        }

        self.fields["users"].widget = forms.CheckboxSelectMultiple(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "left",
                "title": "Include or exclude users into project",
            }
        )
        self.fields["users"].queryset = User.objects.exclude(
            id=self.instance.owner_id
        ).filter(is_server_admin=False)

        self.helper.layout.append(Submit(name="save", value="Save"))

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "fiware_service",
            "webpage_url",
            "logo",
            "owner",
            "users",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Project name",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Project description",
                }
            ),
            "fiware_service": forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Fiware service",
                }
            ),
            "webpage_url": forms.URLInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Project webpage url",
                }
            ),
            "logo": forms.ClearableFileInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Project logo",
                }
            ),
        }
