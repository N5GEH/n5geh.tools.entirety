from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from filip.models import FiwareHeader

from users.models import User
from utils.auth import get_fiware_services
from .models import Project

from django.forms import ModelMultipleChoiceField


class AllSelectableModelMultipleChoiceField(ModelMultipleChoiceField):
    ALL_VALUE = "__all__"

    def clean(self, value):
        if value and self.ALL_VALUE in value:
            return self.queryset
        return super().clean(value)


class ProjectForm(forms.ModelForm):
    def __init__(self, user, request, *args, **kwargs):
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
        self.fields["dashboard_url"].required = False

        self.fields["viewers"] = AllSelectableModelMultipleChoiceField(
            queryset=(
                User.objects.exclude(id=self.instance.owner_id)
                & User.objects.exclude(id=user.id)
            ).filter(is_server_admin=False),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

        self.fields["users"] = AllSelectableModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=(
                User.objects.exclude(id=self.instance.owner_id)
                & User.objects.exclude(id=user.id)
            ).filter(is_server_admin=False),
            required=False,
        )

        if user in self.instance.maintainers.all():
            self.fields["maintainers"] = AllSelectableModelMultipleChoiceField(
                queryset=self.instance.maintainers.all(),
                widget=forms.CheckboxSelectMultiple(
                    attrs={
                        "disabled": True,
                        "data-bs-toggle": "tooltip",
                        "data-bs-placement": "left",
                        "title": "Inclusion or exclusion of maintainers into project can be done by project owners only.",
                    }
                ),
                required=False,
            )
        else:
            self.fields["maintainers"] = AllSelectableModelMultipleChoiceField(
                queryset=(
                    User.objects.exclude(id=self.instance.owner_id)
                    & User.objects.exclude(id=user.id)
                ).filter(is_server_admin=False),
                widget=forms.CheckboxSelectMultiple,
                required=False,
            )

        self.helper.form_tag = False

        self.fields["fiware_service"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Fiware service",
                }
            )
        )
        if not settings.LOCAL_AUTH:
            self.fields["fiware_service"] = forms.ChoiceField()
            self.fields["fiware_service"].choices = [
                (x, x) for x in get_fiware_services(request)
            ]

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
            "dashboard_url",
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
            # "fiware_service": forms.Select(),
            # "fiware_service": forms.TextInput(
            #     attrs={
            #         "data-bs-toggle": "tooltip",
            #         "data-bs-placement": "left",
            #         "title": "Fiware service",
            #     }
            # ),
            "webpage_url": forms.URLInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Project webpage url",
                }
            ),
            "logo": forms.ClearableFileInput(
                attrs={
                    "id": "logo-input",
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Project logo",
                }
            ),
            "dashboard_url": forms.URLInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "left",
                    "title": "Project dashboard url",
                }
            ),
        }
