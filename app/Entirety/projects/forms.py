from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
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
            self.fields["fiware_service"].disabled = True

        else:
            self.fields["owner"].queryset = User.objects.filter(
                Q(is_server_admin=True) | Q(is_project_admin=True)
            )
        self.fields["owner"].widget.attrs["data-bs-toggle"] = "tooltip"
        self.fields["owner"].widget.attrs["data-bs-placement"] = "left"
        self.fields["owner"].widget.attrs[
            "title"
        ] = "The owner is assigned automatically on project creation. It can only be updated by a server admin."

        self.fields["logo"].required = False
        self.fields["webpage_url"].required = False

        self.fields["viewers"] = forms.ModelMultipleChoiceField(
            queryset=(
                User.objects.exclude(id=self.instance.owner_id)
                & User.objects.exclude(id=user.id)
            ).filter(is_server_admin=False),
            widget=forms.CheckboxSelectMultiple,
        )

        self.fields["users"] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=(
                User.objects.exclude(id=self.instance.owner_id)
                & User.objects.exclude(id=user.id)
            ).filter(is_server_admin=False),
        )

        if user in self.instance.maintainers.all():
            self.fields["maintainers"].disabled = True
            self.fields["maintainers"].required = False
            self.fields["maintainers"].queryset = self.instance.maintainers.all()
            self.fields["maintainers"].widget.attrs["data-bs-toggle"] = "tooltip"
            self.fields["maintainers"].widget.attrs["data-bs-placement"] = "left"
            self.fields["maintainers"].widget.attrs[
                "title"
            ] = "Inclusion or exclusion of maintainers into project can by done by project owners only."
        else:
            self.fields["maintainers"] = forms.ModelMultipleChoiceField(
                queryset=(
                    User.objects.exclude(id=self.instance.owner_id)
                    & User.objects.exclude(id=user.id)
                ).filter(is_server_admin=False),
                widget=forms.CheckboxSelectMultiple,
            )

        self.helper.form_tag = False

        if self.is_bound:
            self.fields["viewers"].initial = [
                int(id) for id in self.data.getlist("viewers")
            ]
            self.fields["users"].initial = [
                int(id) for id in self.data.getlist("users")
            ]
            self.fields["maintainers"].initial = [
                int(id) for id in self.data.getlist("maintainers")
            ]
        else:
            if self.instance.pk:
                self.fields["viewers"].initial = list(
                    self.instance.viewers.values_list("id", flat=True)
                )
                self.fields["users"].initial = list(
                    self.instance.users.values_list("id", flat=True)
                )
                self.fields["maintainers"].initial = list(
                    self.instance.maintainers.values_list("id", flat=True)
                )

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get("fiware_service")
        try:
            FiwareHeader(service=service)
        except Exception as e:
            raise ValidationError(e)
        try:
            cleaned_data["viewers"]
        except Exception as e:
            raise ValidationError("At least one viewer must be selected.")
        try:
            cleaned_data["users"]
        except Exception as e:
            raise ValidationError("At least one user must be selected.")
        try:
            cleaned_data["maintainers"]
        except Exception as e:
            raise ValidationError("At least one maintainer must be selected.")

    def save(self, commit=True):
        instance = super().save(commit=True)

        instance.viewers.set(self.cleaned_data["viewers"])
        instance.users.set(self.cleaned_data["users"])
        instance.maintainers.set(self.cleaned_data["maintainers"])

        if commit:
            instance.save()

        return instance

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "fiware_service",
            "webpage_url",
            "logo",
            "owner",
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
