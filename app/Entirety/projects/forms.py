from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from filip.models import FiwareHeader

from users.models import User
from .models import Project


class ProjectForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if not user.is_server_admin:
            self.fields["owner"].disabled = True
            self.fields["owner"].required = False

        else:
            self.fields["owner"].queryset = User.objects.filter(
                is_server_admin=True, is_project_admin=True
            )
        self.fields["owner"].widget.attrs["data-bs-toggle"] = "tooltip"
        self.fields["owner"].widget.attrs["data-bs-placement"] = "left"
        self.fields["owner"].widget.attrs[
            "title"
        ] = "Owner is assigned automatically on project creation. It can only be updated by admin."

        self.fields["users"].widget = forms.CheckboxSelectMultiple(
            attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "left",
                "title": "Include or exclude users into project",
            }
        )
        self.fields["users"].queryset = (
            User.objects.exclude(id=self.instance.owner_id)
            & User.objects.exclude(id=user.id)
        ).filter(is_server_admin=False)

        self.helper.layout.append(Submit(name="save", value="Save"))

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get("fiware_service")
        try:
            FiwareHeader(service=service)
        except Exception as e:
            raise ValidationError(e)

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
